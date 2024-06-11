import keyboard
import pyautogui
from PIL import ImageGrab
from model.Macro import Macro

class MacroController:
    def __init__(self, need_seat_cnt, offset, alarm, view):
        self.macro = Macro(need_seat_cnt, offset, alarm)
        self.view = view
        keyboard.add_hotkey(';', self.stop_macro)

    def start_macro(self):
        self.macro.start_macro()

    def stop_macro(self):
        self.macro.stop_macro()

    def select_seat_area(self):
        left_top = self._wait_for_key('a')
        right_bottom = self._wait_for_key('b')
        self.macro.seat_axis = [left_top, right_bottom]
        print(f"Selected seat point: {self.macro.seat_axis}")
        self.view.capture_region(left_top, right_bottom)

    def select_seat_grade(self):
        my_class_list = []
        screen = ImageGrab.grab()
        while True:
            if keyboard.read_key() == "a":
                x, y = pyautogui.position()
                rgb = screen.getpixel((x, y))
                print(f"Selected Color: {rgb}")
                my_class_list.append(rgb)
            if keyboard.read_key() == "c":
                self.macro.seat_class = set(my_class_list)
                self.view.update_listbox(self.macro.seat_class)
                break

    def select_refresh_axis(self):
        self.macro.refresh_axis = self._wait_for_key('a')

    def select_complete_axis(self):
        self.macro.pay_axis = self._wait_for_key('a')

    def on_listbox_click(self, event):
        selected_index = self.view.color_listbox.curselection()
        if selected_index:
            selected_color = self.view.color_listbox.get(selected_index)
            self.view.draw_color_rectangle(selected_color)

    def _wait_for_key(self, key):
        while True:
            if keyboard.read_key() == key:
                return pyautogui.position()
