# cc-telegram
Bot framework for Telegram Messenger

[![tip for next commit](https://tip4commit.com/projects/43141.svg)](https://tip4commit.com/github/aluminiumgeek/cc-telegram)

## Running ##
Clone the repo, fill settings.py with your settings. Run:

`python3 cc.py`

You can also run bot with different config module. For example, if your settings file called `settings_text.py`, run:

`python3 cc.py -s settings_test`

You can daemonize bot by adding `-d` option:

`python3 cc.py -d`

To get all available options check:

`python3 cc.py --help`

## Modules ##
We support several kinds of modules for bot's reaction to different types of messages:
* If filename starts with `user_` or `owner_`, the command will be available with `/command` syntax. Bot will call module with args as splitted text after `/command` statement. See `modules/user_echo.py` for example.
* If filename starts with `audio_`, `video_`, `text_`, etc, bot will call module with [`message`](https://core.telegram.org/bots/api#message) and `update` objects.

You can return any message from module using `return` statement (see `modules/user_lsmod.py`). You also able to call bot's methods directly from module (to call telegram api or to send chat action, for example).

Check currently available modules by running `/lsmod` command in chat.

## Running tests ##
You can run the full test suite using:

`python -m unittest discover tests`

