import speech_recognition as sr
import pyttsx3
import os
import datetime

# ----------------- Initialisation TTS -----------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def parler(texte: str):
    """Fait parler l'assistant"""
    print("Assistant:", texte)
    engine.say(texte)
    engine.runAndWait()

# ----------------- Variables globales -----------------
recognizer = sr.Recognizer()
micro = sr.Microphone()
paused = False
language = "fr-FR"
api_choice = "sphinx"  # "sphinx" (offline) ou "google" (online)
transcribed_texts = []

# ----------------- Fonctions -----------------
def choisir_api():
    """Choisir API de reconnaissance"""
    global api_choice
    print("\n=== Sélection API ===")
    print("1. Sphinx (hors ligne, local)")
    print("2. Google Speech Recognition (en ligne)")

    choix = input("Choisis ton API (1 ou 2) : ")
    api_choice = "sphinx" if choix == "1" else "google"
    print(f"API sélectionnée : {api_choice}\n")

def choisir_langue():
    """Choisir la langue"""
    global language
    print("\n=== Sélection de la langue ===")
    print("1. Français (fr-FR)")
    print("2. Anglais (en-US)")
    print("3. Espagnol (es-ES)")

    choix = input("Choisis la langue (1, 2 ou 3) : ")
    language = "fr-FR" if choix == "1" else "en-US" if choix == "2" else "es-ES"
    print(f"Langue sélectionnée : {language}\n")

def transcrire_parole():
    """Transcrit la parole en texte avec gestion améliorée"""
    global paused
    with micro as source:
        recognizer.adjust_for_ambient_noise(source)
        print("\n🎤 Parle maintenant... (ou dis 'pause' pour mettre en pause)")
        audio = recognizer.listen(source)
    try:
        if api_choice == "sphinx":
            texte = recognizer.recognize_sphinx(audio, language=language)
        else:
            texte = recognizer.recognize_google(audio, language=language)
        print("Utilisateur :", texte)
        return texte
    except sr.UnknownValueError:
        parler("Je n'ai pas compris.")
        return ""
    except sr.RequestError as e:
        parler(f"Erreur service : {e}")
        return ""
    except Exception as e:
        parler(f"Erreur inattendue : {e}")
        return ""

def enregistrer_transcription():
    """Sauvegarde le texte dans un fichier"""
    if not transcribed_texts:
        parler("Aucun texte à enregistrer.")
        return
    with open("transcription_locale.txt", "w", encoding="utf-8") as f:
        for ligne in transcribed_texts:
            f.write(ligne + "\n")
    parler("Transcription sauvegardée dans 'transcription_locale.txt'.")

# ----------------- Boucle principale -----------------
def assistant_vocal_local():
    global paused
    parler("Bonjour, je suis ton assistant vocal local.")
    choisir_api()
    choisir_langue()
    actif = True

    while actif:
        if paused:
            commande = input("⏸ Pause activée. Tape 'resume' pour reprendre : ").lower()
            if commande == "resume":
                paused = False
                parler("Reprise de l'écoute.")
            continue

        texte = transcrire_parole()
        if not texte:
            continue

        transcribed_texts.append(texte)

        # Commandes vocales
        if "pause" in texte.lower():
            paused = True
            parler("Mise en pause.")
        elif "stop" in texte.lower() or "arrête" in texte.lower():
            parler("Au revoir !")
            actif = False
        elif "enregistre" in texte.lower():
            enregistrer_transcription()
        else:
            parler(f"Tu as dit : {texte}")

# ----------------- Lancement -----------------
if __name__ == "__main__":
    assistant_vocal_local()
