"""Start a trained ChatterBot conversation in the terminal."""

from pathlib import Path

from chatterbot import ChatBot
from chatterbot.tagging import LowercaseTagger
from chatterbot.trainers import ListTrainer
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


# Each question is followed by the answer the bot should learn.
CONVERSATIONS = [
    ["Hello", "Hi! What would you like to talk about?"],
    [
        "Good morning! How are you doing?",
        "I am doing very well, thank you for asking.",
    ],
    ["How are you?", "I'm doing well. How are you?"],
    ["What is your name?", "My name is Shawn's Q&A Bot."],
    [
        "What can you do?",
        "I can answer questions from the conversations I learned.",
    ],
    ["What is Python?", "Python is a programming language."],
    ["What is Django?", "Django is a web framework written in Python."],
    [
        "What is ChatterBot?",
        "ChatterBot learns responses from example conversations.",
    ],
    ["Thank you", "You're welcome!"],
    ["Goodbye", "See you later!"],
]


class Command(BaseCommand):
    help = "Chat with a ChatterBot in the terminal. Type quit to leave."

    def handle(self, *args, **options):
        # Store learned conversations in a local SQLite database.
        database_path = Path(settings.BASE_DIR) / "chatterbot.sqlite3"

        bot = ChatBot(
            "Shawn Q&A Bot",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            database_uri=f"sqlite:///{database_path.as_posix()}",
            # This avoids requiring a separate spaCy language-model download.
            tagger=LowercaseTagger,
            read_only=True,
        )

        trainer = ListTrainer(bot)
        for conversation in CONVERSATIONS:
            trainer.train(conversation)

        self.stdout.write("Bot ready. Type quit to leave.")

        while True:
            try:
                message = input("user: ").strip()
            except (EOFError, KeyboardInterrupt):
                self.stdout.write("\nbot: Goodbye!")
                break

            if message.casefold() in {"quit", "exit"}:
                self.stdout.write("bot: Goodbye!")
                break

            if not message:
                self.stdout.write("bot: Please enter a question.")
                continue

            try:
                response = bot.get_response(message)
            except Exception as exc:
                raise CommandError(
                    f"Unable to get a response: {exc}"
                ) from exc

            self.stdout.write(f"bot: {response}")