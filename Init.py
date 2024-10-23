import os
import shutil

 print("EzfortGraphSettings by Conikku | https://github.com/Conikku/EzfortGraphSettings")

# Set the path to the Fortnite GameUserSettings.ini
fortnite_ini_path = os.path.join(os.getenv('LOCALAPPDATA'), "FortniteGame", "Saved", "Config", "WindowsClient", "GameUserSettings.ini")

# Directory where presets are saved (same directory as this script)
preset_directory = os.path.dirname(os.path.abspath(__file__))

# Function to display the main menu and get user choice
def main_menu():
    print("1: Save current settings as a preset")
    print("2: Apply a preset")
    choice = input("Please enter 1 or 2: ")
    return choice

# Function to save current settings as a preset
def save_preset():
    while True:
        preset_name = input("Please enter a name for your preset: ")
        preset_path = os.path.join(preset_directory, preset_name)
        
        if os.path.exists(preset_path):
            overwrite = input(f"A preset with the name '{preset_name}' already exists. Do you want to overwrite it? (Y/N): ").strip().lower()
            if overwrite == 'n':
                continue  # Ask for a new name
            elif overwrite == 'y':
                shutil.rmtree(preset_path)  # Delete the folder
                os.makedirs(preset_path)  # Create a new one
        else:
            os.makedirs(preset_path)

        try:
            shutil.copy(fortnite_ini_path, os.path.join(preset_path, "GameUserSettings.ini"))
            print(f"Preset '{preset_name}' saved successfully!")
        except Exception as e:
            print(f"Error: Failed to save the preset. {e}")
        break

# Function to apply an existing preset
def apply_preset():
    presets = [f for f in os.listdir(preset_directory) if os.path.isdir(os.path.join(preset_directory, f)) and os.path.exists(os.path.join(preset_directory, f, "GameUserSettings.ini"))]

    if not presets:
        print("No presets found.")
        return

    print("Available presets:")
    for idx, preset in enumerate(presets, start=1):
        print(f"{idx}: {preset}")

    try:
        choice = int(input("Please enter the number corresponding to the preset to apply: ")) - 1
        selected_preset = presets[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    preset_ini_path = os.path.join(preset_directory, selected_preset, "GameUserSettings.ini")
    
    # Backup the current settings
    try:
        shutil.copy(fortnite_ini_path, fortnite_ini_path + ".bak")
        print(f"Backup created at {fortnite_ini_path}.bak")
    except Exception as e:
        print(f"Error: Failed to create backup. {e}")
        return

    # Apply the selected preset
    try:
        shutil.copy(preset_ini_path, fortnite_ini_path)
        print(f"Preset '{selected_preset}' applied successfully!")
    except Exception as e:
        print(f"Error: Failed to apply the preset. {e}")

def main():
    if not os.path.exists(fortnite_ini_path):
        print(f"Error: Could not find Fortnite's GameUserSettings.ini at {fortnite_ini_path}.")
        return

    while True:
        choice = main_menu()

        if choice == "1":
            save_preset()
        elif choice == "2":
            apply_preset()
        else:
            print("Invalid option. Please try again.")

        # Ask if user wants to continue or quit
        cont = input("Do you want to perform another action? (Y/N): ").strip().lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
