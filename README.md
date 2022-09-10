# suipiss

suipiss bot is a reddit bot that responds to this keyword: `suipiss`.

it is currently running on [u/suipiss](https://www.reddit.com/user/suipiss), serving the [r/okbuddyhololive subreddit](https://www.reddit.com/r/okbuddyhololive/).

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Z8Z0EY6XA)

## what is suipiss?

it's complicated

## deploying your own bot

after creating your app on the [reddit prefs apps page](https://www.reddit.com/prefs/apps), complete the following steps:

1. create a copy of the [example.env file](/example.env) and rename it to `.env`

in the newly created `.env` file:

2. replace the variables with your own bot's authentication details

there are more configurations to edit as well, in the [config.yaml file](/config.yaml)

3. replace the variables with your desired configurations. note that username refers to the reddit account's username.

running the `bot.py` script should start the bot. to confirm that the bot is logged in, the script will print out your bot's username.

the bot can notify you (i.e. via discord) when it replies automatically via webhooks. place your discord webhook url into the `.env` file for it to send to.

## customising your messages

messages are stored in the [messages folder](/messages/). for each custom message, put the message on its own line. the bot will look for [`mention.txt`](/messages/mention.txt) and [`thank.txt`](/messages/thank.txt). if the bot is unable to read `mention.txt` or `thank.txt`, it will use the default message instead.

### mention.txt

the bot will use `mention.txt` if the keyword has been mentioned in either a post (submission) or comment. the bot will have a 50% chance of selecting the first message listed in `mention.txt`. the remaining 50% is split equally among the rest of the options.

### thank.txt

when someone replies to the bot's comment thanking the bot, the bot will randomly pick one message from `thank.txt`. all messages have equal chances of being picked.