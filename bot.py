import os
from os.path import join, dirname
from dotenv import load_dotenv
import praw
import signal
from helpers import general, func


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
config = general.try_load_config("config.yaml")
USERNAME = os.environ.get("BOT_USERNAME")
SUBREDDITS = config.get("SUBREDDITS", "okbuddyhololive")
KEYWORD = config.get("KEYWORD", USERNAME)

reddit = praw.Reddit(
    user_agent=os.environ.get("USER_AGENT"),
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    username=USERNAME,
    password=os.environ.get("PASSWORD"),
)


def main():
    print(reddit.user.me())
    general.post_webhook({"content": f"logged in as {reddit.user.me()}"})

    subreddits = reddit.subreddit(SUBREDDITS)
    comment_stream = subreddits.stream.comments(pause_after=-1)
    submission_stream = subreddits.stream.submissions(pause_after=-1)
    while True:
        for comment in comment_stream:
            if comment is None:
                break
            if func.comment_is_self(comment, USERNAME):
                continue
            if func.already_replied_comment(comment, USERNAME):
                continue
            if func.comment_is_self(comment, USERNAME, 1):
                gratitude = ["thank", "good", "love"]
                if func.keyword_in_comment(comment, *gratitude):
                    func.reply_gratitude(comment)
                    continue
            if func.comment_is_self(comment, USERNAME, 2):
                if comment.author.name == "B0tRank":
                    func.reply_custom(comment, "bot??? not bot")
                    continue
            if func.keyword_in_comment(comment, KEYWORD):
                if comment.author.name == "pekofy_bot":
                    func.reply_custom(comment, "suipiss peko suipiss peko")
                elif not func.comment_is_self(comment, USERNAME, 1):
                    # dont reply to own comment to prevent spam
                    func.reply_mention(comment)
                continue

        for submission in submission_stream:
            if submission is None:
                break
            if func.already_replied_submission(submission, USERNAME):
                continue
            if func.keyword_in_submission(submission, KEYWORD):
                func.reply_submission(submission)
                continue


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, general.exit_signal_handler)
    signal.signal(signal.SIGINT, general.exit_signal_handler)
    main()
