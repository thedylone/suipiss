import csv

import bot


def main():
    comments = bot.reddit.user.me().comments.new(limit=None)
    loopComments(comments)


def loopComments(comments):
    with open("bot.csv", "w", newline="") as file:
        csv_writer = csv.writer(file, dialect="excel")
        csv_writer.writerow(["comment id", "comment time"])
        for comment in comments:
            csv_writer.writerow([comment.id, comment.created_utc])


if __name__ == "__main__":
    main()
