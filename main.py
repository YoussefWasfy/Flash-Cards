from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
try:
    words_to_learn_file = open('data/words_to_learn.csv', 'r')
except FileNotFoundError:
    # to read from a different file change the path here
    with open('data/french_words.csv', 'r') as data_file:
        words_dataframe = pandas.read_csv(data_file)
        words_to_learn = words_dataframe.to_dict(orient='records')
else:
    words_dataframe = pandas.read_csv(words_to_learn_file)
    words_to_learn = words_dataframe.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    # change the text here from 'French' to the language you want
    canvas.itemconfigure(card_title, text='French', fill='black')
    # change the word 'French' to what you've put in the line above
    canvas.itemconfigure(card_word, text=current_card['French'], fill='black')
    canvas.itemconfigure(canvas_image, image=card_front)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfigure(canvas_image, image=card_back)
    canvas.itemconfigure(card_title, text='English', fill='white')
    canvas.itemconfigure(card_word, text=current_card['English'], fill='white')


def is_known():
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


window = Tk()
window.title('flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(5000, func=flip_card)
canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas.config(bg=BACKGROUND_COLOR)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, fill='black', font=('Arial', 50, 'italic'))
card_word = canvas.create_text(400, 263, fill='black', font=('Arial', 60, 'bold'))
right_image = PhotoImage(file='images/right.png')
wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)
next_card()
window.mainloop()
