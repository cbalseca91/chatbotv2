from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.base import MIMEBase #Activar para enviar adjuntos

from smtplib import SMTP


class Correo:
    def __init__(self):
        self.mensaje = MIMEMultipart("alternative")
        # Cargar el servidor SMTP adecuado
        # self.smtp = SMTP_SSL("smtp.gmail.com:465")  # Gmail requiere SSL para conectarse.
        self.smtp = SMTP(host='smtp-mail.outlook.com', port=587)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login("chatbot.2020@hotmail.com", "Chat.bot.ups.2020")

    def enviarCorreo(self, mensaje):
        self.mensaje["From"] = "chatbot.2020@hotmail.com"
        self.mensaje["to"] = "chatbot.2020@hotmail.com"
        self.mensaje["subject"] = "RESPUESTA CHATBOT"

        # Mensaje en Texto Plano.
        msg = "Chatbot dice\n\n" + mensaje
        texto = MIMEText(msg, "plain")
        self.mensaje.attach(texto)

        # ACTIVAR ESTO SI SE QUIERE MANDAR ADJUNTOS
        # adjunto = MIMEBase("application","octect-stream")
        # adjunto.set_payload(open("contenido.txt","rb").read())
        # adjunto.add_header("content-Disposition",'attachment;filename="prueba.txt"')
        # self.mensaje.attach(adjunto)
        self.smtp.sendmail(self.mensaje["From"], self.mensaje["to"], self.mensaje.as_string())
        self.smtp.quit()


'''
correo = Correo();
correo.enviarCorreo("La siguiente respuesta no fue satisfactoria:\n\nPregunta: Que es cascada")
'''
