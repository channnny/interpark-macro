import pygame

# 음악 재생을 위한 클래스
class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.mp3_file = "resource/alarm.mp3"  # 알람음 파일 설정
        
    def play_music(self):
        pygame.mixer.music.load(self.mp3_file)
        pygame.mixer.music.play(loops=-1)  # 음악 무한 반복 재생
        
    def stop_music(self):
        pygame.mixer.music.stop()  # 음악 정지