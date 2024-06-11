import random
import pyautogui
import threading
import time
from PIL import ImageGrab
from datetime import datetime
from model import MusicPlayer

class Macro:
    def __init__(self, need_seat_cnt, offset, alarm):
        self.is_running = False
        self.running_cnt = 1 # 매크로 실행 카운트

        self.seat_class = set()
        self.seat_axis = []
        self.refresh_axis = []
        self.pay_axis = []

        self.need_seat_cnt = need_seat_cnt # 필요 좌석 수(연석인 경우 2)
        self.offset = offset # 해상도, 콘서트장 별로 상이할 수 있음
        
        self.music_player = MusicPlayer.MusicPlayer()
        self.alarm = alarm

    def start_macro(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self.run_macro_loop).start()

    def stop_macro(self):
        self.is_running = False
        self.music_player.stop_music()

    def run_macro_loop(self):
        while self.is_running:
            try:
                self.perform_macro_actions()
            except Exception as e:
                print(f"Macro error: {e}")
                self.is_running = False

    def perform_macro_actions(self):
        print(f"Running macro iteration: {self.running_cnt}...")
        self.click_refresh()
        self.search_seat()

    def click(self, x, y):
        pyautogui.click(x, y)
    
    def click_seat(self, x, y):
        offset_x = 0
        offset_y = 0

        for _ in range(self.need_seat_cnt):
            if self.need_seat_cnt == 1:
                return self.click(x, y)
            
            self.click(x + offset_x, y + offset_y)
            offset_x += self.offset
    
    def click_pay(self):
        self.click(self.pay_axis[0], self.pay_axis[1])

    def click_refresh(self):
        self.click(self.refresh_axis[0], self.refresh_axis[1])
        time.sleep(random.random())
        self.running_cnt += 1

    def print_success_time(self):
        current_time = datetime.now().strftime("%Y년 %m월 %d일 %p %I:%M")
        print(f"취켓팅 성공 시간: {current_time}")
    
    def complete_reservation(self, x, y):
        self.print_success_time()
        self.click_seat(x, y)
        self.click_pay()
        self.is_running = False
        if self.alarm:
            self.music_player.play_music()

    def is_color_match(self, rgb, target_colors, delta_error=10):
        for r, g, b in target_colors:
            if all(abs(channel - target) <= delta_error for channel, target in zip(rgb, (r, g, b))):
                return True
        return False
    
    def search_seat(self):
        screen = ImageGrab.grab()
        for y in range(self.seat_axis[0][1], self.seat_axis[1][1], 7):
            for x in range(self.seat_axis[0][0], self.seat_axis[1][0], 7):
                rgb = screen.getpixel((x, y))

                if self.is_color_match(rgb, self.seat_class):
                    if self.need_seat_cnt == 1:
                        return self.complete_reservation(x, y)

                    if self.are_adjacent_seats_available(screen, x, y):
                        return self.complete_reservation(x, y)

    def are_adjacent_seats_available(self, screen, x, y):
        for i in range(1, self.need_seat_cnt):
            offset = i * self.offset
            if not self.is_adjacent_seat_available(screen, x, y, offset):
                return False
        return True

    def is_adjacent_seat_available(self, screen, x, y, offset):
        adjacent_rgb = screen.getpixel((x + offset, y))
        return self.is_color_match(adjacent_rgb, self.seat_class)