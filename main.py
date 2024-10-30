import tkinter as tk
from tkinter import filedialog, messagebox
import yaml
import xml.etree.ElementTree as ET
from difflib import Differ

def read_yml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def read_ditamap(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return [element.text for element in root.iter() if element.text]

def extract_text_from_yml(data):
    texts = []
    for key, value in data.items():
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, dict):
            texts.extend(extract_text_from_yml(value))
    return texts

def compare_texts(yml_text, ditamap_text):
    differ = Differ()
    diff = list(differ.compare(yml_text, ditamap_text))
    return diff

def open_file_yml():
    file_path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yml *.yaml")])
    if file_path:
        entry_yml.delete(0, tk.END)
        entry_yml.insert(0, file_path)

def open_file_ditamap():
    file_path = filedialog.askopenfilename(filetypes=[("DITAMAP Files", "*.ditamap")])
    if file_path:
        entry_ditamap.delete(0, tk.END)
        entry_ditamap.insert(0, file_path)

def compare_files():
    yml_file = entry_yml.get()
    ditamap_file = entry_ditamap.get()

    if not yml_file or not ditamap_file:
        messagebox.showwarning("Ostrzeżenie", "Wybierz oba pliki do porównania!")
        return

    try:
        yml_data = read_yml(yml_file)
        yml_text = extract_text_from_yml(yml_data)
        ditamap_text = read_ditamap(ditamap_file)
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem z odczytem plików: {e}")
        return

    differences = compare_texts(yml_text, ditamap_text)
    text_diff.delete(1.0, tk.END)
    for line in differences:
        text_diff.insert(tk.END, line + "\n")

# Tworzenie okna głównego
root = tk.Tk()
root.title("Porównanie plików YAML i DITAMAP")

# Etykiety i przyciski wyboru plików
label_yml = tk.Label(root, text="Wybierz plik YAML:")
label_yml.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_yml = tk.Entry(root, width=50)
entry_yml.grid(row=0, column=1, padx=5, pady=5)
button_yml = tk.Button(root, text="Wybierz plik", command=open_file_yml)
button_yml.grid(row=0, column=2, padx=5, pady=5)

label_ditamap = tk.Label(root, text="Wybierz plik DITAMAP:")
label_ditamap.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_ditamap = tk.Entry(root, width=50)
entry_ditamap.grid(row=1, column=1, padx=5, pady=5)
button_ditamap = tk.Button(root, text="Wybierz plik", command=open_file_ditamap)
button_ditamap.grid(row=1, column=2, padx=5, pady=5)

# Przycisk porównania
button_compare = tk.Button(root, text="Porównaj", command=compare_files)
button_compare.grid(row=2, column=1, padx=5, pady=10)

# Pole tekstowe na różnice
text_diff = tk.Text(root, width=80, height=20)
text_diff.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Uruchomienie głównej pętli
root.mainloop()