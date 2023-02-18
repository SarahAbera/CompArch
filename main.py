from tkinter import *
from tkinter import filedialog
from tkinter import font
from compiler import Compiler


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.create_widgets()
        self.create_scrolls()
        self.create_textBoxes()
        self.create_menu()
        self.open_python_name = False
        self.open_mips_name = False

        self.mainloop()

    def create_widgets(self):
        self.title("Python to MIPS")

        nav = Frame(self)
        nav.pack(pady=5)

        self.save1 = Button(
            nav, text="save", command=lambda: self.save_file("python"))
        self.save1.pack(side=LEFT)

        self.save2 = Button(
            nav, text="save", command=lambda: self.save_file("mips"))
        self.save2.pack(side=RIGHT)

        self.main_frame = Frame(self)
        self.main_frame.pack()

    def create_scrolls(self):

        # vertical scrollbar for the text box
        self.text_scroll = Scrollbar(self.main_frame)
        self.text_scroll.pack(side=RIGHT, fill=Y)

        # horizontal scrollbar
        self.hor_scroll = Scrollbar(self.main_frame, orient='horizontal')
        self.hor_scroll.pack(side=BOTTOM, fill=X)

        self.python_frame = Frame(self.main_frame, width=100, height=400)
        self.python_frame.pack(side=LEFT, fill=BOTH, pady=5, padx=5)

        self.mips_frame = Frame(self.main_frame, width=100, height=400)
        self.mips_frame.pack(side=RIGHT, fill=BOTH, padx=5, pady=5)

    def create_textBoxes(self):
        # Create Text Box
        self.python_text = Text(self.python_frame,
                                width=60,
                                height=30,
                                font=("Helvetica", 12),
                                selectbackground="#3195f8",
                                selectforeground="white",
                                undo=True,
                                yscrollcommand=self.text_scroll.set,
                                xscrollcommand=self.hor_scroll.set,
                                wrap="none")

        self.mips_text = Text(self.mips_frame,
                              width=60,
                              height=30,
                              font=("Helvetica", 12),
                              selectbackground="#3195f8",
                              selectforeground="black",
                              undo=True,
                              yscrollcommand=self.text_scroll.set,
                              xscrollcommand=self.hor_scroll.set,
                              wrap="none")

        self.python_text.pack(padx=5)
        self.mips_text.pack(padx=5)

        # Configure Scrollbars
        self.text_scroll.config(command=self.mips_text.yview)
        self.hor_scroll.config(command=self.mips_text.xview)

        # Add Status Bar TO Bottom Of App
        self.status_bar = Label(self, text='Ready            ', anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=15)

    def create_menu(self):
        # Create Menu
        python_menu = Menu(self.python_frame)
        self.config(menu=python_menu)

        # Add File Menu
        python_menu.add_command(label='Open', command=self.open_file)
        python_menu.add_command(label='New', command=self.new_file)
        python_menu.add_command(label='Convert To MIPS',
                                command=self.convert_to_mips)

        # Create Menu
        mips_menu = Menu(self.mips_frame)
        # self.config(menu=mips_menu)

        # Add File Menu
        mips_menu.add_command(label='New', command=self.new_file)
        mips_menu.add_command(label='Save', command=self.save_file)

    def save_file(self, message):
        if message == 'python':
            if self.open_python_name:
                # save the file
                text_file = open(self.open_python_name, 'w')
                text_file.write(self.python_text.get(1.0, END))
                name = self.open_python_name
                name = name.replace("C:/Users/hp/Desktop/comparcGUI/", "")
                self.status_bar.config(text=f'Saved: {name}         ')
            else:
                self.save_as_file(message)
        elif message == 'mips':
            if self.open_mips_name:
                # save the file
                text_file = open(self.open_python_name, 'w')
                text_file.write(self.mips_text.get(1.0, END))
                name = self.open_mips_name
                name = name.replace("C:/Users/hp/Desktop/comparcGUI/", "")
                self.status_bar.config(text=f'Saved: {name}         ')
                text_file.close()
            else:
                self.save_as_file(message)
        # close

    def convert_to_mips(self):
        python_source_code = self.python_text.get(1.0, END)

        try:
            mips_code = Compiler(python_source_code).compile()
            self.mips_text.delete("1.0", END)
            self.mips_text.insert(END, mips_code)

            if self.open_python_name:
                self.status_bar.config(
                    text=f'Compiled: {self.open_python_name}         ')
            else:
                self.status_bar.config(text=f'Compiled!         ')
        except Exception as e:
            self.status_bar.config(text=f'Compilation failed: {e}         ')

    def save_as_file(self, message):
        text_file = filedialog.asksaveasfilename(defaultextension=".*",
                                                 initialdir="C:/Users/hp/Desktop/comparcGUI",
                                                 title="Save File",
                                                 filetypes=(("All Files", "*.*"), ("Python File", "*.py"), ("Assembly Files", "*.asm")))
        if text_file:
            # update status bars
            name = text_file
            name = name.replace("C:/Users/hp/Desktop/comparcGUI/", "")
            self.status_bar.config(text=f'Saved: {name}         ')

            if message == 'python':
                # save the file
                text_file = open(text_file, 'w')
                text_file.write(self.python_text.get(1.0, END))
            elif message == 'mips':
                # save the file
                text_file = open(text_file, 'w')
                text_file.write(self.mips_text.get(1.0, END))
            # close
            text_file.close()

    def open_file(self):
        # grab filename
        text_file = filedialog.askopenfilename(
            initialdir="C:/Users/hp/Desktop/comparcGUI",
            title="Open File",
            filetypes=(("All Files", "*.*"), ("Python Files", "*.py"), ("Assembly Files", "*.asm")))
        # check to see file name
        if text_file:
            # make file name global
            self.open_python_name = text_file

        # update status bar
        name = text_file
        name = name.replace("C:/Users/hp/Desktop/comparcGUI/", "")
        self.status_bar.config(text=f'Opened: {name}         ')
        self.title(f"{name} - Python to MIPS!")

        # open the file
        try:
            with open(text_file, 'r') as text_file:
                body = text_file.read()
                self.python_text.delete("1.0", END)
                self.python_text.insert(END, body)
        except:
            pass

    def new_file(self):
        # delete previous text
        self.python_text.delete("1.0", END)
        # update status bar
        self.status_bar.config(text="New File            ")

        self.open_python_name = False


if __name__ == "__main__":
    Application()
