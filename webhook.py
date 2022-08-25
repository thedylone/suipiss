import requests
import os
import json


def post_webhook(data):
    print(
        requests.post(
            url=os.environ.get("WEBHOOK_URL"),
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        ).text
    )


def main():
    post_webhook(
        {
            "content": "hi",
            "embeds": [
                {
                    "title": "hi",
                    "description": "hi :D",
                    "image": {"url": "https://i.redd.it/rtosmchd84z61.jpg"},
                }
            ],
        }
    )


if __name__ == "__main__":
    main()
