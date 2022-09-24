#!/usr/bin/env python

"""
Bot to give access to vpn configuration

Ships in docker container
"""

import logging
import os
from pathlib import Path
from telegram import Update, Bot
from telegram.ext import (
        Application,
        CommandHandler,
        ContextTypes,
        MessageHandler
)
from telegram.ext.filters import TEXT, COMMAND
from telegram.constants import ParseMode

import userdata
import wgconf

from classes import User


# Enable logging
logging.basicConfig(
    format="%(asctime)s;%(name)s;%(levelname)s;%(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def send_confirmation_request(bot: Bot, username: str, user_id: int) -> None:
    admin_ids = userdata.get_admin_ids()
    for admin_id in admin_ids:
        await bot.send_message(
            admin_id, rf"@{username} requests config\. `/accept {user_id}`",
            parse_mode=ParseMode.MARKDOWN_V2)


# Start command - register user and send confirmation request to admins
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    telegram_user = update.effective_user
    if telegram_user is None:
        return

    user_from_database = userdata.get_user_data(telegram_user.id)
    text = "User already registered, waiting approval from admins"
    if user_from_database is None:
        userdata.add_user(User(telegram_user.id))
        await send_confirmation_request(context.bot, telegram_user.username, telegram_user.id)
        text = "Registered new user and send confirmation message to admins"
    elif user_from_database.config_path is not None:
        text = "User already exists, type /get_config to get configuration"
    await update.message.reply_text(text)


async def help_(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Type /start to request config from admin.\n"
            "Help with setting VPN on your device here "
            "https://github.com/koterevma/karkot-simple-vpn-conf#for-user")


async def send_config(user_id: int, config_dir: Path, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    qr_file = config_dir / (config_dir.name + ".png")
    conf_file = config_dir / (config_dir.name + ".conf")

    await bot.send_photo(user_id,
                         photo=qr_file.open("rb"),
                         caption="Request accepted! Here's your configuration",
                         filename=qr_file.name)
    await bot.send_document(user_id,
                            conf_file.open("rb"),
                            filename=conf_file.name)


async def accept(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Accept user and give them configuration"""
    if update.message.from_user.id not in userdata.get_admin_ids():
        await update.message.reply_text("Not an admin, can not accept a user")
        return

    accepted_user_id = int(update.message.text.split()[1])
    new_config_dir = wgconf.get_new_config()
    userdata.update_user(
                accepted_user_id,
                config_path=str(new_config_dir.absolute()))

    await send_config(accepted_user_id, new_config_dir, context)


async def get_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user
    if telegram_user is None:
        return

    user_from_database = userdata.get_user_data(telegram_user.id)
    if user_from_database is None:
        await update.message.reply_text("User is not registered")
        return

    assigned_config = user_from_database.config_path
    if assigned_config is None:
        await update.message.reply_text("User don't have assigned config,"
                                        " try requesting one with /start")
        return

    await send_config(user_from_database.id, Path(assigned_config), context)


def main() -> None:
    """Start the bot."""

    # Add admins in database
    admins = os.getenv("ADMINS")
    if admins is not None:
        logging.info("Got admins=%r", admins)
        userdata.add_admins(map(int, admins.split(",")))

    # Create the Application and pass it bot's token.
    token = os.getenv("TOKEN")
    if token is None:
        raise RuntimeError("Environment variable TOKEN is not set")

    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_))
    application.add_handler(CommandHandler("accept", accept))
    application.add_handler(CommandHandler("get_config", get_config))

    # on non command i.e message - print help
    application.add_handler(MessageHandler(TEXT & ~COMMAND, help_))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
