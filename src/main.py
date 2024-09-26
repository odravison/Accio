import os
import sys
import tkinter as tk
from screeninfo import get_monitors
import pyperclip
import keyboard


if os.geteuid() != 0:
    print("This script must be run as root!")
    sys.exit(1)

class ClipboardManager:
    def __init__(self, root):
        self.root = root
        self.clipboard_history = []
        self.max_history = 10

        self.root.title("Clipboard Manager")
        self.root.withdraw()  # Start with the window hidden
        self.root.attributes('-topmost', True)

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-1>', self.on_select)

        self.root.bind('<Escape>', self.close_window)

        # Set up the hotkey
        self.default_hotkey = 'win+shift+d'
        keyboard.add_hotkey(self.default_hotkey, self.show_window)

        # Monitor clipboard changes
        self.root.after(1000, self.check_clipboard)

    def close_window(self, event=None):
        self.root.withdraw()

    def get_current_monitor(self):
        mouse_x, mouse_y = self.root.winfo_pointerxy()
        for monitor in get_monitors():
            if monitor.x <= mouse_x < monitor.x + monitor.width and monitor.y <= mouse_y < monitor.y + monitor.height:
                return monitor
        return None

    def show_window(self):
        current_monitor = self.get_current_monitor()
        if current_monitor:
            screen_width = current_monitor.width
            screen_height = current_monitor.height
        else:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

        min_height = screen_height // 4
        min_width = 200

        self.root.geometry(f"{min_width}x{min_height}")
        self.root.deiconify()

    def check_clipboard(self):
        current_clipboard = pyperclip.paste()
        if current_clipboard and (not self.clipboard_history or current_clipboard != self.clipboard_history[0]):
            self.clipboard_history.insert(0, current_clipboard)
            if len(self.clipboard_history) > self.max_history:
                self.clipboard_history.pop()
            self.update_listbox()
        self.root.after(1000, self.check_clipboard)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.clipboard_history:
            self.listbox.insert(tk.END, item)

    def on_select(self, event):
        selected_text = self.listbox.get(self.listbox.curselection())
        pyperclip.copy(selected_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardManager(root)
    root.mainloop()