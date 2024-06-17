import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pyautogui
import time
import os
import threading
import queue

"""
Keyboard Shortcuts:
1. ctrl + o      - Open File
2. g             - Grab/Move
3. z             - Constrain movement along the Z-axis
4. ctrl + shift + a - Import STL file
5. g             - Grab/Move
6. shift + z     - Constrain movement on the X-Y plane
7. ctrl + shift + c - Custom command in Blender
8. ctrl + shift + b - Custom command in Blender
"""

class BlenderAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blender Automation")
        self.center_window()

        self.file_path = tk.StringVar(value="F:\\LightSwitchWallPlates\\Images\\Products\\GreenMachine-Sliced3\\GreenMachineHue_Front_200x133.stl")
        self.progress = tk.DoubleVar()
        self.remaining_time = tk.StringVar(value="00:00")

        self.create_widgets()
        self.stl_files = []
        self.current_file_index = 0
        self.total_files = 0
        self.is_running = False
        self.start_time = None
        self.log_queue = queue.Queue()

        self.update_log()

    def center_window(self):
        window_width = 600
        window_height = 470

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def create_widgets(self):
        # Top frame for input path and browse button
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

        tk.Label(top_frame, text="Background 3D Model Path:", anchor='w').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(top_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        tk.Button(top_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        # Progress bar and remaining time
        progress_frame = tk.Frame(self.root, padx=10, pady=10)
        progress_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=500, mode="determinate",
                                            variable=self.progress)
        self.progress_bar.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

        tk.Label(progress_frame, text="Remaining Time:", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        tk.Label(progress_frame, textvariable=self.remaining_time, anchor='w').grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Control buttons
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)

        tk.Button(button_frame, text="Start", command=self.start_process).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Pause", command=self.pause_process).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Stop", command=self.stop_process).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=0, column=3, padx=5, pady=5)

        # Log frame
        log_frame = tk.Frame(self.root, padx=10, pady=10)
        log_frame.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky='ew')

        self.log_text = tk.Text(log_frame, height=10, width=70, state='disabled')
        self.log_text.grid(row=0, column=0, padx=5, pady=5)

        log_scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, padx=5, pady=5, sticky='ns')
        self.log_text['yscrollcommand'] = log_scrollbar.set

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("STL files", "*.stl")])
        self.file_path.set(file_path)

    def start_process(self):
        if not self.file_path.get():
            messagebox.showwarning("Input Error", "Please specify the background 3D model path.")
            return

        self.stl_files = self.get_stl_files()
        self.total_files = len(self.stl_files)
        if self.total_files == 0:
            messagebox.showwarning("No Files Found", "No STL files found in the specified directory.")
            return

        self.progress.set(0)
        self.current_file_index = 0
        self.is_running = True
        self.start_time = None

        threading.Thread(target=self.run_blender_operations).start()

    def get_stl_files(self):
        base_dir = "F:\\LightSwitchWallPlates\\3DModels"
        base_output = "C:\\Users\\RoninStegner\\OneDrive\\Desktop\\Output2"
        stl_files = []
        for folder in "ABCDEFG":
            folder_path = os.path.join(base_dir, folder)
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith(".stl"):
                        stl_files.append(os.path.join(folder_path, file))
            else:
                self.log(f"Folder not found: {folder_path}")
        return stl_files

    def run_blender_operations(self):
        pyautogui.PAUSE = 0.7
        pyautogui.FAILSAFE = True
        output_file = "C:\\Users\\RoninStegner\\OneDrive\\Desktop\\Output2"
        for stl_file in self.stl_files:
            if not self.is_running:
                break

            self.log(f"Processing file: {stl_file}")
            try:
                self.open_blender()
                self.perform_operations(stl_file, output_file)
                self.current_file_index += 1
                self.update_progress()
            except Exception as e:
                self.log(f"Error: {e}")
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.is_running = False
                return

        self.is_running = False

    def open_blender(self):
        self.log("Opening Blender...")
        try:
            os.startfile("C:\\Program Files\\Blender Foundation\\Blender 4.1\\blender.exe")
            time.sleep(7)  # Increased delay for Blender to open

        except Exception as e:
            self.log(f"Error opening Blender: {e}")
            raise

    def perform_operations(self, stl_file, output_file):
        self.log("Performing operations in Blender...")
        try:
            pyautogui.click(400, 400)
            pyautogui.press('a')
            pyautogui.press('x')
            pyautogui.press('enter')

            # Open the first STL file
            pyautogui.hotkey('alt', 'x')
            pyautogui.click(2703, 434)
            self.log("stl_file" + stl_file)
            pyautogui.press('backspace')
            pyautogui.write(stl_file)
            pyautogui.press('enter')
            pyautogui.press('enter')
            pyautogui.scroll(-2000)  # Scroll down (zoom out)
            pyautogui.press('g')
            pyautogui.press('z')
            pyautogui.write('-6.30511')
            pyautogui.press('enter')

            # Import the background model
            pyautogui.hotkey('alt', 'x')
            pyautogui.click(2703, 434)
            self.log("stl_file" + self.file_path.get())
            pyautogui.press('backspace')
            pyautogui.write(self.file_path.get())
            pyautogui.press('enter')
            pyautogui.press('enter')

            pyautogui.press('s')
            pyautogui.press('x')
            pyautogui.write('1.7')
            pyautogui.press('enter')
            pyautogui.press('s')
            pyautogui.press('y')
            pyautogui.write('1.7')
            pyautogui.press('enter')
            pyautogui.press('s')
            pyautogui.press('z')
            pyautogui.write('0.001')
            pyautogui.press('enter')

            pyautogui.hotkey('ctrl', 'alt', 'c') # Add Fuse Tool
            pyautogui.hotkey('ctrl', 'alt', 'b') # Add Boolean Tool
            pyautogui.click(4244, 781) # Boolean Window
            time.sleep(1)
            pyautogui.click(4444, 740) # Intersect
            time.sleep(1)
            pyautogui.click(4670, 818) # Fast
            time.sleep(0.5)
            pyautogui.click(4646, 798) # Window
            time.sleep(0.5)
            pyautogui.click(4687, 828) # Add object
            time.sleep(1)
            pyautogui.click(4687, 828)  # Add object
            time.sleep(15)
            pyautogui.click(4312, 644) # Apply Press
            pyautogui.hotkey('ctrl', 'a')  # Add Fuse Tool
            pyautogui.press('enter')
            time.sleep(10)
            pyautogui.click(4312, 644)  # Apply Press
            pyautogui.hotkey('ctrl', 'a')  # Add Fuse Tool
            pyautogui.press('enter')
            time.sleep(15)
            pyautogui.press('s')
            pyautogui.press('z')
            pyautogui.write('1000')
            pyautogui.press('enter')
            pyautogui.click(4308, 128)  # Delete object
            pyautogui.press('x')
            pyautogui.press('enter')
            pyautogui.hotkey('alt', 'j')  # Export
            self.log("output_file" + output_file)
            pyautogui.press('backspace')
            pyautogui.write(output_file)
            pyautogui.press('enter')
            pyautogui.press('enter')
            self.log("Main is done!")
            time.sleep(20)
        except Exception as e:
            self.log(f"Error performing operations: {e}")
            raise

    def update_progress(self):
        progress_percentage = (self.current_file_index + 1) / self.total_files * 100
        self.progress.set(progress_percentage)

        if self.start_time is None:
            self.start_time = time.time()
        elapsed_time = time.time() - self.start_time
        remaining_time = (elapsed_time / (self.current_file_index + 1)) * (self.total_files - self.current_file_index - 1)
        mins, secs = divmod(remaining_time, 60)
        self.remaining_time.set(f"{int(mins):02}:{int(secs):02}")

        self.log(f"Progress: {progress_percentage:.2f}% - Remaining Time: {self.remaining_time.get()}")

    def pause_process(self):
        self.log("Pausing process...")
        self.is_running = False

    def stop_process(self):
        self.log("Stopping process...")
        self.is_running = False
        self.current_file_index = 0
        self.progress.set(0)
        self.remaining_time.set("00:00")

    def log(self, message):
        self.log_queue.put(message)

    def update_log(self):
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.config(state='disabled')
            self.log_text.see(tk.END)

        self.root.after(100, self.update_log)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlenderAutomationApp(root)
    root.mainloop()
