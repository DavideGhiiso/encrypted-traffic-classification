from scapy.all import *
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yaml

# adds packet to the window if it's from/to the target devices
def callback(pkg):
    global current_window
    if pkg.haslayer(Dot11):
        if pkg.addr2 == TARGET or pkg.addr1 == TARGET:
            current_window.append([pkg.time, len(pkg), pkg.addr2 == TARGET])

if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
        TARGET = config["target"]   
        IFACE = config["interface"]
        n_estimators = config["estimators"]
        window = config["window"]

    scaler = StandardScaler()
    dataset = pd.read_csv("dataset1.csv").dropna()
    # label column
    Y = dataset["Status"]
    dataset = dataset.drop(columns=['Status', 'N.'])
    X = scaler.fit_transform(dataset)
    classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    classifier.fit(X, Y)
    
    while True:
        current_window = []
        sniff(iface=IFACE, prn=callback, store=0, timeout=window)   
        # skip if no packets are capured
        if len(current_window) == 0:
            continue

        df = pd.DataFrame(np.array(current_window), columns=["Timestamp", "Packet Size", "Uplink"])
        curr_win_df = pd.DataFrame(np.array(
            [[df[df["Uplink"] == True]["Timestamp"].count(),
            df[df["Uplink"] == False]["Timestamp"].count(),
            df["Packet Size"].mean(),
            df["Packet Size"].var(),
            df["Timestamp"].diff().mean()]]),
            columns=["Uplink Count", "Downlink Count", "Average Size", "Size Variance", "Inter Time"])

        print(curr_win_df.head())
        # skip if current window has NaN values
        if(curr_win_df.isnull().values.any()):
            continue
        Y_pred = classifier.predict(curr_win_df.dropna().to_numpy())
        print(f"Predicted status: {Y_pred[0]}")
