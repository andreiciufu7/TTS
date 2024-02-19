import tkinter as tk
from tkinter import filedialog
import time
from pydub import AudioSegment
import subprocess
import os
import auth
import pyglet

class PDFtoTextConverter:
    def __init__(self, master):
        self.master = master
        self.file_path = None
        self.audio_file = None
        self.current_position = 0
        self.playing = False
        self.paused = False
        self.player = None
        master.title('PDF to Text Converter')

        self.select_button = tk.Button(master, text='Select File', command=self.select_file)
        self.select_button.grid(row=0, column=0, padx=5, pady=5)

        self.play_button = tk.Button(master, text='Play', command=self.play_pause_audio)
        self.play_button.grid(row=0, column=1, padx=5, pady=5)

        self.ff_button = tk.Button(master, text='>>10s', command=self.fast_forward)
        self.ff_button.grid(row=0, column=2, padx=5, pady=5)

        self.rw_button = tk.Button(master, text='<<10s', command=self.rewind)
        self.rw_button.grid(row=0, column=3, padx=5, pady=5)

        self.current_time_label = tk.Label(master, text='00:00')
        self.current_time_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.remaining_time_label = tk.Label(master, text='00:00')
        self.remaining_time_label.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        self.progress_bar = tk.Scale(master, orient=tk.HORIZONTAL, from_=0, to=100, length=300)
        self.progress_bar.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        self.update_time_labels()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('PDF files', '*.pdf')])
        if file_path:
            self.file_path = file_path
            auth.upCloud(file_path)

    def load_audio_file(self):
        if self.file_path:
            self.audio_file = AudioSegment.from_file(self.file_path, format="mp3")

    def play_pause_audio(self):
        if os.path.exists(r'TTS/output.mp3'):
            if self.paused:
                # Resume playback
                self.player.play()
                self.play_button.configure(text="Pause")
                self.paused = False
                self.playing = True
            elif self.playing:
                # Pause playback
                # Pause playback
                self.player.pause()
                self.play_button.configure(text="Play")
                self.paused = True
                self.playing = False
            else:
               # Start playback from the beginning
                audio_path = os.path.abspath(r'TTS/output.mp3')
                self.player = pyglet.media.Player()
                source = pyglet.media.load(audio_path)
                self.current_position = 0
                self.player.queue(source)
                self.player.play()
                self.play_button.configure(text="Pause")
                self.paused = False
                self.playing = True
            if self.playing:
                self.update_time_labels()
        else:
            # Output.mp3 file doesn't exist
            # You can handle this case based on your requirements
            pass

    def fast_forward(self):
        if self.player.playing:
            current_time = self.player.time + 5  # Add 5 seconds
            current_time = min(current_time, self.player.source.duration)
            self.player.seek(current_time)
        elif self.audio_file:
            self.current_position += 5000  # Add 5 seconds
            self.current_position = min(self.current_position, len(self.audio_file) * 1000)
            self.audio_file = self.audio_file[self.current_position // 1000:]
            self.player.queue(
                pyglet.media.AudioData(self.audio_file.export(), self.audio_file.frame_rate,
                                    self.audio_file.sample_width, self.audio_file.channels))

    def rewind(self):
        if self.player.playing:
            current_time = self.player.time - 5  # Subtract 5 seconds
            current_time = max(current_time, 0)
            self.player.seek(current_time)
        elif self.audio_file:
            self.current_position -= 5000  # Subtract 5 seconds
            self.current_position = max(self.current_position, 0)
            self.audio_file = self.audio_file[self.current_position // 1000:]
            self.player.queue(
                pyglet.media.AudioData(self.audio_file.export(), self.audio_file.frame_rate,
                                    self.audio_file.sample_width, self.audio_file.channels))


    def update_time_labels(self):
        if self.player:
            current_time = self.player.time
            total_duration = self.player.source.duration

            # Update progress bar
            progress = (current_time / total_duration) * 100
            self.progress_bar.set(progress)

            # Format time values as mm:ss
            current_time_formatted = time.strftime('%M:%S', time.gmtime(current_time))
            remaining_time = total_duration - current_time
            remaining_time_formatted = time.strftime('%M:%S', time.gmtime(remaining_time))

            # Update labels
            self.current_time_label.configure(text=current_time_formatted)
            self.remaining_time_label.configure(text=remaining_time_formatted)

        # Schedule next update after 100 milliseconds if playing
        if self.playing:
            self.master.after(100, self.update_time_labels)

root = tk.Tk()
converter = PDFtoTextConverter(root)
root.mainloop()
