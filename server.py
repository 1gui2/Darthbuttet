
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Função para enviar e-mail
def send_email(ip, name, feedback):
    sender_email = "your_email@example.com"  # Substitua pelo seu e-mail
    sender_password = "your_email_password"  # Substitua pela senha do seu e-mail
    recipient_email = "tocomfomeg@gmail.com"  # E-mail de destino

    subject = "Novo IP Capturado"
    body = f"IP: {ip}\nNome: {name}\nFeedback: {feedback}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

@app.route('/log_ip', methods=['POST'])
def log_ip():
    user_ip = request.remote_addr  # Captura o IP do remetente
    name = request.form.get('name')
    feedback = request.form.get('feedback')

    # Enviar os dados por e-mail
    send_email(user_ip, name, feedback)

    # Salvar os dados localmente
    with open("responses.txt", "a") as file:
        file.write(f"IP: {user_ip}, Nome: {name}, Feedback: {feedback}\n")

    return "Obrigado por enviar suas respostas!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
