"""
question_recommender.py

This module handles the interactive quiz functionality of the SmartStudyBot.

It loads multiple-choice questions from a subject-specific JSON file and presents
them to the user in a shuffled order. The user inputs their answers, and the system
provides feedback and scoring in real time.
"""

import json
import random
import datetime
import logging
from config import ENABLE_SOUND
from modules import sound

logger = logging.getLogger(__name__)

# List of available subjects
AVAILABLE_SUBJECTS = ["python", "dsa"]


def normalize_subject(subject):
    """
    Normalizes and validates the subject name input by the user.

    If the subject is not in the AVAILABLE_SUBJECTS list, prompts the user
    repeatedly until a valid one is entered.

    Parameters:
        subject (str): The initial user-provided subject name.

    Returns:
        str: A valid, lowercase subject name present in AVAILABLE_SUBJECTS.
    """

    subject = subject.strip().lower()

    while subject not in AVAILABLE_SUBJECTS:
        logger.warning("⚠️  Invalid subject '%s'. Please choose from: %s",
                       subject, ", ".join(AVAILABLE_SUBJECTS))
        subject = input(
            f"Enter a valid subject ({'/'.join(AVAILABLE_SUBJECTS)}): ").strip().lower()

    return subject


def load_questions(subject):
    """
    Loads and parses a JSON file containing multiple-choice questions.

    Parameters:
        subject (str): The subject name, used to locate the corresponding JSON file.

    Returns:
        list[dict] | None: A list of questions if successfully loaded and parsed,
                           otherwise None.
    """
    try:
        with open(f"data/questions/{subject}.json", encoding="utf-8") as file:
            questions = json.load(file)
            logger.info("📥 Loaded questions for subject: %s", subject)
            return questions
    except FileNotFoundError:
        logger.error("❌ Subject '%s' not found. Quiz aborted.", subject)
    except json.JSONDecodeError as e:
        logger.error("❌ Failed to parse JSON for subject '%s': %s", subject, e)
    return None


def run_quiz(questions):
    """
    Presents multiple-choice questions to the user and tracks their score.

    Loops through the given list of questions, shows them one by one,
    and evaluates user responses.

    Parameters:
        questions (list[dict]): A list of 5 multiple-choice question dictionaries.

    Returns:
        int: The total number of correct answers (score out of 5).
    """

    score = 0
    logger.info("\n🎯 Starting quiz! Answer the next 5 questions:\n")

    for index, q in enumerate(questions, 1):
        logger.info("🧠 [Question %d] %s", index, q["question"])
        for i, option in enumerate(q["options"], 1):
            logger.info("   %d) %s", i, option)

        answer = input("➡️  Enter your choice (1-4): ")
        if is_correct_answer(answer, q):
            logger.info("✅ Correct!\n")
            score += 1
        else:
            logger.info(
                "❌ Incorrect! The correct answer was: %s\n", q["answer"])

    return score


def is_correct_answer(answer, question):
    """
    Validates the user's input and checks if the selected answer is correct.

    Parameters:
        answer (str): The user's input, expected to be a number between 1 and 4.
        question (dict): The question dictionary containing options and correct answer.

    Returns:
        bool: True if the answer is correct, False otherwise or if input is invalid.
    """

    try:
        selected = int(answer)
        return question["options"][selected - 1] == question["answer"]
    except (ValueError, IndexError):
        logger.warning("⚠️  Invalid input: '%s'. Skipping question.\n", answer)
        return False


def give_feedback(score):
    """
    Logs performance-based feedback and plays audio cues if enabled.

    Parameters:
        score (int): The user's quiz score (from 0 to 5).

    Returns:
        None
    """

    logger.info("🏁 Quiz completed!")
    logger.info("📊 Your score: %d/5", score)

    if score == 5:
        logger.info("🎉 Excellent! You're a quiz master!")
    elif score >= 3:
        logger.info("👍 Good job! Keep practicing.")
    else:
        logger.info("📚 Review the topic and try again.")

    if ENABLE_SOUND:
        if score >= 3:
            sound.play_success_sound()
        else:
            sound.play_failure_sound()


def return_score_history_list():
    """
    Loads and parses 'score_history.json'. 

    Parameters: 
        None

    Returns:
        quiz history (list[dict]): each dict contains quiz subject, score and date.
    """

    try:
        file_location = './data/score_history.json'
        with open(file_location) as score_history_file:
            data = json.load(score_history_file)
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error while opening json file. Error message: '{e}'")
        logger.info(
            f"Make sure the file at '{file_location}' points to a valid json file.")
        return []
    except FileNotFoundError as e:
        logger.error(f"File not found. Error message: '{e}'")
        logger.info(
            f"Make sure '{file_location}' points to a valid location and 'score_history.json' file exists.")
        return []


def format_and_show_score_history():
    """
    Displays all quiz history data with logger. 

    Parameters: 
        None

    Returns:
        None
    """

    data = return_score_history_list()
    if not data:
        logger.info("No quizes done yet!")
        return
    for completed_quiz in data:
        logger.info(f"Subject: {completed_quiz["subject"]}")
        logger.info(f"Score: {completed_quiz["score"]}")
        logger.info(f"Date of completion: {completed_quiz["date"]}\n")


def store_score(subject, score):
    """
    Used to store completed quiz information. Adds a dict with subject, score and date to 'score_history.json'. 

    Parameters:
        subject (str): The subject name.
        score (int): The user's quiz score. 

    Returns:
        None
    """

    data = return_score_history_list()
    date_of_test_completion = datetime.datetime.now()
    new_data = {"subject": subject, "score": score,
                "date": str(date_of_test_completion)}
    data.append(new_data)

    with open('./data/score_history.json', 'w') as f:
        json.dump(data, f, indent=3)


def ask_questions(subject):
    """
    Orchestrates the quiz flow for the given subject.

    This function normalizes the subject, loads the corresponding question file,
    runs the quiz with the first 5 shuffled questions, and provides feedback and
    audio cues (if enabled via config).

    Parameters:
        subject (str): The name of the subject to load questions from.

    Returns:
        None
    """

    subject = normalize_subject(subject)

    if subject is None:
        return

    questions = load_questions(subject)
    if not questions:
        return

    random.shuffle(questions)
    score = run_quiz(questions[:5])
    store_score(subject, score)
    give_feedback(score)
