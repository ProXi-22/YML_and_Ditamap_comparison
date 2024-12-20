import customtkinter as ctk
from tkinter import filedialog, messagebox, Scrollbar, RIGHT, Y, X, BOTH
import yaml
import xml.etree.ElementTree as ET
from difflib import Differ

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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
        entry_yml.delete(0, ctk.END)
        entry_yml.insert(0, file_path)

def open_file_ditamap():
    file_path = filedialog.askopenfilename(filetypes=[("DITAMAP Files", "*.ditamap")])
    if file_path:
        entry_ditamap.delete(0, ctk.END)
        entry_ditamap.insert(0, file_path)

def compare_files():
    yml_file = entry_yml.get()
    ditamap_file = entry_ditamap.get()

    if not yml_file or not ditamap_file:
        messagebox.showwarning("Warning!", "Choose both files for comparison!")
        return

    try:
        yml_data = read_yml(yml_file)
        yml_text = extract_text_from_yml(yml_data)
        ditamap_text = read_ditamap(ditamap_file)
    except Exception as e:
        messagebox.showerror("Error", f"There is a problem with reading the files: {e}")
        return

    differences = compare_texts(yml_text, ditamap_text)

    text_diff_left.delete("1.0", ctk.END)
    text_diff_right.delete("1.0", ctk.END)

    # Wstawienie całego tekstu dla obu plików z podświetleniem różnic
    for line in differences:
        if line.startswith("- "):
            text_diff_left.insert(ctk.END, line[2:] + "\n", "highlight")
        elif line.startswith("+ "):
            text_diff_right.insert(ctk.END, line[2:] + "\n", "highlight")
        elif line.startswith("  "):
            text_diff_left.insert(ctk.END, line[2:] + "\n")
            text_diff_right.insert(ctk.END, line[2:] + "\n")

# Tworzenie głównego okna
root = ctk.CTk()
root.title("Comparison of YAML and DITAMAP files")

# Centrowanie okna na środku ekranu
window_width, window_height = 1600, 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cord = int((screen_width / 2) - (window_width / 2))
y_cord = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_cord}+{y_cord}")

# Etykiety i przyciski wyboru plików
label_yml = ctk.CTkLabel(root, text="Choose YAML file:")
label_yml.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_yml = ctk.CTkEntry(root, width=400)
entry_yml.grid(row=0, column=1, padx=10, pady=10)
button_yml = ctk.CTkButton(root, text="Choose file", command=open_file_yml)
button_yml.grid(row=0, column=2, padx=10, pady=10)

label_ditamap = ctk.CTkLabel(root, text="Choose DITAMAP file:")
label_ditamap.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_ditamap = ctk.CTkEntry(root, width=400)
entry_ditamap.grid(row=1, column=1, padx=10, pady=10)
button_ditamap = ctk.CTkButton(root, text="Choose file", command=open_file_ditamap)
button_ditamap.grid(row=1, column=2, padx=10, pady=10)

# Przycisk porównania
button_compare = ctk.CTkButton(root, text="Compare", command=compare_files)
button_compare.grid(row=2, column=1, padx=10, pady=10)

# Pola tekstowe dla porównań
frame_diff = ctk.CTkFrame(root, bg_color="white")
frame_diff.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Konfiguracja skalowalności
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)
frame_diff.grid_columnconfigure(0, weight=1)
frame_diff.grid_columnconfigure(1, weight=1)

# Pole tekstowe i suwak dla YAML
text_diff_left = ctk.CTkTextbox(frame_diff, fg_color="white", text_color="black", width=800, height=1000)
text_diff_left.grid(row=0, column=0, padx=(5, 0), pady=5, sticky="nsew")
text_diff_left.tag_config("highlight", background="yellow")

scroll_y_left = Scrollbar(frame_diff, orient="vertical", command=text_diff_left.yview)
scroll_y_left.grid(row=0, column=0, sticky="nse")
text_diff_left.configure(yscrollcommand=scroll_y_left.set)

# Pole tekstowe i suwak dla DITAMAP
text_diff_right = ctk.CTkTextbox(frame_diff, fg_color="white", text_color="black", width=800, height=1000)
text_diff_right.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nsew")
text_diff_right.tag_config("highlight", background="yellow")

scroll_y_right = Scrollbar(frame_diff, orient="vertical", command=text_diff_right.yview)
scroll_y_right.grid(row=0, column=1, sticky="nse")
text_diff_right.configure(yscrollcommand=scroll_y_right.set)

# Dodanie suwaków poziomych
scroll_x_left = Scrollbar(frame_diff, orient="horizontal", command=text_diff_left.xview)
scroll_x_left.grid(row=1, column=0, sticky="sew")
text_diff_left.configure(xscrollcommand=scroll_x_left.set)

scroll_x_right = Scrollbar(frame_diff, orient="horizontal", command=text_diff_right.xview)
scroll_x_right.grid(row=1, column=1, sticky="sew")
text_diff_right.configure(xscrollcommand=scroll_x_right.set)

# Uruchomienie głównej pętli
root.mainloop()
