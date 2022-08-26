import time
import random
import re
import praw
import os
import signal
import sys

import webhook

USERNAME = os.environ.get("USERNAME")


def exit_signal_handler(signal, frame):
    print("shutting gracefully...")
    webhook.post_webhook({"content": "shutting gracefully..."})
    sys.exit(0)


def reply_submission(submission):
    """submits a comment to a submission."""
    try:
        with open("messages/mention.txt", "r", encoding="utf-8") as f:
            reply_text_messages = f.read().splitlines()
        if not reply_text_messages:
            print("messages/mention.txt empty, using default")
            reply_text_messages = ["suipiss"]
    except:
        print("unable to open messages/mention.txt, using default")
        reply_text_messages = ["suipiss"]
    reply_text_weights = [0.5] + [0.5 / (len(reply_text_messages) - 1)] * (
        len(reply_text_messages) - 1
    )
    submission.reply(
        body=random.choices(reply_text_messages, weights=reply_text_weights, k=1)
    )
    print(f"replied to post https://www.reddit.com{submission.permalink}")
    webhook.post_webhook(
        {"content": f"replied to post https://www.reddit.com{submission.permalink}"}
    )


def reply_mention(mention):
    """
    submits a comment as a reply to a mentioned comment.
    has a 50% chance to reply with the first message in reply_text_messages,
    with 50% chance split among the other messages in reply_text_messages.
    """
    try:
        with open("messages/mention.txt", "r", encoding="utf-8") as f:
            reply_text_messages = f.read().splitlines()
        if not reply_text_messages:
            print("messages/mention.txt empty, using default")
            reply_text_messages = ["suipiss"]
    except:
        print("unable to open messages/mention.txt, using default")
        reply_text_messages = ["suipiss"]
    reply_text_weights = [0.5] + [0.5 / (len(reply_text_messages) - 1)] * (
        len(reply_text_messages) - 1
    )
    mention.reply(
        body=random.choices(reply_text_messages, weights=reply_text_weights, k=1)
    )
    print(f"mentioned https://www.reddit.com{mention.permalink}")
    webhook.post_webhook(
        {"content": f"mentioned https://www.reddit.com{mention.permalink}"}
    )


def reply_gratitude(comment):
    """
    submits a comment as a reply to a comment thanking the bot.
    randomly chooses a message from reply_text_messages.
    """
    try:
        with open("messages/thank.txt", "r", encoding="utf-8") as f:
            reply_text_messages = f.read().splitlines()
        if not reply_text_messages:
            print("messages/thank.txt empty, using default")
            reply_text_messages = ["suipiss"]
    except:
        print("unable to open messages/thank.txt, using default")
        reply_text_messages = ["suipiss"]
    comment.reply(body=random.choice(reply_text_messages))
    print(f"thanked https://www.reddit.com{comment.permalink}")
    webhook.post_webhook(
        {"content": f"thanked https://www.reddit.com{comment.permalink}"}
    )


def reply_custom(comment, reply_message):
    """submits a comment as a reply to a comment with a custom reply message."""
    comment.reply(body=reply_message)
    print(
        f"replied custom comment with {reply_message} at https://www.reddit.com{comment.permalink}"
    )
    webhook.post_webhook(
        {
            "content": f"replied custom comment with {reply_message} at https://www.reddit.com{comment.permalink}"
        }
    )


def already_replied_submission(submission):
    """checks if a submission has already been replied to."""
    for top_comment in submission.comments:
        if top_comment.parent().id != submission.id:
            break
        if top_comment.author == "suipiss":
            print(f"same https://www.reddit.com{submission.permalink}")
            return True
    return False


def already_replied_comment(comment):
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
        if top_comment.author == "suipiss":
            print(f"same https://www.reddit.com{comment.permalink}")
            return True
    return False


def main():
    reddit = praw.Reddit(
        user_agent=os.environ.get("USER_AGENT"),
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        username=USERNAME,
        password=os.environ.get("PASSWORD"),
    )
    print(reddit.user.me())
    webhook.post_webhook({"content": f"logged in as {reddit.user.me()}"})

    subreddits = reddit.subreddit(os.environ.get("SUBREDDITS", "okbuddyhololive"))
    comment_stream = subreddits.stream.comments(pause_after=-1)
    submission_stream = subreddits.stream.submissions(pause_after=-1)
    while True:
        for comment in comment_stream:
            if comment is None:
                break
            if (
                not comment.author
                or comment.author == USERNAME
                or already_replied_comment(comment)
            ):
                continue
            if comment.parent().author and comment.parent().author.name == USERNAME:
                gratitude = ["thank", "good", "love"]
                if any(
                    thank in re.sub("[^a-z0-9]", "", comment.body.lower())
                    for thank in gratitude
                ):
                    reply_gratitude(comment)
                    continue
            if (
                not comment.is_root
                and comment.parent().parent().author
                and comment.parent().parent().author.name == USERNAME
            ):
                if comment.author.name == "B0tRank":
                    reply_custom(comment, "bot??? not bot")
                    continue
            if (
                "suipiss" in re.sub("[^a-z0-9]", "", comment.body.lower())
                and comment.parent().author
                and comment.parent().author.name != USERNAME
            ):
                if comment.author.name == "pekofy_bot":
                    reply_custom(
                        comment, "suipiss peko suipiss peko suipiss peko suipiss peko"
                    )
                else:
                    reply_mention(comment)
                continue

        for submission in submission_stream:
            if submission is None:
                break
            if already_replied_submission(submission):
                continue
            if "suipiss" in re.sub(
                "[^a-z0-9]", "", submission.title.lower()
            ) or "suipiss" in re.sub("[^a-z0-9]", "", submission.selftext.lower()):
                reply_submission(submission)
                continue


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, exit_signal_handler)
    signal.signal(signal.SIGINT, exit_signal_handler)
    signal.signal(signal.SIGBREAK, exit_signal_handler)
    main()
