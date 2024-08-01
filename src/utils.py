import pandas as pd
import smtplib

from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders

# load env
import os
from dotenv import load_dotenv
load_dotenv()

def custom_message(message:str, tags_replaces:dict):
    """
    message: string com messagem contendo tags. Examplo de tag: <name>
    tags_replaces: dicionario com keys como tags e valores como valores que irão substituir as tags. Examplo {"<name>": "Lucas"}
    assert isinstance(message, str)
    """
    assert isinstance(message, str), "Mensagem deve ser uma string."
    assert isinstance(tags_replaces, dict), "tags_replaces deve ser um dicionario."

    for tag, value in tags_replaces.items():
        message = message.replace(tag, value)

    return message
    

def send_mail(df_data: pd.DataFrame, module_name:str, message: str, subject:str, debug=True, send_debug=False, max_debug_count_send:int=1):

    mail_id = os.getenv('MAIL_ID')
    mail_password = os.getenv('MAIL_APP_PASSWORD')

    assert isinstance(mail_id, str), "Verifique se o arquivo .env existe e está configurado corretamente. Para instruções siga o readme.md do projeto https://github.com/glucard/dcc-mail-sender"
    assert isinstance(mail_password, str), "Verifique se o arquivo .env existe e está configurado corretamente. Para instruções siga o readme.md do projeto https://github.com/glucard/dcc-mail-sender"

    assert isinstance(module_name, str)
    assert isinstance(df_data, pd.DataFrame)
    assert isinstance(debug, bool)
    assert isinstance(send_debug, bool)
    assert isinstance(max_debug_count_send, int)

    assert isinstance(message, str)
    assert isinstance(subject, str)

    if send_debug:
        debug_send_count=0
        debug_mail = os.getenv('DEBUG_MAIL')
        assert isinstance(debug_mail, str), "Verifique se o arquivo .env existe e está configurado corretamente. Para instruções siga o readme.md do projeto https://github.com/glucard/dcc-mail-sender"

    # creates SMTP session
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(mail_id, mail_password)
        print("Enviando emails...")
        for index, row in df_data.iterrows():
            try:
                print(f"Enviando a {row['nome']}...", end=" ")
                if row['attachments_paths'] == "":
                    print(f"Ignorando {row['nome']}. Não possui arquivos a serem enviados.")
                    continue

                to_mail = row['email']
                if send_debug:
                    to_mail = debug_mail

                # Create the email message
                msg = MIMEMultipart()
                msg['From'] = mail_id
                msg['To'] = to_mail
                msg['Subject'] = subject

                body = custom_message(message, {
                    "<pname>": row['nome'],
                })

                attachments_paths = row['attachments_paths']

                # Attach the body of the email
                msg.attach(MIMEText(body, 'plain'))

                for attachment_path in attachments_paths.split('|'):
                    # Open the PDF file in binary mode
                    with open(attachment_path, 'rb') as attachment:
                        # Create a MIMEBase object# Create a MIMEApplication object
                        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                        # Attach the MIMEApplication object to the email message
                        msg.attach(part)
                if debug:
                    if send_debug and debug_send_count < max_debug_count_send:
                        s.sendmail(from_addr=mail_id, to_addrs=debug_mail, msg=msg.as_string())
                        debug_send_count += 1
                else:
                    # s.sendmail(from_addr=mail_id, to_addrs=row['email'], msg=msg.as_string())
                    pass
                df_data.loc[index, module_name] = True
                print(f"Enviado com sucesso a {row['nome']} {row['email']}")
            except Exception as e:
                print(f"Erro ao enviar para {row['nome']}.", e)

    print("Enviar emails terminou.")

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

    if not 'attachments_paths' in df_columns:
        df_data['attachments_paths'] = r""

    return df_data

def add_attachments(df_data: pd.DataFrame, attachments_folder_path:str):
    
    assert isinstance(df_data, pd.DataFrame), "df_data deve ser um objeto DataFrame de pandas."
    assert isinstance(attachments_folder_path, str), "attachments_folder_path deve ser uma string"
    assert os.path.isdir(attachments_folder_path), f"'{attachments_folder_path}' é um caminho invalido."

    file_names = os.listdir(attachments_folder_path)

    for fn in file_names:
        fn_extracted_name = fn.lower()[:-11]
        p_file_index = df_data[df_data["nome"].apply(lambda x: x.lower()) == fn_extracted_name].index[0]
        # assert isinstance(p_file_index, int), "p_file_indexd deve ser um int."
        df_data.loc[p_file_index, 'attachments_paths'] += "|" if df_data.loc[p_file_index, 'attachments_paths'] != "" else ""
        df_data.loc[p_file_index, 'attachments_paths'] +=  os.path.join(attachments_folder_path, fn)
        #print(fn_extracted_name, p_file_index)

# codigo dedicado a minha namorada linda e bonita <3