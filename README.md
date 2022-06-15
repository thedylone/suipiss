# suipiss

suipiss bot is a reddit bot that responds to this keyword: `suipiss`.

it is currently running on [u/suipiss](https://www.reddit.com/user/suipiss), serving the [r/okbuddyhololive subreddit](https://www.reddit.com/r/okbuddyhololive/).

## what is suipiss?

it's complicated

## deploying your own bot

after creating your app on the [reddit prefs apps page](https://www.reddit.com/prefs/apps), complete the following steps:

1. create a copy of the [example.env file](/example.env) and rename it to `.env`

in the newly created `.env` file:

2. replace the variables with your own bot's authentication details
3. specify which subreddits to monitor

running the `bot.py` script should start the bot. to confirm that the bot is logged in, the script will print out your bot's username.