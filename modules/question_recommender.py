"""
question_recommender.py

This module handles the interactive quiz functionality of the SmartStudyBot.

It loads multiple-choice questions from a subject-specific JSON file and presents
them to the user in a shuffled order. The user inputs their answers, and the system
provides feedback and scoring in real time.
"""

import json
import random
import logging

logger = logging.getLogger(__name__)

# List of available subjects
AVAILABLE_SUBJECTS = ["python", "dsa"]

def ask_questions(subject):
    """
    Displays a multiple-choice quiz to the user based on the given subject.

    The function attempts to load a list of questions from a JSON file located
    at 'data/questions/{subject}.json' using UTF-8 encoding. If the file is found,
    it selects the first 5 questions after shuffling and presents them one by one
    to the user. The user inputs their answer, and the function provides feedback
    and tracks the score.

    Parameters:
        subject (str): The name of the subject whose questions will be loaded.

    Returns:
        None
    """

    subject = subject.strip().lower()
    # Keep prompting until valid subject is entered
    while subject not in AVAILABLE_SUBJECTS:
        logger.warning("⚠️  Invalid subject '%s'." \
        " Please choose from: %s", subject, ", ".join(AVAILABLE_SUBJECTS))
        subject = input(f"Enter a valid subject ({','
        ' '.join(AVAILABLE_SUBJECTS)}): ").strip().lower()
        
    try:
        with open(f"data/questions/{subject}.json", encoding="utf-8") as file:
            questions = json.load(file)
            logger.info("✅ Loaded questions for subject: %s", subject)
    except FileNotFoundError:
        logger.error("❌ Subject '%s' not found. Quiz aborted.", subject)
        return
    except json.JSONDecodeError as e:
        logger.error("❌ Failed to parse JSON for subject '%s': %s", subject, e)
        return

    random.shuffle(questions)
    score = 0

    for q in questions[:5]:
        logger.info("❓ Question: %s", q["question"])
        for i, option in enumerate(q["options"], 1):
            logger.info("   %d. %s", i, option)

        answer = input("Enter your choice (1-4): ")
        try:
            selected = int(answer)
            if q["options"][selected - 1] == q["answer"]:
                logger.info("✅ Correct!")
                score += 1
            else:
                logger.info("❌ Incorrect. Correct answer: %s", q["answer"])
        except (ValueError, IndexError):
            logger.warning("⚠️ Invalid input: '%s'. Skipping question.", answer)

    logger.info("📊 Quiz finished. Score: %d/5", score)
