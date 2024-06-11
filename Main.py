import subprocess
import time
import pyautogui
import os
import glob
import pyperclip


# Function to open PrusaSlicer
def open_prusaslicer():
    prusaslicer_path = "C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer.exe"
    subprocess.Popen([prusaslicer_path])
    time.sleep(10)  # Adjust this delay if needed
    print("PrusaSlicer opened.")


# Function to send Ctrl+O, open a file, and delete it
def open_and_delete_file(file_path):
    try:
        print(f"Opening file: {file_path}")
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(1)
        pyperclip.copy(file_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(5)  # Wait for the file to load
        pyautogui.press('delete')
        time.sleep(1)  # Wait for the delete action to complete
        print(f"File {file_path} opened and deleted.")
    except Exception as e:
        print(f"Error opening or deleting file {file_path}: {e}")


# Function to open a new instance of PrusaSlicer
def open_new_instance():
    pyautogui.hotkey('ctrl', 'shift', 'i')
    time.sleep(10)  # Adjust this delay if needed
    print("New instance of PrusaSlicer opened.")


# Function to import a new file and split it into objects
def import_and_split_file(file_path):
    try:
        print(f"Importing file: {file_path}")
        pyautogui.hotkey('ctrl', 'i')
        time.sleep(1)
        pyperclip.copy(file_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(5)  # Wait for the file to load
        # Right-click and choose split to object (adjust coordinates as needed)
        pyautogui.rightClick(2544, 855)  # Adjust coordinates as needed
        time.sleep(1)
        pyautogui.click(2686, 555)  # Adjust coordinates as needed for "split to object"
        time.sleep(1)
        pyautogui.click(2918, 555)  # Adjust coordinates as needed for "split to object"
        time.sleep(2)
        print(f"File {file_path} imported and split into objects.")
    except Exception as e:
        print(f"Error importing or splitting file {file_path}: {e}")


# Function to slice and export G-code
def slice_and_export_gcode(export_path):
    try:
        print("Pressing 'A', waiting for 5 seconds...")
        pyautogui.press('a')
        time.sleep(5)

        print("Pressing 'Ctrl+R' to slice, waiting for 20 seconds...")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(30)

        print("Pressing 'Ctrl+G' to export the G-code...")
        pyautogui.hotkey('ctrl', 'g')
        time.sleep(1)
        pyperclip.copy(export_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

        print("Pressing 'Ctrl+5' to go back to the editor view...")
        pyautogui.hotkey('ctrl', '5')
        time.sleep(1)
        pyautogui.press('delete')
        time.sleep(1)
        print("G-code exported and file deleted.")
    except Exception as e:
        print(f"Error during slicing and exporting G-code: {e}")


# Main function
def main():
    base_dir = "F:\\LightSwitchWallPlates\\Images\\Products"
    pattern = "*Sliced2"
    folders = [f for f in glob.glob(os.path.join(base_dir, pattern)) if os.path.isdir(f)]

    # Enable/disable batch function
    enable_batch = False

    if not enable_batch:
        print("Batch function is disabled.")

    # Open an initial instance of PrusaSlicer
    open_prusaslicer()

    for index, folder in enumerate(folders):
        start_time = time.time()

        # File path for deleting
        delete_file_path = os.path.join(folder, "3DModels", "A", "A-1(F).3mf")
        open_and_delete_file(delete_file_path)

        # File path for importing and splitting
        import_file_path = "F:\\LightSwitchWallPlates\\Images\\Products\\BlueLeaf-Sliced2\\3DModels\\Pictures-(C-1,C-2,C-3,B-1,A-2,A-3).stl"
        import_and_split_file(import_file_path)

        # Slice and export G-code
        export_path = "C:\\Users\\Ronin Stegner\\OneDrive\\Desktop\\Output"
        slice_and_export_gcode(export_path)

        elapsed_time = time.time() - start_time
        remaining_time = elapsed_time * (len(folders) - (index + 1))
        print(f"Elapsed time for {folder}: {elapsed_time:.2f} seconds.")
        print(f"Estimated remaining time: {remaining_time:.2f} seconds.")

        # Open a new instance of PrusaSlicer for each subsequent folder
        if enable_batch and index < len(folders) - 1:
            open_new_instance()


if __name__ == "__main__":
    main()
