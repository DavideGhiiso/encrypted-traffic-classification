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

scaler = StandardScaler()
dataset = pd.read_csv("dataset.csv").dropna()

# label column
Y = dataset["Status"]
dataset = dataset.drop(columns=['Status', 'N.'])
X = scaler.fit_transform(dataset)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

accuracies = []
for est in range(10, 101, 10):
    classifier = RandomForestClassifier(n_estimators=est, random_state=42)
    classifier.fit(X_train, Y_train)
    Y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    accuracies.append((est, accuracy))
    print(f"Accuracy for n_estimators={est}: {accuracy:.4f}")

best_est = max(accuracies, key=lambda x: x[1])[0]
print(f"Best n_estimators value: {best_est}")
classifier = RandomForestClassifier(n_estimators=best_est, random_state=42)
classifier.fit(X_train, Y_train)
Y_pred = classifier.predict(X_test)
cm = confusion_matrix(Y_test, Y_pred)
cmd = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=["idle", "browsing", "streaming"])
cmd.plot(cmap=plt.cm.Blues)
plt.show()
