import time
import random
import re
import praw
import helpers.general as gen


def reply_submission(submission, webhook=True, debug=False):
    """
    submits a comment to a submission.
    attempts to retrieve messages from messages/mention.txt.
    if there are multiple messages, the first messages has a
    50% chance of being selected.
    return True if successful.
    """
    reply_messages = gen.try_import_messages("messages/mention.txt")
    reply_weights = gen.assign_random_weights(reply_messages)
    msg = random.choices(reply_messages, weights=reply_weights, k=1)[0]
    notif = f"[POST] https://www.reddit.com{submission.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    else:
        try:
            submission.reply(body=msg)
            if webhook:
                gen.post_webhook({"content": notif})
            return True
        except Exception as e:
            print(e)
            if webhook:
                gen.post_webhook({"content": e})
            return False


def reply_mention(mention, webhook=True, debug=False):
    """
    submits a comment as a reply to a mentioned comment.
    attempts to retrieve messages from messages/mention.txt.
    if there are multiple messages, the first messages has a
    50% chance of being selected.
    return True if successful.
    """
    reply_messages = gen.try_import_messages("messages/mention.txt")
    reply_weights = gen.assign_random_weights(reply_messages)
    msg = random.choices(reply_messages, weights=reply_weights, k=1)[0]
    notif = f"[MENTION] https://www.reddit.com{mention.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    else:
        try:
            mention.reply(body=msg)
            if webhook:
                gen.post_webhook({"content": notif})
            return True
        except Exception as e:
            print(e)
            if webhook:
                gen.post_webhook({"content": e})
            return False


def reply_gratitude(comment, webhook=True, debug=False):
    """
    submits a comment as a reply to a comment thanking the bot.
    attempts to retrieve messages from messages/thank.txt.
    all messages have equal chance of being selected.
    return True if successful.
    """
    reply_messages = gen.try_import_messages("messages/thank.txt")
    msg = random.choice(reply_messages)
    notif = f"[THANK] https://www.reddit.com{comment.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    else:
        try:
            comment.reply(body=msg)
            if webhook:
                gen.post_webhook({"content": notif})
            return True
        except Exception as e:
            print(e)
            if webhook:
                gen.post_webhook({"content": e})
            return False


def reply_custom(comment, msg, webhook=True, debug=False):
    """
    submits a comment as a reply to a comment
    with a custom reply message.
    returns True if successful.
    """
    notif = f"[CUSTOM] https://www.reddit.com{comment.permalink} with {msg}"
    print(notif)
    if debug:
        print("debug: assume reply successful")
        return True
    else:
        try:
            comment.reply(body=msg)
            if webhook:
                gen.post_webhook({"content": notif})
            return True
        except Exception as e:
            print(e)
            if webhook:
                gen.post_webhook({"content": e})
            return False


def already_replied_submission(submission, username):
    """checks if a submission has already been replied to."""
    for top_comment in submission.comments:
        if top_comment.parent().id != submission.id:
            break
        if top_comment.author == username:
            print(f"same https://www.reddit.com{submission.permalink}")
            return True
    return False


def already_replied_comment(comment, username):
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
    comment.replies.replace_more()
    child_comments = comment.replies.list()
    for top_comment in child_comments:
        if top_comment.parent().id != comment.id:
            break
        if top_comment.author == username:
            print(f"same https://www.reddit.com{comment.permalink}")
            return True
    return False


def comment_is_self(comment, username, parent_level=0):
    """checks if a comment's author is the user"""
    while parent_level > 0:
        if hasattr(comment, "parent"):
            comment = comment.parent()
            parent_level -= 1
        else:
            return False
    return comment.author and comment.author == username


def keyword_in_comment(comment, *keywords):
    body = re.sub("[^a-z0-9]", "", comment.body.lower())
    return any(key in body for key in keywords)


def keyword_in_submission(submission, *keywords):
    title = re.sub("[^a-z0-9]", "", submission.title.lower())
    text = re.sub("[^a-z0-9]", "", submission.selftext.lower())
    return any(key in title or key in text for key in keywords)
