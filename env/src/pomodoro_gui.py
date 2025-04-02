import TkEasyGUI as sg
import datetime
import pygame

# 全体の設定
SOUND_FILE = "./assets/levelup.mp3"
RAP_SEC = 25 * 60
# 再生するための設定
pygame.mixer.init()
pygame.mixer.music.load(SOUND_FILE)

layout = [
    [sg.Text("25:00", key="-output-", font=("Helvetica", 70))],
    [sg.Button("スタート", font=("Helvetica", 10)), sg.Button("ストップ", font=("Helvetica", 10)), sg.Button("リセット", font=("Helvetica", 10))],
]
# ウィンドウの作成
window = sg.Window("ポモドーロタイマー", layout)
start_time = None
# イベントループ
while True:
    event, _ = window.read(timeout=10)
    
    if event == sg.WINDOW_CLOSED:
        break

    if event == "スタート":
        start_time = datetime.datetime.now()
    if event == "ストップ": 
        break
    if event == "リセット":
        break
    if start_time is None:
        continue
    # 経過時間を計算
    now = datetime.datetime.now()
    delta = now - start_time
    if delta.seconds >= RAP_SEC:
        pygame.mixer.music.play()
        start_time = None
        window['-output-'].update("00:00")
        continue
    # 残り時間を表示
    remain = RAP_SEC - delta.seconds
    formatted_time = f"{remain // 60:02d}:{remain % 60:02d}"
    window['-output-'].update(formatted_time)
window.close()
    
    