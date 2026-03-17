import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import os 
import pyttsx3
import numpy as np                                        
import webbrowser
from datetime import datetime
import time

nome_assistente = "A.L.F.R.E.D."
usuario = "Joao"
bateria = 100
estudar = True


def falar(texto):
    print(f"A.L.F.R.E.D.: {texto}")
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        for voz in voices:
            if "Maria" in voz.name:
                engine.setProperty('voice', voz.id)
                break
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(texto)
        engine.runAndWait()
        engine.stop() 
        del engine
    except Exception as e:
         print(f"Error na voz: {e}")

def ouvir():
    fs =    44100
    segundos = 5

    print(f"\n{nome_assistente}: Fala comigo...")

    falar("Fala comigo...")
    gravaçao = sd.rec(int(segundos * fs), samplerate=fs, channels=1)
    sd.wait()

    audio_int16 = (gravaçao * 32767).astype(np.int16)
    write('comando.wav', fs, audio_int16)

    reconhecedor = sr.Recognizer()
    with sr.AudioFile('comando.wav') as fonte:
        audio = reconhecedor.record(fonte)
    reconhecedor = sr.Recognizer()
    reconhecedor.phrase_threshold = 1.0
    reconhecedor.non_speaking_duration = 0.8
    try:
        texto_ouvido = reconhecedor.recognize_google(audio, language='pt-BR')
        print(f"Voce disse: {texto_ouvido}")
        return texto_ouvido.lower()
    except:
        return "nada"
    finally:
        if os.path.exists("comando.wav"):
            os.remove("comando.wav")

def saudar():
    falar(f"Boa boa, {usuario}. Sistemas em {bateria}%.")
    
saudar()
def executar_tarefa(comando):
    if "pesquisar" in comando:
        termo = comando.replace("pesquisar", "")
        falar(f"Procurando por {termo} na internet, muita calma nessa hora. ")
        webbrowser.open(f"https://www.google.com/search?q={termo}")
    
    elif "youtube" in comando:    
        falar("Abrindo o Youtube... Oque veremos hoje? ")
        webbrowser.open("https://www.youtube.com")
    elif "horas" in comando:
        from datetime import datetime
        agora = datetime.now()
        hora = agora.hour
        hora_formatada = agora.strftime ('%H:%M')

        if hora < 12:
            saudar  = "Bom dia"
        elif hora < 18:
            saudar = "Boa tarde"
        else:
            saudar = "Boa noite"
                
        falar(f"{saudar} são exatamente... {hora_formatada}. O tempo esta passando rapido de mais")

while True:
    comando = ouvir ().lower()
    
    if "nada" in comando:
        continue

    if "youtube" in comando or "pesquisar" in comando or "horas" in comando:
        executar_tarefa(comando)
        continue

    if "status" in comando:
        falar(f"Sistemas operacionais em 100%")
    
    elif "estudar" in comando or "estudar" in comando:
        if estudar == True:
         falar("Entendido. Preparando o ambiente. Tente não se distrair com redes sociais. ")
         os.system("code")
         webbrowser.open("https://music.youtube.com/playlist?list=PL3f9jvs1Sm_51VgjeHA3_7AiqnJukGIhS&si=g8gZgFkC2o1KrBZZ")
    elif "descansar" in comando or "descanso" in comando:
        falar("Descansar né, que o cara né de ferro. Vou marcar uns 20 minutos. Começando agora")
        time.sleep(20 * 60)
        falar("Opa, deu tempo já. ")
    elif "sair" in comando:    
        falar("Desligando sistemas...Até logo.")
        break

    else:
        falar("Comando não encontrado na minha base de dados.")
