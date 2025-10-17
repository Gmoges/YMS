
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
FRAMS = 1024                       #. Number of audio frames
SAMPLE = pyaudio.paInt16           #. 16-bit resolution per audio sample
CHANNEL = 1
RATE = 44100                       # CD quality

# 4. printing YMS LOGO

logo = """
__  ____  _______               ___                 ____
 \ \/ /  |/  / __/ ___ ___ _____/ (____    _______ _/ / /
  \  / /|_/ _\ \  / _ `/ // / _  / / _ \  / __/ _ `/ / / 
  /_/_/  /_/___/  \_,_/\_,_/\_,_/_/\___/  \__/\_,_/_/_/  
"""
logo = "\033[34m" + logo + "\033[0m"
print(logo)

PORT = 2119  #Port number the server is runing

# 5. PyAudio
audio = pyaudio.PyAudio()        # Initializes the audio system
stream_in = audio.open(format=SAMPLE, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=FRAMS)  

# captures voice

stream_out = audio.open(format=SAMPLE, channels=CHANNEL, rate=RATE, output=True, frames_per_buffer=FRAMS)
# plays the user’s voice


# 6. TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a TCP socket
server.bind(("0.0.0.0", PORT)) # bind in any host and port 2119
server.listen(1)
print(" Waiting for connection...")
connection, addressUser = server.accept()
print(f" Connected by {addressUser}")



def send_audio():
    while True:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False) # Continuously geting dta from user
            ciphertext = cipher_enc.encrypt(data)   # Encrypt before sending
            conn.sendall(ciphertext) # Sends encrypted audio to server
        except:
            break

def receive_audio():
    while True:
        try:
            data = conn.recv(2048)                  #reciving up to 2048 bytes
            if not data:                            # connection closed
                break
            plaintext = cipher_dec.decrypt(data)    # Decrypt before playing
            stream_out.write(plaintext)             # Decrypts the audio
        except:
            break

t1 = threading.Thread(target=send_audio)            # Handles sending audio
t2 = threading.Thread(target=receive_audio)         # Handles receiving audio
t1.start()
t2.start()

t1.join()
t2.join()

# closed the connection

conn.close()
stream_in.close()
stream_out.close()
audio.terminate()
