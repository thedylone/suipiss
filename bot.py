import time
import random
import re
import praw
import os

USERNAME = os.environ.get("USERNAME")


def reply_submission(submission):
    """submits a comment to a submission."""
    submission.reply("suipiss")
    print(f"replied to post {submission.permalink}")


def reply_mention(mention):
    """
    submits a comment as a reply to a mentioned comment.
    has a 50% chance to reply with the first message in reply_text_messages,
    with 50% chance split among the other messages in reply_text_messages.
    """
    reply_text_messages = [
        "suipiss",
        "[suipiss](https://youtube.com/clip/UgkxphA8-saXuOVatZ-TXls3l-JVYEzTRO6X)",
        "suisex",
        "i love suipiss mmmmmmmmmmmmmmmmmmm",
        "ringo juice yum",
        "u heard of SUIPISS? a holy liquid occationally leaks from somewhere between two legs of suisei's",
        "This fucking joke of a subreddit is the sole reason I can no longer watch Suisei's streams anymore. She WAS my favourite streamer of all time, nevermind in the context of hololive. Her streams are a masterpiece especially compared to today's vtuber trash on youtube. On my darkest days, I would put her stream on and be moved to tears everytime. But the fucking basement dwellers of r/okbuddyhololive have ruined any sense of enjoyment I had watching her streams. Mainly because of the stupid fucking meme of \"HoLY SHIt GuYS mY sUiPiSs iS CoMInG I bOuGht fIVe LiTTeRs?!!??\" And whenever I watch her streams and her her voice, I break down in hysterics because all I can think of is that dumbass fucking meme and the subhuman trash populating that subreddit. It ruins and emotional weigh and meaning to her videos because it's clouded by their absolute stupidity. I had to bring this up to my therapist because she was so special to me and this whole experience psychologically damaged me. I guess art is dead because people can't take art seriously anymore. They have to make it about some dead fucking meme or something and entirely devalue the art. This is the death of art happening before our very eyes, folks. And if you won't stand for the most influential artist of the century and not let their name be smeared by jokers of the internet, than you are not a true hololive fan. I want r/okbuddyhololive to be taken down because this is a disgrace to human expression and an assult on the psyche. Fuck you and fuck your dumbass fucking memes. Suisei deserves way better.",
        "I've been mixing my own urine, various perfumes and chemicals to make the perfect emulation of Hoshimachi Suisei's urine scent.",
        "I have also been eating a rather Asian diet to emulate what Suisei would eat and drink.",
        "I'm about three weeks into the project and have been strategically disposing portions of old urine, replacing it with new urine, adding slight touches of extra ammonia, expired apple juice (I suspect her urine would have a rather tangy flavour) and trace amounts of nitric acid.",
        "I've been mixing my own urine, various perfumes and chemicals to make the perfect emulation of Hoshimachi Suisei's urine scent. I have also been eating a rather Asian diet to emulate what Suisei would eat and drink. I'm about three weeks into the project and have been strategically disposing portions of old urine, replacing it with new urine, adding slight touches of extra ammonia, expired apple juice (I suspect her urine would have a rather tangy flavour) and trace amounts of nitric acid.",
        "(I suspect her urine would have a rather tangy flavour)",
        "There's some semen in the mix as well, sorry about that.",
        "It's very bubbly because of 7 Up, which I used to simulate the prescence of carbonated beverages in her diet",
        "My plan is to smell the cup periodically during her streams. Drink rarely in sips so the mixture doesn't harm me.",
    ]
    reply_text_weights = [0.5] + [0.5 / (len(reply_text_messages) - 1)] * (
        len(reply_text_messages) - 1
    )
    mention.reply(random.choices(reply_text_messages, weights=reply_text_weights, k=1))
    print(f"mentioned {mention.permalink}")


def reply_gratitude(comment):
    """
    submits a comment as a reply to a comment thanking the bot.
    randomly chooses a message from reply_text_messages.
    """
    reply_text_messages = [
        "suipiss",
        "arigathanks",
        "pekoggers",
        "suipiss <3",
        "fubuhappy",
        ":D",
        "suicum",
    ]
    comment.reply(random.choice(reply_text_messages))
    print(f"thanked {comment.permalink}")


def reply_custom(comment, reply_message):
    """submits a comment as a reply to a comment with a custom reply message."""
    comment.reply(reply_message)
    print(f"replied custom comment with {reply_message} at {comment.permalink}")


def already_replied_submission(submission):
    """checks if a submission has already been replied to."""
    for top_comment in submission.comments:
        if top_comment.parent().id != submission.id:
            break
        if top_comment.author == "suipiss":
            print(f"same {submission.permalink}")
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
            print(f"same {comment.permalink}")
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
    main()
