'''
Script used to determine the optimal parameter of the kNN algorithm
and get the confusion matrix
'''
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
    dataset_path = config["dataset_path"]

status_labels = ["idle", "browsing", "streaming"]
scaler = StandardScaler()
dataset = pd.read_csv(dataset_path).dropna()

# label column
Y = dataset["Status"]
dataset = dataset.drop(columns=['Status', 'N.'])
X = scaler.fit_transform(dataset)

# class balance
print("Class Balance: ",end='')
for l in status_labels:
    perc = Y[Y == l].count()/len(Y) * 100
    print(f"{l}: {perc:.2f}% ",end="")
print()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)

accuracies = []
for est in range(10, 101, 10):
    classifier = RandomForestClassifier(n_estimators=est, random_state=42)
    classifier.fit(X_train, Y_train)
    Y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    accuracies.append((est, accuracy))
    print(f"Accuracy for n_estimators={est}:\t{accuracy:.4f}")

best_est = max(accuracies, key=lambda x: x[1])[0]
print(f"Best n_estimators value: {best_est}")
classifier = RandomForestClassifier(n_estimators=best_est, random_state=42)
classifier.fit(X_train, Y_train)
Y_pred = classifier.predict(X_test)
cm = confusion_matrix(Y_test, Y_pred)
cmd = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=status_labels)
cmd.plot(cmap=plt.cm.Blues)
plt.show()
