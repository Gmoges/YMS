
#  librarys

import socket           #  used for Network communication
import pyaudio          #. record and play audio from the microphone and speakers
import threading        #. multiple tasks at the same time
from Crypto.Cipher import AES   # inport Advanced Encryption Standard(AES) to decript data

#   symmetric key (must be same as user side code)
MY_key = b"This1sH4k3R1o9!!"    #. to encrypt/decrypt
MY_nonce = b"123456789012"      #. is randem number  encryption uniqueness but it's fixed for now!
YMS_enc = AES.new(MY_key, AES.MODE_EAX, nonce=MY_nonce)    #. encrypt  audio data
YMS_dec = AES.new(MY_key, AES.MODE_EAX, nonce=MY_nonce)    #. decrypt  audio data

#  Audio settings
FRAMS = 1024                       #. Number audio frames
SAMPLE = pyaudio.paInt16           #. 16-bit per audio sample
CHANNEL = 1
RATE = 44100                       # CD quality

#  printing YMS LOGO

logo = """
__  ____  _______               ___                 ____
 \ \/ /  |/  / __/ ___ ___ _____/ (____    _______ _/ / /
  \  / /|_/ _\ \  / _ `/ // / _  / / _ \  / __/ _ `/ / / 
  /_/_/  /_/___/  \_,_/\_,_/\_,_/_/\___/  \__/\_,_/_/_/  
"""
logo = "\033[34m" + logo + "\033[0m"
print(logo)

PORT_Opend = 2119  #Port number the server is runing

#  PyAudio
audieo = pyaudio.PyAudio()        # Initializes the audio system
stream_in = audieo.open(format=SAMPLE, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=FRAMS)  

# captures voice

stream_out = audieo.open(format=SAMPLE, channels=CHANNEL, rate=RATE, output=True, frames_per_buffer=FRAMS)
# plays the user’s voice


#  TCP Server
srver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a TCP socket
srver.bind(("0.0.0.0", PORT_Opend)) # bind in any host and port 2119
srver.listen(1)
print(" Wait for connection...")
connection, addressUser = srver.accept()
print(f" Connected by {addressUser}")



def sent_audio():
    while True:
        try:
            data = stream_in.read(FRAMS, exception_on_overflow=False) # Continuously geting dta from user
            ciphertext = YMS_enc.encrypt(data)   # Encrypt before sending
            connection.sendall(ciphertext) # Sends encrypted audio to server
        except:
            break

def receive_audio():
    while True:
        try:
            data = connection.recv(2048)                  #reciving up to 2048 bytes
            if not data:                            # connection closed
                break
            plaintext = YMS_dec.decrypt(data)    # Decrypt before playing
            stream_out.write(plaintext)             # Decrypts the audio
        except:
            break

tsend = threading.Thread(target=sent_audio)            # Handles sending audio
trecive = threading.Thread(target=receive_audio)         # Handles receiving audio
tsend.start()
trecive.start()

tsend.join()
trecive.join()

# closed the connection

connection.close()
stream_in.close()
stream_out.close()
audieo.terminate()
