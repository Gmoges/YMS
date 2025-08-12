import socket
import pyaudio
import threading

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
PORT = int(input("Enter port: "))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
print("📞 Connected to server")

def send_audio():
    while True:
        try:
            data = stream_in.read(CHUNK, exception_on_overflow=False)
            client.sendall(data)
        except:
            break

def receive_audio():
    while True:
        try:
            data = client.recv(CHUNK)
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

client.close()
stream_in.close()
stream_out.close()
audio.terminate()
