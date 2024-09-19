# DCC-MAIL-SENDER


## Uso

### Requisitos:

 - Python
 - Tkinter

### Configurando

1. Baixe manualmente o repositorio e extraia ou use `git clone https://github.com/glucard/dcc-mail-sender`

2. Instalando tkinter

    - #### linux:
        ```bash
        apt-get install python3-tk
        ```
    - #### windows:
        ```bash
        pip install tk
        ```

#### Configurando `.env`
1. Copie o arquivo `.env.example` e renomeie para `.env` no diretorio raiz do projeto;
2. <a href='https://myaccount.google.com/apppasswords'>Crie sua senha de aplicativo</a> (autenticação de dois fatores deve estar ativada) e adicione em `.env` como `MAIL_APP_PASSWORD="sua_senha"`; (Tome cuidado com a sua senha. Não passe ou demonstre a ninguém)
3. Adicione seu ID de email (example_id_email@gmail.com) em `MAIL_ID="your_mail_id"`. O ID de email não deve conter `@gmail.com`;
4. Caso deseje usar a função debug, adicione um email a ser enviado os emails de teste em `DEBUG_MAIL="your_debug_email@example.com"`

`.env` deve parecer com:

![dot_env_example](media/dot_env_example.png)   

### Executando:


1. configure com os passos acima.
2. após configurado execute o arquivo `app.py`

    ```bash
    cd dcc-email-sender
    python3 app.py
    ```

## Contribuições:

### Melhorias reconhecidas que podem ser implmentadas:
 - Adicionar variaveis para mensagem automatica para pessoas a depender do arquivo que as mesmas contém;
 - Interface de log durante envio dos emails;
 - Janela de configuração para remover necessidade de configurar `.env`;
 - Talvez uma thread para cada email a ser enviado resolva o problema de demora enquanto envia emails (ou não);
 - Talvez usar o OAUTH para fazer autenticação para envios dos emails;
 - Verificação dos emails já enviados quando houve errado;