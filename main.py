import tkinter
import random
from tkinter import messagebox
import pyperclip
import json

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR -------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(10, 12))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(4, 6))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(4, 6))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password_string = "".join(password_list)
    # password_entry.config(text=f"{password_string}")
    password_entry.delete(0, 'end')
    password_entry.insert(0, f"{password_string}")
    pyperclip.copy(password_string)


# ---------------------------- SEARCH -------------------------------------------- #


def search_site():
    searched_website = website_entry.get().upper()
    if len(searched_website) == 0:
        messagebox.showerror(title="Validation incomplete", message="Please make sure you provided a website name")
    else:
        try:
            search_saved_data = open("data.json", "r")
            data = json.load(search_saved_data)
            if searched_website in data:
                messagebox.showinfo(title="Search results:",
                                    message=f"username: {data[searched_website]['email']} "
                                            f"\npassword: {data[searched_website]['password']}")
            else:
                messagebox.showerror(title="Site not found", message="Double-check the spelling of the site")
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No data found!")


def create_edit_file():
    website = website_entry.get().upper()
    username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }}
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Validation incomplete", message="Please make sure you haven't left any fields "
                                                                    "empty!")
    else:
        is_ok = messagebox.askyesno(title=website, message=f"These are the details entered: \n{username} \nPassword:"
                                    f"{password} \nIs it ok to save?")
        if is_ok:
            try:
                # open json file in read mode, make a copy of content and update the copy with the new data
                saved_data = open("data.json", "r")
                data = json.load(saved_data)
                # reopen the json file in write mode and append / save the copy of data (updated with new data and old)
            # if it does not find the file aka it gets a file error it creates a file, and then it dumps the data
            except FileNotFoundError:
                saved_data = open("data.json", "w")
                json.dump(new_data, saved_data, indent=4)
            # after tyring to open or create with exception "what else" may it do? It gets here only if the file was
            # found. Update the copy of data, open the file and save the new modified copy in the place of the old file
            else:
                data.update(new_data)
                saved_data = open("data.json", "w")
                json.dump(data, saved_data, indent=4)
            # delete the input provided previously from keyboard
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------------------ #


window = tkinter.Tk()
window.title("Password manager")
window.config(padx=50, pady=50, bg=YELLOW)

# ---------- CANVAS + IMAGE ---------- #
canvas = tkinter.Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
locker_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_img)
canvas.grid(column=1, row=0)

# ----------  BUTTONS ---------------- #
add_button = tkinter.Button(text="Add", highlightthickness=0, command=create_edit_file, width=43)
add_button.grid(column=1, row=4, columnspan=2)

generate_password_button = tkinter.Button(text="Generate password", highlightthickness=0, command=generate_password,
                                          width=14)
generate_password_button.grid(column=2, row=3)

search_site_button = tkinter.Button(text="Search", highlightthickness=0, command=search_site, width=14)
search_site_button.grid(column=2, row=1)

# ---------- LABELS ------------------ #
website_label = tkinter.Label(text="Website:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
website_label.grid(column=0, row=1)

email_username_label = tkinter.Label(text="Email/Username:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
email_username_label.grid(column=0, row=2)

password_label = tkinter.Label(text="Password:", font=(FONT_NAME, 12, "bold"), bg=YELLOW)
password_label.grid(column=0, row=3)

# ---------- ENTRIES ----------------- #
website_entry = tkinter.Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_username_entry = tkinter.Entry(width=50)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, "drakkaroktesting@Gmail.com")

password_entry = tkinter.Entry(width=32)
password_entry.grid(column=1, row=3)

window.mainloop()
