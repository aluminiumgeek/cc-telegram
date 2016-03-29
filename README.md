# cc-telegram
Async bot framework for Telegram Messenger designed for Python >= 3.5.  
Named after [シー・ツー ](https://en.wikipedia.org/wiki/C.C._(Code_Geass))

[![tip for next commit](https://tip4commit.com/projects/43141.svg)](https://tip4commit.com/github/aluminiumgeek/cc-telegram)  
![1](https://img.shields.io/badge/code-geass-green.svg)

## Running ##
Clone the repo, fill settings.py with your settings. Run:

`python3 cc.py`

You can also run bot with different config module. For example, if your settings file is called `settings_test.py`, run:

`python3 cc.py -s settings_test`

You can daemonize bot by adding `-d` option:

`python3 cc.py -d`

To get all available options check:

`python3 cc.py --help`

## Modules ##
All modules should be written with async in mind, since modules executor is non-blocking and built on top of Python's `asyncio`.  
However, if you write blocking module, it will not block main event loop anyway, CC is designed to run blocking module in another thread.

Async modules should define `main` method as `async def main(bot, *args, **kwargs)` and use `await` keyword where it's needed. You can check some modules inside `modules` dir of this repo and see differences between blocking and non-blocking modules.

Module types:
- `user_*` - command called with '/command' syntax, available for all users
- `owner_*` - command called with '/command' syntax, available only for owner (there's `owner` option in the settings)
- `audio_*` - module will be called on each audio message
- `video_*` - called on each video message
- `text_*` - called on each text message
- `photo_*` - called on each message with photo
- `sticker_*` - called on each message with sticker

Check currently available modules by running `/lsmod` command in chat.

## Running tests ##
You can run the full test suite using:

`python3 -m unittest discover tests`

