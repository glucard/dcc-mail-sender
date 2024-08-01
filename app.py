from src.utils import get_df_data, send_mail, add_attachments
from src.gui import FileSelectorWindow

import tkinter as tk

def debug():
    df_data = get_df_data("debug_data\CERTIFICADOS.xlsx", "ds_3")
    add_attachments(df_data, attachments_folder_path=r"C:\Users\glucas\Documents\a\repos\dcc-mail-sender\debug_data\DS-001")
    add_attachments(df_data, attachments_folder_path=r"C:\Users\glucas\Documents\a\repos\dcc-mail-sender\debug_data\DS-002")
    send_mail(df_data=df_data, module_name="ds_3", message="Testando <pname>. será que funciona?? vamove", subject="Debugging dcc mail sender", debug=True, send_debug=True, max_debug_count_send=2)
    df_data.to_excel("debug_data\output_datetime.xlsx", index=False)
    print(df_data)

def debug_gui():
    root = tk.Tk()
    app = FileSelectorWindow(root)
    root.mainloop()
    
if __name__ == "__main__":
    debug_gui()