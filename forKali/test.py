# -*- coding: utf-8 -*-
import socket
import threading
from Crypto.Cipher import AES
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader, SoundRecorder
from kivy.clock import Clock
import os

# ------------------ CONFIGURATION ------------------
SERVER_IP = "192.168.1.10"   # Replace with your server IP
SERVER_PORT = 5000
CHUNK = 1024                 # Number of bytes per audio chunk
KEY = b"This1sH4k3R1o9!!"    # 16-byte AES key
NONCE = b"123456789012"      # 12-byte fixed nonce
# ---------------------------------------------------

cipher_enc = AES.new(KEY, AES.MODE_EAX, nonce=NONCE)
cipher_dec = AES.new(KEY, AES.MODE_EAX, nonce=NONCE)

class AudioChatApp(App):

    def build(self):
        btn = Button(text="Start Encrypted Audio Chat")
        btn.bind(on_press=self.start_audio_chat)
        return btn

    def start_audio_chat(self, instance):
        # Start the socket client
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER_IP, SERVER_PORT))

        # Start sending & receiving threads
        threading.Thread(target=self.send_audio).start()
        threading.Thread(target=self.receive_audio).start()

    # ----------------- SEND AUDIO -------------------
    def send_audio(self):
        recorder = SoundRecorder()
        audio_file = "temp_audio.wav"

        while True:
            try:
                # Record small chunk (0.1 sec)
                recorder.start(audio_file)
                Clock.schedule_once(lambda dt: recorder.stop(), 0.1)
                
                # Read recorded audio
                if os.path.exists(audio_file):
                    with open(audio_file, "rb") as f:
                        data = f.read()
                    if data:
                        ciphertext = cipher_enc.encrypt(data)
                        self.client.sendall(ciphertext)
                    os.remove(audio_file)
            except Exception as e:
                print("Send audio error:", e)
                break

    # ----------------- RECEIVE AUDIO ----------------
    def receive_audio(self):
        while True:
            try:
                data = self.client.recv(CHUNK*2)
                if not data:
                    break

                plaintext = cipher_dec.decrypt(data)

                # Save decrypted chunk temporarily
                with open("recv_chunk.wav", "wb") as f:
                    f.write(plaintext)

                # Play the chunk
                sound = SoundLoader.load("recv_chunk.wav")
                if sound:
                    sound.play()
            except Exception as e:
                print("Receive audio error:", e)
                break

if __name__ == "__main__":
    AudioChatApp().run()
