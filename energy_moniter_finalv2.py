import pandas as pd
import matplotlib.pyplot as plt
import serial
import time
import csv
from datetime import datetime, timedelta
import os
import matplotlib.dates as mdates

# ---------------- SETTINGS ----------------
file_path = "D:/het.code/project shell/energy_data.csv"
port = "COM11"
baud_rate = 115200

BASE_THRESHOLD = 5
ROLLING_WINDOW = 10
ADAPT_DAYS = 2
DEVIATION_FACTOR = 1.4
# ------------------------------------------

# Ensure CSV exists
if not os.path.exists(file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "energy_value"])

# Open serial
try:
    ser = serial.Serial(port, baud_rate, timeout=0.1)
    time.sleep(2)
except Exception as e:
    print(f"Serial Error on {port}: {e}")
    exit()

# Initialization
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    old_df = pd.read_csv(file_path)
    if not old_df.empty:
        last_date = pd.to_datetime(old_df["date"].iloc[-1])
        simulated_date = last_date + timedelta(days=1)
    else:
        simulated_date = datetime(2026, 1, 1)
else:
    simulated_date = datetime(2026, 1, 1)

effective_baseline = BASE_THRESHOLD
high_count = 0
low_count = 0

dates_list = []
energy_list = []

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), constrained_layout=True)

print("System Started...")

while True:
    try:
        # -------- READ LATEST SERIAL DATA --------
        if ser.in_waiting > 0:
            lines = ser.readlines()
            raw_line = lines[-1].decode('utf-8', errors='ignore').strip()

            try:
                energy_value = float(raw_line)
            except ValueError:
                continue
        else:
            continue

        # -------- SAVE TO CSV --------
        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([simulated_date.strftime("%Y-%m-%d"), energy_value])

        dates_list.append(simulated_date)
        energy_list.append(energy_value)

        # -------- DYNAMIC BASELINE --------
        recent_window = energy_list[-ROLLING_WINDOW:]
        dynamic_baseline = sum(recent_window) / len(recent_window)

        # -------- ADAPTATION LOGIC --------
        status_msg = "Normal"

        if energy_value > effective_baseline:
            high_count += 1
            low_count = 0

            if energy_value > (effective_baseline * DEVIATION_FACTOR):
                status_msg = "SPIKE!"
                print(f"🚨 ABNORMAL SPIKE: {energy_value} kW")
            else:
                print(f"⚠ Above Baseline: {energy_value} kW")

            if high_count >= ADAPT_DAYS:
                effective_baseline = dynamic_baseline
                print(f"🔁 Baseline Adapted UP to: {round(effective_baseline, 3)}")
                high_count = 0
        else:
            low_count += 1
            high_count = 0

            if low_count >= ADAPT_DAYS:
                if dynamic_baseline < effective_baseline:
                    effective_baseline = dynamic_baseline
                    print(f"🔽 Baseline Adapted DOWN to: {round(effective_baseline, 3)}")
                low_count = 0

        # -------- EFFICIENCY CALCULATION --------
        efficiency = (effective_baseline / dynamic_baseline) * 100 if dynamic_baseline != 0 else 100

        # -------- PLOTTING --------
        ax1.clear()

        plot_dates = dates_list[-50:]
        plot_energy = energy_list[-50:]

        # Main line
        ax1.plot(plot_dates, plot_energy, marker='o', color='tab:blue', label="Real-time Usage")

        # Safe zone shading
        ax1.fill_between(plot_dates, 0, effective_baseline, color='green', alpha=0.1)

        # Spike markers
        spike_dates = []
        spike_values = []

        for d, v in zip(plot_dates, plot_energy):
            if v > effective_baseline * DEVIATION_FACTOR:
                spike_dates.append(d)
                spike_values.append(v)

        ax1.scatter(spike_dates, spike_values, color='red', s=80, label="Abnormal Spike")

        # Threshold line
        ax1.axhline(y=effective_baseline, color='r', linestyle='--',
                    label=f"Baseline: {round(effective_baseline,2)}")

        ax1.set_title(f"Energy Usage ({status_msg}) | Efficiency: {round(efficiency,1)}%")
        ax1.legend()
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

        # -------- MONTHLY BAR GRAPH --------
        temp_df = pd.DataFrame({'date': dates_list, 'val': energy_list})
        temp_df['month'] = temp_df['date'].dt.to_period("M")
        monthly_avg = temp_df.groupby('month')['val'].mean()

        ax2.clear()
        ax2.bar(monthly_avg.index.astype(str), monthly_avg.values, color='tab:green')
        ax2.set_title("Monthly Average Energy Usage")
        ax2.set_ylabel("Avg kW")

        plt.pause(0.01)

        # -------- SIMULATION PROGRESSION --------
        simulated_date += timedelta(days=1)
        time.sleep(0.2)

    except Exception as e:
        print(f"Runtime Error: {e}")
        time.sleep(1)
