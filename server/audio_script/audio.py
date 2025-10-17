# audio for server side

import socket       # to crete TCP connection
import pyaudio      # to control audio input and output
import threading    # To  send & receive at the same time without blocking


# Audio settings
CHUNK = 1024      
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100   # in every second 44,100 or 44.1KHz audios are captured from the mic or sent to the speaker.


logo = """

__  ____  _______               ___                 ____
 \ \/ /  |/  / __/ ___ ___ _____/ (____    _______ _/ / /
  \  / /|_/ _\ \  / _ `/ // / _  / / _ \  / __/ _ `/ / / 
  /_/_/  /_/___/  \_,_/\_,_/\_,_/_/\___/  \__/\_,_/_/_/  
                                                         

"""



logo = "\033[34m" + logo + "\033[0m"

print(logo)


PORT = 2119
# PyAudio
audio = pyaudio.PyAudio()
stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", PORT))
server.listen(1)
print(" Waiting for connection...")
conn, addr = server.accept()
print(f" Connected by {addr}")

def send_audio():
    while True:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            conn.sendall(data)
        except:
            break

def receive_audio():
    while True:
        try:
            data = conn.recv(CHUNK)
            if not data:
                break
            stream_out.write(data)
        except:
            break

t1 = threading.Thread(target=send_audio)
t2 = threading.Thread(target=receive_audio)
t1.start()
t2.start()

t1.join()
t2.join()

conn.close()
stream_in.close()
stream_out.close()
audio.terminate()
