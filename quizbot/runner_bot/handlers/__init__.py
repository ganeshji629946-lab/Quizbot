"""
Advance Quiz Bot — Open Source Project
This project was originally developed by Gagan (github.com/devgaganin).
Reference: https://t.me/advance_quiz_bot
The codebase has been reviewed and verified with the assistance of Claude AI.
"""

from __future__ import annotations

from telegram.ext import Application

from . import admin, ai_quiz, mix, pdf_quiz, poll_quiz, quiz_play, reports, scheduling, setup_wizard, translation


# Keep quiz deep links routed to the normal quiz handler, but give a bare
# /start a short welcome response.
_start_quiz = quiz_play.start_quiz


async def _start_quiz_with_welcome(update, ctx) -> None:
    if not ctx.args:
        await update.message.reply_text("Welcome 🤗")
        return
    await _start_quiz(update, ctx)


quiz_play.start_quiz = _start_quiz_with_welcome

_MODULES = (
    quiz_play,     # /start, /pause, /resume, /stop, /leaderboard, /slow, /fast, /normal, poll answers
    setup_wizard,  # qs_* quiz-setup wizard callbacks
    poll_quiz,     # /pollquiz, /pollstop
    mix,           # /mix
    ai_quiz,       # /aiquiz
    pdf_quiz,      # /pdfquiz
    reports,       # /html, /pdf, compare_ callback
    scheduling,    # /schedule, /viewschedule, /cancelschedule
    translation,   # /trans
    admin,         # /help, channel command routing (registered last so it doesn't
                   # shadow the more specific per-feature MessageHandlers above)
)


def register(application: Application) -> None:
    """Register every handler module's commands/callbacks on `application`."""
    for module in _MODULES:
        module.register(application)
