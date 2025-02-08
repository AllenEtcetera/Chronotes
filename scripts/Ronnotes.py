import sys
import time
import threading
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import Menu,filedialog,messagebox,simpledialog


BASE_DIR = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).resolve().parent

#################### Hourpass ####################
def toggle_hourpass():
    global notif_on
    notif_on = not notif_on
    if notif_on:
        def notify():
            while notif_on:
                time.sleep(6) #3600 is 1 hour
                if notif_on:
                    messagebox.showinfo("Hour Passed","An hour has passed!")
        threading.Thread(target=notify,daemon=True).start()

#################### Encrypt/Decrypt stuff ####################
def encrypt(text,shift):
    result = ""
    # traverse text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

def decrypt(text,shift):
    result = ""
    # traverse text
    for i in range(len(text)):
        char = text[i]
        # Decrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) - shift - 65) % 26 + 65)
        # Decrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            result += char
    return result

#################### File save functions ####################
def save_data(file_path,text,encrypt_data=False,shift=3):
    if encrypt_data:
        text = encrypt(text,shift)
    with open(file_path, 'w') as file:
        file.write(text)
    print(f"File saved: {file_path}")
# Save as
def saveas_file():
    # Open file save thingy
    global file_path
    file_path = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        encrypt_data = messagebox.askyesno("Encrypt","Encrypt this file while saving?")
        save_data(file_path, text.get("1.0",tk.END), encrypt_data)
    else:
        print("No file selected")
# Save current
def save_file():
    if file_path:
        encrypt_data = messagebox.askyesno("Encrypt","Encrypt this file while saving?")
        save_data(file_path, text.get("1.0",tk.END), encrypt_data)
    else:
        saveas_file()

#################### File open function ####################
def open_file():
    if text.get("1.0",tk.END).strip():  # Check if text is present
        if messagebox.askyesnocancel("Save", "Save before opening a different file?"):
            save_file()
    # Open file open thingy
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    # Relay file path
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        decrypt_data = messagebox.askyesno("Decrypt","Decrypt data on file?")
        if decrypt_data:
            content = decrypt(content,3)
        text.delete("1.0",tk.END)
        text.insert(tk.END,content)
        print(f"File opened: {file_path}")
    else:
        print("No file selected")

#################### New file function ####################
def new_file():
    if text.get("1.0",tk.END).strip():  # Check if text is present
        if messagebox.askyesnocancel("Save", "Save before starting a new file?"):
            save_file()
    text.delete("1.0",tk.END)  # Clear all text

###################### Close function #####################
def on_close():
    if messagebox.askyesnocancel("Quit", "Save before exiting?"):
        save_file()
    rootNote.destroy() # End program
    
##################### File edit stuff #####################
# Undo
def undo_text():
    try:
        text.edit_undo()
    except tk.TclError:
        pass
# Redo
def redo_text():
    try:
        text.edit_redo()
    except tk.TclError:
        pass
# Cut, Copy, Paste
def cut_text():
    text.event_generate("<<Cut>>")
def copy_text():
    text.event_generate("<<Copy>>")
def paste_text():
    text.event_generate("<<Paste>>")
# Find
def find_text():
    text.tag_remove('found','1.0',tk.END) # Clear
    search_string = simpledialog.askstring("Find","Find:")
    if search_string:
        idx = '1.0'
        while True:
            idx = text.search(search_string,idx,nocase=1,stopindex=tk.END)
            if not idx:
                break
            end_idx = f"{idx}+{len(search_string)}c"
            text.tag_add('found',idx,end_idx)
            idx = end_idx
        text.tag_config('found', background='yellow', foreground='black')
# Find and Replace
def replace_text():
    find_string = simpledialog.askstring("Find", "Find:")
    if find_string:
        replace_string = simpledialog.askstring("Replace", "Replace with:")
        if replace_string is not None:  # Allow empty string replacements
            content = text.get("1.0", tk.END)
            new_content = content.replace(find_string, replace_string)
            text.delete("1.0", tk.END)
            text.insert("1.0", new_content)


#################### Create window ####################
def create_window():
    global text, rootNote, file_path, notif_on
    notif_on = False
    rootNote = tk.Tk()
    rootNote.title("Ronnotes")
    # Create thing to put text in
    text = tk.Text(rootNote, undo=True, wrap=tk.WORD)
    text.pack()
    # Call closing function upon termination
    rootNote.protocol("WM_DELETE_WINDOW", on_close)
    # Create menu bar
    menubar = Menu(rootNote)
    # Create File menu and add stuff
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="New",command=new_file)
    file_menu.add_command(label="Open",command=open_file)
    file_menu.add_command(label="Save",command=save_file)
    file_menu.add_command(label="Save As",command=saveas_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit",command=on_close)
    menubar.add_cascade(label="File",menu=file_menu)

    # Create an Edit menu and add stuff
    edit_menu = Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Undo",command=undo_text)
    edit_menu.add_command(label="Redo",command=redo_text)
    edit_menu.add_separator()
    edit_menu.add_command(label="Cut",command=cut_text)
    edit_menu.add_command(label="Copy",command=copy_text)
    edit_menu.add_command(label="Paste",command=paste_text)
    edit_menu.add_separator()
    edit_menu.add_command(label="Find",command=find_text)
    edit_menu.add_command(label="Replace",command=replace_text)
    menubar.add_cascade(label="Edit",menu=edit_menu)

    # Create a reminder section
    edit_menu = Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Hour Pass",command=toggle_hourpass)
    edit_menu.add_separator()
    edit_menu.add_command(label="Task",command=lambda:subprocess.Popen(['python', str(BASE_DIR / 'OttoRemind.py')]))
    menubar.add_cascade(label="Remind",menu=edit_menu)

    # Configure the menu bar
    rootNote.config(menu=menubar)
    # Avoid file open prompt upon starting
    file_path = None
    # Run the application
    rootNote.mainloop()
create_window()