import json
from difflib import get_close_matches

def load_info(memory_file):
    with open(memory_file) as file:
        data = json.load(file)
    return data

def save_info(memory_file, data):
    with open(memory_file, "w") as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    else:
        return None

def get_ans(question, info):
    for q in info["questions"]:
        if q["question"] == question:
            return q["answer"]

def add_new_ans(user_input, new_answer, info):
    info["questions"].append({"question": user_input, "answer": new_answer})
    save_info("memory.json", info)

def main():

    info = load_info("memory.json")

    while True:

        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye", "see you"]:
            break
        best_matches = find_best_match (user_input, [q["question"] for q in info["questions"]] )

        if best_matches:
            answer = get_ans(best_matches, info)
            print(f"🤖: {answer}")

        else:

            learning_mode = input("🤖: I don't have that information. Can you teach me? (yes/no): ")
            if learning_mode.lower().strip() in ["yes", "y"]:
                new_answer = input("🤖: Type a response: ")

                if new_answer:
                    add_new_ans(user_input, new_answer, info)
                    print ("🤖: Thank you for teaching me a response!!")
                else:
                    print("🤖: Please Enter something!")
                    continue

if __name__ == "__main__":
    main()
