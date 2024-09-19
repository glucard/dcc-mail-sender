from src.utils import get_df_data, send_mail, add_attachments
from src.gui import FileSelectorWindow

import tkinter as tk

def gui():
    root = tk.Tk()
    app = FileSelectorWindow(root)
    root.attributes('-fullscreen',True)
    root.mainloop()
    
if __name__ == "__main__":
    gui()

    