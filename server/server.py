import socket
import pyaudio
import threading

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PORT = 2119
# PyAudio
audio = pyaudio.PyAudio()
stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# TCP Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", PORT))
server.listen(1)
print("🎧 Waiting for connection...")
conn, addr = server.accept()
print(f"✅ Connected by {addr}")

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
