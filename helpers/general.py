import os
from os.path import join, dirname
from dotenv import load_dotenv
import sys
import requests
import json
import yaml

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def exit_signal_handler(signal, frame):
    """handle exit when signal is received"""
    print("shutting gracefully...")
    post_webhook({"content": "shutting gracefully..."})
    sys.exit(0)


def try_load_config(path):
    """
    attempts to read a config yaml file and returns the config
    if successful. raises error if config file cannot be read.
    """
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"{path} not found!")
        if path == "config.yaml":
            print("creating config.yaml...")
            with open("config.yaml", "w") as f:
                yaml.dump({"SUBREDDITS": "", "KEYWORD": ""}, f)
            print("please fill in the config.yaml with your configurations")
        raise e
    except yaml.scanner.ScannerError or yaml.parser.ParserError as e:
        print("invalid file! please ensure it is valid")
        raise e
    except Exception as e:
        print("an error occured")
        raise e
    return config


def try_import_messages(path, default_message="suipiss"):
    """
    attempts to read file at given path and return list
    of items split by line. if file is empty or unable to
    be read, returns a list containing the default message.
    """
    reply_text_messages = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reply_text_messages = f.read().splitlines()
    except OSError:
        print(f"unable to open {path}")
    except Exception as e:
        print(f"unexpected error opening {path}: {e}")
    if not reply_text_messages:
        print("no messages found, using default message")
        reply_text_messages = [default_message]
    return reply_text_messages


def assign_random_weights(list):
    """
    returns a list of weights from the input.
    if there are multiple items, the first item has 0.5 chance,
    and the remaining 0.5 is split among the remaining items.
    """
    length = len(list)
    if length == 0:
        weights = []
    elif length > 1:
        weights = [0.5] + [0.5 / (length - 1)] * (length - 1)
    elif length == 1:
        weights = [1]
    return weights


def post_webhook(data, url=os.environ.get("WEBHOOK_URL")):
    req = requests.post(
        url=url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    return req.status_code
