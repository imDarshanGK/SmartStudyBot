"""
help.py

Provides the show_help function, which displays information about each
SmartStudyBot feature to guide users through the available options.

This is intended to help first-time users understand how to use:
- Summarize a topic
- Get study resources
- Practice questions
- Hear a response (TTS)
"""

def show_help():
    """
    Displays an explanation of each SmartStudyBot feature to help users
    understand what to expect from each option in the main menu.
    """
    help_text = """
    Help - SmartStudyBot Features

    1. Summarize a topic:
    > Provide a text or topic. The bot will summarize the key points clearly and concisely.

    2. Get study resources:
    > The bot recommends external resources such as articles, videos, or trusted websites related to your study topic.

    3. Practice questions:
    > The bot creates multiple choice questions based on the content you provide. Great for reviewing and self-testing.

    4. Hear a response:
    > The bot converts your text into audio, so you can listen to summaries or study materials while multitasking.

    Press ENTER to return to the main menu.
    """
    input(help_text)
