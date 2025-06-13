import tkinter as tk
import random


# Загрузка слов из файла
def load_words(filename="words.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print("Файл words.txt не найден!")
        return []


# Рисуем виселицу в виде строк
hangman_stages = [
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
   /|\   |
         |
         |
    ''',
    '''
    ------
    |    |
    О    |
   /|\   |
   /     |
         |
    ''',
    '''
    ------
    |    |
    О    |
   /|\   |
   / \   |
         |
    '''
]


# Главный класс игры
class HangmanGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Игра Виселица")
        self.geometry("400x500")

        self.words = load_words("words.txt")
        if not self.words:
            self.word = "ДЕФОЛТ"  # Если слов нет, используем дефолтное
        else:
            self.word = random.choice(self.words)

        self.guessed_word = ["_"] * len(self.word)
        self.incorrect_guesses = []
        self.attempts_left = 6

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Текстовое поле для отображения текущего состояния слова
        self.word_label = tk.Label(self, text=" ".join(self.guessed_word), font=("Helvetica", 16))
        self.word_label.pack(pady=20)

        # Место для рисования виселицы
        self.hangman_label = tk.Label(self, text=hangman_stages[0], font=("Courier", 12), height=8)
        self.hangman_label.pack()

        # Место для отображения неправильных букв
        self.incorrect_label = tk.Label(self, text="Неверные буквы: ", font=("Helvetica", 12))
        self.incorrect_label.pack(pady=10)

        # Панель с кнопками для каждой буквы
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)
        self.create_buttons()

    def create_buttons(self):
        # Русский алфавит
        alphabet = "АБВГДЕЁЖЗИИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"

        # Количество колонок на экране (определяем, сколько букв будет в строке)
        columns = 8

        # Создаем кнопки для букв
        for i, letter in enumerate(alphabet):
            row = i // columns  # Строка
            column = i % columns  # Колонка

            button = tk.Button(self.button_frame, text=letter, width=4, command=lambda l=letter: self.make_guess(l))
            button.grid(row=row, column=column, padx=5, pady=5)

    def make_guess(self, letter):
        # Отключаем кнопку после нажатия
        for button in self.button_frame.winfo_children():
            if button["text"] == letter:
                button.config(state="disabled")

        if letter in self.word:
            # Открываем букву в слове
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
            self.update_display()
            if "_" not in self.guessed_word:
                self.game_over("Вы победили! Слово отгадано.")
        else:
            # Добавляем неправильный ответ
            self.incorrect_guesses.append(letter)
            self.attempts_left -= 1
            self.update_display()
            if self.attempts_left == 0:
                self.game_over(f"Вы проиграли! Загаданное слово было: {self.word}")

    def update_display(self):
        # Обновление отображения
        self.word_label.config(text=" ".join(self.guessed_word))
        self.incorrect_label.config(text=f"Неверные буквы: {', '.join(self.incorrect_guesses)}")
        self.hangman_label.config(text=hangman_stages[6 - self.attempts_left])

    def game_over(self, message):
        # Конец игры
        self.word_label.config(text=message)
        for button in self.button_frame.winfo_children():
            button.config(state="disabled")


# Запуск игры
if __name__ == "__main__":
    game = HangmanGame()
    game.mainloop()
