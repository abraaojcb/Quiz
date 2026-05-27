import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Lembre-se de colocar as suas informações reais aqui
EMAIL_REMETENTE = "gamequizify@gmail.com"
SENHA_DE_APP = "ouhq iiun rjgl yifw" 

def enviar_email_otp(email_destino, codigo_otp):
    mensagem = MIMEMultipart()
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = email_destino
    mensagem["Subject"] = "Código de Verificação - Meu Jogo"

    corpo_email = f"Olá!\n\nSeu código de ativação é: {codigo_otp}\n\nBem-vindo ao jogo!"
    mensagem.attach(MIMEText(corpo_email, "plain"))

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_DE_APP)
        servidor.sendmail(EMAIL_REMETENTE, email_destino, mensagem.as_string())
        servidor.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False