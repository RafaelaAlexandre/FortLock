import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email, smtp_username='fortlock.faeterj@gmail.com', smtp_password='rbueosbvkzwvcfsq'):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Criação da mensagem MIME
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject

        # Anexando o corpo da mensagem
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Conexão com o servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
