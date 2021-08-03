import tkinter as tk
from tkinter.ttk import *

window = tk.Tk()
window.title('Board Game Suggestor')
# write your code here
choice_one_label = Label(window, text='CHOICE #1')
choice_one_label.grid(row=1,column=1)
game_choice_one = Combobox(window, textvariable=['test1', 'test2', 'test3'], values=[1,2,3])
game_choice_one.grid(row=1,column=2, pady=15, padx=10)

choice_two_label = Label(window, text='CHOICE #2')
choice_two_label.grid(row=2,column=1)
game_choice_two = Combobox(window, textvariable=['test1', 'test2', 'test3'], values=[1,2,3])
game_choice_two.grid(row=2,column=2, pady=15, padx=10)

choice_three_label = Label(window, text='CHOICE #3')
choice_three_label.grid(row=3,column=1)
game_choice_three = Combobox(window, textvariable=['test1', 'test2', 'test3'], values=[1,2,3])
game_choice_three.grid(row=3,column=2, pady=15, padx=10)

choice_four_label = Label(window, text='CHOICE #4')
choice_four_label.grid(row=4,column=1)
game_choice_four = Combobox(window, textvariable=['test1', 'test2', 'test3'], values=[1,2,3])
game_choice_four.grid(row=4,column=2, pady=15, padx=10)

choice_five_label = Label(window, text='CHOICE #5')
choice_five_label.grid(row=5,column=1)
game_choice_five = Combobox(window, textvariable=['test1', 'test2', 'test3'], values=[1,2,3])
game_choice_five.grid(row=5,column=2, pady=15, padx=10)


get_results_button = Button(text='Get My Results')
get_results_button.grid(row=7, column=1, pady=15, padx=15)

window.mainloop()