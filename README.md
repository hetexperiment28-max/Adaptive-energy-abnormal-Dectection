# ⚡ Smart Adaptive Energy Monitoring System

##  Overview
This project implements a real-time adaptive energy monitoring system using ESP8266 and Python.  
It detects abnormal energy usage patterns using a rolling baseline model and dynamically adjusts thresholds to handle sustained changes such as new appliance installation.

The system provides live visualization and monthly trend analysis.

---

## System Architecture

ESP8266 (Potentiometer Input)  
→ Serial Communication  
→ Python Processing  
→ Adaptive Baseline Model  
→ Anomaly Detection  
→ Live Dashboard Visualization  

---

##  Features

- Real-time serial data acquisition
- Adaptive threshold adjustment
- Sustained anomaly detection logic
- Major spike detection
- Live updating dashboard
- Monthly average bar chart
- CSV-based persistent storage

---

##  Adaptive Logic

- Initial fixed baseline (5 kW)
- Rolling window mean calculation
- Baseline adapts if high/low usage sustained
- Spike detection using deviation factor

---

##  Technology Stack

**Hardware**
- ESP8266 (NodeMCU)
- Potentiometer (Load Simulation)

**Software**
- Python
- Pandas
- Matplotlib
- PySerial

**Data Storage**
- CSV File

----------------------

## 📊 Visualization

- Real-time daily usage graph
- Adaptive baseline line
- Spike detection markers
- Monthly average bar chart

-----------------------

## 🔮 Future Enhancements

- Integration with real smart energy meters
- Cloud-based monitoring
- Advanced ML model integration (Isolation Forest, LSTM)
- Web dashboard implementation
- Smart grid scalability

---

## ⚙ How to Run

1. Upload Arduino code (named : esp8266.ino ) to ESP8266 board.
2. open any code editor (VS code preffered)
3. Install required Python libraries:
4. run code and plug esp to computer to fetch live data.

