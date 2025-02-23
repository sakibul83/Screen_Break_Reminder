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
        master.geometry("400x600") 
        master.configure(bg="#e0e0e0")  

        # Input section
        self.time_label = tk.Label(master, text="Set Time (in seconds):", bg="#e0e0e0", font=("Arial", 12))
        self.time_label.pack(pady=5)

        self.time_entry = tk.Entry(master, font=("Arial", 12), bg="white")
        self.time_entry.pack(pady=5)


        self.start_button = tk.Button(master, text="Start Reminder", command=self.start_reminder,
                                       bg="#32CD32", fg="black", font=("Arial", 12, "bold"), activebackground="#228B22", relief="raised", padx=10, pady=5)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop Reminder", command=self.stop_reminder,
                                      bg="#FF4500", fg="black", font=("Arial", 12, "bold"), activebackground="#B22222", relief="raised", padx=10, pady=5)
        self.stop_button.pack(pady=5)

        self.sound_button = tk.Button(master, text="Choose Sound", command=self.choose_sound,
                                       bg="#1E90FF", fg="black", font=("Arial", 12, "bold"), activebackground="#4682B4", relief="raised", padx=10, pady=5)
        self.sound_button.pack(pady=5)

        self.timer_label = tk.Label(master, text="Next break in: ", bg="#e0e0e0", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        self.breaks_taken = 0
        self.breaks_label = tk.Label(master, text=f"Breaks Taken: {self.breaks_taken}", bg="#e0e0e0", font=("Arial", 12))
        self.breaks_label.pack(pady=5)

     
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
            "Stretch for 2 mintues.",
            "Look away from the screen and focus on a distant object.",
            "Take a short walk around the room.",
            "Do 10 jumping jacks.",
            "Close your eyes and take 5 deep breaths."
        ]

    def start_reminder(self):
        try:
            self.interval = int(self.time_entry.get())
            self.is_running = True
            self.update_timer(self.interval)
            self.remind_thread = threading.Thread(target=self.remind)
            self.remind_thread.daemon = True
            self.remind_thread.start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def stop_reminder(self):
        self.is_running = False

    def choose_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3"), ("WAV files", "*.wav")])
        if file_path:
            self.sound_file = file_path
            pygame.mixer.music.load(self.sound_file)

    def update_timer(self, seconds):
        if self.is_running:
            self.timer_label.config(text=f"Next break in: {seconds} seconds")
            if seconds > 0:
                self.master.after(1000, self.update_timer, seconds - 1)

    def remind(self):
        while self.is_running:
            time.sleep(self.interval)
            if self.is_running:
                pygame.mixer.music.play()
                self.show_break_message()
                self.breaks_taken += 1
                self.breaks_label.config(text=f"Breaks Taken: {self.breaks_taken}")
                self.update_timer(self.interval)

    def show_break_message(self):
        quote = random.choice(self.quotes)
        activity = random.choice(self.activities)
        self.motivation_label.config(text=f"{quote}\n{activity}")
        self.animate_motivation()

    def animate_motivation(self):
        for i in range(3):
            self.motivation_label.config(fg="#FF4500")
            self.master.update()
            time.sleep(0.5)
            self.motivation_label.config(fg="black")
            self.master.update()
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    reminder_app = ScreenBreakReminder(root)
    root.mainloop()
