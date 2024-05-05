import speech_recognition as sr
import pyttsx3

# Função para ouvir e reconhecer a fala do usuário
def ouvir():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga alguma coisa...")
        reconhecedor.adjust_for_ambient_noise(source)  # Ajusta o ruído ambiente
        audio = reconhecedor.listen(source)

    try:
        texto = reconhecedor.recognize_google(audio, language='pt-BR')
        print("Você disse:", texto)
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return ""
    except sr.RequestError as e:
        print("Erro ao recuperar os resultados; {0}".format(e))
        return ""

# Função para responder ao usuário
def responder(texto):
    motor = pyttsx3.init()
    motor.setProperty('rate', 150)  # Velocidade de fala
    motor.setProperty('volume', 0.9)  # Volume
    motor.say(texto)
    motor.runAndWait()

# Função principal
def main():
    responder("Olá! Eu sou uma IA simples. Como posso ajudar você?")
    while True:
        entrada = ouvir().lower()
        if "parar" in entrada:
            responder("Até logo!")
            break
        # Adicione aqui sua lógica para processar a entrada do usuário e gerar uma resposta
        resposta = "Você disse: " + entrada
        responder(resposta)

if __name__ == "__main__":
    main()
