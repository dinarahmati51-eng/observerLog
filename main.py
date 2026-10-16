import tkinter as tk
from tkinter import messagebox

from Observation import Observation, Photometric_observation
from database import ObservationDatabase
from visual import show_observations, plot_exposure_times


def add_observation():
    target = target_entry.get().strip()
    observer = observer_entry.get().strip()
    filter_name = filter_entry.get().strip()
    exposure_text = exposure_entry.get().strip()
    observation_type = "Observation"
    wavelength_text = wavelength_entry.get().strip()

    if not target or not observer or not filter_name or not exposure_text:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    try:
        exposure = float(exposure_text)
        if exposure <= 0:
            raise ValueError

        if observation_type == "Photometric":
            wavelength = float(wavelength_text)
            if wavelength <= 0:
                raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter valid positive numbers for exposure and wavelength."
        )
        return

    if observation_type == "Photometric":
        observation = Photometric_observation(
            target, observer, filter_name, exposure, wavelength
        )
    else:
        observation = Observation(
            target, observer, filter_name, exposure
        )

    db.add_observation(observation)

    messagebox.showinfo("Success", "Observation added successfully!")

    target_entry.delete(0, tk.END)
    observer_entry.delete(0, tk.END)
    filter_entry.delete(0, tk.END)
    exposure_entry.delete(0, tk.END)
    wavelength_entry.delete(0, tk.END)


def show_all_observations():
    observations = db.show_observations()
    df = show_observations(observations)

    if df is None or df.empty:
        messagebox.showinfo("Observations", "No observations found.")
        return

    result_window = tk.Toplevel(root)
    result_window.title("All Observations")
    result_window.geometry("850x300")

    text_box = tk.Text(result_window, wrap="none", width=110, height=16)
    text_box.pack(fill="both", expand=True)

    text_box.insert("1.0", df.to_string(index=False))
    text_box.config(state="disabled")


def search_observations():
    target = target_entry.get().strip()

    if not target:
        messagebox.showerror("Error", "Enter a target name to search.")
        return

    results = db.search_observation(target)

    if not results:
        messagebox.showinfo("Search", "No observations found.")
        return

    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.geometry("850x250")

    text_box = tk.Text(result_window, wrap="none", width=110, height=12)
    text_box.pack(fill="both", expand=True)

    columns = [
        "id", "target", "observer", "filter_name",
        "exposure", "observation_type", "wavelength", "date"
    ]

    import pandas as pd
    df = pd.DataFrame(results, columns=columns)

    text_box.insert("1.0", df.to_string(index=False))
    text_box.config(state="disabled")


def show_chart():
    observations = db.show_observations()

    if not observations:
        messagebox.showinfo("Chart", "No observations available.")
        return

    plot_exposure_times(observations)

def export_csv():
    try:
        db.export_to_csv()
        messagebox.showinfo(
            "Success",
            "Observations exported to observations.csv successfully!"
        )
    except Exception as error:
        messagebox.showerror("Export Error", str(error))


def import_csv():
    try:
        count = db.import_from_csv()
        messagebox.showinfo(
            "Success",
            f"{count} new observations imported successfully!"
        )
    except Exception as error:
        messagebox.showerror("Import Error", str(error))


db = ObservationDatabase()

root = tk.Tk()
root.title("Observer Log")
root.geometry("600x650")

title_label = tk.Label(
    root,
    text="Observer Log",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)

form_frame = tk.Frame(root)
form_frame.pack(pady=5)

tk.Label(form_frame, text="Target name:").grid(
    row=0, column=0, sticky="w", padx=8, pady=5
)
target_entry = tk.Entry(form_frame, width=30)
target_entry.grid(row=0, column=1, padx=8, pady=5)

tk.Label(form_frame, text="Observer name:").grid(
    row=1, column=0, sticky="w", padx=8, pady=5
)
observer_entry = tk.Entry(form_frame, width=30)
observer_entry.grid(row=1, column=1, padx=8, pady=5)

tk.Label(form_frame, text="Filter name:").grid(
    row=2, column=0, sticky="w", padx=8, pady=5
)
filter_entry = tk.Entry(form_frame)
filter_entry.grid(row=2, column=1, padx=8, pady=5)

tk.Label(form_frame, text="Exposure time (seconds):").grid(
    row=3, column=0, sticky="w", padx=8, pady=5
)
exposure_entry = tk.Entry(form_frame, width=30)
exposure_entry.grid(row=3, column=1, padx=8, pady=5)

tk.Label(form_frame, text="Wavelength (optional):").grid(
    row=4, column=0, sticky="w", padx=8, pady=5
)
wavelength_entry = tk.Entry(form_frame, width=30)
wavelength_entry.grid(row=4, column=1, padx=8, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Observation",
    command=add_observation
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Show All",
    command=show_all_observations
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Search",
    command=search_observations
).grid(row=0, column=2, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Show Chart",
    command=show_chart
).grid(row=0, column=3, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Show Chart",
    command=show_chart
).grid(row=0, column=3, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Exit",
    command=root.destroy
).grid(row=0, column=4, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Import CSV",
    command=import_csv
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    button_frame,
    text="Exit",
    command=root.destroy
).grid(row=0, column=4, padx=5, pady=5)

root.mainloop()