import os
import ast
import tkinter as tk
from tkinter import scrolledtext, StringVar, messagebox

def extract_docstrings(source_dir):
    docstrings = {}
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    node = ast.parse(f.read(), filename=file)
                    for n in ast.walk(node):
                        if isinstance(n, ast.FunctionDef):
                            docstrings[n.name] = ast.get_docstring(n)
                        elif isinstance(n, ast.ClassDef):
                            docstrings[n.name] = ast.get_docstring(n)
    return docstrings

def save_to_file():
    with open("docstrings_output.txt", "w") as f:
        for name, doc in docstrings.items():
            f.write(f"{name}: {doc}\n\n")
    messagebox.showinfo("Success", "Documentazione salvata in docstrings_output.txt")

def show_docstrings(docstrings):
    button_font = ('Arial', 10)  # Definisci qui il font per i pulsanti

    def update_display():
        search_term = search_var.get().lower()
        filter_type = filter_var.get()
        text_area.delete(1.0, tk.END)  # Pulisci l'area di testo
        for name, doc in docstrings.items():
            if (filter_type == "All" or filter_type in name) and (search_term in name.lower() or (doc and search_term in doc.lower())):
                text_area.insert(tk.END, f"{name}: {doc}\n\n")
                # Aggiungi un pulsante "Modifica" per ogni docstring
                edit_button = tk.Button(text_area, text=f"Edit {name}", command=lambda n=name: edit_docstring(n))
                text_area.window_create(tk.END, window=edit_button)  # Inserisci il pulsante nell'area di testo
                text_area.insert(tk.END, "\n")  # Aggiungi una nuova riga dopo il pulsante

    def edit_docstring(name):
        def save_docstring():
            new_doc = doc_entry.get("1.0", tk.END).strip()
            if name in docstrings:
                docstrings[name] = new_doc
                update_display()  # Aggiorna l'area di testo
                edit_window.destroy()  # Chiudi la finestra di modifica

        edit_window = tk.Toplevel()
        edit_window.title(f"Edit {name}")

        doc_entry = tk.Text(edit_window, width=60, height=10)
        doc_entry.pack(padx=10, pady=10)
        doc_entry.insert(tk.END, docstrings[name])  # Inserisci il docstring attuale

        save_button = tk.Button(edit_window, text="Save", command=save_docstring)
        save_button.pack(pady=10)

    def add_docstring():
        def save_new_docstring():
            name = name_entry.get().strip()
            new_doc = doc_entry.get("1.0", tk.END).strip()
            if name and new_doc:
                docstrings[name] = new_doc
                with open("src/Prov1.py", "a") as f:  # Aggiungi il nuovo docstring al file
                    f.write(f"\n\ndef {name}():\n    \"\"\"{new_doc}\"\"\"\n    pass\n")
                update_display()  # Aggiorna l'area di testo
                add_window.destroy()  # Chiudi la finestra di aggiunta

        add_window = tk.Toplevel()
        add_window.title("Add New Docstring")

        tk.Label(add_window, text="Function/Class Name:").pack(padx=10, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(padx=10, pady=5)

        tk.Label(add_window, text="Docstring:").pack(padx=10, pady=5)
        doc_entry = tk.Text(add_window, width=60, height=10)
        doc_entry.pack(padx=10, pady=5)

        save_button = tk.Button(add_window, text="Save", command=save_new_docstring)
        save_button.pack(pady=10)

    # Creazione della finestra principale
    window = tk.Tk()
    window.title("Docstring Viewer")

    # Creazione della barra di ricerca
    search_var = StringVar()
    search_entry = tk.Entry(window, textvariable=search_var)
    search_entry.pack(padx=10, pady=5)
    search_entry.bind("<KeyRelease>", lambda event: update_display())  # Aggiorna i risultati durante la digitazione

    # Creazione delle opzioni di filtraggio
    filter_var = StringVar(value="All")
    filter_frame = tk.Frame(window)
    filter_frame.pack(padx=10, pady=10)
    tk.Radiobutton(filter_frame, text="All", variable=filter_var, value="All", command=update_display).pack(side=tk.LEFT)
    tk.Radiobutton(filter_frame, text="Classes", variable=filter_var, value="Class", command=update_display).pack(side=tk.LEFT)
    tk.Radiobutton(filter_frame, text="Functions", variable=filter_var, value="Function", command=update_display).pack(side=tk.LEFT)

    # Pulsante per aggiungere un nuovo docstring
    add_button = tk.Button(window, text="Add New Docstring", command=add_docstring, font=button_font, bg="#4CAF50", fg="white")
    add_button.pack(pady=10)

    # Pulsante per salvare la documentazione
    save_button = tk.Button(window, text="Save Documentation", command=save_to_file, font=button_font, bg="#2196F3", fg="white")
    save_button.pack(pady=10)

    # Creazione di un'area di testo scorrevole
    text_area = scrolledtext.ScrolledText(window, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    # Aggiunta dei docstring all'area di testo inizialmente
    update_display()

    # Avvio della GUI
    window.mainloop()

if __name__ == "__main__":
    source_directory = "src"  # Modifica con il percorso del tuo codice sorgente
    docstrings = extract_docstrings(source_directory)
    show_docstrings(docstrings)