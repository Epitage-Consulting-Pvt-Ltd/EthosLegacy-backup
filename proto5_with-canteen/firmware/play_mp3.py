# import pygame
# import os

# class MP3Player:
#     def __init__(self, thank_you, rejected):
#         # Get the current directory
#         current_dir = os.path.dirname(os.path.abspath(__file__))
        
#         # Construct the full paths for the MP3 files
#         self.thank_you_path = os.path.join(current_dir, thank_you.mp3)
#         self.rejected_path = os.path.join(current_dir, rejected.mp3)
    
#     def play_thank_you(self):
#         self._play_mp3(self.thank_you_path)

#     def play_rejected(self):
#         self._play_mp3(self.rejected_path)

#     def _play_mp3(self, file_path):
#         # Initialize Pygame with the dummy video driver
#         pygame.display.init()

#         pygame.mixer.init()
#         pygame.mixer.music.load(file_path)

#         print("Playing:", file_path)
#         pygame.mixer.music.play()

#         # Wait for the music to finish playing
#         pygame.mixer.music.set_endevent(pygame.USEREVENT)
#         pygame.event.wait()

#         # Quit Pygame properly
#         pygame.mixer.quit()
#         pygame.display.quit()

#         print("Playback complete")
import os
import pygame

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()

        # Use the absolute paths to the MP3 files
        script_dir = os.path.dirname(__file__)
        self.thank_you_sound = None
        self.rejected_sound = None
        
        try:
            self.thank_you_sound = pygame.mixer.Sound(os.path.join(script_dir, "thank-you.mp3"))
            self.rejected_sound = pygame.mixer.Sound(os.path.join(script_dir, "rejected.mp3"))
        except pygame.error as e:
            print("Error loading sound files:", e)

    def play_thank_you(self):
        if self.thank_you_sound:
            try:
                self.thank_you_sound.play()
            except pygame.error as e:
                print("Error playing thank you sound:", e)
        else:
            print("Thank you sound not loaded.")

    def play_rejected(self):
        if self.rejected_sound:
            try:
                self.rejected_sound.play()
            except pygame.error as e:
                print("Error playing rejected sound:", e)
        else:
            print("Rejected sound not loaded.")






