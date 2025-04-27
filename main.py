import sys
import os
import random
import string
import pyperclip
import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
from ttkbootstrap.constants import BOTH, W, X, PRIMARY, SUCCESS, INFO

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PassForge")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.set_window_icon()
        self.center_window(400,500)

        # Frame
        frame = ttk.Frame(root, padding=(20, 60, 20, 20))  # (left, top, right, bottom)
        frame.pack(expand=True, fill=BOTH)

        # About Buttonpy 
        self.about_button = ttk.Button(root, text="About", bootstyle=INFO, width=6, command=self.show_about)
        self.about_button.place(x=330, y=10)

        # Password Length
        ttk.Label(frame, text="Password Length:").pack(anchor=W)
        self.length_entry = ttk.Entry(frame, bootstyle=PRIMARY)
        self.length_entry.pack(fill=X, pady=(0, 10))

        # Options
        self.include_uppercase = ttk.BooleanVar(value=True)
        self.include_numbers = ttk.BooleanVar(value=True)
        self.include_symbols = ttk.BooleanVar(value=True)

        ttk.Checkbutton(frame, text="Include Uppercase Letters", variable=self.include_uppercase).pack(anchor=W)
        ttk.Checkbutton(frame, text="Include Numbers", variable=self.include_numbers).pack(anchor=W)
        ttk.Checkbutton(frame, text="Include Symbols", variable=self.include_symbols).pack(anchor=W)

        # Generate Button
        self.generate_button = ttk.Button(frame, text="Generate Password", bootstyle=SUCCESS, command=self.generate_password)
        self.generate_button.pack(pady=15, fill=X)

        # Output Password
        self.password_output = ttk.Entry(frame, font=('Helvetica', 14), justify='center')
        self.password_output.pack(fill=X, pady=(0, 10))

        # Password Strength Label
        self.strength_label = ttk.Label(frame, text="", font=('Helvetica', 12, 'bold'))
        self.strength_label.pack(pady=(0, 10))

        # Copy Button
        self.copy_button = ttk.Button(frame, text="Copy to Clipboard", bootstyle=INFO, command=self.copy_to_clipboard)
        self.copy_button.pack(fill=X)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_window_icon(self):
        if getattr(sys, 'frozen', False):
            # If running as .exe
            icon_path = os.path.join(sys._MEIPASS, "passforge.ico")
        else:
            # If running from .py file
            icon_path = "passforge.ico"
        self.root.iconbitmap(icon_path)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length <= 0:
                raise ValueError
            if length > 128:
                messagebox.showwarning(
                    title="Warning",
                    message="Maximum allowed length is 128 characters.\nPassword will be generated with 128 characters."
                )
                length = 128
        except ValueError:
            messagebox.showerror(title="Error", message="Please enter a valid positive number.")
            return

        chars = string.ascii_lowercase
        if self.include_uppercase.get():
            chars += string.ascii_uppercase
        if self.include_numbers.get():
            chars += string.digits
        if self.include_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror(title="Error", message="Please select at least one character type.")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_output.delete(0, ttk.END)
        self.password_output.insert(0, password)

        # Analyze strength
        self.update_strength_label(password)

    def update_strength_label(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        score = sum([has_upper, has_lower, has_digit, has_symbol])

        # Simple Scoring
        if length < 6 or score <= 2:
            self.strength_label.config(text="Weak", foreground="red")
        elif length >= 6 and score == 3:
            self.strength_label.config(text="Medium", foreground="orange")
        else:
            self.strength_label.config(text="Strong", foreground="green")

    def copy_to_clipboard(self):
        password = self.password_output.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo(title="Copied!", message="Password copied to clipboard!")

    def show_about(self):
        about_window = ttk.Toplevel(self.root)
        about_window.title("About PassForge")
        about_window.geometry("350x200")
        about_window.resizable(False, False)

        frame = ttk.Frame(about_window, padding=20)
        frame.pack(expand=True, fill=BOTH)

        ttk.Label(frame, text="PassForge", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="A simple, secure password generator.\nBuilt with Python and ttkbootstrap.", justify="center").pack(pady=(0, 10))
        ttk.Label(frame, text="Version: 1.0.0", justify="center").pack(pady=(0, 10))
        github_link = ttk.Label(frame, text="View on GitHub", foreground="blue", cursor="hand2")
        github_link.pack()
        github_link.bind("<Button-1>", lambda e: self.open_github())

    def open_github(self):
        import webbrowser
        webbrowser.open_new("https://github.com/jimmysnetwork/passforge")

if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    PasswordGeneratorApp(app)
    app.mainloop()
