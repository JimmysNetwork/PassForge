import sys
import os
import random
import string
import pyperclip
import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import base64
from ttkbootstrap.constants import BOTH, W, X, Y, LEFT, RIGHT, VERTICAL, PRIMARY, SUCCESS, INFO

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PassForge")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        self.set_window_icon()
        self.center_window(700, 800)

        self.password_history = []

        frame = ttk.Frame(root, padding=(20, 60, 20, 20))
        frame.pack(expand=True, fill=BOTH)

        # About Button
        self.about_button = ttk.Button(root, text="About", bootstyle=INFO, width=6, command=self.show_about)
        self.about_button.place(x=630, y=6)

        # Password Length
        ttk.Label(frame, text="Password Length:").pack(anchor=W)
        self.length_entry = ttk.Entry(frame, bootstyle=PRIMARY)
        self.length_entry.pack(fill=X, pady=(0, 10))

        # Batch Size
        ttk.Label(frame, text="How Many Passwords:").pack(anchor=W)
        self.batch_entry = ttk.Entry(frame, bootstyle=PRIMARY)
        self.batch_entry.insert(0, "1")
        self.batch_entry.pack(fill=X, pady=(0, 10))

        # Options
        self.include_uppercase = ttk.BooleanVar(value=True)
        self.include_numbers = ttk.BooleanVar(value=True)
        self.include_symbols = ttk.BooleanVar(value=True)

        ttk.Checkbutton(frame, text="Include Uppercase Letters", variable=self.include_uppercase).pack(anchor=W)
        ttk.Checkbutton(frame, text="Include Numbers", variable=self.include_numbers).pack(anchor=W)
        ttk.Checkbutton(frame, text="Include Symbols", variable=self.include_symbols).pack(anchor=W)

        # Generate Button
        self.generate_button = ttk.Button(frame, text="Generate Password(s)", bootstyle=SUCCESS, command=self.generate_password)
        self.generate_button.pack(pady=15, fill=X)

        # Output Password
        self.password_output = ttk.Entry(frame, font=('Helvetica', 14), justify='center')
        self.password_output.pack(fill=X, pady=(0, 10))

        # Password Strength Label
        self.strength_label = ttk.Label(frame, text="", font=('Helvetica', 12, 'bold'))
        self.strength_label.pack(pady=(0, 10))

        self.passwords_created_label = ttk.Label(frame, text="", font=('Helvetica', 10))
        self.passwords_created_label.pack(pady=(0, 10))

        # Copy Button
        self.copy_button = ttk.Button(frame, text="Copy to Clipboard", bootstyle=INFO, command=self.copy_to_clipboard)
        self.copy_button.pack(fill=X, pady=(0, 10))

        # Export Button
        self.export_button = ttk.Button(frame, text="Export Passwords", bootstyle=PRIMARY, command=self.export_passwords)
        self.export_button.pack(fill=X, pady=(0, 20))

        # Load Button (NEW)
        self.load_button = ttk.Button(frame, text="Load Passwords", bootstyle=PRIMARY, command=self.load_passwords)
        self.load_button.pack(fill=X, pady=(0, 20))

        # Password History Header
        history_header = ttk.Frame(frame)
        history_header.pack(fill=X, pady=(10, 0))

        ttk.Label(history_header, text="Password History:", font=('Helvetica', 12, 'bold')).pack(side=LEFT)

        self.clear_history_btn = ttk.Button(history_header, text="Clear", bootstyle="danger-outline", width=6, command=self.clear_history)
        self.clear_history_btn.pack(side=RIGHT, padx=(0, 5))

        # History Scrollable Area
        history_container = ttk.Frame(frame)
        history_container.pack(fill=BOTH, expand=True, pady=(0, 10))

        self.history_canvas = ttk.Canvas(history_container, background="white")
        self.history_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(history_container, orient=VERTICAL, command=self.history_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.scrollable_history_frame = ttk.Frame(self.history_canvas)
        self.history_canvas.create_window((0, 0), window=self.scrollable_history_frame, anchor="nw")

        self.history_canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_history_frame.bind("<Configure>", self.on_history_frame_configure)
        self.history_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def center_child_window(self, window, width, height):
        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def set_window_icon(self):
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "passforge.ico")
        else:
            icon_path = "passforge.ico"
        self.root.iconbitmap(icon_path)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            batch_size = int(self.batch_entry.get())
            if length <= 0 or batch_size <= 0:
                raise ValueError
            if length > 128:
                messagebox.showwarning(title="Warning", message="Maximum allowed length is 128 characters. Password(s) will be generated with 128 characters.")
                length = 128
        except ValueError:
            messagebox.showerror(title="Error", message="Please enter valid positive numbers.")
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

        passwords = [''.join(random.choice(chars) for _ in range(length)) for _ in range(batch_size)]

        self.password_output.delete(0, ttk.END)
        self.password_output.insert(0, passwords[0])

        self.update_strength_label(passwords[0])

        self.password_history.extend(passwords)
        self.update_history_display()

        self.passwords_created_label.config(
            text=f"✅ {batch_size} Password{'s' if batch_size > 1 else ''} Created!"
        )

    def update_strength_label(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)

        score = sum([has_upper, has_lower, has_digit, has_symbol])

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

    def update_history_display(self):
        for widget in self.scrollable_history_frame.winfo_children():
            widget.destroy()

        for pw in reversed(self.password_history):
            pw_frame = ttk.Frame(self.scrollable_history_frame)
            pw_frame.pack(fill=X, pady=2)

            pw_label = ttk.Label(pw_frame, text=pw, font=("Courier", 10), anchor="w")
            pw_label.pack(side=LEFT, expand=True)

            copy_btn = ttk.Button(pw_frame, text="Copy", width=6, command=lambda p=pw: self.copy_specific_password(p))
            copy_btn.pack(side=RIGHT)

        self.history_canvas.update_idletasks()
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))

    def on_history_frame_configure(self, event):
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.history_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def clear_history(self):
        self.password_history.clear()
        self.update_history_display()
        messagebox.showinfo("Cleared", "Password history cleared!")

    def copy_specific_password(self, password):
        pyperclip.copy(password)
        messagebox.showinfo(title="Copied!", message="Password copied to clipboard!")

    def export_passwords(self):
        if not self.password_history:
            messagebox.showerror(title="Error", message="No passwords to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".passforge", filetypes=[("PassForge Files", "*.passforge")], title="Save Passwords")

        if file_path:
            passwords_joined = '\n'.join(self.password_history)
            encoded = base64.b64encode(passwords_joined.encode('utf-8'))
            with open(file_path, 'wb') as f:
                f.write(encoded)
            messagebox.showinfo(title="Exported", message="Passwords exported successfully!")
            self.clear_history()

    
    def load_passwords(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".passforge",
            filetypes=[("PassForge Files", "*.passforge")],
            title="Load Passwords"
        )

        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    encoded = f.read()

                decoded = base64.b64decode(encoded).decode('utf-8')
                passwords = decoded.split('\n')

                # Extend the history
                self.password_history.extend(passwords)
                self.update_history_display()

                messagebox.showinfo("Loaded", "Passwords loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load passwords.\n\n{str(e)}")

    def show_about(self):
        about_window = ttk.Toplevel(self.root)
        about_window.title("About PassForge")
        about_window.geometry("350x200")
        about_window.resizable(False, False)

        frame = ttk.Frame(about_window, padding=20)
        frame.pack(expand=True, fill=BOTH)

        ttk.Label(frame, text="PassForge", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="A simple, secure password generator.\nBuilt with Python and ttkbootstrap.", justify="center").pack(pady=(0, 10))
        ttk.Label(frame, text="Version: 1.5.0", justify="center").pack(pady=(0, 10))
        github_link = ttk.Label(frame, text="View on GitHub", foreground="blue", cursor="hand2")
        github_link.pack()
        github_link.bind("<Button-1>", lambda e: self.open_github())

        self.center_child_window(about_window, 350, 200)

    def open_github(self):
        import webbrowser
        webbrowser.open_new("https://github.com/jimmysnetwork/passforge")

if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    PasswordGeneratorApp(app)
    app.mainloop()
