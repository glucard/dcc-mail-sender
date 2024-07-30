import pandas as pd
import smtplib

# load env
import os
from dotenv import load_dotenv
load_dotenv()

def send_mail(df_data: pd.DataFrame, debug=True, send_debug=False, max_debug_count_send:int=1):

    mail_id = os.getenv('MAIL_ID')
    mail_password = os.getenv('MAIL_APP_PASSWORD')

    assert isinstance(mail_id, str)
    assert isinstance(mail_password, str)
    assert isinstance(df_data, pd.DataFrame)
    assert isinstance(debug, bool)
    assert isinstance(send_debug, bool)
    assert isinstance(max_debug_count_send, int)

    if send_debug:
        debug_send_count=0
        debug_mail = os.getenv('DEBUG_MAIL')
        assert isinstance(debug_mail, str)

    # creates SMTP session
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(mail_id, mail_password)
        
        for index, row in df_data.iterrows():
            try:
                # message to be sent
                message = f"""\
                    Debugging {row['nome']}\ntest\n\ntest

                    att
                    """
                # sending the mail
                if debug:
                    print(row['nome'], row['email'])
                    if send_debug and debug_send_count < max_debug_count_send:
                        s.sendmail(from_addr=mail_id, to_addrs=debug_mail)
                        debug_send_count += 1
                    
                else:
                    pass
            except Exception as e:
                print(e)

def get_df_data(file_path: str, module_name: str):

    """
    file_path: local do arquivo com extensão
    module_name: nome do curso/modulo atual dos certificados a serem enviados
    """

    assert isinstance(file_path, str)
    assert isinstance(module_name, str)

    file_extension = file_path.split(sep='.')[-1]

    read_funcs = {
        "xlsx": pd.read_excel,
    }

    df_data = read_funcs[file_extension](file_path)

    df_columns = df_data.columns

    assert "nome" in df_columns
    assert "email" in df_columns

    if not module_name in df_columns:
        df_data[module_name] = False

    return df_data