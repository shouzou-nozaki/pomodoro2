import TkEasyGUI as sg
import datetime
import time
import pygame

# 設定
RAP_SEC = 25 * 60  # 作業時間（25分）
BREAK_SEC = 5 * 60  # 休憩時間（5分）
RAP_SOUND = "./assets/beep.mp3"
GOAL_SOUND = "./assets/levelup.mp3"
SECTION_COUNT = 4

# pygame初期化
pygame.mixer.init()
pygame.mixer.music.load(RAP_SOUND)

# GUIレイアウト
layout = [
    [sg.Text("25:00", key="-OUTPUT-", font=("Helvetica", 60))],
    [sg.Button("スタート", font=("Helvetica", 10)), 
     sg.Button("ストップ", font=("Helvetica", 10)), 
     sg.Button("リセット", font=("Helvetica", 10))]
]

# ウィンドウ作成
window = sg.Window("ポモドーロタイマー", layout)

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
        if not running:
            start_time = time.time()  # 現在時刻を記録
            running = True

    if event == "ストップ":
        running = False

    if event == "リセット":
        running = False
        start_time = None
        rap_count = 0

        mode = "WORK"
        window["-OUTPUT-"].update("25:00")

    if running and start_time:
        elapsed = time.time() - start_time  # 経過秒数
        total_time = RAP_SEC if mode == "WORK" else BREAK_SEC
        remain = total_time - int(elapsed)

        if remain <= 0:
            # 音を鳴らす
            pygame.mixer.music.play()
            # 作業→休憩 or 休憩→作業の切り替え
            mode = "BREAK" if mode == "WORK" else "WORK"
            start_time = time.time()  # タイマーリセット
            total_time = RAP_SEC if mode == "WORK" else BREAK_SEC
            remain = total_time

        # `MM:SS` 形式に変換して表示更新
        formatted_time = f"{remain // 60:02d}:{remain % 60:02d}"
        window["-OUTPUT-"].update(formatted_time)

window.close()
