import random

class User:
    def __init__(self, id, score = 0, name = None):
        self.id = int(id)
        self.score = int(score)
        self.name = name
        self.CORRECT_ANSWER_INCREMENT = int(1)
        self.INCORRECT_ANSWER_DECREMENT = int(3)
        if self.name == None:
            self.name = "Abobus#" + str(random.randint(1000, 9999))

    def write(self) -> None:
        with open("src/users.txt", "a") as file:
            file.write(str(self.id) + ' ' + str(self.score) + ' ' + str(self.name))
            file.write('\n')

    def reset(self) -> None:
        self.score = 0

    def correct_answer(self) -> None: 
        self.score += self.CORRECT_ANSWER_INCREMENT

    def incorrect_answer(self) -> None:
        self.score -= self.INCORRECT_ANSWER_DECREMENT

    def rename(self, name):
        self.name = str(name)
    
class UserDatabase:
    def __init__(self):
        self.users = dict()
        with open("src/users.txt") as file:
            for line in file.readlines():
                tmp = line.split()
                self.users[int(tmp[0])] = User(*tmp)

        self.top_user = None
        for user in self.users:
            if self.top_user == None or self.top_user.score < self.users[user].score:
                self.top_user = self.users[user]

        self.type = dict()
        self.wait_list = dict()

    def sync_file(self) -> None:
        with open("src/users.txt", "wb"):
           pass
        
        for user in self.users:
            self.users[user].write()

    def update_top(self) -> None:
        self.top_user = None
        for user in self.users:
            if self.top_user == None or self.top_user.score < self.users[user].score:
                self.top_user = self.users[user]
    
    def add_user(self, user_id) -> None:
        self.users[int(user_id)] = User(int(user_id))

        if self.top_user == None or self.top_user.score < self.users[int(user_id)].score:
                self.top_user = self.users[int(user_id)]

        self.users[int(user_id)].write()
    
    def exists(self, id) -> bool:
        if int(id) in self.users:
            return True
        else:
            return False
    
    def get_score(self, id) -> int:
        return self.users[int(id)].score
    
    def reset(self, id) -> None:
        self.users[int(id)].reset()

    def rename(self, id, name) -> None:
        self.users[int(id)].rename(name)

    def answered(self, id, status) -> None:
        if status:
            self.users[int(id)].correct_answer()
        else:
            self.users[int(id)].incorrect_answer()

class Exercise:
    def __init__(self, question, answer, variants):
        self.question = question
        self.answer = answer
        self.variants = variants

class ExercisesList:
    def __init__(self, type):
        self.type = type
        self.exercises = []
        if type == "emphasis":
            with open("src/emphasis.txt") as file:
                for line in file.readlines():
                    tmp = line.split()
                    variants = tmp[2:]
                    current = Exercise(tmp[0], tmp[1], variants)
                    self.exercises.append(current)

        if type == "prepri":
            with open("src/prepri.txt") as file:
                for line in file.readlines():
                    tmp = line.split()
                    variants = tmp[2:]
                    current = Exercise(tmp[0], tmp[1], variants)
                    self.exercises.append(current)

        if type == "suffix":
            with open("src/suffix.txt") as file:
                for line in file.readlines():
                    tmp = line.split()
                    variants = tmp[2:]
                    current = Exercise(tmp[0], tmp[1], variants)
                    self.exercises.append(current)

        if type == "prefix":
            with open("src/prefix.txt") as file:
                for line in file.readlines():
                    tmp = line.split()
                    variants = tmp[2:]
                    current = Exercise(tmp[0], tmp[1], variants)
                    self.exercises.append(current)

    def pick(self) -> Exercise:
        return self.exercises[random.randint(0, len(self.exercises) - 1)]
    
