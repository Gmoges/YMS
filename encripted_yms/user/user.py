
#  1.librarys

import socket           #  used for Network communication
import pyaudio          #. record and play audio from the microphone and speakers
import threading        #. multiple tasks at the same time
from Crypto.Cipher import AES   # inport Advanced Encryption Standard(AES) to decript data

#  2. symmetric key (must be same as user side code)
key = b"This1sH4k3R1o9!!"    #. sed to encrypt/decrypt
nonce = b"123456789012"      #. random-like number ensuring encryption uniqueness but it's fixed for now!
cipher_enc = AES.new(key, AES.MODE_EAX, nonce=nonce)    #. encrypt outgoing audio
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)    #. decrypt incoming audio

# 3. Audio settings
CHUNK = 1024                       #. Number of audio frames
FORMAT = pyaudio.paInt16           #. 16-bit resolution per audio sample
CHANNELS = 1
RATE = 44100

# PyAudio
audio = pyaudio.PyAudio()
stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

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
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
print(" Connected to server")

def send_audio():
    while True:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            ciphertext = cipher_enc.encrypt(data)
            client.sendall(ciphertext)
        except:
            break

def receive_audio():
    while True:
        try:
            data = client.recv(2048)
            if not data:
                break
            plaintext = cipher_dec.decrypt(data)   
            stream_out.write(plaintext)
        except:
            break

t1 = threading.Thread(target=send_audio)
t2 = threading.Thread(target=receive_audio)

# starting 

t1.start()
t2.start()

# waiting to finsh before closed the program 
t1.join()
t2.join()

# closed connection 

client.close()
stream_in.close()
stream_out.close()
audio.terminate()
