import random

OPTIONS = {"en": ["rock", "paper", "scissors"],
           "ru": ["камень", "бумага", "ножницы"]}
COMMANDS = {"!exit": "exit",
            "!выход": "exit",
            "!rating": "rating",
            "!рейтинг": "rating"
            }
RESULTS = {"en": {"Lose": "Sorry, but the computer chose {0}",
                  "Draw": "There is a draw ({0})",
                  "Win": "Well done. The computer chose {0} and failed"},
           "ru": {"Lose": "Извини, но компьютер выбрал {0} и выиграл",
                  "Draw": "Ничья, все выбрали {0}",
                  "Win": "Молодец! Компьютер выбрал {0} и проиграл!"}}
MESSAGES = {"en": {"wrong_input": "Invalid input",
                   "exit": "Bye!",
                   "ask_name": "Enter your name: ",
                   "say_hi": "Hello, {0}!",
                   "cur_rating": "Your rating: {0}"
                   },
            "ru": {"wrong_input": "Неправильный ввод",
                   "exit": "Пока!",
                   "ask_name": "Введите Ваше имя: ",
                   "say_hi": "Привет, {0}!",
                   "cur_rating": "Текущий счет: {0}"
                   }}

file_name = "rating.txt"


class Game:
    def __init__(self, language='en'):
        self.options = OPTIONS[language]
        self.results = RESULTS[language]
        self.messages = MESSAGES[language]
        self.user_name = ""
        self.current_rating = 0
        self.all_ratings = dict()

    def ask_user_name(self):
        self.user_name = input(self.messages["ask_name"])
        print(self.messages["say_hi"].format(self.user_name))

    def ask_user_input(self):
        return input()

    def show_user_result(self, user, comp):
        i = self.options.index(user)
        new_list = self.options[i+1:] + self.options[:i]

        if user == comp:
            res = "Draw"
            self.current_rating += 50
#        elif ((user == 0 and comp == 2) or
#              (user == 1 and comp == 0) or
#              (user == 2 and comp == 1)):
        elif new_list.index(comp) >= len(new_list) / 2:
            res = "Win"
            self.current_rating += 100
        else:
            res = "Lose"

        print(self.results[res].format(comp))

    def show_current_rating(self):
        print(self.messages["cur_rating"].format(self.current_rating))

    def load_ratings(self):
        with open(file_name, "r+") as file:
            for line in file:
                score = line.split()
                self.all_ratings.update({score[0]: int(score[1])})

        self.current_rating = self.all_ratings.get(self.user_name, 0)

    def ai_choice(self):
        random.seed()
        return self.options[random.randint(0, len(self.options) - 1)]

    def process_command(self, command):
        if command == "exit":
            return -1
        elif command == "rating":
            self.show_current_rating()
            return None
        else:
            return None

    def process_user_input(self, user_input):
        if user_input in COMMANDS.keys():
            return self.process_command(COMMANDS[user_input])
        elif user_input in self.options:
            return self.options.index(user_input)
        else:
            print(self.messages["wrong_input"])
            return None

    def make_turn(self, user_input):
        comp = self.ai_choice()
        self.show_user_result(user_input, comp)

    def ask_options_list(self):
        new_options = input()
        if new_options:
            self.options = new_options.split(",")

    def run(self):

        self.ask_user_name()
        self.load_ratings()

        self.ask_options_list()
        print("Okay, let's start")

        while True:
            user_input = self.ask_user_input()
            result = self.process_user_input(user_input)
            if result == -1:
                break
            elif result is not None:
                self.make_turn(user_input)


game = Game()
game.run()
