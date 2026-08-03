'''
Script used to determine the optimal parameter of the kNN algorithm
and get the confusion matrix
'''
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

scaler = StandardScaler()
dataset = pd.read_csv("dataset.csv").dropna()

# label column
Y = dataset["Status"]
dataset = dataset.drop(columns=['Status', 'N.'])
X = scaler.fit_transform(dataset)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

accuracies = []
for k in range(1, 6):
    knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
    knn.fit(X_train, Y_train)
    Y_pred = knn.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    accuracies.append(accuracy)
    print(f"Accuracy for k={k}: {accuracy:.4f}")

k = np.argmax(accuracies) + 1
print(f"Best k value: {k}")
knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_test)
cm = confusion_matrix(Y_test, Y_pred)
cmd = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=["idle", "browsing", "streaming"])
cmd.plot(cmap=plt.cm.Blues)
plt.show()
