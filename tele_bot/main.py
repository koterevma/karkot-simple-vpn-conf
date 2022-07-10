#!/usr/bin/env python

"""
Bot to give access to vpn configuration

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import userdata

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    data_path, is_admin = userdata.get_user_data(user.id)
    text = f"{user.id=}, {data_path=}, {is_admin=}"
    await update.message.reply_text(text)


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Type /start to send a request for a vpn configuration")


def main() -> None:
    """Start the bot."""

    # Add admins in database
    admins = os.getenv("ADMINS")
    if admins is not None:
        logging.info(f"Got {admins=}")
        userdata.add_admins(admins)

    # Create the Application and pass it bot's token.
    token = os.getenv("TOKEN")
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_))

    # on non command i.e message - print help
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

