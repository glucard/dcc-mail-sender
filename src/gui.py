import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import threading

from src.utils import get_df_data, send_mail, add_attachments
from src.custom_exceptions import ThreadWithException

class FileSelectorWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("DCC Mail Sender - File Selector")

        self.label = tk.Label(root, text="Select an Excel file containing names and emails:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.select_button.pack(pady=5)

        self.file_label = tk.Label(root, text="")
        self.file_label.pack(pady=10)

        
        self.module_label = tk.Label(root, text="Nome do modulo:")
        self.module_label.pack(pady=10)
        
        self.module_input = tk.Entry(self.root, width=50)
        self.module_input.pack(pady=1)

        self.next_button = tk.Button(root, text="Next", command=self.open_main_window)
        self.next_button.pack(pady=20)

        self.filepath = ""

    def retrieve_module_input(self):
        return self.module_input.get()

    def browse_file(self):
        self.filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if self.filepath:
            self.file_label.config(text=f"Selected file: {self.filepath}")

    def open_main_window(self):
        if self.filepath:
            try:
                module_name = self.retrieve_module_input()
                data = get_df_data(file_path=self.filepath, module_name=module_name)
                print(data)
                if 'nome' in data.columns and 'email' in data.columns:
                    self.root.destroy()
                    MainWindow(data, module_name)
                else:
                    messagebox.showerror("Error", "The file must contain 'nome' and 'email' columns.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read the file: {e}")
        else:
            messagebox.showwarning("Input Error", "Please select a file!")

class MainWindow:
    def __init__(self, data, module_name):
        self.root = tk.Tk()
        self.root.title("DCC Mail Sender - Main Window")
        self.root.attributes('-fullscreen',True)

        self.data = data
        self.module_name = module_name

        self.label = tk.Label(self.root, text="Email Sender")
        self.label.pack(pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.acceptable_columns = ['nome', 'email', 'attachments_paths']
        self.tree = ttk.Treeview(self.frame, columns=list(self.acceptable_columns), show='headings')
        for col in self.acceptable_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=256)

        self.update_tree()

        self.tree.pack(side=tk.LEFT)

        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.send_button = tk.Button(self.root, text="Adicionar pasta de anexos", command=self.add_attachments)
        self.send_button.pack(pady=20)
        
        self.subject_label = tk.Label(self.root, text="Subject:")
        self.subject_label.pack()
        self.subject_entry = tk.Entry(self.root, width=50)
        self.subject_entry.pack(pady=5)

        self.message_label = tk.Label(self.root, text="Message:")
        self.message_label.pack()
        self.message_text = tk.Text(self.root, width=50, height=10)
        self.message_text.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_email)
        self.send_button.pack(pady=20)

        self.check_debug = tk.IntVar(value=1) 
        self.check_debug_button = tk.Checkbutton(self.root, text = "Debug Mode", 
                    variable = self.check_debug, 
                    onvalue = 1, 
                    offvalue = 0, 
                    height = 2)
        self.check_debug_button.pack()

        self.root.mainloop()
    
    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def update_tree(self):
        self.clear_tree()
        temp_data = self.data[self.acceptable_columns].copy()
        for index, row in temp_data.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def add_attachments(self):
        try:
            folder_path = filedialog.askdirectory()
            if folder_path:
                add_attachments(df_data=self.data, attachments_folder_path=folder_path)
            self.update_tree()
        except Exception as e:
            messagebox.showerror("Erro", e)
            self.root.destroy()
            

    def send_email(self):
        subject = self.subject_entry.get()
        message = self.message_text.get("1.0", tk.END)
        checkbox_debug = True if self.check_debug.get() == 1 else False

        if subject and message:
            # Here you would call the existing email sending function
            try:
                send_email_function(subject, message, checkbox_debug, data=self.data, module_name=self.module_name)  # Replace with your actual function
                messagebox.showinfo("Success", "Email sent successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

def send_email_function(subject, message,checkbox_debug, data:pd.DataFrame, module_name:str):
    # This is a placeholder for your actual email sending logic
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print(f"Debug Mode {checkbox_debug}")

    send_thread = ThreadWithException(target=send_mail,args=(data, module_name, message, subject, checkbox_debug, checkbox_debug, 2), daemon=True)
    send_thread.start()
    #send_thread.join()
    # send_mail(df_data=data, module_name=module_name, message=message, subject=subject, debug=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectorWindow(root)
    root.mainloop()
