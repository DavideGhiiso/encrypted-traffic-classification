'''
Script to gather data from the sniffer wireless interface and stores it into a CSV file.
It both saves the packets and builds the dataset usable by the classifier
'''

from scapy.all import *
import yaml
import csv
from process_packets import build_dataset
import pandas as pd

#TARGET = "bc:f7:30:50:4e:7c"
consecutive_windows = 10
packet_count = 16468
window_count = 89
filename = "packets.csv"
status_labels = ["idle", "browsing", "streaming"]

def packet_callback(pkg):
    global packet_count, status, window_count
    if pkg.haslayer(Dot11):
        if pkg.addr2 == TARGET or pkg.addr1 == TARGET:
            packet_count += 1
            packet_size = len(pkg)
            ts = pkg.time
            uplink = (pkg.addr2 == TARGET)
            with open("packets.csv", "a") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([packet_count, ts, window_count, packet_size, uplink, status_labels[status]])

if __name__ == "__main__":
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
        TARGET = config["target"]   
        IFACE = config["interface"]
        window = config["window"]
    status = 0 # 0: idle, 1: browsing, 2: streaming

    status_counter = [5,0,5]
    while status >= 0 and status < 3:
        wnd_ctr = 0
        while wnd_ctr < consecutive_windows:
            wnd_ctr += 1
            print(f"Window: {window_count}, {packet_count} packets")
            print(f"windows per status: {status_counter}")
            sniff(iface=IFACE, prn=packet_callback, store=0, timeout=window)
            window_count += 1
        status = int(input("Capture finished. Insert next status: "))
        if(status >= 0 and status < 3):
            status_counter[status] += 1
    build_dataset("packets.csv").dropna().to_csv("dataset.csv", index=False)
