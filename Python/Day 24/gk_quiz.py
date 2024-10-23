import json
import random
import argparse
import os
import requests

# Function to load quiz data from the file
def load_quiz_data():
    if os.path.exists('quiz_data.json'):
        with open('quiz_data.json', 'r') as f:
            return json.load(f)
    else: 
        return {}

# Function to save the quiz data
def save_quiz_data(data):
    with open('quiz_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Function to fetch quiz questions from Open Trivia DB API
def fetch_questions_from_api(amount=5):
    url = f"https://opentdb.com/api.php?amount={amount}&category=9&type=multiple"
    response = requests.get(url)
    data = response.json()
    
    if data['response_code'] == 0:
        return data['results']
    else:
        print("Error fetching data from API")
        return []

# Function to store API quiz questions into local JSON
def store_api_question(quiz_name, amount=5):
    questions_from_api = fetch_questions_from_api(amount)
    data = load_quiz_data()
    
    if quiz_name not in data:
        data[quiz_name] = []
    
    for item in questions_from_api:
        question = item['question']
        answer = item['correct_answer']
        data[quiz_name].append({
            "question": question,
            "answer": answer
        })

    save_quiz_data(data)
    print(f"{amount} questions from API added to {quiz_name} quiz.")

# Function to add a quiz question manually
def add_question(quiz_name, question, answer):
    data = load_quiz_data()
    
    if quiz_name not in data:
        data[quiz_name] = []
    
    data[quiz_name].append({
        "question": question,
        "answer": answer
    })
    
    save_quiz_data(data)
    print(f"Question added to {quiz_name} quiz.")
    
# Function to take a quiz
def take_quiz(quiz_name):
    data = load_quiz_data()
    
    if quiz_name not in data:
        print(f"No quiz found with the name '{quiz_name}'.")
        return
    
    questions = data[quiz_name]
    random.shuffle(questions)  # Shuffle questions to randomize quiz order
    
    correct_answers = 0
    for q in questions:
        print(f"Question: {q['question']}")
        user_answer = input("Your answer: ").strip().lower()
        
        if user_answer == q['answer'].strip().lower():
            print("Correct!\n")
            correct_answers += 1
        else:
            print(f"Incorrect! The correct answer was: {q['answer']}\n")
    
    print(f"Quiz over! You got {correct_answers} out of {len(questions)} correct.")

# CLI Interface
def main():
    parser = argparse.ArgumentParser(description="Quiz Application")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Add question manually
    add_parser = subparsers.add_parser("add", help="Add a new quiz question")
    add_parser.add_argument("--quiz", required=True, help="Quiz name (e.g., Python, GK)")
    add_parser.add_argument("--question", required=True, help="Question text")
    add_parser.add_argument("--answer", required=True, help="Correct answer")

    # Take quiz command
    take_parser = subparsers.add_parser("take", help="Take a quiz")
    take_parser.add_argument("--quiz", required=True, help="Quiz name (e.g., Python, GK)")

    # Fetch questions from API and store in quiz
    api_parser = subparsers.add_parser("fetch", help="Fetch questions from Open Trivia API")
    api_parser.add_argument("--quiz", required=True, help="Quiz name to store questions")
    api_parser.add_argument("--amount", type=int, default=5, help="Number of questions to fetch (default is 5)")

    args = parser.parse_args()

    if args.command == "add":
        add_question(args.quiz, args.question, args.answer)
    elif args.command == "take":
        take_quiz(args.quiz)
    elif args.command == "fetch":
        store_api_question(args.quiz, args.amount)

if __name__ == "__main__":
    main()