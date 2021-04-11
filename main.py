import json
import string
from random import choices, shuffle, choice
from tkinter import *
from tkinter import messagebox

import pyperclip

entries = []
s_data = {}


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
    file_name = "passwords"

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

            # write to markdown file
            with open(file_name + ".md", 'a') as out_file:
                out_file.writelines(entries)

            new_dict = {
                webs_e: {
                    "user": user_e,
                    "pass": pass_e
                }
            }

            try:
                with open(file_name + ".json", 'r') as json_file:
                    old_data = json.load(json_file)
                    old_data.update(new_dict)
            except FileExistsError:
                pass

            with open(file_name + ".json", 'w') as json_file:
                json.dump(old_data, json_file, indent=4)

            s_data.update(new_dict)

            website_inp.delete(0, END)
            pass_inp.delete(0, END)

    else:
        messagebox.showinfo(message="fill in all the fields")


# -- SEARCH PASSWORD ---------------- #
def search_but():
    in_txt = website_inp.get()
    if in_txt != '':
        sites = list(s_data.keys())
        pass_inp.delete(0, END)

        if in_txt in sites:
            password = s_data[in_txt]['pass']
            pass_inp.insert(END, password)
            pyperclip.copy(password)
        else:
            pass_inp.insert(END, "N O T   F O U N D")


def md2json():
    # use to restore json file from markdown :)
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

try:
    with open("passwords.json", 'r') as json_file:
        s_data = json.load(json_file)
except FileExistsError:
    pass

# -- UI SETUP ------------------------ #
win = Tk()
win.title("password manager")
win.config(padx=30, pady=20)

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
website_lbl = Label(text="website: ", anchor='e', width=8)
website_lbl.grid(column=0, row=1)

user_lbl = Label(text="username: ", anchor='e', width=8)
user_lbl.grid(column=0, row=2)

pass_lbl = Label(text="password: ", anchor='e', width=8)
pass_lbl.grid(column=0, row=3)

# entries
website_inp = Entry(width=28, bg="grey96")
website_inp.grid(column=1, row=1)
website_inp.focus()

user_inp = Entry(width=35, bg="grey96")
user_inp.grid(column=1, row=2, columnspan=2)
user_inp.insert(END, "fred@flintstone.com")

pass_inp = Entry(width=28, bg="grey96")
pass_inp.grid(column=1, row=3)

# buttons
gen_but = Button(
    text="generate",
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

search_but = Button(
    text="search",
    highlightthickness=0,
    command=search_but
)

search_but.grid(column=2, row=1)

win.mainloop()
