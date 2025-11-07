from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import configparser



main = Tk()
main.title("AmTCD")
main.option_add("*tearOff", FALSE)
main_menu = Menu()
current_file = None 


def about_programm():
    messagebox.showinfo("О программе", "Программа для 'прозрачного шифрования'\n© Nguyen T., Russia, 2025'")
def click_reference():
    reference = Tk()
    reference.title("Справка")
    reference.geometry("350x170+600+350")
    label = Label(reference,text='Приложение с графическим интерфейсом\n"Блокнот TCD" (файл приложения: TCD).\nПозволяет: создавать / открывать / сохранять\nзашифрованный текстовый файл, предусмотернны\nвывод не модальной формы "Справка",\nвывод модальной формы "О программе".',justify="left")
    label.place(x=5,y=5)
    close_button = Button(reference, text="OK",width=7,height=1, command=reference.destroy).place(x=275,y=130)

def copy():
    text = text_field.get("sel.first", "sel.last")
    text_field.clipboard_clear()     
    text_field.clipboard_append(text) 

def paste():
    text = text_field.clipboard_get()  
    text_field.insert("insert", text)  

def new_win():
    global current_file
    text_field.delete("1.0", END)
    current_file = None

def saveas_file():
    global current_file
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if filepath:
        text = text_field.get("1.0", END)
        config = configparser.ConfigParser()
        config['main']={
            'keyopen': "sssssssssss",
            'mess': text
        }
        current_file = filepath
        with open(current_file, "w") as file:
            config.write(file)

def save_file():
    global current_file
    if current_file:
        text = text_field.get("1.0", END)
        config = configparser.ConfigParser()
        config['main']={
            'keyopen': "sssssssssss",
            'mess': text
        }
        with open(current_file, "w") as file:
            config.write(file)
    else:
        saveas_file()

def open_file():
    filepath = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txtx"), ("All Files", "*.*")]
    )
    global current_file
    if filepath != "":
        with open(filepath, "r") as file:
            text =file.read()
            text_field.delete("1.0", END)
            text_field.insert("1.0", text)
    current_file = filepath







file_menu = Menu()
file_menu.add_command(label="Новый",command=new_win)
file_menu.add_command(label="Открыть",command=open_file)
file_menu.add_command(label="Сохранить",command=save_file)
file_menu.add_command(label="Сохранить как", command=saveas_file)
file_menu.add_separator()
file_menu.add_command(label="Выход",command=main.destroy)

edit_menu = Menu()
edit_menu.add_command(label="Копировать",command=copy)
edit_menu.add_command(label="Вставить",command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Параметры...")

ref_menu = Menu()
ref_menu.add_command(label="Cодержание",command=click_reference)
ref_menu.add_separator()
ref_menu.add_command(label="О программе...",command=about_programm)

main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_cascade(label="Правка", menu=edit_menu)
main_menu.add_cascade(label="Справка", menu=ref_menu)

text_field = Text()
text_field.pack(fill=BOTH, expand=1)

main.config(menu=main_menu)
main.mainloop()