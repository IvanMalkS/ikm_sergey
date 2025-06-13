
"""
Игра "Виселица" с графическим интерфейсом на tkinter.

Модуль содержит класс HangmanGame для запуска игры в угадывание слов
с визуальным отображением виселицы.
"""

import tkinter as tk
import random


def load_words(filename="words.txt"):
    """
    Загружает слова из текстового файла.
    
    Args:
        filename (str): Имя файла со словами
        
    Returns:
        list: Список слов из файла или пустой список при ошибке
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print("Файл words.txt не найден!")
        return []


HANGMAN_STAGES = [
    '''
    ------
    |    |
         |
         |
         |
         |
    ''',
    '''
    ------
    |    |
    О    |
         |
         |
         |
    ''',
    '''
    ------
    |    |
    О    |
    |    |
         |
         |
    ''',
    '''
    ------
    |    |
    О    |
   /|    |
         |
         |
    ''',
    '''
    ------
    |    |
    О    |
   /|\\   |
         |
         |
    ''',
    '''
    ------
    |    |
    О    |
   /|\\   |
   /     |
         |
    ''',
    '''
    ------
    |    |
    О    |
   /|\\   |
   / \\   |
         |
    '''
]


class HangmanGame(tk.Tk):
    """
    Главный класс игры "Виселица".
    
    Наследует от tk.Tk и реализует полнофункциональную игру
    с графическим интерфейсом.
    """
    
    def __init__(self):
        """
        Инициализирует игру, загружает слова и создает интерфейс.
        """
        super().__init__()

        self.title("Игра Виселица")
        self.geometry("400x500")

        self.words = load_words("words.txt")
        if not self.words:
            self.word = "ДЕФОЛТ"
        else:
            self.word = random.choice(self.words)

        self.guessed_word = ["_"] * len(self.word)
        self.incorrect_guesses = []
        self.attempts_left = 6

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """
        Создает виджеты пользовательского интерфейса.
        """
        self.word_label = tk.Label(
            self, 
            text=" ".join(self.guessed_word), 
            font=("Helvetica", 16)
        )
        self.word_label.pack(pady=20)

        self.hangman_label = tk.Label(
            self, 
            text=HANGMAN_STAGES[0], 
            font=("Courier", 12), 
            height=8
        )
        self.hangman_label.pack()

        self.incorrect_label = tk.Label(
            self, 
            text="Неверные буквы: ", 
            font=("Helvetica", 12)
        )
        self.incorrect_label.pack(pady=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)
        self.create_buttons()

    def create_buttons(self):
        """
        Создает кнопки для букв русского алфавита.
        """
        alphabet = "АБВГДЕЁЖЗИИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
        columns = 8

        for i, letter in enumerate(alphabet):
            row = i // columns
            column = i % columns

            button = tk.Button(
                self.button_frame, 
                text=letter, 
                width=4, 
                command=lambda l=letter: self.make_guess(l)
            )
            button.grid(row=row, column=column, padx=5, pady=5)

    def make_guess(self, letter):
        """
        Обрабатывает выбор буквы игроком.
        
        Args:
            letter (str): Выбранная игроком буква
        """
        for button in self.button_frame.winfo_children():
            if button["text"] == letter:
                button.config(state="disabled")

        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
            self.update_display()
            if "_" not in self.guessed_word:
                self.game_over("Вы победили! Слово отгадано.")
        else:
            self.incorrect_guesses.append(letter)
            self.attempts_left -= 1
            self.update_display()
            if self.attempts_left == 0:
                self.game_over(
                    f"Вы проиграли! Загаданное слово было: {self.word}"
                )

    def update_display(self):
        """
        Обновляет отображение игры на экране.
        """
        self.word_label.config(text=" ".join(self.guessed_word))
        self.incorrect_label.config(
            text=f"Неверные буквы: {', '.join(self.incorrect_guesses)}"
        )
        self.hangman_label.config(
            text=HANGMAN_STAGES[6 - self.attempts_left]
        )

    def game_over(self, message):
        """
        Завершает игру и отображает результат.
        
        Args:
            message (str): Сообщение о результате игры
        """
        self.word_label.config(text=message)
        for button in self.button_frame.winfo_children():
            button.config(state="disabled")


if __name__ == "__main__":
    game = HangmanGame()
    game.mainloop()
