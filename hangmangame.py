import tkinter as tk
import random

class HangmanGame:
    def _init_(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f8ff")

        
        self.word_list = {
            "python": "A popular programming language.",
            "hangman": "The name of this game!",
            "jupyter": "An open-source web application for interactive computing.",
            "notebook": "A type of computer program or physical book.",
            "computer": "An electronic device for storing and processing data.",
            "programming": "The process of writing computer programs.",
            "algorithm": "A set of rules to be followed in calculations.",
            "developer": "A person who develops computer software.",
            "keyboard": "A panel of keys that operates a computer or typewriter.",
            "tkinter": "The standard Python interface to the Tk GUI toolkit.",
            "machine": "Short for 'Machine Learning'.",
            "learning": "The process of acquiring knowledge.",
            "artificial": "Opposite of 'natural'; used in AI context.",
            "intelligence": "Ability to acquire and apply knowledge; used in AI.",
            "data": "Facts and statistics collected together for reference or analysis.",
            "network": "A system of interconnected things, often computers.",
            "neural": "Relating to the structure of the brain or neural networks.",
            "training": "The process of teaching a model in machine learning.",
            "dataset": "A collection of data used for analysis or training models.",
            "model": "A system or mathematical structure used to make predictions."
        }

        self.word, self.hint = self.get_word()
        self.word_letters = set(self.word)
        self.used_letters = set()
        self.lives = 3

        self.create_widgets()
        self.update_display()

    def get_word(self):
        word, hint = random.choice(list(self.word_list.items()))
        return word, hint

    def create_widgets(self):
        # Main title
        self.title_label = tk.Label(self.master, text="Hangman Game", font=("Helvetica", 32, "bold"), bg="#f0f8ff", fg="#333333")
        self.title_label.pack(pady=10)

        self.question_label = tk.Label(self.master, text=f"Question: {self.hint}", font=("Helvetica", 16, "italic"), bg="#f0f8ff", fg="#8e44ad")
        self.question_label.pack(pady=5)

        
        self.word_label = tk.Label(self.master, text="", font=("Courier", 24, "bold"), bg="#f0f8ff", fg="#005f99")
        self.word_label.pack(pady=10)

        
        self.lives_label = tk.Label(self.master, text="", font=("Helvetica", 16), bg="#f0f8ff", fg="#e74c3c")
        self.lives_label.pack(pady=5)

        
        self.used_letters_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="#f0f8ff", fg="#7f8c8d")
        self.used_letters_label.pack(pady=5)

        
        self.status_label = tk.Label(self.master, text="", font=("Helvetica", 14, "italic"), bg="#f0f8ff", fg="#2980b9")
        self.status_label.pack(pady=5)

        
        self.guess_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.guess_frame.pack(pady=20)

        self.guess_entry = tk.Entry(self.guess_frame, font=("Helvetica", 16), width=5, justify='center')
        self.guess_entry.pack(side=tk.LEFT, padx=10)
        self.guess_entry.bind("<Return>", self.check_guess_event)

        self.guess_button = tk.Button(self.guess_frame, text="Guess", font=("Helvetica", 14, "bold"),
                                      command=self.check_guess, bg="#2ecc71", fg="white", activebackground="#27ae60")
        self.guess_button.pack(side=tk.LEFT, padx=5)

       
        self.hint_button = tk.Button(self.master, text="Reveal a Letter (-1 life)", font=("Helvetica", 12),
                                     command=self.reveal_letter, bg="#3498db", fg="white", activebackground="#2980b9")
        self.hint_button.pack(pady=5)

    def update_display(self):
        word_list = [letter if letter in self.used_letters else '_' for letter in self.word]
        self.word_label.config(text=" ".join(word_list))
        self.lives_label.config(text=f"Lives Left: {self.lives} ❤")
        self.used_letters_label.config(text=f"Used Letters: {' '.join(sorted(list(self.used_letters)))}")
        self.guess_entry.delete(0, tk.END)

    def check_guess_event(self, event):
        self.check_guess()

    def check_guess(self):
        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            self.status_label.config(text="Please enter a single letter.")
            return

        if guess in self.used_letters:
            self.status_label.config(text=f"You've already tried '{guess}'.")
            return

        self.used_letters.add(guess)

        if guess in self.word_letters:
            self.word_letters.remove(guess)
            self.status_label.config(text=f"Good guess! '{guess}' is in the word.")
        else:
            self.lives -= 1
            self.status_label.config(text=f"Wrong guess! '{guess}' is not in the word.")

        self.update_display()
        self.check_game_over()

    def reveal_letter(self):
        if self.lives > 1 and len(self.word_letters) > 0:
            revealed = random.choice(list(self.word_letters))
            self.used_letters.add(revealed)
            self.word_letters.remove(revealed)
            self.lives -= 1
            self.status_label.config(text=f"A letter was revealed: '{revealed}'")
            self.update_display()
            self.check_game_over()
        else:
            self.status_label.config(text="No more lives to reveal a letter!")

    def check_game_over(self):
        if len(self.word_letters) == 0:
            self.show_center_popup(f"🎉 Congratulations! You cracked the hint! The word was: {self.word.upper()}")
            self.disable_game()
        elif self.lives == 0:
            self.show_center_popup(f"💀 Game Over! The word was: {self.word.upper()}")
            self.disable_game()

    def disable_game(self):
        self.guess_entry.config(state='disabled')
        self.guess_button.config(state='disabled')
        self.hint_button.config(state='disabled')

    def show_center_popup(self, message):
        popup = tk.Toplevel(self.master)
        popup.withdraw()  # Hide initially to avoid flicker
        popup.title("Result")
        popup.configure(bg="#f0f8ff")
        popup.resizable(False, False)

        width, height = 400, 200
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        popup.deiconify()  # Show popup after setup

        popup.grab_set()   # Modal behavior
        popup.focus_set()

        label = tk.Label(popup, text=message, font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333333", wraplength=350)
        label.pack(pady=40)

        tk.Button(popup, text="OK", command=popup.destroy, font=("Helvetica", 12, "bold"),
                  bg="#2ecc71", fg="white").pack(pady=10)

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main() 