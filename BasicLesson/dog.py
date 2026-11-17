class Dog:

    def __init__(self, name: str):
        self.name = name
        self.tricks = []

    def add_tricks(self, tricks: str):
        self.tricks.append(tricks)