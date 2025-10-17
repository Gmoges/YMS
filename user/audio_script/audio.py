
#  librarys

import socket           #  used for Network communication
import pyaudio          #. record and play audio from the microphone and speakers
import threading        #. multiple tasks at the same time
from Crypto.Cipher import AES   # inport Advanced Encryption Standard(AES) to decript data

#   symmetric key (must be same as user side code)
key = b"This1sH4k3R1o9!!"    #. sed to encrypt/decrypt
nonce = b"123456789012"      #. random-like number ensuring encryption uniqueness but it's fixed for now!
YMS_enc = AES.new(key, AES.MODE_EAX, nonce=nonce)    #. encrypt outgoing audio
YMS_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)    #. decrypt incoming audio

#  Audio settings
FRAMS = 1024                       #. Number audio frames
SAMPLE = pyaudio.paInt16           #. 16-bit per audio sample
CHANNEL = 1
RATE = 44100                       # CD quality
# PyAudio
audio = pyaudio.PyAudio()        # Initializes the audio system


get_audio = audio.open(format=SAMPLE, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=FRAMS) 

send_audio = audio.open(format=SAMPLE, channels=CHANNEL, rate=RATE, output=True, frames_per_buffer=FRAMS)


logo = """
__  ____  _______               ___                 ____
 \ \/ /  |/  / __/ ___ ___ _____/ (____    _______ _/ / /
  \  / /|_/ _\ \  / _ `/ // / _  / / _ \  / __/ _ `/ / / 
  /_/_/  /_/___/  \_,_/\_,_/\_,_/_/\___/  \__/\_,_/_/_/  
"""
logo = "\033[34m" + logo + "\033[0m"
print(logo)


IP = input("Enter server IP: ")
PORT = 2119
User = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
User.connect((IP, PORT))
print(" Connected to server")

def send_audio():
    while True:
        try:
            data = get_audio.read(FRAMS, exception_on_overflow=False)
            ciphertext = YMS_enc.encrypt(data)
            User.sendall(ciphertext)
        except:
            break

def receive_audio():
    while True:
        try:
            data = User.recv(2048)
            if not data:
                break
            plaintext = YMS_dec.decrypt(data)   
            send_audio.write(plaintext)
        except:
            break

tsend = threading.Thread(target=send_audio)
tresive = threading.Thread(target=receive_audio)

# starting 

tsend.start()
tresive.start()

# waiting to finsh before closed the program 
tsend.join()
tresive.join()

# closed connection 

User.close()
get_audio.close()
send_audio.close()
audio.terminate()
