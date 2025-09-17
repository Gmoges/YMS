import socket
import pyaudio
import threading
from Crypto.Cipher import AES

# 🔑 Shared symmetric key (16 bytes for AES-128)
key = b"This1sH4k3R1o9!!"
nonce = b"123456789012"  # must be same on both sides
cipher_enc = AES.new(key, AES.MODE_EAX, nonce=nonce)
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=nonce)

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
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

# Connect to server
IP = input("Enter server IP: ")
PORT = 2119
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
print("📞 Connected to server")

def send_audio():
    while True:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            ciphertext = cipher_enc.encrypt(data)   # 🔒 Encrypt before sending
            client.sendall(ciphertext)
        except:
            break

def receive_audio():
    while True:
        try:
            data = client.recv(2048)
            if not data:
                break
            plaintext = cipher_dec.decrypt(data)   # 🔓 Decrypt before playing
            stream_out.write(plaintext)
        except:
            break

t1 = threading.Thread(target=send_audio)
t2 = threading.Thread(target=receive_audio)
t1.start()
t2.start()

t1.join()
t2.join()

client.close()
stream_in.close()
stream_out.close()
audio.terminate()
