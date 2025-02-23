import tkinter as tk
from tkinter import messagebox, filedialog
import time
import threading
import pygame
import random

pygame.mixer.init()

default_sound = "/Users/sakibul/Downloads/All projects/screen_break_reminder/sound/s1.mp3"
pygame.mixer.music.load(default_sound) 

class ScreenBreakReminder:
    def __init__(self, master):
        self.master = master
        master.title("Screen Break Reminder")
        master.geometry("400x700")
        master.configure(bg="#e0e0e0")  

        # Gradient background animation
        self.gradient_colors = ["#ff9a9e", "#fad0c4", "#fad0c4", "#fbc2eb", "#a18cd1"]
        self.current_color_index = 0
        self.animate_background()

        # Input section
        self.time_label = tk.Label(master, text="Set Time (in seconds):", bg="#e0e0e0", font=("Arial", 12))
        self.time_label.pack(pady=5)

        self.time_entry = tk.Entry(master, font=("Arial", 12), bg="white")
        self.time_entry.pack(pady=5)

        self.break_label = tk.Label(master, text="Break Duration (in seconds):", bg="#e0e0e0", font=("Arial", 12))
        self.break_label.pack(pady=5)
        
        self.break_entry = tk.Entry(master, font=("Arial", 12), bg="white")
        self.break_entry.pack(pady=5)

        self.start_button = tk.Button(master, text="🔔 Start Reminder", command=self.start_reminder,
                                      bg="#32CD32", fg="black", font=("Arial", 12, "bold"), relief="raised", padx=10, pady=5)
        self.start_button.pack(pady=5)
        self.add_hover_effects(self.start_button, "#228B22", "#32CD32")

        self.stop_button = tk.Button(master, text="⏹️ Stop Reminder", command=self.stop_reminder,
                                     bg="#FF4500", fg="black", font=("Arial", 12, "bold"), relief="raised", padx=10, pady=5)
        self.stop_button.pack(pady=5)
        self.add_hover_effects(self.stop_button, "#B22222", "#FF4500")

        self.sound_button = tk.Button(master, text="🎵 Choose Sound", command=self.choose_sound,
                                      bg="#1E90FF", fg="black", font=("Arial", 12, "bold"), relief="raised", padx=10, pady=5)
        self.sound_button.pack(pady=5)
        self.add_hover_effects(self.sound_button, "#4682B4", "#1E90FF")

        self.volume_label = tk.Label(master, text="Volume Control:", bg="#e0e0e0", font=("Arial", 12))
        self.volume_label.pack(pady=5)
        
        self.volume_slider = tk.Scale(master, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.set_volume, bg="#e0e0e0")
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=5)

        self.timer_label = tk.Label(master, text="Next break in: ", bg="#e0e0e0", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        self.breaks_taken = 0
        self.breaks_label = tk.Label(master, text=f"Breaks Taken: {self.breaks_taken}", bg="#e0e0e0", font=("Arial", 12))
        self.breaks_label.pack(pady=5)

        self.progress_canvas = tk.Canvas(master, width=200, height=200, bg="#e0e0e0", highlightthickness=0)
        self.progress_canvas.pack(pady=10)
        
        self.motivation_frame = tk.Frame(master, bg="#FFD700", height=100, width=350)
        self.motivation_frame.pack(pady=10)

        self.motivation_label = tk.Label(self.motivation_frame, text="", bg="#FFD700", font=("Arial", 14, "bold"))
        self.motivation_label.pack(pady=20)

        self.is_running = False
        self.sound_file = default_sound

        self.quotes = [
            "Take a deep breath and stretch!",
            "Your eyes need rest too. Blink and relax!",
            "Great job! Keep a healthy balance.",
            "Stand up, walk a little, and refresh!",
            "Stay hydrated! Take a sip of water."
        ]

        self.activities = [
            "Stretch for 2 minutes.",
            "Look away from the screen and focus on a distant object.",
            "Take a short walk around the room.",
            "Do 10 jumping jacks.",
            "Close your eyes and take 5 deep breaths."
        ]

    def animate_background(self):
        self.master.configure(bg=self.gradient_colors[self.current_color_index])
        self.current_color_index = (self.current_color_index + 1) % len(self.gradient_colors)
        self.master.after(3000, self.animate_background)

    def add_hover_effects(self, widget, hover_color, normal_color):
        def on_enter(event):
            widget.config(bg=hover_color)
        def on_leave(event):
            widget.config(bg=normal_color)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def start_reminder(self):
        try:
            self.interval = int(self.time_entry.get())
            self.break_duration = int(self.break_entry.get())
            self.is_running = True
            self.update_timer(self.interval)
            self.remind_thread = threading.Thread(target=self.remind)
            self.remind_thread.daemon = True
            self.remind_thread.start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def stop_reminder(self):
        self.is_running = False

    def choose_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
        if file_path:
            self.sound_file = file_path
            pygame.mixer.music.load(self.sound_file)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_timer(self, seconds):
        if self.is_running:
            self.timer_label.config(text=f"Next break in: {seconds} seconds")
            self.update_progress_circle(seconds, self.interval)
            if seconds > 0:
                self.master.after(1000, self.update_timer, seconds - 1)

    def update_progress_circle(self, time_left, total_time):
        self.progress_canvas.delete("all")
        angle = (1 - (time_left / total_time)) * 360
        self.progress_canvas.create_oval(10, 10, 190, 190, outline="#ccc", width=10)
        self.progress_canvas.create_arc(10, 10, 190, 190, start=90, extent=-angle, fill="#32CD32")

    def remind(self):
        while self.is_running:
            time.sleep(self.interval)
            if self.is_running:
                pygame.mixer.music.play()
                self.show_break_message()
                self.breaks_taken += 1
                self.breaks_label.config(text=f"Breaks Taken: {self.breaks_taken}")
                self.update_timer(self.interval)
                time.sleep(self.break_duration)

    def show_break_message(self):
        quote = random.choice(self.quotes)
        activity = random.choice(self.activities)
        self.motivation_label.config(text=f"{quote}\n{activity}")
        self.animate_motivation()

    def animate_motivation(self):
        colors = ["#FF4500", "#32CD32", "#1E90FF", "#FFD700", "#8A2BE2"]
        for _ in range(3):
            self.motivation_frame.config(bg=random.choice(colors))
            self.master.update()
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    reminder_app = ScreenBreakReminder(root)
    root.mainloop()
