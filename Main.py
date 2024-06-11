import subprocess
import time
import pyautogui
import os
import glob
import pyperclip
import tkinter as tk
from tkinter import ttk
from threading import Thread

stop_requested = False

# Function to open PrusaSlicer
def open_prusaslicer():
    prusaslicer_path = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer.exe"
    subprocess.Popen([prusaslicer_path])
    time.sleep(5)  # Adjusted delay to ensure PrusaSlicer is fully loaded
    log_message("PrusaSlicer opened.")

# Function to send Ctrl+O, open a file, and delete it
def open_and_delete_file(file_path):
    try:
        log_message(f"Opening file: {file_path}")
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(0.1)
        pyperclip.copy(file_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(5)  # Increase the delay for the file to load
        pyautogui.press('delete')
        time.sleep(2)  # Increase the delay for the delete action to complete
        log_message(f"File {file_path} opened and deleted.")
    except Exception as e:
        log_message(f"Error opening or deleting file {file_path}: {e}")

# Function to open a new instance of PrusaSlicer
def open_new_instance():
    try:
        prusaslicer_path = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer.exe"
        subprocess.Popen([prusaslicer_path])
        time.sleep(5)  # Adjusted delay to ensure the new instance is fully loaded
        log_message("New instance of PrusaSlicer opened.")
    except Exception as e:
        log_message(f"Error opening new instance of PrusaSlicer: {e}")

# Function to import a new file and split it into objects
def import_and_split_file(file_path):
    try:
        log_message(f"Importing file: {file_path}")
        pyautogui.hotkey('ctrl', 'i')
        time.sleep(0.1)
        pyperclip.copy(file_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(5)  # Increase the delay for the file to load
        pyautogui.rightClick(2544, 855)  # Adjust coordinates as needed
        time.sleep(0.1)
        pyautogui.click(2686, 555)  # Adjust coordinates as needed for "split to object"
        time.sleep(0.1)
        pyautogui.click(2918, 555)  # Adjust coordinates as needed for "split to object"
        time.sleep(5)  # Increase the delay for the split action to complete
        log_message(f"File {file_path} imported and split into objects.")
    except Exception as e:
        log_message(f"Error importing or splitting file {file_path}: {e}")

# Function to slice and export G-code
def slice_and_export_gcode(export_path, folder_name, file_index):
    try:
        log_message("Pressing 'A', waiting for 3 seconds...")
        pyautogui.press('a')
        time.sleep(3)

        log_message("Pressing 'Ctrl+R' to slice, waiting for 20 seconds...")
        pyautogui.hotkey('ctrl', 'r')
        update_progress(0, 20)
        for i in range(20):
            if stop_requested:
                log_message("Stopping operation...")
                return
            time.sleep(1)
            update_progress(i + 1, 20)

        log_message("Pressing 'Ctrl+G' to export the G-code...")
        pyautogui.hotkey('ctrl', 'g')
        time.sleep(0.1)
        pyperclip.copy(export_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)

        pyautogui.click(2955, 72)  # Click to focus on file explorer path bar
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')  # Select existing name
        time.sleep(0.1)
        pyautogui.press('delete')  # Delete existing name
        time.sleep(0.1)
        pyautogui.typewrite(export_path)
        time.sleep(0.1)

        pyautogui.click(2781, 1286)  # Click to focus on file name
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')  # Select existing name
        time.sleep(0.1)
        pyautogui.press('delete')  # Delete existing name
        time.sleep(0.1)

        new_folder_name = folder_name.split('-')[0].replace(" ", "").lower() + "SlicedF"
        new_file_name = new_folder_name + str(file_index + 1)

        pyautogui.typewrite(new_file_name)
        time.sleep(0.1)        pyautogui.press('enter')
        time.sleep(0.1)

        # Additional steps: Press delete and arrange
        pyautogui.press('delete')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(3)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(5)  # Give some time to close

        log_message("G-code exported, file renamed, and additional steps performed.")
    except Exception as e:
        log_message(f"Error during slicing and exporting G-code: {e}")

# Function to log messages in the GUI
def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    root.update()

# Function to update remaining time
def update_remaining_time(start_time, total_tasks, completed_tasks):
    elapsed_time = time.time() - start_time
    remaining_tasks = total_tasks - completed_tasks
    if completed_tasks > 0:
        estimated_total_time = (elapsed_time / completed_tasks) * total_tasks
        remaining_time = estimated_total_time - elapsed_time
        minutes, seconds = divmod(int(remaining_time), 60)
        remaining_time_label.config(text=f"Estimated Remaining Time: {minutes} minutes {seconds} seconds")
        slices_remaining_label.config(text=f"Slices Remaining: {remaining_tasks}")
        progress_var.set((completed_tasks / total_tasks) * 100)
        progress_percent_label.config(text=f"{(completed_tasks / total_tasks) * 100:.2f}%")
    else:
        remaining_time_label.config(text="Estimating remaining time...")
        slices_remaining_label.config(text="Slices Remaining: N/A")
        progress_percent_label.config(text="0%")
    root.update()

# Function to update progress bar
def update_progress(current, total):
    progress_var.set((current / total) * 100)
    progress_percent_label.config(text=f"{(current / total) * 100:.2f}%")
    root.update()

# Function to stop the automation
def stop_automation():
    global stop_requested
    stop_requested = True
    log_message("Stop requested. Please wait for the current operation to finish.")

# Main function
def main():
    global stop_requested
    stop_requested = False

    base_dir = "F:\\LightSwitchWallPlates\\Images\\Products"
    pattern = "*Sliced2"
    folders = [f for f in glob.glob(os.path.join(base_dir, pattern)) if os.path.isdir(f)]
    enable_batch = True  # Set this to True to enable batch processing

    total_tasks = len(folders)
    start_time = time.time()

    for index, folder in enumerate(folders):
        if stop_requested:
            break

        task_start_time = time.time()

        open_prusaslicer()

        delete_file_path = os.path.join(folder, "3DModels", "A", "A-1(F).3mf")
        open_and_delete_file(delete_file_path)

        import_file_path = os.path.join(folder, "3DModels", "Pictures-(C-1,C-2,C-3,B-1,A-2,A-3).stl")
        import_and_split_file(import_file_path)

        export_path = "C:\\Users\\Ronin Stegner\\OneDrive\\Desktop\\Output"
        slice_and_export_gcode(export_path, os.path.basename(folder), index)

        elapsed_time = time.time() - task_start_time
        log_message(f"Elapsed time for {folder}: {elapsed_time:.2f} seconds.")

        update_remaining_time(start_time, total_tasks, index + 1)

        if enable_batch and index < total_tasks - 1:
            open_new_instance()

    if not stop_requested:
        log_message("All tasks completed.")
    else:
        log_message("Automation stopped by user.")

# Function to start the main function in a separate thread
def start_main():
    thread = Thread(target=main)
    thread.start()

# Setting up the GUI
root = tk.Tk()
root.title("PrusaSlicer Automation")
root.geometry("800x600")

log_frame = tk.Frame(root)
log_frame.pack(pady=10)

log_text = tk.Text(log_frame, wrap='word', height=20, width=100)
log_text.pack(side=tk.LEFT, fill=tk.BOTH)

log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=log_scrollbar.set)

remaining_time_label = ttk.Label(root, text="Estimated Remaining Time: Calculating...")
remaining_time_label.pack(pady=10, side=tk.RIGHT)

slices_remaining_label = ttk.Label(root, text="Slices Remaining: N/A")
slices_remaining_label.pack(pady=10, side=tk.RIGHT)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, padx=20, fill=tk.X)

progress_percent_label = ttk.Label(root, text="0%")
progress_percent_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="Start", command=start_main)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_automation)
stop_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
