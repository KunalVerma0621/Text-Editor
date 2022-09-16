from tkinter import *
from tkinter import ttk
from ctypes import windll
from tkinter import messagebox as msg
from tkinter import filedialog as fd
import os.path
from tkinter.colorchooser import askcolor
from tkinter import font
from time import strftime
from tkinter.font import Font

# colors
YELLOW = "#F2AA4C"

# font style
LARGE_FONT_STYLE = ("consolas", 14, "normal")
SMALL_FONT_STYLE = ("Times New Roman", 15, "normal")
TEXT_FONT = ["consolas", 16, "normal"]
FONT_LABEL = ("consolas", 15, "normal")
SELECT_FONT = ("@Microsoft YaHei UI Light", 12, "normal")

# global variable
file = None
file_name = "Untitled"


# noinspection PyMethodMayBeStatic
class Leafpad(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("leafpad_icon.ico")
        self.title(f'{file_name} - Leafpad')
        self.geometry("1200x700")
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)
        self.create_menu_bar()
        self.text_area = self.create_text_area()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.font_name = StringVar()
        self.font_size = StringVar()
        self.font_weight = StringVar()
        self.key = ["Control-s", "Control-S", "Control-n", "Control-N", "Control-g", "Control-G", "Control-Shift-S",
                    "Control-Shift-s", "Control+", "Control-", "Control0", "Control-b", "Control-B", "Control-k",
                    "Control-K", "Control-u", "Control-U", "Control-i", "Control-I", "Control-t", "Control-T",
                    "Control-f", "Control-F", "Control-r", "Control-R", "Control-l", "Control-L"]
        self.bind_keys()
        self.protocol("WM_DELETE_WINDOW", self.delete)

    def bind_keys(self):
        for item in self.key:
            if item == "Control-s" or item == "Control-S":
                self.bind(f'<{item}>', lambda event: self.save())
            elif item == "Control-Shift-s" or item == "Control-Shift-S":
                self.bind(f'<{item}>', lambda event: self.save())
            elif item == "Control-n" or item == "Control-N":
                self.bind(f'<{item}>', lambda event: self.new())
            elif item == "Control-g" or item == "Control-G":
                self.bind(f'<{item}>', lambda event: self.open())
            elif item == "Control+":
                self.bind('<Control-=>', lambda event, x=item: self.zoom(x))
            elif item == "Control-":
                self.bind('<Control-minus>', lambda event, x=item: self.zoom(x))
            elif item == "Control0":
                self.bind('<Control-0>', lambda event, x=item: self.zoom(x))
            elif item == "Control-l" or item == "Control-L":
                self.bind(f'<{item}>', lambda event: self.normal())
            elif item == "Control-b" or item == "Control-B":
                self.bind(f'<{item}>', lambda event: self.bold())
            elif item == "Control-i" or item == "Control-I":
                self.bind(f'<{item}>', lambda event: self.italic_msg())
            elif item == "Control-k" or item == "Control-K":
                self.bind(f'<{item}>', lambda event: self.italic())
            elif item == "Control-u" or item == "Control-U":
                self.bind(f'<{item}>', lambda event: self.underline())
            elif item == "Control-t" or item == "Control-T":
                self.bind(f'<{item}>', lambda event: self.date())
            elif item == "Control-f" or item == "Control-F":
                self.bind(f'<{item}>', lambda event: self.find())
            elif item == "Control-r" or item == "Control-R":
                self.bind(f'<{item}>', lambda event: self.replace())

    def create_menu_bar(self):
        self.create_file_bar()
        self.create_edit_bar()
        self.create_theme_bar()
        self.create_text_zoom()
        self.create_about()
        self.create_status_bar()
        self.window_resize()

    # noinspection PyBroadException
    def delete(self):
        global file_name
        global file
        final_text = self.text_area.get('1.0', 'end')
        filetypes = (("Text Documents (*.txt)", '*.txt'),
                     ('All files', '*.*'))
        if len(final_text) == 1 and file_name == "Untitled":
            self.destroy()
        elif len(final_text) != 1 and file_name == "Untitled":
            ans = msg.askyesno(title="Leafpad",
                               message=f'Do you want to save changes to {os.path.basename(str(file_name))}')
            if ans:
                try:
                    file = fd.asksaveasfilename(defaultextension=".txt", title="Save Files", filetypes=filetypes,
                                                confirmoverwrite=False)
                    if os.path.basename(file) in os.listdir(os.path.dirname(file)):
                        msg.showerror(title="File exist", message=f'{os.path.basename(file)} file already exist.')
                    else:
                        file_name = os.path.basename(file)
                        self.title(f'{file_name} - Leafpad')
                        with open(file, "w") as f:
                            f.write(final_text)
                        self.destroy()
                except Exception:
                    return 0
            else:
                self.destroy()
        elif len(final_text) == 1 and file_name != "Untitled" or len(final_text) != 1 and file_name != "Untitled":
            try:
                with open(os.path.abspath(str(file)), "r") as f:
                    if f.read().strip() == final_text.strip():
                        self.destroy()
                    else:
                        ans = msg.askyesno(title="Leafpad",
                                           message=f'Do you want to save changes to\n {os.path.abspath(str(file))} ?')
                        if ans:
                            with open(os.path.abspath(str(file)), "w") as f1:
                                f1.write(final_text.strip())
                            self.destroy()
                        else:
                            self.destroy()
            except Exception:
                msg.showerror(title="Leafpad", message="file not found")

    def evaluate_operation(self, value):
        if value == "New":
            self.new()
        elif value == "New Window":
            pass
        elif value == "Open":
            self.open()
        elif value == "Save":
            self.save()
        elif value == "Save As":
            self.save_as()
        elif value == "Time/Date":
            self.date()
        elif value == "Exit":
            self.delete()

    def set_textarea(self):
        global file_name
        file_name = "Untitled"
        self.title(f'{file_name} - Leafpad')
        self.text_area.delete('1.0', 'end')

    def date(self):
        self.text_area.insert('end', strftime('%H:%M %p %d %B'))

    # noinspection PyBroadException
    def new(self):
        global file
        global file_name
        filetypes = (("Text Documents (*.txt)", '*.txt'),
                     ('All files', '*.*'))
        final_text = self.text_area.get('1.0', 'end')
        if len(final_text) != 1 and file_name == "Untitled":
            try:
                ans = msg.askyesnocancel(title="Leafpad", message="Do you want to save changes to untitled? ")
                if ans == TRUE:
                    file = fd.asksaveasfilename(defaultextension=".txt", filetypes=filetypes, title="Save File",
                                                confirmoverwrite=False)
                    try:
                        if os.path.basename(file) in os.listdir(os.path.dirname(file)):
                            msg.showerror(title="File exist", message=f'{os.path.basename(file)} file already exist.')
                        else:
                            with open(os.path.abspath(str(file)), "w") as f:
                                f.write(final_text)
                            self.set_textarea()
                    except Exception:
                        self.set_textarea()

                elif ans == FALSE:
                    self.set_textarea()

                else:
                    file_name = "Untitled"
                    self.title(f'{file_name} - Leafpad')
                    self.text_area.delete('1.0', 'end')
                    self.text_area.insert('1.0', final_text)

            except Exception:
                self.set_textarea()

        elif len(final_text) != 1 and file_name != "Untitled" or len(final_text) == 1 and file_name != "Untitled":
            try:
                with open(os.path.abspath(str(file)), "r") as f:
                    if f.read().strip() == final_text.strip():
                        self.set_textarea()
                    else:
                        ans = msg.askyesno(title="Leafpad",
                                           message=f'Do you want to save changes to\n {os.path.abspath(file)} ?')
                        if ans is True:
                            with open(os.path.abspath(str(file)), "w") as f1:
                                f1.write(final_text)
                        self.set_textarea()
            except Exception:
                self.set_textarea()

        elif len(final_text) == 1 and file_name == "Untitled":
            return 0

    # noinspection PyBroadException
    def save(self):
        global file_name
        global file
        final_text = self.text_area.get('1.0', 'end')
        filetypes = (("Text Documents (*.txt)", '*.txt'),
                     ('All files', '*.*'))
        if len(final_text) != 1 and file_name == "Untitled" or len(final_text) == 1 and file_name == "Untitled":
            try:
                file = fd.asksaveasfilename(defaultextension=".txt", title="Save Files", filetypes=filetypes,
                                            confirmoverwrite=False)
                if os.path.basename(file) in os.listdir(os.path.dirname(file)):
                    msg.showerror(title="File exist", message=f'{os.path.basename(file)} file already exist.')
                else:
                    file_name = os.path.basename(file)
                    self.title(f'{file_name} - Leafpad')
                    with open(file, "w") as f:
                        f.write(final_text)
            except Exception:
                return 0

        elif len(final_text) != 1 and file_name != "Untitled" or len(final_text) == 1 and file_name != "Untitled":
            try:
                with open(os.path.abspath(str(file)), "w") as f:
                    f.write(final_text)
            except Exception:
                msg.showerror(title="Error", message="File Not Saved")

    # noinspection PyBroadException
    def open(self):
        global file
        global file_name
        final_text = self.text_area.get('1.0', 'end')
        filetypes = (("Text Documents (*.txt)", '*.txt'),
                     ('All files', '*.*'))
        if len(final_text) != 1 and file_name == "Untitled":
            ans = msg.askyesnocancel(title="Leafpad", message="Do you want to save changes to untitled? ")
            if ans == TRUE:
                file = fd.asksaveasfilename(title="Save file", defaultextension=".txt")
                try:
                    with open(os.path.abspath(str(file)), "w") as f1:
                        f1.write(final_text)
                except Exception:
                    return 0
                file = fd.askopenfilename(title="Open a file", filetypes=filetypes)
                if file:
                    file_name = os.path.basename(str(file))
                    self.title(f'{file_name} - Leafpad')
                    self.text_area.delete('1.0', 'end')
                    with open(file, "r") as f1:
                        self.text_area.insert('1.0', f1.read())
                else:
                    return 0

            elif ans == FALSE:
                file = fd.askopenfilename(title="Open a file", filetypes=filetypes)
                if file:
                    try:
                        file_name = os.path.basename(str(file))
                        self.title(f'{file_name} - Leafpad')
                        self.text_area.delete('1.0', 'end')
                        with open(file, "r") as f1:
                            self.text_area.insert('1.0', f1.read())
                    except Exception:
                        return 0

            else:
                return 0

        elif len(final_text) == 1 and file_name == "Untitled":
            file = fd.askopenfilename(filetypes=filetypes)
            file_name = os.path.basename(file)
            try:
                if file:
                    self.title(f'{file_name} - Leafpad')
                    with open(file, "r") as f:
                        self.text_area.insert('1.0', f.read())
                else:
                    file_name = "Untitled"
                    self.title(f'{file_name} - Leafpad')
            except Exception:
                file_name = "Untitled"
                self.text_area.delete('1.0', 'end')

        elif len(final_text) == 1 and file_name != "Untitled":
            try:
                with open(os.path.abspath(str(file)), "r") as f:
                    if f.read().strip() == final_text.strip():
                        file = fd.askopenfilename(title="Open a file", filetypes=filetypes)
                        if file:
                            file_name = os.path.basename(str(file))
                            self.title(f'{file_name} - Leafpad')
                            self.text_area.delete('1.0', 'end')
                            with open(file, "r") as f1:
                                self.text_area.insert('1.0', f1.read())
                    else:
                        ans = msg.askyesno(title="Leafpad",
                                           message=f'Do you want to save changes to\n {os.path.abspath(str(file))} ?')
                        if ans is True:
                            with open(os.path.abspath(str(file)), "w") as f1:
                                f1.write(final_text.strip())
                        file = fd.askopenfilename(title="Open a file", filetypes=filetypes)
                        if file:
                            file_name = os.path.basename(str(file))
                            self.title(f'{file_name} - Leafpad')
                            self.text_area.delete('1.0', 'end')
                            with open(file, "r") as f1:
                                self.text_area.insert('1.0', f1.read())
            except Exception:
                msg.showerror(title="Leafpad", message="file not open or may be your data not saved")

        elif len(final_text) != 1 and file_name != "Untitled":
            try:
                with open(os.path.abspath(str(file)), "r") as f:
                    if f.read().strip() == final_text.strip():
                        file = fd.askopenfilename(title="Open a file", filetypes=filetypes)
                        if file:
                            file_name = os.path.basename(str(file))
                            self.title(f'{file_name} - Leafpad')
                            self.text_area.delete('1.0', 'end')
                            with open(os.path.abspath(str(file)), "r") as f1:
                                self.text_area.insert('1.0', f1.read())
                    else:
                        ans = msg.askyesno(title="Leafpad",
                                           message=f'Do you want to save changes to\n {os.path.abspath(str(file))} ?')
                        if ans is True:
                            with open(os.path.abspath(str(file)), "w") as f1:
                                f1.write(final_text.strip())
                        file = fd.askopenfilename(title="Open a file", filetypes=filetypes)
                        if file:
                            file_name = os.path.basename(str(file))
                            self.title(f'{file_name} - Leafpad')
                            self.text_area.delete('1.0', 'end')
                            with open(file, "r") as f1:
                                self.text_area.insert('1.0', f1.read())
            except Exception:
                msg.showerror(title="Leafpad", message="file not open or may be your data not saved.")

    def save_as(self):
        self.save()

    def create_file_bar(self):
        file_menu = Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New", font=SMALL_FONT_STYLE, accelerator="Ctrl+N",
                              command=lambda x="New": self.evaluate_operation(x))
        file_menu.add_command(label="New Window", font=SMALL_FONT_STYLE, accelerator="Ctrl+Shift+N",
                              command=lambda x="New Window": self.evaluate_operation(x), state=DISABLED)
        file_menu.add_command(label="Open", font=SMALL_FONT_STYLE, accelerator="Ctrl+G",
                              command=lambda x="Open": self.evaluate_operation(x))
        file_menu.add_separator()
        file_menu.add_command(label="Save", font=SMALL_FONT_STYLE, accelerator="Ctrl+S",
                              command=lambda x="Save": self.evaluate_operation(x))
        file_menu.add_command(label="Save As", font=SMALL_FONT_STYLE, accelerator="Ctrl+Shift+S",
                              command=lambda x="Save As": self.evaluate_operation(x))
        file_menu.add_separator()
        file_menu.add_command(label="Time/Date", font=SMALL_FONT_STYLE, accelerator="Ctrl+T",
                              command=lambda x="Time/Date": self.evaluate_operation(x))
        file_menu.add_command(label="Exit", font=SMALL_FONT_STYLE, command=lambda x="Exit": self.evaluate_operation(x))
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        return self.menu_bar

    def evaluate_edit_operation(self, value):
        if value == "Undo":
            self.text_area.event_generate("<<Undo>>")
        elif value == "Redo":
            self.text_area.event_generate("<<Redo>>")
        elif value == "Cut":
            self.text_area.event_generate("<<Cut>>")
        elif value == "Copy":
            self.text_area.event_generate("<<Copy>>")
        elif value == "Paste":
            self.text_area.event_generate("<<Paste>>")
        elif value == "Select All":
            self.text_area.tag_add("sel", '1.0', 'end')
            return
        elif value == "Find":
            self.find()
        elif value == "Replace":
            self.replace()

    def replace(self):
        replace_window = Toplevel(self)
        replace_window.iconbitmap("leafpad_icon.ico")
        replace_window.title("Replace")
        replace_window.geometry("550x300")
        replace_window.resizable(False, False)
        find = StringVar()
        replace = StringVar()
        replace_window.columnconfigure(1, weight=1)
        replace_window.focus()

        def replace_word():
            text_area_value = self.text_area.get('1.0', 'end')
            if find.get() in text_area_value:
                final_text = text_area_value.replace(str(find.get()), str(replace.get()), 1)
                self.text_area.delete('1.0', 'end')
                self.text_area.insert('1.0', final_text)

                replace_ans = Label(replace_window, font=("consolas", 15), anchor=W, foreground=YELLOW,
                                    text=f'Successfully replace first occurrence of {find.get()} with {replace.get()}')
                replace_ans.grid(row=3, column=0, columnspan=4, sticky=NSEW)
                replace_ans.config(wraplength=550)

            else:
                replace_ans = Label(replace_window, font=("consolas", 15), anchor=W, foreground="red",
                                    text=f'Oops! their is no occurrence of {find.get()}')
                replace_ans.grid(row=3, column=0, columnspan=4, sticky=NSEW)
                replace_ans.config(wraplength=550)

        def replace_all_word():
            text_area_value = self.text_area.get('1.0', 'end')
            if find.get() in text_area_value:
                final_text = text_area_value.replace(str(find.get()), str(replace.get()))
                self.text_area.delete('1.0', 'end')
                self.text_area.insert('1.0', final_text)

                replace_ans = Label(replace_window, font=("consolas", 15), anchor=W, foreground=YELLOW,
                                    text=f'Successfully replace all occurrence of {find.get()} with {replace.get()}')
                replace_ans.grid(row=3, column=0, columnspan=4, sticky=NSEW)
                replace_ans.config(wraplength=550)

            else:
                replace_ans = Label(replace_window, font=("consolas", 15), anchor=W, foreground="red",
                                    text=f'Oops! their is no occurrence of {find.get()}')
                replace_ans.grid(row=3, column=0, columnspan=4, sticky=NSEW)
                replace_ans.config(wraplength=550)

        find_label = Label(replace_window, text="Find What", font=("consolas", 15), anchor=NW)
        find_label.grid(row=0, column=0, pady=10, padx=5, sticky=NW)

        find_entry = Entry(replace_window, textvariable=find, font=("consolas", 15))
        find_entry.grid(row=0, column=1, columnspan=2, pady=10, ipadx=13, ipady=10, padx=10, sticky=NW)
        find_entry.focus_set()

        replace_label = Label(replace_window, text="Replace with", font=("consolas", 15), anchor=NW)
        replace_label.grid(row=1, column=0, pady=10, padx=5, sticky=NW)

        replace_entry = Entry(replace_window, textvariable=replace, font=("consolas", 15))
        replace_entry.grid(row=1, column=1, columnspan=2, pady=10, ipadx=13, ipady=10, padx=10, sticky=NW)

        replace_button = Button(replace_window, text="Replace", font=("consolas", 15), command=replace_word)
        replace_button.grid(row=2, column=0, pady=10, padx=10, sticky=NSEW)

        replaceall_button = Button(replace_window, text="Replace All", font=("consolas", 15),
                                   command=replace_all_word)
        replaceall_button.grid(row=2, column=1, pady=10, columnspan=1, padx=10, sticky=NSEW)

        cancel_button = Button(replace_window, text="Cancel", font=("consolas", 15),
                               command=replace_window.destroy)
        cancel_button.grid(row=2, column=2, pady=10, padx=10, sticky=NSEW)

    def find(self):
        find_window = Toplevel(self)
        find_window.iconbitmap("leafpad_icon.ico")
        find_window.title("Find")
        find_window.geometry("500x230")
        find_window.resizable(False, False)
        find = StringVar()
        find_window.focus()

        # noinspection PyUnusedLocal
        def click(event):
            self.text_area.tag_config('Found', background='white', foreground='black')

        def find_word():
            idx = 0
            self.text_area.tag_remove("Found", '1.0', END)
            find1 = find.get()
            if find:
                idx = '1.0'  # idx stands for index
            while 1:
                idx = self.text_area.search(find1, idx, nocase=True, stopindex=END)
                if not idx:
                    break
                last_idx = '%s+%dc' % (idx, len(find1))
                self.text_area.tag_add('Found', idx, last_idx)
                idx = last_idx
            self.text_area.tag_config('Found', foreground='white', background='blue')
            self.text_area.bind("<1>", click)

        find_label = Label(find_window, text="Find What", font=("consolas", 15))
        find_label.grid(row=0, column=0, pady=10, padx=5, sticky=NSEW)

        find_entry = Entry(find_window, textvariable=find, font=("consolas", 15))
        find_entry.grid(row=0, column=1, pady=10, ipadx=10, padx=10, ipady=10, sticky=NSEW)
        find_entry.focus()

        find_button = Button(find_window, text="Find", font=("consolas", 15), command=find_word)
        find_button.grid(row=1, column=0, pady=10, padx=20, sticky=NSEW)

        cancel_button = Button(find_window, text="Cancel", font=("consolas", 15), command=find_window.destroy)
        cancel_button.grid(row=1, column=1, pady=10, padx=10, sticky=NSEW)

    def create_edit_bar(self):
        edit = Menu(self.menu_bar, tearoff=False)
        edit.add_command(label="Undo", font=SMALL_FONT_STYLE, accelerator="Ctrl+Z",
                         command=lambda x="Undo": self.evaluate_edit_operation(x))
        edit.add_command(label="Redo", font=SMALL_FONT_STYLE, accelerator="Ctrl+Y",
                         command=lambda x="Redo": self.evaluate_edit_operation(x))
        edit.add_separator()
        edit.add_command(label="Cut", font=SMALL_FONT_STYLE, accelerator="Ctrl+X",
                         command=lambda x="Cut": self.evaluate_edit_operation(x))
        edit.add_command(label="Copy", font=SMALL_FONT_STYLE, accelerator="Ctrl+C",
                         command=lambda x="Copy": self.evaluate_edit_operation(x))
        edit.add_command(label="Paste", font=SMALL_FONT_STYLE, accelerator="Ctrl+V",
                         command=lambda x="Paste": self.evaluate_edit_operation(x))
        edit.add_separator()
        edit.add_command(label="Find", font=SMALL_FONT_STYLE, accelerator="Ctrl+F",
                         command=lambda x="Find": self.evaluate_edit_operation(x))
        edit.add_command(label="Replace", font=SMALL_FONT_STYLE, accelerator="Ctrl+R",
                         command=lambda x="Replace": self.evaluate_edit_operation(x))
        edit.add_command(label="Select All", font=SMALL_FONT_STYLE, accelerator="Ctrl+A",
                         command=lambda x="Select All": self.evaluate_edit_operation(x))
        self.menu_bar.add_cascade(label="Edit", menu=edit)
        return self.menu_bar

    # noinspection PyBroadException
    def change_background(self):
        colors = askcolor(title="Change theme")
        try:
            if colors[1] == "#000000" or colors[1] == "#800000":
                self.text_area.config(fg="white")
                self.text_area.configure(bg=f'{colors[1]}')
            else:
                self.text_area.config(fg="black")
                self.text_area.configure(bg=f'{colors[1]}')
        except Exception:
            self.text_area.config(bg="white")

    def change_font(self):
        font_window = Toplevel(self)
        font_window.iconbitmap("leafpad_icon.ico")
        font_window.title("Find")
        font_window.geometry("650x350")
        font_window.resizable(False, False)
        font_weight_list = ["normal", "bold", "italic", "bold italic"]
        font_size_list = []
        for j in range(15, 50):
            font_size_list.append(str(j))
        font_list = []
        for i in font.families():
            font_list.append(i)

        def apply_font():
            global TEXT_FONT
            font_name = self.font_name.get()
            font_size = self.font_size.get()
            font_weight = self.font_weight.get()
            temp_font = [font_name, int(font_size), font_weight]
            TEXT_FONT = temp_font
            self.text_area.configure(font=TEXT_FONT)
            font_window.destroy()

        font_label = Label(font_window, text="Font:", font=FONT_LABEL, anchor=W)
        font_label.grid(row=0, column=0, sticky=W, pady=10)
        select_font = ttk.Combobox(font_window, textvariable=self.font_name, state="readonly", values=font_list,
                                   font=SELECT_FONT, height=8)
        select_font.grid(row=1, column=0, pady=5, padx=5)
        select_font.set("Consolas")

        font_weight_label = Label(font_window, text="Font Style:", font=FONT_LABEL, anchor=W)
        font_weight_label.grid(row=0, column=1, sticky=W, pady=10)
        select_font_weight = ttk.Combobox(font_window, textvariable=self.font_weight, state="readonly", height=8,
                                          values=font_weight_list, font=SELECT_FONT)
        select_font_weight.grid(row=1, column=1, pady=5, padx=5)
        select_font_weight.set("normal")

        font_size_label = Label(font_window, text="Font Size:", font=FONT_LABEL, anchor=W)
        font_size_label.grid(row=0, column=2, sticky=W, pady=10)
        select_font_size = ttk.Combobox(font_window, textvariable=self.font_size, state="readonly", height=8,
                                        values=font_size_list, font=SELECT_FONT)
        select_font_size.grid(row=1, column=2, pady=5, padx=5)
        select_font_size.set("15")

        apply_button = Button(font_window, text="Apply Changes", font=FONT_LABEL, anchor=S, command=apply_font)
        apply_button.grid(row=2, column=1, sticky=S, pady=150)

        cancel_button = Button(font_window, text="Cancel", font=FONT_LABEL, anchor=S, command=font_window.destroy)
        cancel_button.grid(row=2, column=2, sticky=S, pady=150)

    def normal(self):
        try:
            current_tag = self.text_area.tag_names("sel.first")
            if "normal" in current_tag:
                self.text_area.tag_add("normal", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("normal", "sel.first", "sel.last")
                bold_font = Font(self.text_area, self.text_area.cget("font"))
                bold_font.configure(weight="normal")
                self.text_area.tag_configure("normal", font=bold_font)
        except Exception as e:
            msg.showerror("Exception", str(e))

    def bold(self):
        try:
            current_tag = self.text_area.tag_names("sel.first")
            if "bold" in current_tag:
                self.text_area.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("bold", "sel.first", "sel.last")
                bold_font = Font(self.text_area, self.text_area.cget("font"))
                bold_font.configure(weight="bold")
                self.text_area.tag_configure("bold", font=bold_font)
        except Exception as e:
            msg.showerror("Exception", str(e))

    def italic_msg(self):
        msg.showinfo("Leafpad", message="For italic please press Control-k")

    def italic(self):
        try:
            current_tag = self.text_area.tag_names("sel.first")
            if "italic" in current_tag:
                self.text_area.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("italic", "sel.first", "sel.last")
                italic_font = Font(self.text_area, self.text_area.cget("font"))
                italic_font.configure(slant="italic")
                self.text_area.tag_configure("italic", font=italic_font)
        except Exception as e:
            msg.showerror("Exception", str(e))

    def underline(self):
        try:
            current_tag = self.text_area.tag_names("sel.first")
            if "underline" in current_tag:
                self.text_area.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text_area.tag_add("underline", "sel.first", "sel.last")
                italic_font = Font(self.text_area, self.text_area.cget("font"))
                italic_font.configure(underline=True)
                self.text_area.tag_configure("underline", font=italic_font)
        except Exception as e:
            msg.showerror("Exception", str(e))

    # noinspection PyBroadException
    def font_color(self):
        try:
            colors = askcolor(title="Font Color")
            self.text_area.configure(fg=f'{colors[1]}')
        except Exception:
            self.text_area.config(fg="black")

    def create_theme_bar(self):
        theme = Menu(self.menu_bar, tearoff=False)
        theme.add_command(label="Change Theme", font=SMALL_FONT_STYLE, command=self.change_background)
        theme.add_command(label="Change Font", font=SMALL_FONT_STYLE, command=self.change_font)
        theme.add_command(label="Font Color", font=SMALL_FONT_STYLE, command=self.font_color)
        theme.add_separator()
        theme.add_command(label="Normal", accelerator="Ctrl+L", font=SMALL_FONT_STYLE, command=self.normal)
        theme.add_command(label="Bold", accelerator="Ctrl+B", font=SMALL_FONT_STYLE, command=self.bold)
        theme.add_command(label="Italic", accelerator="Ctrl+K", font=SMALL_FONT_STYLE, command=self.italic)
        theme.add_command(label="Underline", accelerator="Ctrl+U", font=SMALL_FONT_STYLE, command=self.underline)
        self.menu_bar.add_cascade(label="Preference", menu=theme)

    def zoom(self, value):
        global TEXT_FONT
        if value == "Zoom In" or value == "Control+":
            TEXT_FONT[1] += 2
            self.text_area.config(font=TEXT_FONT)
        elif value == "Zoom Out" or value == "Control-":
            TEXT_FONT[1] -= 2
            self.text_area.config(font=TEXT_FONT)
        elif value == "Restore Default Zoom" or value == "Control0":
            TEXT_FONT[1] = 16
            self.text_area.config(font=TEXT_FONT)

    def create_text_zoom(self):
        zoom = Menu(self.menu_bar, tearoff=False)
        zoom.add_command(label="Zoom In", font=SMALL_FONT_STYLE, accelerator="Ctrl+Plus",
                         command=lambda value="Zoom In": self.zoom(value))
        zoom.add_command(label="Zoom Out", font=SMALL_FONT_STYLE, accelerator="Ctrl+Minus",
                         command=lambda value="Zoom Out": self.zoom(value))
        zoom.add_command(label="Restore Default Zoom", font=SMALL_FONT_STYLE, accelerator="Ctrl+0",
                         command=lambda value="Restore Default Zoom": self.zoom(value))
        self.menu_bar.add_cascade(label="View", menu=zoom)

    # noinspection PyBroadException
    def about(self):
        try:
            about_window = Toplevel(self)
            about_window.iconbitmap("leafpad_icon.ico")
            about_window.title("About Leafpad")
            about_window.geometry("650x350")
            about_window.resizable(False, False)
            about_window.focus()
            label_text = "Leafpad is written in Python language using Tkinter library.\nThe name of this text" \
                         "editor is derived from the Linux operating system."

            image = PhotoImage(file='leafpad_image.png')
            image_label = Label(about_window, image=image)
            image_label.grid(row=0, column=0, padx=20, pady=15)

            label1 = Label(about_window, text="Windows Leafpad - Text Editor\nAll Rights Reserved 2022", font=18)
            label1.grid(row=0, column=1, padx=20, pady=10)

            label2 = Label(about_window, text=label_text, font=18, justify=CENTER)
            label2.grid(row=1, column=0, columnspan=4, pady=15)

            label3 = Label(about_window, text="This Text Editor is Developed by Kunal Verma.", font=18, justify=CENTER)
            label3.grid(row=2, column=0, columnspan=3, pady=15, padx=10)

            btn_frame = Frame(about_window, highlightbackground="#1E90FF", bd=0, highlightthickness=3)
            btn = Button(btn_frame, text="OK", command=lambda: about_window.destroy(), font=15, relief=GROOVE)
            btn.grid(ipadx=25, ipady=3)
            btn_frame.grid(row=3, column=0, columnspan=4)

            about_window.mainloop()

        except KeyboardInterrupt:
            return 0

    def create_about(self):
        about = Menu(self.menu_bar, tearoff=False)
        about.add_cascade(label="About Notepad", font=SMALL_FONT_STYLE, command=self.about)
        self.menu_bar.add_cascade(label="About", menu=about)

    def create_text_area(self):
        scroll_y = Scrollbar(self, orient=VERTICAL, width=20)
        scroll_y.grid(row=0, column=1, rowspan=2, sticky=NSEW)
        scroll_x = Scrollbar(self, orient=HORIZONTAL, width=20)
        scroll_x.grid(row=1, column=0, sticky=NSEW)
        text_area = Text(self, width=200, height=42, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
                         wrap="none", font=TEXT_FONT)
        text_area.grid(row=0, column=0, sticky=NSEW)
        text_area.focus()
        text_area.configure(undo=True, maxundo=-1, autoseparators=True)
        scroll_y.config(command=text_area.yview)
        scroll_x.config(command=text_area.xview)
        return text_area

    def create_status_bar(self):
        status_bar = Label(self, text="Leafpad | 100% | Window (CRLF) | UTF-8 ", font=LARGE_FONT_STYLE, anchor=SE)
        status_bar.grid(row=2, column=0, sticky=NSEW)

    def window_resize(self):
        window_resize = ttk.Sizegrip(self)
        window_resize.grid(row=2, column=1, sticky=SW)


if __name__ == '__main__':
    l1 = Leafpad()
    windll.shcore.SetProcessDpiAwareness(1)
    l1.mainloop()
