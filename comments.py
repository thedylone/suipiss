import praw
import csv
import os

def main():
    reddit = praw.Reddit(
        user_agent=os.environ["user_agent"],
        client_id=os.environ["client_id"],
        client_secret=os.environ["client_secret"],
        username=os.environ["username"],
        password=os.environ["password"],
    )
    print(reddit.user.me())
    comments = reddit.user.me().comments.new(limit=None)
    loopComments(comments)

def loopComments(comments):
    with open('bot.csv', 'w', newline='') as file:
        csv_writer = csv_writer(file, dialect='excel')
        csv_writer.writerow(['comment id', 'comment time'])
        for comment in comments:
            csv_writer.writerow([comment.id, comment.created_utc])