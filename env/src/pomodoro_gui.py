import TkEasyGUI as sg
import time
import pygame

# 設定
RAP_SEC = 25 * 60  # 作業時間（25分）
BREAK_SEC = 5 * 60  # 休憩時間（5分）
RAP_SOUND = "./assets/beep.mp3"
GOAL_SOUND = "./assets/levelup.mp3"
APP_ICON = "./assets/tomato.ico"
MAX_RAP_COUNT = 1

# pygame初期化
pygame.mixer.init()
pygame.mixer.music.load(RAP_SOUND)

# GUIレイアウト
layout = [
    [sg.Text("0 RAP目",   key="-RAP-",    font=("Helvetica", 10))],
    [sg.Text("25:00",     key="-OUTPUT-", font=("Helvetica", 60))],
    [
        sg.Button("スタート", font=("Helvetica", 10)), 
        sg.Button("ストップ" ,   font=("Helvetica", 10)), 
        sg.Button("リセット",  font=("Helvetica", 10))]
]

# ウィンドウ作成
window = sg.Window("ポモドーロタイマー", layout, icon=APP_ICON)

# タイマー用変数
start_time = None
running = False
rap_count = 0
mode = "WORK"  # "WORK"（作業） or "BREAK"（休憩）

# メインループ
while True:
    event, _ = window.read(timeout=100)

    if event == sg.WINDOW_CLOSED:
        break

    if event == "スタート":
        if rap_count == 0:
            rap_count += 1 # RAPカウント更新
            window["-RAP-"].update(f"{rap_count} RAP目")
        if not running:
            start_time = time.time()  # 現在時刻を記録
            running = True

    if event == "ストップ":
        running = False

    if event == "リセット":
        running = False
        start_time = None
        mode = "WORK"
        rap_count = 0
        window["-RAP-"].update(f"{rap_count} RAP目")
        window["-OUTPUT-"].update("25:00")

    if running and start_time:
        elapsed = time.time() - start_time  # 経過秒数
        total_time = RAP_SEC if mode == "WORK" else BREAK_SEC
        remain = total_time - int(elapsed)

        if remain <= 0:
            if rap_count < MAX_RAP_COUNT:
                # 作業終了後は休憩へ、休憩終了後は次のRAPへ
                if mode == "WORK":
                    pygame.mixer.music.load(RAP_SOUND)
                    pygame.mixer.music.play()
                    mode = "BREAK"
                else:
                    pygame.mixer.music.load(RAP_SOUND)
                    pygame.mixer.music.play()
                    rap_count += 1
                    window["-RAP-"].update(f"{rap_count} RAP目")
                    mode = "WORK"
                start_time = time.time()
            else:
                # 最終回終了 → ゴール音＆タイマー停止
                pygame.mixer.music.load(GOAL_SOUND)
                pygame.mixer.music.play()
                running = False
                window["-OUTPUT-"].update("00:00")
                continue  # 下のupdateをスキップ
        # `MM:SS` 形式に変換して表示更新
        formatted_time = f"{remain // 60:02d}:{remain % 60:02d}"
        window["-OUTPUT-"].update(formatted_time)

window.close()
