import tkinter as tk
from tkinter import messagebox
import random
from HMGraphics import HangingMan

MAX_ERRORS = 8

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎩 Hangman Game")
        self.root.geometry("600x650")
        self.root.configure(bg="#f5f5f5")

        self.word = ""
        self.correct = ""
        self.wrong = ""
        self.errors = 0
        self.hint_used = False
        self.games_played = 0
        self.games_won = 0

        # ----- Top Title -----
        self.label_title = tk.Label(root, text="Hangman", font=("Helvetica", 24, "bold"), bg="#f5f5f5", fg="#333")
        self.label_title.pack(pady=20)

        # ----- Difficulty Buttons -----
        self.frame_diff = tk.Frame(root, bg="#f5f5f5")
        self.label_diff = tk.Label(self.frame_diff, text="Select Difficulty:", font=("Arial", 12), bg="#f5f5f5")
        self.label_diff.pack(side=tk.LEFT, padx=10)

        for i, label in enumerate(["Simple", "Easy", "Medium", "Hard", "Very Hard"], start=1):
            tk.Button(self.frame_diff, text=label, command=lambda d=i: self.start_game(d),
                      bg="#4CAF50", fg="white", font=("Arial", 10), padx=5, pady=2).pack(side=tk.LEFT, padx=5)

        self.frame_diff.pack(pady=10)

        # ----- Game Frame -----
        self.frame_game = tk.Frame(root, bg="#f5f5f5")

        self.label_word = tk.Label(self.frame_game, font=("Courier", 24), bg="#f5f5f5", fg="#000")
        self.label_word.pack(pady=10)

        self.text_hangman = tk.Text(self.frame_game, height=8, width=20, font=("Courier", 14),
                                    bg="#fff3e0", fg="#d32f2f", borderwidth=0)
        self.text_hangman.pack(pady=5)
        self.text_hangman.config(state=tk.DISABLED)

        self.label_wrong = tk.Label(self.frame_game, text="Wrong Letters:", font=("Arial", 12), bg="#f5f5f5", fg="#444")
        self.label_wrong.pack()

        self.label_status = tk.Label(self.frame_game, text="", font=("Arial", 11), bg="#f5f5f5", fg="#00796B")
        self.label_status.pack(pady=5)

        self.label_lives = tk.Label(self.frame_game, text="Lives: 8", font=("Arial", 11), bg="#f5f5f5", fg="#333")
        self.label_lives.pack()

        self.entry_guess = tk.Entry(self.frame_game, font=("Arial", 14), justify="center")
        self.entry_guess.pack(pady=5)

        self.frame_buttons = tk.Frame(self.frame_game, bg="#f5f5f5")
        self.button_submit = tk.Button(self.frame_buttons, text="Guess", command=self.make_guess,
                                       bg="#2196F3", fg="white", font=("Arial", 10), padx=10)
        self.button_hint = tk.Button(self.frame_buttons, text="Hint (-1 life)", command=self.use_hint,
                                     bg="#FF9800", fg="white", font=("Arial", 10), padx=10)
        self.button_submit.pack(side=tk.LEFT, padx=5)
        self.button_hint.pack(side=tk.LEFT, padx=5)
        self.frame_buttons.pack()

        # ----- Stats -----
        self.label_stats = tk.Label(root, text="Wins: 0 | Played: 0", font=("Arial", 10), bg="#f5f5f5", fg="#555")
        self.label_stats.pack(pady=10)

    def load_words(self, difficulty):
        with open("dictionary-large.txt") as file:
            words = file.read().strip().split()

        if difficulty == 1:
            return [w for w in words if len(w) == 4]
        elif difficulty == 2:
            return [w for w in words if 5 <= len(w) <= 6]
        elif difficulty == 3:
            return [w for w in words if 7 <= len(w) <= 8]
        elif difficulty == 4:
            return [w for w in words if 9 <= len(w) <= 10]
        else:
            return [w for w in words if len(w) >= 11]

    def start_game(self, difficulty):
        self.word = random.choice(self.load_words(difficulty)).lower()
        self.correct = ""
        self.wrong = ""
        self.errors = 0
        self.hint_used = False
        self.label_status.config(text="")
        self.entry_guess.delete(0, tk.END)

        self.frame_diff.pack_forget()
        self.frame_game.pack(pady=10)
        self.update_display()
        self.enable_game_controls()

    def update_display(self):
        display_word = " ".join([c if c in self.correct else "_" for c in self.word])
        self.label_word.config(text=display_word)

        self.label_wrong.config(text="Wrong Letters: " + " ".join(self.wrong))
        self.label_lives.config(text=f"Lives: {MAX_ERRORS - self.errors}")
        self.text_hangman.config(state=tk.NORMAL)
        self.text_hangman.delete("1.0", tk.END)
        self.text_hangman.insert(tk.END, HangingMan[self.errors])
        self.text_hangman.config(state=tk.DISABLED)

        if "_" not in display_word:
            self.end_game(True)

    def make_guess(self):
        guess = self.entry_guess.get().strip().lower()
        self.entry_guess.delete(0, tk.END)

        if not guess.isalpha():
            self.label_status.config(text="Only letters allowed.")
            return

        if len(guess) == 1:
            if guess in self.correct or guess in self.wrong:
                self.label_status.config(text="Letter already guessed.")
                return
            if guess in self.word:
                self.correct += guess
                self.label_status.config(text=f"✅ '{guess}' is correct!")
            else:
                self.wrong += guess
                self.errors += 1
                self.label_status.config(text=f"❌ '{guess}' is not in the word.")
        else:
            if guess == self.word:
                self.correct = self.word
                self.label_status.config(text=f"🎉 You guessed the word!")
                self.update_display()
                return
            else:
                self.errors = MAX_ERRORS
                self.label_status.config(text=f"❌ Incorrect full word guess.")

        if self.errors >= MAX_ERRORS:
            self.end_game(False)
        else:
            self.update_display()

    def use_hint(self):
        if self.hint_used:
            self.label_status.config(text="Hint already used.")
            return

        remaining = [c for c in self.word if c not in self.correct]
        if remaining:
            hint_letter = random.choice(remaining)
            self.correct += hint_letter
            self.errors += 1
            self.hint_used = True
            self.label_status.config(text=f"Hint revealed: '{hint_letter}'")
            self.update_display()
        else:
            self.label_status.config(text="No more letters to reveal.")

    def end_game(self, win):
        self.games_played += 1
        if win:
            self.games_won += 1
            messagebox.showinfo("🎉 You Win!", f"You guessed the word: {self.word}")
        else:
            messagebox.showinfo("💀 Game Over", f"You were hanged!\nThe word was: {self.word}")

        self.update_stats()
        self.disable_game_controls()
        self.ask_replay()

    def update_stats(self):
        self.label_stats.config(text=f"Wins: {self.games_won} | Played: {self.games_played}")

    def ask_replay(self):
        if messagebox.askyesno("Play Again?", "Do you want to play again?"):
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.label_word.config(text="")
        self.label_wrong.config(text="")
        self.label_status.config(text="")
        self.label_lives.config(text="Lives: 8")
        self.text_hangman.config(state=tk.NORMAL)
        self.text_hangman.delete("1.0", tk.END)
        self.text_hangman.config(state=tk.DISABLED)
        self.entry_guess.delete(0, tk.END)
        self.frame_game.pack_forget()
        self.frame_diff.pack()

    def disable_game_controls(self):
        self.entry_guess.config(state=tk.DISABLED)
        self.button_submit.config(state=tk.DISABLED)
        self.button_hint.config(state=tk.DISABLED)

    def enable_game_controls(self):
        self.entry_guess.config(state=tk.NORMAL)
        self.button_submit.config(state=tk.NORMAL)
        self.button_hint.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
