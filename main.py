from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}                                            # создаем внешний пустой словарь, для его дальнейшего использования в функциях


try:
    data = pandas.read_csv("data/words_to_learn.csv")        # берем список из сокращенного после изучения слова списка
except FileNotFoundError:                                    # если сокращенного после изучения слова списка еще нет, то
    original_data = pandas.read_csv("data/french_words.csv")          # берем инфу из csv файла с полным списком
    to_learn = original_data.to_dict(orient="records")                # переводим в словарь со спец отображением через "records"
else:
    to_learn = data.to_dict(orient="records")                # переводим в словарь со спец отображением через "records"


def next_card():                                                # функция, вызываемая кнопками, перелистывает слова на одном языке
    global current_card                                         # берем глобальную переменную словаря
    global flip_timer                                           # берем глобальную переменную таймера
    window.after_cancel(flip_timer)                             # отменяем действие таймера
    current_card = random.choice(to_learn)                      # из словаря рандомно выбираем ключ и значение
    canvas.itemconfig(card_title, text="French", fill="black")  # устанавливаем подпись
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")   # выводим слово на французском
    canvas.itemconfig(card_background, image=card_front_img)    # устанавливаем фон канваса
    flip_timer = window.after(3000, func=flip_card)             # обновляем обновление экрана и заново вызываем функцию flip_card


def flip_card():                                                              # функция переворачивания карты
    canvas.itemconfig(card_title, text="English", fill="white")               # меняем текст языка и цвет
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")  # меняем текст перевода и цвет. текст взяли из current_card, которая наполнилась в функц next_card
    canvas.itemconfig(card_background, image=card_back_img)                   # меняем фон карты


def reduce_cards():                                                 # функция сокращения списка слов
    to_learn.remove(current_card)                                   # удаляем выученное слово из списка
    new_data = pandas.DataFrame(to_learn)                           # форматируем в DataFrame
    new_data.to_csv("data/words_to_learn.csv", index=False)         # создаем новый csv файл, отменяем прописывание индекса в новом файле перед словами.
    next_card()                                                     # вызываем следующую карту


window = Tk()                                               #создали окно
window.title("Flashy")                                      # дали окну название
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)        #прописали отступы и выбрали цвет фона

flip_timer = window.after(3000, func=flip_card)             # устанавливаем таймер на 3 секунды, чтобы вызвать функцию

canvas = Canvas(width=800, height=526)                      # запускаем канвас для отображения в окне всех конструкций
card_front_img = PhotoImage(file="images/card_front.png")   # выбрали передний фон для канвас
card_back_img = PhotoImage(file="images/card_back.png")     # выбрали задний фон для канвас
card_background = canvas.create_image(400, 263, image=card_front_img)         # размещаем фон
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))  # создаем подписи
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)    # устанавливаем задний фон для канваса и прописываем 0 для рамки
canvas.grid(row=0, column=0, columnspan=2)                  # размещаем канвас

# Buttons
cross_image = PhotoImage(file="images/wrong.png")
button_unknown = Button(image=cross_image, highlightthickness=0, command=next_card)
button_unknown.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
button_known = Button(image=check_image, highlightthickness=0, command=reduce_cards)
button_known.grid(row=1, column=1)

next_card()

window.mainloop()
