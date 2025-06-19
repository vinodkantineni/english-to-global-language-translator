# import the required libraries
import tkinter as tk
from tkinter import ttk, messagebox
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import pyttsx3

# Define top 3 global language models
LANGUAGE_MODELS = {
    "Spanish": "Helsinki-NLP/opus-mt-en-es",
    "French": "Helsinki-NLP/opus-mt-en-fr",
    "Russian": "Helsinki-NLP/opus-mt-en-ru"
}

# Initialize global variables
model = None
tokenizer = None

# Load the selected model
def load_model(language):
    global model, tokenizer
    model_name = LANGUAGE_MODELS[language]
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    except Exception as e:
        messagebox.showerror("Model Load Error", str(e))

# Translate the text
def translate_text():
    if model is None or tokenizer is None:
        messagebox.showerror("Error", "Please select a language first!")
        return

    input_text = input_entry.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Warning", "Please enter some text to translate.")
        return

    try:
        inputs = tokenizer(input_text, return_tensors="pt", padding=True)
        output_tokens = model.generate(**inputs)
        translated_text = tokenizer.batch_decode(output_tokens, skip_special_tokens=True)[0]
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# Speak the translated text
def speak_text():
    text = output_text.get("1.0", tk.END).strip()
    if text:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        messagebox.showinfo("Info", "No translated text to speak.")

# Handle language selection
def on_language_select(event):
    language = language_combo.get()
    load_model(language)

# GUI setup
root = tk.Tk()
root.title("English to Global Language Translator")
root.geometry("600x500")
root.config(padx=10, pady=10)

# Language selection
tk.Label(root, text="Select Language:", font=("Arial", 12)).pack()
language_combo = ttk.Combobox(root, values=list(LANGUAGE_MODELS.keys()), font=("Arial", 12), state="readonly")
language_combo.pack()
language_combo.bind("<<ComboboxSelected>>", on_language_select)

# Input box
tk.Label(root, text="Enter English Text:", font=("Arial", 12)).pack(pady=(20, 5))
input_entry = tk.Text(root, height=6, font=("Arial", 12))
input_entry.pack(fill=tk.BOTH, expand=True)

# Translate button
translate_btn = tk.Button(root, text="Translate", command=translate_text, font=("Arial", 12), bg="green", fg="white")
translate_btn.pack(pady=10)

# Output box
tk.Label(root, text="Translated Text:", font=("Arial", 12)).pack()
output_text = tk.Text(root, height=6, font=("Arial", 12), bg="#f0f0f0")
output_text.pack(fill=tk.BOTH, expand=True)

# Speak button
speak_btn = tk.Button(root, text="🔊 Speak", command=speak_text, font=("Arial", 12), bg="blue", fg="white")
speak_btn.pack(pady=10)

root.mainloop()
