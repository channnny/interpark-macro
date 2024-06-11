import tkinter as tk
from view.MacroView import MacroView
from controller.MacroController import MacroController

# 필요한 좌석 수
NEED_SEAT_CNT = 2

# 좌석 클릭 후 버튼이 커지는 현상으로 x 좌표 간격 조정 값(해상도/콘서트장 별로 상이할 수 있음)
OFFSET = 20

# 취켓팅 성공 후 알람 유무
ALARM = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("please win this war..")
    root.geometry("1600x1200")

    # 컨트롤러와 뷰 생성 및 연결
    controller = MacroController(NEED_SEAT_CNT, OFFSET, ALARM, None)
    view = MacroView(root, controller)
    controller.view = view

    root.mainloop()