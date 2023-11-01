import tkinter as tk
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_TEXT_FONT = ("Ariel", 40, "italic")
WORD_TEXT_FONT = ("Ariel", 60, "bold")
DISPLAY_CARD_FRONT_SECONDS = 3


class FlashCardApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Dictionary
        words_dataframe = pandas.read_csv("data/french_words.csv")
        self.words_dict = words_dataframe.transpose().to_dict()
        self.index = 0
        self.chosen_word = {}

        # App Window
        self.title("flashy")
        self.config(padx=50, pady=20, background=BACKGROUND_COLOR)
        self.canvas = tk.Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
        self.card_front_image = tk.PhotoImage(file="images/card_front.png")
        self.card_back_image = tk.PhotoImage(file="images/card_back.png")
        self.card_image = self.canvas.create_image(410, 263, image=self.card_front_image, anchor="center")
        self.language_text = self.canvas.create_text(400, 150, text="French", font=LANGUAGE_TEXT_FONT)
        self.word_text = self.canvas.create_text(400, 263, text="French word", font=WORD_TEXT_FONT)
        self.canvas.grid(row=0, column=0, columnspan=2)

        # App Buttons
        self.wrong_button_image = tk.PhotoImage(file="images/wrong.png")
        self.wrong_button = tk.Button(
            image=self.wrong_button_image,
            relief="groove",
            highlightthickness=0,
            command=lambda: self.user_clicks_button(button=self.wrong_button)
        )
        self.wrong_button.grid(row=1, column=0)
        self.right_button_image = tk.PhotoImage(file="images/right.png")
        self.right_button = tk.Button(
            image=self.right_button_image,
            relief="groove",
            highlightthickness=0,
            command=lambda: self.user_clicks_button(button=self.right_button)
        )
        self.right_button.grid(row=1, column=1)
        self.timer = tk.NONE
        self.get_new_card()

    def display_flash_card(self, seconds):
        if seconds > 0:
            self.timer = self.canvas.after(1000, self.display_flash_card, seconds - 1)
        else:
            self.canvas.itemconfig(self.card_image, image=self.card_back_image)
            self.canvas.itemconfig(self.language_text, text="English")
            self.canvas.itemconfig(self.word_text, text=self.chosen_word["English"])

    def get_new_card(self):
        self.index, self.chosen_word = random.choice(list(self.words_dict.items()))
        self.canvas.itemconfig(self.card_image, image=self.card_front_image)
        self.canvas.itemconfig(self.language_text, text="French")
        self.canvas.itemconfig(self.word_text, text=self.chosen_word["French"])
        self.display_flash_card(DISPLAY_CARD_FRONT_SECONDS)

    def user_clicks_button(self, *, button):
        # If the user clicks the 'Check' button. Remove that word from the dictionary
        if button == self.right_button:
            self.words_dict.pop(self.index)

        self.get_new_card()
