import json
import string
from random import choices, shuffle, choice
from tkinter import *
from tkinter import messagebox

import pyperclip


# -- PASSWORD GENERATOR -------------- #
def gen_but():
    new_password = []
    new_password += choices(string.ascii_lowercase, k=6)
    new_password += choices(string.ascii_uppercase, k=6)
    new_password += choices(string.punctuation, k=6)
    new_password += choices(string.digits, k=6)
    shuffle(new_password)
    new_password = "".join(new_password)

    # the '|' character confuses the markdown table :)
    if '|' in new_password:
        new_password = new_password.replace('|', choice(string.ascii_lowercase))

    pyperclip.copy(new_password)

    pass_inp.delete(0, END)
    pass_inp.insert(0, new_password)


# -- SAVE PASSWORD ------------------- #
def add_but():
    global entries
    file_name = "passwords.md"

    webs_e = website_inp.get()
    user_e = user_inp.get()
    pass_e = pass_inp.get()

    if len(webs_e) and len(pass_e):

        dash = "-----"

        is_ok = messagebox.askokcancel(
            title="check the data",
            message=f"{dash} website {dash}\n{webs_e}\n"
                    f"{dash} username {dash}\n{user_e}\n"
                    f"{dash} password {dash}\n{pass_e}\n"
                    f"\nare you okay to save this?"
        )

        if is_ok:
            file_entry = f"|{webs_e}|{user_e}|{pass_e}|\n"

            entries.append(file_entry)

            with open(file_name, 'a') as out_file:
                out_file.writelines(entries)

            website_inp.delete(0, END)
            pass_inp.delete(0, END)

    else:
        messagebox.showinfo(message="fill in all the fields")


def md2json():
    # use to restore json data from md file :)

    json_data = {}
    with open("passwords.md", 'r') as md_file:
        data = md_file.readlines()

    for x in range(4, len(data)):
        d = data[x].split('|')
        head = d[1]

        json_data[head] = {
            "user": d[2],
            "pass": d[3]
        }

    with open("passwords.json", 'w+') as json_file:
        json.dump(json_data, json_file, indent=4)


# md2json()


# -- UI SETUP ------------------------ #
win = Tk()
win.title("password manager")
win.config(padx=20, pady=20)

# image
logo = PhotoImage(file="logo.png")

canvas = Canvas(
    width=200,
    height=200,
    bg="white",
    highlightthickness=0
)

canvas.create_image(
    100, 100,
    image=logo,
)

canvas.grid(column=1, row=0)

# labels
website_lbl = Label(text="website: ", anchor='e', width=14)
website_lbl.grid(column=0, row=1)

user_lbl = Label(text="email / username: ", anchor='e', width=14)
user_lbl.grid(column=0, row=2)

pass_lbl = Label(text="password: ", anchor='e', width=14)
pass_lbl.grid(column=0, row=3)

# entries
website_inp = Entry(width=35, bg="grey96")
website_inp.grid(column=1, row=1, columnspan=2)
website_inp.focus()

user_inp = Entry(width=35, bg="grey96")
user_inp.grid(column=1, row=2, columnspan=2)
user_inp.insert(END, "fred@flintstone.com")

pass_inp = Entry(width=21, bg="grey96")
pass_inp.grid(column=1, row=3)

# buttons
gen_but = Button(
    text="generate password",
    highlightthickness=0,
    command=gen_but
)

gen_but.grid(column=2, row=3)

add_but = Button(
    text="add password",
    width=36,
    highlightthickness=0,
    command=add_but
)

add_but.grid(column=1, row=4, columnspan=2)

win.mainloop()
