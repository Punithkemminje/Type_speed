from tkinter import *
from tkinter import Text , ttk
import random
#from english_words import english_words_lower_set as english_word_list

bk_clr = '#f5bfea'
# ------------------------------------- Widget ----------------------#
window = Tk()
window.geometry("493x500")
window.title('Type speed tester')
window.resizable(False,False)
window.config(bg=bk_clr)

# --------------------------- To get random word from text file ----------------------#
with open('word.txt' , 'r') as data :
    words = data.read()
    word_list = words.split("\n")
def get_words() :
    new_word = random.choice(word_list)
    return new_word


# -------------------------- Count down timer ---------------------------#
time_left_lbl = Label(bg='#f5bfea')
time_left_lbl.place(x=350 , y=30)


# ----------------------- Close window --------------------------------- #
def close() :
    window.destroy()


# ----------------------- Restart window -------------------------------- #
def reset() :
    window.bind('<space>' , space)
    window.bind('<Key>' , click)
    global result_lbl , report_lbl , correct_word_lbl , wrong_words_lbl , time_left_lbl , text_entry , wrong_words , correct_word_indx
    wrong_words = []
    correct_word_indx = []
    result_lbl.config(text="")
    report_lbl.config(text="")
    time_left_lbl.config(text="")
    correct_word_lbl.config(text="")
    wrong_words_lbl.config(text="")
    type_word_lbl.config(text=f"Word: \t{random_word}")
    text_entry = Text(width=43 , height=100 , border=10 , font='Arial' , bg='#f1d3f5')
    text_entry.place(x=0 , y=200)


def count_down(count) :
    global word , result_lbl , report_lbl , correct_word_lbl , wrong_words_lbl
    time_left_lbl.config(text=f"Time left: {count}" , font='Arial' , fg='black')
    if count == 0 :  # Show result and restart option
        time_left_lbl.config(text=f"Times up" , font='Arial' , fg='#e00417')
        correct_word = ""
        mistake_word = ""
        type_word_lbl.config(text="")
        text_entry.destroy()
        window.unbind('<space>')
        if len(wrong_words) > 0 :
            report = "Correct word:\tYour word\n"
            for i in range(len(correct_word_indx)) :
                correct_word += f"{word_list[correct_word_indx[i]]}\n"
                mistake_word += f"{wrong_words[i]}\n"
                try:
                    word.remove(wrong_words[i])
                except ValueError:
                    report = "Type words in sequence!"
                    correct_word = ""
                    mistake_word = ""
        else :
            word = word[:-1]
            if '' in word :
                report = "Avoid too much white space"
            else :
                report = "Congratulations for zero mistake!"
        word = [element for element in word if element != '']  # Remove empty string from list
        result_lbl = Label(window , text=f"Score: {len(word)} words/min" , font='Arial' , fg='Blue' , bg=bk_clr)
        result_lbl.place(x=150 , y=10)
        report_lbl = Label(window , text=report , font='Arial' , bg='#f5bfea')
        report_lbl.place(x=120 , y=70)
        correct_word_lbl = Label(text=correct_word , fg='Green' , font='Arial' , bg=bk_clr)
        correct_word_lbl.place(x=120 , y=100)
        wrong_words_lbl = Label(text=mistake_word , fg='Red' , font='Arial' , bg=bk_clr)
        wrong_words_lbl.place(x=310 , y=100)
        restart = ttk.Button(text="Restart" , command=reset)
        restart.place(x=130 , y=400)
        exit = ttk.Button(text="Exit" , command=close)
        exit.place(x=300 , y=400)

    else :
        window.after(1000 , count_down , count - 1)


# ---------------------------------- Text label ------------------------------------#
random_word = get_words()
type_word_lbl = Label(text=f"Word: \t{random_word}" , font='Arial' , bg=bk_clr)
type_word_lbl.place(x=10 , y=30)

# ------------------------------------- Text entry --------------------------------#
text_entry = Text(window , width=43 , height=100 , border=10 , font='Arial' , bg='#f1d3f5')
text_entry.place(x=0 , y=200)
text_entry.focus()


# -------------------- To bind click event and countdown timer----------------------------#
def click(e) :
    if len(text_entry.get("1.0","end-1c"))>=1:
        window.unbind('<Key>')
        count_down(60)


window.bind('<Key>' , click)
# -------------------- To bind space bar key -------------------------------#
wrong_words = []
correct_word_indx = []


def space(e) :
    global word , random_word , wrong_words , correct_word_indx , entered_text , text_entry
    word = text_entry.get("1.0" , "end-1c").split(" ")
    entered_text = word[-2]
    if entered_text == random_word :
        pass
    else :
        if len(entered_text) > 0 :
            correct_word_indx.append(word_list.index(random_word))  # To get index of correct word
            wrong_words.append(entered_text)  # Append wrong typed words
    if len(entered_text) > 0 :  # To check entered text is whitespace
        random_word = get_words().strip()  # call the function to get random word only when alphabet is typed
        type_word_lbl.config(text=f"Word: \t{random_word}")


window.bind('<space>' , space)  # Bind spacebar key

window.mainloop()
