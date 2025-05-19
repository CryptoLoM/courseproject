from buffer import *

# === GUI Interface ===


def run_gui():

    def browse_file(entry):
        filename = filedialog.askopenfilename()
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def browse_save(entry):
        filename = filedialog.asksaveasfilename()
        if filename:
            entry.delete(0, tk.END)
            entry.insert(0, filename)

    def run_action():
        try:
            if var.get() == 'encrypt':
                status_label.config(text="🔐 Шифрування...")
            else:
                status_label.config(text="🔓 Дешифрування...")
            root.update_idletasks()  # Оновити GUI до запуску обробк
            process_file(input_entry.get(), output_entry.get(), key_entry.get(), var.get())
            messagebox.showinfo("Success!", f"✅File was {var.get()}ed!")
        except Exception as e:
            messagebox.showerror("❌Error", str(e))

    root = tk.Tk()
    root.title("HIGHT Cipher")
    root.geometry("400x400")

    # 🔼 Інструкції вгорі
    tk.Label(root, text="Welcome to the program for encrypting and decrypting files!", wraplength=600,
             justify="center", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=(10, 0))


    # 🔽 Поля вводу нижче
    tk.Label(root, text="Вхідний файл").grid(row=6, column=0)
    input_entry = tk.Entry(root, width=40)
    input_entry.grid(row=6, column=1)
    tk.Button(root, text="Огляд", command=lambda: browse_file(input_entry)).grid(row=6, column=2)

    tk.Label(root, text="Файл виводу").grid(row=7, column=0)
    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=7, column=1)
    tk.Button(root, text="Огляд", command=lambda: browse_save(output_entry)).grid(row=7, column=2)

    tk.Label(root, text="Файл ключа").grid(row=8, column=0)
    key_entry = tk.Entry(root, width=40)
    key_entry.grid(row=8, column=1)
    tk.Button(root, text="Огляд", command=lambda: browse_file(key_entry)).grid(row=8, column=2)

    var = tk.StringVar(value='encrypt')
    tk.Radiobutton(root, text="Шифрування", variable=var, value='encrypt').grid(row=9, column=1, sticky='w')
    tk.Radiobutton(root, text="Розшифрування", variable=var, value='decrypt').grid(row=10, column=1, sticky='w')

    tk.Button(root, text="Виконати", command=run_action).grid(row=11, column=1, pady=10)
    status_label = tk.Label(root, text="Готово", fg="blue")
    status_label.grid(row=12, column=1)

    root.mainloop()