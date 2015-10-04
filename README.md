# cc-telegram
Bot framework for Telegram Messenger

## Modules ##
We are supporting several kinds of modules for bot's reaction to different types of messages:
* If filename starts with `user_` or `owner_`, the command will be available with `/command` syntax. Bot will call module with args as splitted text after `/command` statement. See `modules/user_echo.py` for example.
* If filename starts with `audio_`, `video_`, `text_`, etc, bot will call module with [`message`](https://core.telegram.org/bots/api#message) and `update` objects.

You can return any message from module using `return` statement (see `modules/user_lsmod.py`). You also able to call bot's methods directly from module (to call telegram api or to send chat action, for example).
