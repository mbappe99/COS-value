import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import json

DATA_FILE = "creature_prices.json"
BACKGROUND_IMAGE_URL = "https://postimg.cc/QHVCq9hC"  # Replace with your image URL


# Load data from JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


# Save data to JSON
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(creatures, f, indent=4)


# Update UI when selecting a creature
def update_ui(event=None):
    creature = creature_var.get()
    if creature in creatures:
        data = creatures[creature]
        price_label.config(text=f"Value: {data['value']} Mush")
        demand_label.config(text=f"Player Demand: {data['demand']}/10 Players")
        stability_label.config(text=f"Price Stability: {data['stability']}")
        tips_label.config(text=f"Trading Tips: {data['tips']}")
        last_update_label.config(text=f"Last Update: {data['last_update']}")
    else:
        price_label.config(text="Value: N/A")
        demand_label.config(text="Player Demand: N/A")
        stability_label.config(text="Price Stability: N/A")
        tips_label.config(text="Trading Tips: N/A")
        last_update_label.config(text="Last Update: N/A")


# Function to manually update values
def update_values():
    creature = creature_var.get()
    if not creature:
        messagebox.showerror("Error", "Please enter a creature name!")
        return

    value = value_entry.get()
    demand = demand_entry.get()
    stability = stability_entry.get()
    tips = tips_entry.get()

    creatures[creature] = {
        "value": value,
        "demand": demand,
        "stability": stability,
        "tips": tips,
        "last_update": "25 March 2025"  # Auto-updating date
    }

    save_data()
    update_ui()
    messagebox.showinfo("Success", f"{creature} updated!")


# Load existing creature data
creatures = load_data()

# Create the GUI
root = tk.Tk()
root.title("Creatures of Sonaria Price Tracker")
root.geometry("500x400")

# Fetch the image from URL
response = requests.get(BACKGROUND_IMAGE_URL)

# Debugging: Check the response details
print(f"HTTP Status Code: {response.status_code}")
if response.status_code == 200:
    # Check the content type of the response (should be an image format)
    print(f"Content-Type: {response.headers['Content-Type']}")

    try:
        bg_image = Image.open(BytesIO(response.content))  # Open the image from the downloaded data
        bg_image = bg_image.resize((500, 400), Image.Resampling.LANCZOS)  # Resize to match window size

        # Create PhotoImage object from the background image
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a Canvas widget for the background image
        canvas = tk.Canvas(root, width=500, height=400)
        canvas.pack(fill="both", expand=True)

        # Display the background image on the canvas
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    except IOError:
        messagebox.showerror("Error", "Unable to open the image. Please check the URL or image format.")
else:
    messagebox.showerror("Error", f"Failed to load image. HTTP Status Code: {response.status_code}")

# Create a frame to hold other widgets, so they don't overlap with the image
frame = tk.Frame(root, bg="black", bd=5)
frame.place(relwidth=1, relheight=1)  # Ensure the frame fills the entire window

# Add the rest of your widgets over the background image
tk.Label(frame, text="Enter Creature Name:", fg="white", bg="black").pack(pady=10)
creature_var = tk.StringVar()
creature_dropdown = ttk.Combobox(frame, textvariable=creature_var, values=list(creatures.keys()))
creature_dropdown.pack(pady=10)
creature_dropdown.bind("<<ComboboxSelected>>", update_ui)

price_label = tk.Label(frame, text="Value: N/A", fg="white", bg="black")
price_label.pack(pady=10)
demand_label = tk.Label(frame, text="Player Demand: N/A", fg="white", bg="black")
demand_label.pack(pady=10)
stability_label = tk.Label(frame, text="Price Stability: N/A", fg="white", bg="black")
stability_label.pack(pady=10)
tips_label = tk.Label(frame, text="Trading Tips: N/A", fg="white", bg="black")
tips_label.pack(pady=10)
last_update_label = tk.Label(frame, text="Last Update: N/A", fg="white", bg="black")
last_update_label.pack(pady=10)

# Manual update section
tk.Label(frame, text="Update Creature Info:", fg="white", bg="black").pack(pady=10)
value_entry = tk.Entry(frame)
value_entry.pack(pady=5)
demand_entry = tk.Entry(frame)
demand_entry.pack(pady=5)
stability_entry = tk.Entry(frame)
stability_entry.pack(pady=5)
tips_entry = tk.Entry(frame)
tips_entry.pack(pady=5)

update_button = tk.Button(frame, text="Update", command=update_values, bg="green", fg="white")
update_button.pack(pady=10)

root.mainloop()
