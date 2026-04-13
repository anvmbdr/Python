import pygame
import os

class MusicPlayer:

    def __init__(self):
        pygame.mixer.init()

        self.playlist = []          # List of track file paths
        self.track_names = []       # Display names
        self.current_index = 0      # Current track index
        self.is_playing = False
        self.volume = 0.7           # Default volume (0.0 - 1.0)
        pygame.mixer.music.set_volume(self.volume)

    def load_playlist(self, music_folder):
        supported = (".mp3", ".wav", ".ogg", ".flac")
        if not os.path.exists(music_folder):
            print(f"[Player] Folder '{music_folder}' not found.")
            return

        files = sorted([
            f for f in os.listdir(music_folder)
            if f.lower().endswith(supported)
        ])

        self.playlist = [os.path.join(music_folder, f) for f in files]
        self.track_names = [os.path.splitext(f)[0] for f in files]

        if self.playlist:
            print(f"[Player] Loaded {len(self.playlist)} track(s).")
        else:
            print("[Player] No audio files found in folder.")

    def add_track(self, filepath):
        if os.path.exists(filepath):
            self.playlist.append(filepath)
            name = os.path.splitext(os.path.basename(filepath))[0]
            self.track_names.append(name)

    def play(self):
        if not self.playlist:
            print("[Player] Playlist is empty.")
            return
        try:
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True
            print(f"[Player] Playing: {self.get_current_name()}")
        except Exception as e:
            print(f"[Player] Error playing track: {e}")

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        print("[Player] Stopped.")

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        if self.is_playing:
            self.play()
        print(f"[Player] Next: {self.get_current_name()}")

    def prev_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        if self.is_playing:
            self.play()
        print(f"[Player] Previous: {self.get_current_name()}")

    def volume_up(self):
        self.volume = min(1.0, self.volume + 0.1)
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(0.0, self.volume - 0.1)
        pygame.mixer.music.set_volume(self.volume)

    def get_current_name(self):
        if self.playlist:
            return self.track_names[self.current_index]
        return "No track loaded"

    def get_status(self):
        return "▶ Playing" if self.is_playing and pygame.mixer.music.get_busy() else "■ Stopped"

    def check_auto_next(self):
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.next_track()
