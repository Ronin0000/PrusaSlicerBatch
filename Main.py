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
def slice_and_export_gcode(export_path, folder_name, file_index):
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
        time.sleep(1)
        # Navigate file explorer, paste path, and rename file
        pyautogui.click(2955, 72)  # Click to focus on file explorer path bar
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Select existing name
        time.sleep(1)
        pyautogui.press('delete')  # Delete existing name
        time.sleep(1)
        pyautogui.typewrite(export_path)
        time.sleep(1)
        pyautogui.click(2781, 1286)  # Click to focus on file name
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')  # Select existing name
        time.sleep(1)
        pyautogui.press('delete')  # Delete existing name
        time.sleep(1)
        new_file_name = folder_name.replace(" ", "").lower() + str(file_index + 1) + ".gcode"
        pyautogui.typewrite(new_file_name)  # Type new name
        time.sleep(1)
        print("G-code exported, file renamed.")
    except Exception as e:
        print(f"Error during slicing and exporting G-code: {e}")



# Main functiona
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
        slice_and_export_gcode(export_path, os.path.basename(folder), index)

        elapsed_time = time.time() - start_time
        if not enable_batch:
            print(f"Elapsed time for {folder}: {elapsed_time:.2f} seconds.")

        # Open a new instance of PrusaSlicer for each subsequent folder
        if enable_batch and index < len(folders) - 1:
            open_new_instance()


if __name__ == "__main__":
    main()
