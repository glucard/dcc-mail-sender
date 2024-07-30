from src.utils import get_df_data, send_mail

def debug():
    df_data = get_df_data("debug_data\CERTIFICADOS.xlsx", "ds_3")
    print(df_data)
    df_data.to_excel("debug_data\output.xlsx", index=False)
    send_mail(df_data=df_data, module_name="ds_3", debug=True, send_debug=True, max_debug_count_send=0)

if __name__ == "__main__":
    debug()