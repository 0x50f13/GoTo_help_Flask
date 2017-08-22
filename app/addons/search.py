import Stemmer
import numpy as np


class Question:
    def __init__(self, title, description, tags, id):

        stemmer = Stemmer.Stemmer('russian')

        title_words = title.split(' ')
        description_words = description.split(' ')

        self.title = set()
        self.description = set()

        for word in title_words:
            self.title.add(stemmer.stemWord(word))

        for word in description_words:
            self.description.add(stemmer.stemWord(word))

        # i belive that we dont need to stemm tags
        self.tags = set(tags)
        self.id = id


class Question_analyzer:
    def __init__(self):

        self.questions = []
        # self.title_words = set()
        # self.discribtion_words = set()
        # self.tags = set()

    def add_question(self, title, description, tags, id, likes):
        self.questions.append(Question(title, description, tags, id))

    def find(self, string):

        stemmer = Stemmer.Stemmer('russian')

        string = string.split(' ')
        words_to_find = set()

        for i in range(len(string)):
            words_to_find.add(stemmer.stemWord(string[i]))

        distances = []
        for question in self.questions:
            distances.append(((len(question.description ^ words_to_find) ** 1 / 2) * 1 + \
                              (len(question.title ^ words_to_find) ** 1 / 2) * 2 + \
                              (len(question.tags ^ words_to_find) ** 1 / 2) * 3, question.id))

        distances.sort()

        return distances
