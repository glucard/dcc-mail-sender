# DCC-MAIL-SENDER

### Configurando

#### Configurando `.env`
- Crie um arquivo e renomeie para `.env` no diretorio raiz do projeto;
- <a href='https://myaccount.google.com/apppasswords'>Crie sua senha de aplicativo</a> (autenticação de dois fatores deve estar ativada) e adicione em `.env` como `MAIL_APP_PASSWORD="sua_senha"`; (Tome cuidado com a sua senha. Não passe ou demonstre a ninguém)
- Adicione seu ID de email (example_id_email@gmail.com) em `MAIL_ID="your_mail_id"`. O ID de email não deve conter `@gmail.com`;

`.env` deve parecer com:

![dot_env_example](media/dot_env_example.png)   


## Contribuições:

### Melhorias reconhecidas que podem ser implmentadas:
 - Adicionar variaveis para mensagem automatica para pessoas a depender do arquivo que as mesmas contém;
 - Interface de log durante envio dos emails;
 - Janela de configuração para remover necessidade de configurar `.env`;
 - Talvez uma thread para cada email a ser enviado resolva o problema de demora enquanto envia emails (ou não);
 - Talvez usar o OAUTH para fazer autenticação para envios dos emails;
 - Verificação dos emails já enviados quando houve errado;