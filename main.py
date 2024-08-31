import json
import random
import pyperclip
from tkinter import END
from tkinter import Tk
from tkinter import Label
from tkinter import PhotoImage
from tkinter import Button
from tkinter import Entry
from tkinter import Canvas
from tkinter import TclError
from tkinter import messagebox
from characters import all_characters

COLORS = [
    "#39375b",
    "#745c97",
    "#d597ce",
    "#f5b0cb",
    "#eaf887",
    "#79dc96",
    "#3bbbb3",
    "#377aaf",
    "#074684",
    "#0ea5c6",
    "#a0edf7",
    "#f2efb6",
    "#449187",
    "#91e4a6",
    "#5f64c0",
    "#453064"
]


def get_font(fontname='Consolas', size=12, fonttype='normal') -> tuple:
    return fontname, size, fonttype


def generate_password() -> str:
    password = ''
    for _ in range(10):
        characters = random.choice(all_characters)
        password += random.choice(characters)
        password_textfield.delete(0, END)
        try:
            password_textfield.clipboard_clear()
        except TclError:
            pass

    password_textfield.insert(index=END, string=password)
    password_textfield.clipboard_append(password_textfield.get())


def find_password():
    website = website_textfield.get()
    if website:
        try:
            with open(file='data.json', mode='r') as data_file:
                data = json.load(data_file)
                if website in data:
                    email_username = data[website].get('Email')
                    password = data[website].get('Password')
                else:
                    messagebox.showwarning(title=f"Website doesn't exist in the data file!",
                                           message=f"You have no password related to {website}")
        except FileNotFoundError:
            messagebox.showwarning(title='Warning', message='No data file have been found')
        else:
            if website in data:
                messagebox.showinfo(title=website,
                                    message=f'Email/Username: {email_username}\nPassword: {password}')
            pyperclip.copy(password)
    else:
        messagebox.showwarning(title="Website filed is empty", message="You haven't entered any website")


def save_password():
    website = website_textfield.get()
    email = email_textfield.get()
    password = password_textfield.get()
    new_data = {
        website: {
            'Email': email,
            'Password': password
        }
    }
    if website and email and password:  # Checks if any field is empty
        try:
            with open(file='data.json', mode='r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(file='data.json', mode='w') as data_file:
                json.dump(obj=new_data, fp=data_file, indent=4)
        else:
            data.update(new_data)
            with open(file='data.json', mode='w') as data_file:
                json.dump(obj=data, fp=data_file, indent=4)
        finally:
            website_textfield.delete(0, END)
            email_textfield.delete(0, END)
            password_textfield.delete(0, END)
    else:
        messagebox.showwarning(title=website, message="Please don't leave any field empty")


window = Tk()
window.configure(padx=20, pady=20, background=COLORS[14])
window.title('Password Manager')
window.geometry('+400+280')

canvas = Canvas(width=200, height=200, highlightthickness=0, background=COLORS[14])
logo_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

website_label = Label(text='Website: ', background=COLORS[14], foreground=COLORS[15],
                      font=get_font(fonttype='bold'))
website_label.grid(row=1, column=0)

website_textfield = Entry(width=23, background=COLORS[7], foreground=COLORS[13],
                          font=get_font(fontname='Arial', size=14, fonttype='italic'))
website_textfield.grid(row=1, column=1, columnspan=1)

email_username_label = Label(text='Email/Username: ', background=COLORS[14], foreground=COLORS[15],
                             font=get_font(fonttype='bold'))
email_username_label.grid(row=2, column=0)

email_textfield = Entry(width=35, background=COLORS[7], foreground=COLORS[13],
                        font=get_font(fontname='Arial', size=14, fonttype='italic'))
email_textfield.grid(row=2, column=1, columnspan=2)

password_label = Label(text='Password: ', background=COLORS[14], foreground=COLORS[15],
                       font=get_font(fonttype='bold'))
password_label.grid(row=3, column=0)

password_textfield = Entry(width=23, background=COLORS[7], foreground=COLORS[13],
                           font=get_font(fontname='Arial', size=14, fonttype='italic'))
password_textfield.grid(row=3, column=1)

generate_password_button = Button(text='Generate Password', background=COLORS[6], foreground=COLORS[8],
                                  font=get_font(size=10))
generate_password_button.configure(command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(width=38, text='Add', background=COLORS[6], foreground=COLORS[8],
                    font=get_font('Consolas', size=14, fonttype='bold'))
add_button.configure(command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(width=17, text='Search', background=COLORS[6], foreground=COLORS[8],
                       font=get_font(size=10), command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
