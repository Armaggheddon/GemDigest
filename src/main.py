#! /usr/bin/python3

"""This script serves as the entry point for running the bot application.

It imports the `bot` module and executes its `run()` function if the script is 
executed as the main program.

Imports:
    - bot: The module containing the bot logic, with a `run` function to 
        start the bot.

Usage:
    To run the bot, execute this script:
        $ ./script_name.py
"""
import bot


if __name__ == '__main__':
    bot.run()
