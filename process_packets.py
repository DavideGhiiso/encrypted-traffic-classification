'''
The function builds the dataset starting from the packets by extracting the relevant features:
Uplink Packet Count, Downlink Packet Count, Average Size, Size Variance, Inter Arrival Time
'''
import csv
import pandas as pd
def build_dataset(filename):
    df = pd.read_csv(filename, index_col="N.")
    dataset = pd.DataFrame()
    dataset["N."] = df.index
    # group by the same window number and extract the features
    # uplink and downlink packet number
    dataset["Uplink Count"] = df[df["Uplink"] == True].groupby("Window")["Uplink"].count() 
    dataset["Downlink Count"] = df[df["Uplink"] == False].groupby("Window")["Uplink"].count()
    # average size and variance of packets
    dataset["Average Size"] = df.groupby("Window")["Packet Size"].mean()
    dataset["Size Variance"] = df.groupby("Window")["Packet Size"].var()
    # average inter arrival time of packets
    df["delta"] = df.groupby("Window")["Timestamp"].diff()
    dataset["Inter Time"] = df.groupby("Window")["delta"].mean()
    dataset["Status"] = df.groupby("Window")["Status"].first()
    return dataset

#dataset = build_dataset("packets.csv")
#print(dataset.head())