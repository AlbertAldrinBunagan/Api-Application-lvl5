import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import requests

class QuoteAndDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quote and Dictionary App")
        self.root.geometry("900x650")
        self.style = Style(theme="flatly")
        self.dark_mode = False  

        self.setup_quote_app()

        self.setup_dictionary_app()

    def setup_quote_app(self):
        frame_quote = ttk.Frame(self.root, style="TFrame")
        frame_quote.pack(padx=20, pady=20)

        self.quote_label = ttk.Label(frame_quote, text="", wraplength=700, font=("Helvetica", 18, 'bold'), style="TLabel")
        self.quote_label.grid(row=0, column=0, pady=(0, 20))

        self.author_label = ttk.Label(frame_quote, text="", font=("Helvetica", 14, 'bold'), style="TLabel")
        self.author_label.grid(row=1, column=0, pady=(0, 20))

        button_get_quote = ttk.Button(frame_quote, text="Get Quote", command=self.get_quote, style="TButton")
        button_get_quote.grid(row=2, column=0, pady=(0, 20))

        # Initial quote
        self.get_quote()

    def setup_dictionary_app(self):
        frame_search = ttk.Frame(self.root, style="TFrame")
        frame_search.pack(padx=20, pady=20)

        label_word = ttk.Label(frame_search, text="Enter a word:", font=('TkDefaultFont', 15, 'bold'), style="TLabel")
        label_word.grid(row=0, column=0, padx=5, pady=5)

        self.entry_word = ttk.Entry(frame_search, width=20, font=('TkDefaultFont 15'))
        self.entry_word.grid(row=0, column=1, padx=5, pady=5)

        button_search = ttk.Button(frame_search, text="Search", command=self.search_definition, style="TButton")
        button_search.grid(row=0, column=2, padx=5, pady=5)

        frame_output = ttk.Frame(self.root, style="TFrame")
        frame_output.pack(padx=20, pady=10)

        self.text_output = tk.Text(frame_output, height=10, state='disabled', font=('TkDefaultFont', 15))
        self.text_output.pack()

    def search_definition(self):
        word = self.entry_word.get()
        try:
            definition = self.get_definition(word)
            self.text_output.configure(state='normal')
            self.text_output.delete('1.0', tk.END)
            self.text_output.insert(tk.END, definition)
            self.text_output.configure(state='disabled')
        except requests.RequestException as e:
            print(f"Error searching definition: {e}")
            # Provide user feedback about the error.

    def get_quote(self):
        url = "https://api.quotable.io/random"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            self.quote_label.config(text="")
            self.author_label.config(text="")
            self.quote_label.config(text=data['content'])
            self.author_label.config(text=data['author'])
        except requests.RequestException as e:
            print(f"Error getting quote: {e}")

    def toggle_dark_mode(self):
        theme = "darkly" if not self.dark_mode else "flatly"
        self.style.theme_use(theme)
        self.dark_mode = not self.dark_mode

    @staticmethod
    def get_definition(word):
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            if data:
                meanings = data[0]['meanings']
                definitions = []
                for meaning in meanings:
                    definitions.append(f"• Meaning: {meaning['partOfSpeech']}\nDefinition: {meaning['definitions'][0]['definition']}\n")
                return '\n'.join(definitions)
            return "No definition found."
        return "Error in fetching definition."

def main():
    root = tk.Tk()
    app = QuoteAndDictionaryApp(root)

    toggle_button = ttk.Button(root, text="Toggle Dark Mode", command=app.toggle_dark_mode)
    toggle_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
