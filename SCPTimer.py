import tkinter as tk
import pygetwindow as gw
import pywinauto
import keyboard
from datetime import datetime, timedelta


class TimerOverlay:
    def __init__(self, game_window):
        self.game_window = game_window
        self.overlay = tk.Toplevel()
        self.overlay.geometry("200x230")
        self.overlay.wm_attributes("-topmost", True)
        self.overlay.wm_attributes("-disabled", True)
        self.overlay.overrideredirect(True)

        self.countdown_label_11 = tk.Label(self.overlay, text="Light Decontamination:")
        self.countdown_label_11.pack(pady=5)
        self.countdown_label_11_timer = tk.Label(self.overlay, text="")
        self.countdown_label_11_timer.pack()

        self.countdown_label_5 = tk.Label(self.overlay, text="Spawn Wave:")
        self.countdown_label_5.pack(pady=5)
        self.countdown_label_5_timer = tk.Label(self.overlay, text="")
        self.countdown_label_5_timer.pack()

        self.spawns_label = tk.Label(self.overlay, text="")
        self.spawns_label.pack()

        self.made_by_label = tk.Label(self.overlay, text="Made By SkippyzNJiff!")
        self.made_by_label.pack(pady=5)

        self.version_label = tk.Label(self.overlay, text="V 1.00")
        self.version_label.pack()

        self.current_number = 1
        self.countdown11_end_time = datetime.now() + timedelta(minutes=11, seconds=30)
        self.countdown5_end_time = datetime.now() + timedelta(minutes=5)
        self.update_countdowns()  # Start the countdown updates
        self.count_spawns()

        # Bind Ctrl+K to reset timers globally
        keyboard.add_hotkey("ctrl+k", self.reset_timers)  # Global key binding

    def update_countdowns(self):
        self.update_countdown11()
        self.update_countdown5()

    def update_countdown11(self):
        remaining_time_11 = self.countdown11_end_time - datetime.now()
        if remaining_time_11.total_seconds() <= 0:
            self.countdown_label_11_timer.config(text="Complete!")
        else:
            minutes_11 = remaining_time_11.seconds // 60
            seconds_11 = remaining_time_11.seconds % 60
            self.countdown_label_11_timer.config(text=f"{minutes_11:02d}:{seconds_11:02d}")
            self.overlay.after(250, self.update_countdown11)

    def update_countdown5(self):
        remaining_time_5 = self.countdown5_end_time - datetime.now()
        if remaining_time_5.total_seconds() <= 0:
            self.countdown_label_5_timer.config(text="Complete!")
            self.current_number += 1
            self.countdown5_end_time += timedelta(minutes=5)
            self.overlay.after(1000, self.update_countdown5)  # Wait for 1 second
        else:
            minutes_5 = remaining_time_5.seconds // 60
            seconds_5 = remaining_time_5.seconds % 60
            self.countdown_label_5_timer.config(text=f"{minutes_5:02d}:{seconds_5:02d}")
            self.overlay.after(250, self.update_countdown5)

    def count_spawns(self):
        self.spawns_label.config(text=f"Spawns: {self.current_number}")
        self.current_number += 1
        self.overlay.after(300000, self.count_spawns)  # Wait for 5 minutes (300,000 milliseconds)

    def reset_timers(self):
        self.countdown_label_11_timer.config(text="")
        self.countdown_label_5_timer.config(text="")
        self.spawns_label.config(text="")
        self.current_number = 1
        self.countdown11_end_time = datetime.now() + timedelta(minutes=11, seconds=30)
        self.countdown5_end_time = datetime.now() + timedelta(minutes=5)


def create_overlay():
    game_window = gw.getWindowsWithTitle('SCPSL')[0]
    game_hwnd = game_window._hWnd

    game_position = (game_window.left, game_window.top)
    game_size = (game_window.width, game_window.height)

    overlay = TimerOverlay(game_window)

    overlay_width = overlay.overlay.winfo_reqwidth()
    overlay_height = overlay.overlay.winfo_reqheight()
    x = game_position[0] + game_size[0] - overlay_width
    y = game_position[1]
    overlay.overlay.geometry(f"+{x}+{y}")

    pywinauto.win32functions.SetWindowLong(overlay.overlay.winfo_id(), pywinauto.win32defines.GWL_HWNDPARENT, game_hwnd)

    overlay.overlay.mainloop()


def main():
    create_overlay()
    tk.mainloop()


if __name__ == "__main__":
    main()
