import tkinter as tk
import random
from functools import partial
from tkinter import messagebox
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match Game")
        self.root.geometry("480x540")
        self.root.resizable(False, False)

        self.buttons = []
        self.first = None
        self.second = None
        self.matches = 0
        self.game_started = False
        self.start_time = None

        self.symbols = ['♠', '♥', '♦', '♣', '★', '☀']

        # Timer label
        self.timer_label = tk.Label(root, text="Time: 0.0 sec", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        # Frame for cards
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Start and Retry buttons frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Game", font=("Arial", 12), command=self.start_game)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.retry_btn = tk.Button(btn_frame, text="Retry", font=("Arial", 12), command=self.retry_game, state="disabled")
        self.retry_btn.grid(row=0, column=1, padx=10)

        # Create buttons but disable until start
        self.create_buttons()
        self.disable_all_buttons()

    def create_buttons(self):
        self.buttons.clear()
        self.values = []
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        items = self.symbols * 2
        random.shuffle(items)
        self.values = items

        for i in range(4):
            row = []
            for j in range(3):
                idx = i * 3 + j
                btn = tk.Button(self.frame, text="?", font=("Arial", 24), width=4, height=2,
                                command=partial(self.reveal, idx), bg="SystemButtonFace")
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def enable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="normal", text="?")

    def start_game(self):
        if self.game_started:
            return
        self.game_started = True
        self.start_btn.config(state="disabled")
        self.retry_btn.config(state="normal")
        self.matches = 0
        self.first = None
        self.second = None
        self.create_buttons()
        self.enable_all_buttons()
        self.start_time = time.time()
        self.update_timer()

    def retry_game(self):
        self.game_started = False
        self.start_btn.config(state="normal")
        self.retry_btn.config(state="disabled")
        self.timer_label.config(text="Time: 0.0 sec")
        self.disable_all_buttons()
        self.first = None
        self.second = None
        self.matches = 0

    def update_timer(self):
        if self.game_started:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed:.1f} sec")
            self.root.after(100, self.update_timer)

    def reveal(self, idx):
        if not self.game_started:
            return
        i, j = divmod(idx, 3)
        btn = self.buttons[i][j]

        # Animation effect: change color briefly
        btn.config(bg="lightblue")

        btn.config(text=self.values[idx], state="disabled")

        if self.first is None:
            self.first = (idx, btn)
        elif self.second is None:
            self.second = (idx, btn)
            self.root.after(600, self.check_match)

    def check_match(self):
        idx1, btn1 = self.first
        idx2, btn2 = self.second

        if self.values[idx1] == self.values[idx2]:
            self.matches += 1
            btn1.config(bg="lightgreen")
            btn2.config(bg="lightgreen")
            if self.matches == 6:
                self.game_started = False
                elapsed = time.time() - self.start_time
                self.timer_label.config(text=f"Time: {elapsed:.1f} sec")
                msg = f"Great! You matched all pairs in {elapsed:.1f} seconds."
                if elapsed < 20:
                    msg += "\nExcellent memory!"
                elif elapsed < 40:
                    msg += "\nGood job!"
                else:
                    msg += "\nKeep practicing!"
                messagebox.showinfo("Congratulations!", msg)
                self.disable_all_buttons()
                self.retry_btn.config(state="normal")
        else:
            btn1.config(text="?", state="normal", bg="SystemButtonFace")
            btn2.config(text="?", state="normal", bg="SystemButtonFace")

        self.first = None
        self.second = None
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()





