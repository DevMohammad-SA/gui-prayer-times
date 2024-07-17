import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
from adhanpy import PrayerTimes
from adhanpy.calculation import CalculationMethod
from zoneinfo import ZoneInfo

# Global variables
cities = {
    "Riyadh": (24.7136, 46.6753),
    "Jeddah": (21.4858, 39.1925),
    "Mecca": (21.4225, 39.8262),
    "Medina": (24.5247, 39.5692),
    "Dammam": (26.3927, 49.9777),
    "Khobar": (26.2794, 50.208),
    "Tabuk": (28.3835, 36.5662),
    "Buraydah": (26.3259, 43.9744),
    "Khamis Mushait": (18.3061, 42.7296),
    "Abha": (18.2164, 42.5053),
    "Taif": (21.2703, 40.4158),
    "Hail": (27.5219, 41.6907),
    "Najran": (17.5065, 44.1315),
    "Yanbu": (24.0897, 38.0637),
    "Jizan": (16.8897, 42.5706),
    "Al Ahsa": (25.3792, 49.5874),
    "Al Jubail": (27.0004, 49.6536),
    "Al Qunfudhah": (19.1268, 41.0789),
    "Arar": (30.9753, 41.0381),
    "Al Bahah": (20.0129, 41.4675),
    "Sakakah": (29.9697, 40.2064),
    "Qurayyat": (31.3295, 37.3422),
    "Rafha": (29.6204, 43.4934),
    "Tarout Island": (26.5784, 50.0257)
}

calculation_methods = [
    CalculationMethod.MUSLIM_WORLD_LEAGUE,
    CalculationMethod.EGYPTIAN,
    CalculationMethod.KARACHI,
    CalculationMethod.UMM_AL_QURA,
    CalculationMethod.DUBAI,
    CalculationMethod.QATAR,
    CalculationMethod.KUWAIT,
    CalculationMethod.MOON_SIGHTING_COMMITTEE,
    CalculationMethod.SINGAPORE,
    CalculationMethod.NORTH_AMERICA
]

# Function to calculate and update prayer times
def update_prayer_times():
    # Clear previous results
    for label in prayer_labels:
        label.config(text="")

    # Get selected city coordinates
    selected_city = city_combobox.get()
    coordinates = cities[selected_city]

    # Get selected calculation method
    selected_method = calculation_method_combobox.get()

    # Calculate prayer times
    today = datetime.date.today()
    method = selected_method
    Riyadh = ZoneInfo("Asia/Riyadh")  # Time zone

    prayer = PrayerTimes.PrayerTimes(
        coordinates=coordinates,
        date=today,
        calculation_method=method,
        time_zone=Riyadh
    )

    # Update labels with prayer times
    prayer_labels[0].config(text=f"Fajr: {prayer.fajr.strftime('%I:%M %p')}", font=("Georgia", 14))
    prayer_labels[1].config(text=f"Sunrise: {prayer.sunrise.strftime('%I:%M %p')}", font=("Georgia", 14))
    prayer_labels[2].config(text=f"Dhuhr: {prayer.dhuhr.strftime('%I:%M %p')}", font=("Georgia", 14))
    prayer_labels[3].config(text=f"Asr: {prayer.asr.strftime('%I:%M %p')}", font=("Georgia", 14))
    prayer_labels[4].config(text=f"Maghrib: {prayer.maghrib.strftime('%I:%M %p')}", font=("Georgia", 14))
    prayer_labels[5].config(text=f"Isha: {prayer.isha.strftime('%I:%M %p')}", font=("Georgia", 14))
    #prayer_labels[6].config(text=f"Next prayer :{prayer.night_length.strftime('%I:%M %p')}", font=("Georgia", 14))
# Function to change calculation method
def change_calculation_method():
    method = simpledialog.askinteger("Calculation Method", "Enter the number of the calculation method:\n"
                                     "1. Muslim World League\n"
                                     "2. Egyptian\n"
                                     "3. Karachi\n"
                                     "4. Umm Al-Qura\n"
                                     "5. Dubai\n"
                                     "6. Qatar\n"
                                     "7. Kuwait\n"
                                     "8. Moon Sighting Committee\n"
                                     "9. Singapore\n"
                                     "10. North America")

    if method in range(1, len(calculation_methods) + 1):
        calculation_method_combobox.current(method - 1)
        update_prayer_times()
    else:
        messagebox.showerror("Error", "Invalid calculation method number.")

# Create tkinter window
root = tk.Tk()
root.title("Today's Prayer Times")
root.resizable(False, False)  # Disable resizing

# Frame to hold labels and controls
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew")

# Label and Combobox for city selection
city_label = ttk.Label(frame, text="Select City:")
city_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

city_combobox = ttk.Combobox(frame, values=list(cities.keys()), state="readonly")
city_combobox.grid(row=0, column=1, padx=10, pady=5)
city_combobox.current(0)  # Set default selection

# Label and Combobox for calculation method selection
calculation_method_label = ttk.Label(frame, text="Select Calculation Method:")
calculation_method_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

calculation_method_combobox = ttk.Combobox(frame, values=[method.name for method in calculation_methods], state="readonly")
calculation_method_combobox.grid(row=1, column=1, padx=10, pady=5)
calculation_method_combobox.current(0)  # Set default selection

# Labels to display prayer times
prayer_labels = []
prayer_names = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
for i, name in enumerate(prayer_names):
    label = ttk.Label(frame, text="", font=("Georgia", 14))
    label.grid(row=i+2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
    prayer_labels.append(label)

# Button to update prayer times
update_button = ttk.Button(root, text="Update Prayer Times", command=update_prayer_times)
update_button.grid(row=7, column=0, pady=10)

# Button to change calculation method
change_method_button = ttk.Button(root, text="Change Calculation Method", command=change_calculation_method)
change_method_button.grid(row=8, column=0, pady=10)

# Initially calculate and display prayer times
update_prayer_times()

root.mainloop()
