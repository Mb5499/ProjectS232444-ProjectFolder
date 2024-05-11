import tkinter as tk
from tkinter import ttk
import subprocess
import re

        
def run_raslast_and_update_display():
    python_executable = "python"
    raslast_script_path = "/home/senior/Downloads/raslast.py"

    try:
        # Run raslast.py and capture its output
        result = subprocess.run([python_executable, raslast_script_path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        # Print the script output for debugging
        print("Script output:", output)

        # Extract the first five words from the output for pattern comparison
        first_five_words = ' '.join(output.split()[:5])

        # Define the patterns for the first five words
        corrected_prediction_pattern = "Original prediction was an outlier"
        regular_prediction_pattern = "Prediction for the last input"

        # Regex to extract SOH value
        corrected_regex = r'Corrected Prediction \(mean of last 4 inputs\): (\d+\.\d+)'
        regular_regex = r'(\d+\.\d+)'

        # Compare the first five words to the patterns
        if corrected_prediction_pattern in first_five_words:
            # Search for corrected prediction value
            match = re.search(corrected_regex, output)
            if match:
                corrected_soh = float(match.group(1)) * 100  # Convert to percentage if needed
                soh_label.config(text=f"Corrected SOH: {corrected_soh:.2f}%")
                update_battery_display(corrected_soh)
            else:
                soh_label.config(text="Could not extract corrected SOH.")
        elif regular_prediction_pattern in first_five_words:
            # Search for last prediction value
            match2 = re.search(regular_regex, output)
            if match2:
                last_soh = float(match2.group(0))* 100  # Convert to percentage if needed
                soh_label.config(text=f"Last SOH: {last_soh:.2f}%")
                update_battery_display(last_soh)
            else:
                soh_label.config(text="Could not extract last SOH.")
        else:
            soh_label.config(text="Unknown output format.")
               
    except subprocess.CalledProcessError as e:
        soh_label.config(text=f"Error running raslast.py: {e}")


# Place this code where you're setting up your widgets




def update_battery_display(soh):
    # Update the progress bar based on the SOH value
    print("Script output:", soh)

    # Adjust the fill width based on the SOH; scaling it to the new battery size
    fill_width = 28.6 + (soh * 3.19)  # Adjust this formula based on your new battery size

    # Update the battery fill on the canvas
    battery_canvas.coords(battery_fill, 11, 11, fill_width, 170)  # Update this based on your new size

    # Change fill color based on SOH value
    fill_color = "#B90E0A" if soh < 75 else ("#FED000" if soh < 80 else "#008000")
    battery_canvas.itemconfig(battery_fill, fill=fill_color)



def measure_soh_button_pressed():
    # This function is called when the "Measure SOH" button is pressed
    run_raslast_and_update_display()

# Main window configuration
root = tk.Tk()
root.title("Battery SOH Measurement")
root.geometry('600x600')
root.configure(bg='black')

# Make layout scalable
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Frame that expands with the window, containing widgets
frame = tk.Frame(root, bg='#18191A')
frame.grid(sticky='nsew')
frame.columnconfigure(0, weight=1)  # Allows the left side of the grid to expand
frame.columnconfigure(1, weight=1)  # Central column configured to expand
frame.columnconfigure(2, weight=1)  # Allows the right side of the grid to expand
frame.rowconfigure(0, weight=1)  # Allows the top row where the button is placed to expand
frame.rowconfigure(2, weight=1)  # Allows the row where the SOH label is to expand
frame.rowconfigure(3, weight=3)  # Gives the battery canvas more weight to expand more prominently


# Button with specific padding, centered, with a lighter blue color
measure_soh_button = tk.Button(frame, text="Measure SOH", command=measure_soh_button_pressed, bg='#0A7EC6', fg='white', font=('Verdana', 24), padx=20, pady=5)
measure_soh_button.grid(row=0, column=1, sticky='n', padx=10, pady=10)

# Canvas for the battery display, with adjustments to position and size
battery_canvas = tk.Canvas(frame, bg='#18191A', highlightthickness=0)  # Background set to black to match the frame
battery_canvas.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)  # Adjusted padding for centering

# Drawing a white rectangle as the background for the battery
battery_background = battery_canvas.create_rectangle(10, 10, 180, 90, fill="white", outline="#18191A")

# Adjusted size for the battery outline to make it bigger
battery_outline = battery_canvas.create_rectangle(10, 10, 350, 170, fill="white", outline="black")

# Adjust the terminal to match the new size
battery_terminal = battery_canvas.create_rectangle(352, 70, 372, 110, outline="black", fill="white")

# Initial fill size can be adjusted if you're dynamically updating it in your application
battery_fill = battery_canvas.create_rectangle(11, 11, 29, 170, fill="#B90E0A", outline="")


# Label for SOH display, adjusted to scale and match the theme
soh_label = ttk.Label(frame, text="SOH: N/A", background='#18191A', foreground='white', font=('Verdana', 26))  # Increased font size
soh_label.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)  # Updated sticky for scaling


root.mainloop()
