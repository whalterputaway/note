import secrets
from tkinter import *
from tkinter import messagebox, filedialog
import configparser
import base64
import webbrowser
import os
main = Tk()
main.title("AmTCD")
main.option_add("*tearOff", FALSE)
main_menu = Menu()
current_file = None 
config = configparser.ConfigParser()
config.read('AmTCD.ini')
master_key = config['main']['keyuser'].encode()
def show_help(event="None"):
    help_window = Toplevel(main)
    help_window.title("Справочная информация")
    help_window.geometry("695x150+600+350")
    help_window.transient(main)
    help_window.grab_set()
    about = Label(help_window, text="Слова благодарности: Хотел бы выразить огромное спасибо Папе и Маме, за все что они для меня сделали и не сделали!\n © Нгуен Чыонг 2025.",anchor="w")
    about.place(x=5,y=5)
def open_html_page():
    file_path = os.path.abspath("index.html")
    webbrowser.open(f"file://{file_path}")
def xor_bytes(data: bytes, key: bytes) -> bytes:
    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ key[i % len(key)])
    return bytes(result)
def encrypt_with_master(plaintext: str, master_key: bytes):
    file_key = secrets.token_bytes(32)
    encrypted_text = xor_bytes(plaintext.encode('utf-8'), file_key)
    encrypted_file_key = xor_bytes(file_key, master_key)
    return encrypted_text, encrypted_file_key
def decrypt_with_master(encrypted_text: bytes, encrypted_file_key: bytes, master_key: bytes):
    file_key = xor_bytes(encrypted_file_key, master_key)
    decrypted_text = xor_bytes(encrypted_text, file_key)
    return decrypted_text.decode('utf-8')
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
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if filepath:
        text = text_field.get("1.0", END)
        mass = encrypt_with_master(text,master_key)
        config = configparser.ConfigParser()
        config['main']={'keyopen': base64.b64encode(mass[1]).decode(),'mess': base64.b64encode(mass[0]).decode()}
        current_file = filepath
        with open(current_file, "w") as file:
            config.write(file)
def save_file():
    global current_file
    if current_file:
        text = text_field.get("1.0", END)
        mass = encrypt_with_master(text,master_key)
        config = configparser.ConfigParser()
        config['main']={'keyopen': base64.b64encode(mass[1]).decode(),'mess': base64.b64encode(mass[0]).decode()}
        with open(current_file, "w") as file:
            config.write(file)
    else:
        saveas_file()
def open_file():
    global current_file
    filepath = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if not filepath:
        return
    config = configparser.ConfigParser()
    config.read(filepath)
    keyopen = base64.b64decode(config['main']['keyopen'])
    mess = base64.b64decode(config['main']['mess'])
    decrypted = decrypt_with_master(mess, keyopen, master_key)
    text_field.delete("1.0", END)
    text_field.insert("1.0", decrypted)
    current_file = filepath
menus = {"Файл": {"Новый": new_win,"Открыть": open_file,"Сохранить": save_file,"Сохранить как":saveas_file,"-": None,"Выход": main.destroy},"Правка": {"Копировать": copy,"Вставить": paste,"-": None,"Параметры...": lambda: None},"Справка": {"Содержание": open_html_page,"-": None,"О программе...": about_programm}}
for menu_name, items in menus.items():
    menu = Menu(main_menu, tearoff=0)
    for label, cmd in items.items():
        if label == "-":
            menu.add_separator()
        else:
            menu.add_command(label=label, command=cmd)
    main_menu.add_cascade(label=menu_name, menu=menu)
text_field = Text()
text_field.pack(fill=BOTH, expand=1)
main.bind('<F1>', show_help)
main.config(menu=main_menu)
main.mainloop()