import pickle


class Car:

    def __init__(self, year, color, model):
        self.year = year
        self.color = color
        self.model = model

    def paint_job(self, new_color):
        self.color = new_color

    def info(self):
        return f'{self.year} {self.color} {self.model}'
