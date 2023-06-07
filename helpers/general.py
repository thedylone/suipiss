"""general helper functions"""

import os
import sys
import json
from os.path import join, dirname
from dotenv import load_dotenv
import yaml
import requests

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


def exit_signal_handler(_signal, _frame):
    """handle exit when signal is received"""
    print("shutting gracefully...")
    post_webhook({"content": "shutting gracefully..."})
    sys.exit(0)


def try_load_config(path) -> dict:
    """
    attempts to read a config yaml file and returns the config
    if successful. raises error if config file cannot be read.
    """
    config: dict = {}
    try:
        with open(path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError as err:
        print(f"{path} not found!")
        if path == "config.yaml":
            print("creating config.yaml...")
            with open("config.yaml", "w", encoding="utf-8") as file:
                yaml.dump({"SUBREDDITS": "", "KEYWORD": ""}, file)
            print("please fill in the config.yaml with your configurations")
        raise err
    except yaml.scanner.ScannerError as err:
        print("invalid file! please ensure it is valid")
        raise err
    except Exception as err:
        print("an error occured")
        raise err
    return config


def try_import_messages(path, default_message="suipiss") -> list[str]:
    """
    attempts to read file at given path and return list
    of items split by line. if file is empty or unable to
    be read, returns a list containing the default message.
    """
    reply_text_messages: list[str] = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            reply_text_messages = file.read().splitlines()
    except OSError:
        print(f"unable to open {path}")
    except Exception as err:
        print(f"unexpected error opening {path}: {err}")
    if not reply_text_messages:
        print("no messages found, using default message")
        reply_text_messages = [default_message]
    return reply_text_messages


def assign_random_weights(input_list: list[str]) -> list[float]:
    """
    returns a list of weights from the input.
    if there are multiple items, the first item has 0.5 chance,
    and the remaining 0.5 is split among the remaining items.
    """
    length: int = len(input_list)
    weights: list[float] = []
    if length == 0:
        weights = []
    elif length > 1:
        weights = [0.5] + [0.5 / (length - 1)] * (length - 1)
    elif length == 1:
        weights = [1]
    return weights


def post_webhook(data, url=os.environ.get("WEBHOOK_URL")) -> int:
    """posts data to webhook"""
    if not url:
        return 0
    req: requests.Response = requests.post(
        url=url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    return req.status_code
