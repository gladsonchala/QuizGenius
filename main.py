import requests
import json
import random


class Questions:
    base_url = "https://opentdb.com"
    path = ''
    score = 0

    def getCategories(self):
        self.path = '/api_category.php'
        response = requests.get(self.base_url + self.path)
        parsed_data = json.loads(response.text)
        for category in parsed_data['trivia_categories']:
            print(f"Category ID: {category['id']}, Name: {category['name']}")

    def trueFalse(self, amount = 3, category = 9):
        self.path = f'/api.php?type=boolean&amount={amount}&category={category}'
        self.score = 0
        response = requests.get(self.base_url + self.path)
        parsed_data = json.loads(response.text)
        if response.status_code == 200 and parsed_data['response_code'] == 0:
            for index, question in enumerate(parsed_data['results'], start=1):
                question_text = question['question'].replace(
                    "&quot;", '"').replace("&#039;", "'")
                print(f"Question {index}: {question_text}")
                print("True or False?")
                user_answer = input("Enter your answer: ").capitalize()

                correct_answer = question['correct_answer'].replace(
                    "&quot;", '"').replace("&#039;", "'")

                if user_answer == correct_answer:
                    self.score += 1
                    print("Correct!")
                else:
                    print("Incorrect. The correct answer is:", correct_answer)

                print("\n")

            print("Quiz completed! You answered", self.score, "out of", amount)

    def choiceQuestions(self, amount = 3, category = 9):
        self.path = f'/api.php?amount={amount}&category={category}&type=multiple'
        self.score = 0
        response = requests.get(self.base_url + self.path)
        parsed_data = json.loads(response.text)
        if response.status_code == 200 and parsed_data['response_code'] == 0:
            for index, question in enumerate(parsed_data['results'], start=1):
                question_text = question['question'].replace(
                    "&quot;", '"').replace("&#039;", "'")
                print(f"Question {index}: {question_text}")

                answers = [question['correct_answer']] + \
                    question['incorrect_answers']
                answers = [answer.replace("&quot;", '"').replace("&#039;", "'") for answer in answers]

                random.shuffle(answers)

                for i, answer in enumerate(answers, start=1):
                    print(f"{i}. {answer}")

                user_answer = input("Enter the number of your answer: ")

                correct_index = answers.index(question['correct_answer']) + 1

                if user_answer == str(correct_index):
                    self.score += 1
                    print("Correct!")
                else:
                    print("Incorrect. The correct answer is:",
                          correct_index, ". ", question['correct_answer'])

                print("\n")

            print("Quiz completed! You answered", self.score, "out of", amount)

def main():
    q = Questions()
    while True:
        print("______________________________________")
        print("|~~~ 🎉 Welcome to QuizGenius! 🎉 ~~~|")
        print("|~~~ 🎮 1. Start the game         ~~~|")
        print("|~~~ 📚 2. View categories        ~~~|")
        print("|~~~ 🚪 3. Quit the game          ~~~|")
        print("|____________________________________|")
        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            print("\n1. True/False questions ❓")
            print("2. Multiple choice questions 📝")
            question_type = input("Choose the type of questions: ")
            amount = input("Enter the number of questions you want to answer: ")
            category = input("Enter the category ID you want (or press Enter to use the default): ")

            if category == '':
                category = 9  # default category
            else:
                category = int(category)

            if question_type == '1':
                q.trueFalse(int(amount), category)
            elif question_type == '2':
                q.choiceQuestions(int(amount), category)
            else:
                print("Invalid choice. Please try again. 😞")

        elif user_choice == '2':
            q.getCategories()

        elif user_choice == '3':
            print("Thank you for playing QuizGenius. Goodbye! 👋😊")
            break

        else:
            print("Invalid choice. Please try again. 😞")
            
if __name__ == "__main__":
    main()