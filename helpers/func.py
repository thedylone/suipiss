"""bot functions for reddit bot"""

import time
import random
import re
import praw
import helpers.general as gen

REDDIT_URL = "https://reddit.com"


def comment_logic(
    comment, username, keyword, custom_logic, debug=False
) -> str:
    """handle the logic for comments"""
    if comment_is_user(comment, username):
        # ignore own comments
        return "comment is self"
    if already_replied_comment(comment, username):
        # prevent spam, don't reply again
        return "already replied"
    if comment_is_user(comment, username, 1):
        # parent is user
        gratitude: list[str] = ["thank", "good", "love"]
        if keyword_in_comment(comment, *gratitude):
            return (
                "replied"
                if reply_gratitude(comment=comment, debug=debug)
                else "failed"
            )
        if debug:
            return "parent is self"
    for custom in custom_logic.get("parent_is_self", []):
        if not comment_is_user(comment, username, custom.get("level")):
            continue
        if comment.author.name != custom.get("author"):
            continue
        msg: str = custom.get("msg")
        return (
            msg
            if debug
            else "replied"
            if reply_custom(comment=comment, msg=msg, debug=debug)
            else "failed"
        )
    if keyword_in_comment(comment, keyword):
        for custom in custom_logic.get("keyword_in_comment", []):
            if comment.author.name != custom.get("author"):
                continue
            msg: str = custom.get("msg")
            return (
                msg
                if debug
                else "replied"
                if reply_custom(comment=comment, msg=msg, debug=debug)
                else "failed"
            )
        if not comment_is_user(comment, username, 1):
            # dont reply to own comment's reply to prevent spam
            return (
                "replied"
                if reply_mention(mention=comment, debug=debug)
                else "failed"
            )
        if debug:
            return "keyword in comment (no reply)"
    return "no reply"


def submission_logic(submission, username, keyword, debug=False) -> str:
    """handle the logic for submissions"""
    if already_replied_submission(submission, username):
        # prevent spam, don't reply again
        return "already replied"
    if keyword_in_submission(submission, keyword):
        return (
            "replied"
            if reply_submission(submission, debug=debug)
            else "failed"
        )
    return "no reply"


def reply_submission(submission, debug=False) -> bool:
    """
    submits a comment to a submission.
    attempts to retrieve messages from messages/mention.txt.
    if there are multiple messages, the first messages has a
    50% chance of being selected.
    return True if successful.
    """
    reply_messages: list[str] = gen.try_import_messages("messages/mention.txt")
    reply_weights: list[float] = gen.assign_random_weights(reply_messages)
    msg: str = random.choices(reply_messages, weights=reply_weights, k=1)[0]
    notif: str = f"[POST] {REDDIT_URL}{submission.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    try:
        submission.reply(body=msg)
        gen.post_webhook({"content": notif})
        return True
    except Exception as err:
        print(err)
        gen.post_webhook({"content": err})
        return False


def reply_mention(mention, debug=False) -> bool:
    """
    submits a comment as a reply to a mentioned comment.
    attempts to retrieve messages from messages/mention.txt.
    if there are multiple messages, the first messages has a
    50% chance of being selected.
    return True if successful.
    """
    reply_messages: list[str] = gen.try_import_messages("messages/mention.txt")
    reply_weights: list[float] = gen.assign_random_weights(reply_messages)
    msg: str = random.choices(reply_messages, weights=reply_weights, k=1)[0]
    notif: str = f"[MENTION] {REDDIT_URL}{mention.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    try:
        mention.reply(body=msg)
        gen.post_webhook({"content": notif})
        return True
    except Exception as err:
        print(err)
        gen.post_webhook({"content": err})
        return False


def reply_gratitude(comment, debug=False) -> bool:
    """
    submits a comment as a reply to a comment thanking the bot.
    attempts to retrieve messages from messages/thank.txt.
    all messages have equal chance of being selected.
    return True if successful.
    """
    reply_messages: list[str] = gen.try_import_messages("messages/thank.txt")
    msg: str = random.choice(reply_messages)
    notif: str = f"[THANK] {REDDIT_URL}{comment.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    try:
        comment.reply(body=msg)
        gen.post_webhook({"content": notif})
        return True
    except Exception as err:
        print(err)
        gen.post_webhook({"content": err})
        return False


def reply_custom(comment, msg, debug=False) -> bool:
    """
    submits a comment as a reply to a comment
    with a custom reply message.
    returns True if successful.
    """
    notif: str = f"[CUSTOM] {REDDIT_URL}{comment.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    try:
        comment.reply(body=msg)
        gen.post_webhook({"content": notif})
        return True
    except Exception as err:
        print(err)
        gen.post_webhook({"content": err})
        return False


def already_replied_submission(submission, username) -> bool:
    """checks if a submission has already been replied to."""
    for top_comment in submission.comments:
        if top_comment.parent().id != submission.id:
            break
        if top_comment.author == username:
            print(f"same {REDDIT_URL}{submission.permalink}")
            return True
    return False


def already_replied_comment(comment, username) -> bool:
    """checks if a comment has already been replied to."""
    second_refresh = False
    for _ in range(2):
        try:
            comment.refresh()
            break
        except praw.exceptions.ClientException:
            print("comments didn't load, trying again...")
            if second_refresh:
                print("couldn't load comments, assuming already replied")
                return True
            time.sleep(10)
            second_refresh = True
    # comment.replies.replace_more()
    child_comments = comment.replies.list()
    for top_comment in child_comments:
        if top_comment.parent().id != comment.id:
            break
        if top_comment.author == username:
            print(f"same {REDDIT_URL}{comment.permalink}")
            return True
    return False


def comment_is_user(comment, username, parent_level=0) -> bool:
    """checks if a comment's author is the user"""
    while parent_level > 0:
        if hasattr(comment, "parent"):
            comment = comment.parent()
            parent_level -= 1
        else:
            return False
    return comment.author and comment.author == username


def keyword_in_comment(comment, *keywords) -> bool:
    """
    check if any keywords appear in comment body text.
    keywords should be lowercase, alphanumeric only, no spaces.
    """
    body: str = re.sub("[^a-z0-9]", "", comment.body.lower())
    return any(key in body for key in keywords)


def keyword_in_submission(submission, *keywords) -> bool:
    """
    check if any keywords appear in submission title or body text.
    keywords should be lowercase, alphanumeric only, no spaces.
    """
    title: str = re.sub("[^a-z0-9]", "", submission.title.lower())
    text: str = re.sub("[^a-z0-9]", "", submission.selftext.lower())
    return any(key in title or key in text for key in keywords)
