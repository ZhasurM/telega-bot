#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from html import escape
from uuid import uuid4

TOKEN = os.getenv('TOKEN')

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import (
    InlineQueryResultArticle, 
    InlineQueryResultCachedPhoto, 
    InputTextMessageContent, 
    Update, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove,
    )
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    InlineQueryHandler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Меню"],["Информация", "Осставить отзыв  "],["kkkkk"]]

    await update.message.reply_text(
        "Главное меню",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Самса"],["Плов", "Напитки"],["огшртлотлот"]]

    await update.message.reply_text(
        "Главное меню",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            type='article',
            description="uirjfrkfokrmfrk",
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
            #photo_url="https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf",
            thumb_url="https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf",
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            type='article',
            description="uirjfrkfokrmfrk",
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
            #photo_url="https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf",
            thumb_url="https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf",
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            type='article',
            description="uirjfrkfokrmfrk",
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
            #photo_url="https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf",
            thumb_url="https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf",
        ),
    ]

    await update.inline_query.answer(results)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Меню$"), menu)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), menu)],
            PHOTO: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), menu)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
        },
        fallbacks=[CommandHandler("cancel", menu)],
    )

    application.add_handler(conv_handler)

    # on non command i.e message - echo the message on Telegram
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()