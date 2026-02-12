import pandas as pd
import matplotlib.pyplot as plt
import serial
import time
from datetime import datetime, timedelta
import os

# ---------------- SETTINGS ----------------
file_path = "D:/het.code/project shell/energy_data.csv"
port = "COM11"
baud_rate = 115200

BASE_THRESHOLD = 5
ADAPT_DAYS = 2
DEVIATION_FACTOR = 1.4
SIMULATION_SPEED = 5   # 1 day = 5 sec
ROLLING_WINDOW = 5
# ------------------------------------------

# Ensure CSV exists
if not os.path.exists(file_path):
    df_init = pd.DataFrame(columns=["date", "energy_value"])
    df_init.to_csv(file_path, index=False)

# Serial
ser = serial.Serial(port, baud_rate)
time.sleep(2)

# Simulated starting date
simulated_date = datetime(2026, 1, 1)

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

baseline = BASE_THRESHOLD
high_count = 0

print("System Started...")

while True:
    try:
        # Read ESP
        line = ser.readline().decode().strip()
        energy_value = float(line)

        # Read existing CSV
        df = pd.read_csv(file_path)

        # Append simulated date
        new_row = pd.DataFrame([[simulated_date.date(), energy_value]],
                               columns=["date", "energy_value"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_path, index=False)

        print(f"Date: {simulated_date.date()} | Usage: {round(energy_value,2)} kW")

        # ---------------- ADAPTIVE LOGIC ----------------

        if len(df) >= ROLLING_WINDOW:
            rolling_avg = df["energy_value"].tail(ROLLING_WINDOW).mean()
            baseline = rolling_avg  # baseline moves up AND down

        # Warning logic
        if energy_value > baseline:
            high_count += 1
            print("⚠ Above Threshold")

            if high_count >= ADAPT_DAYS:
                print("🔁 Sustained High Usage Detected")
                high_count = 0
        else:
            high_count = 0
            print("Normal Usage")

        # Major spike detection
        if energy_value > baseline * DEVIATION_FACTOR:
            print("🚨 Major Abnormal Spike!")

        # ------------------------------------------------

        # Convert date column properly
        df["date"] = pd.to_datetime(df["date"])

        # Create month column
        df["month"] = df["date"].dt.to_period("M")

        monthly_avg = df.groupby("month")["energy_value"].mean()

        # ---------------- PLOT 1: Daily ----------------
        ax1.clear()
        ax1.plot(df["energy_value"], marker='o')
        ax1.axhline(y=baseline, color='r', linestyle='--')
        ax1.set_title("Daily Energy Usage")
        ax1.set_ylabel("Energy (kW)")

        # ---------------- PLOT 2: Monthly Avg ----------
        ax2.clear()
        ax2.plot(monthly_avg.index.astype(str), monthly_avg.values,
                 marker='s', color='green')
        ax2.set_title("Monthly Average Usage Trend")
        ax2.set_ylabel("Avg Energy (kW)")
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.pause(0.1)

        # Move to next simulated day
        simulated_date += timedelta(days=1)

        time.sleep(SIMULATION_SPEED)

    except Exception as e:
        print("Error:", e)
