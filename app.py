from src.utils import get_df_data, send_mail

def debug():
    df_data = get_df_data("debug_data\debug.xlsx", "ds_3")
    print(df_data)
    df_data.to_excel("debug_data\output.xlsx", index=False)
    send_mail(df_data=df_data, debug=True, send_debug=True)

if __name__ == "__main__":
    debug()