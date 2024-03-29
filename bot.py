"""main file for the bot"""

import argparse
import os
import signal
import time
from os.path import dirname, join

import praw
from dotenv import load_dotenv

from helpers import func, general

dotenv_path: str = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
config: dict = general.try_load_config("config.yaml")
USERNAME: str = os.environ.get("BOT_USERNAME", "suipiss")
SUBREDDITS: str = config.get("SUBREDDITS", "okbuddyhololive")
KEYWORD: str = config.get("KEYWORD", USERNAME)
DEBUG_MODE = False

reddit = praw.Reddit(
    user_agent=os.environ.get("USER_AGENT"),
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    username=USERNAME,
    password=os.environ.get("PASSWORD"),
)


def main():
    """main function"""
    print(reddit.user.me())
    if not DEBUG_MODE:
        general.post_webhook({"content": f"logged in as {reddit.user.me()}"})

    subreddits = reddit.subreddit(SUBREDDITS)
    comment_stream = subreddits.stream.comments(pause_after=-1)
    submission_stream = subreddits.stream.submissions(pause_after=-1)
    custom_logic: dict = general.try_load_config("custom.yaml")
    while True:
        try:
            for comment in comment_stream:
                if comment is None:
                    break
                func.comment_logic(
                    comment,
                    USERNAME,
                    KEYWORD,
                    custom_logic=custom_logic,
                    debug=DEBUG_MODE,
                )

            for submission in submission_stream:
                if submission is None:
                    break
                func.submission_logic(
                    submission, USERNAME, KEYWORD, debug=DEBUG_MODE
                )
        except Exception as e:
            # if 429 HTTP error or 503 HTTP error, sleep for 10 minutes
            if "429" in str(e) or "503" in str(e):
                time.sleep(600)
            else:
                raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run reddit bot")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="run in debug mode",
    )
    args = parser.parse_args()
    DEBUG_MODE = args.debug
    if not DEBUG_MODE:
        signal.signal(signal.SIGTERM, general.exit_signal_handler)
        signal.signal(signal.SIGINT, general.exit_signal_handler)
    try:
        main()
    except Exception as e:
        if not DEBUG_MODE:
            general.post_webhook({"content": f"fatal error encountered: {e}"})
        raise e
