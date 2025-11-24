# train_models.py
import pickle
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

gesture_names = ["POWER", "LATERAL", "POINTER", "OPEN", "TRIPOD"]
position_names = ["LEFT", "CENTER", "RIGHT"]

# ---------------------------------------------------------
# Load processed data
# ---------------------------------------------------------
with open("processed/processed_data.pkl", "rb") as f:
    Xg, yg, Xp, yp = pickle.load(f)

# ---------------------------------------------------------
# Train gesture classifier
# ---------------------------------------------------------
xtr, xte, ytr, yte = train_test_split(Xg, yg, test_size=0.2, stratify=yg)

clf_g = RandomForestClassifier(n_estimators=300)
clf_g.fit(xtr, ytr)
ypred = clf_g.predict(xte)

print("\nGESTURE CLASSIFICATION:")
print(classification_report(yte, ypred, target_names=gesture_names))

cm = confusion_matrix(yte, ypred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=gesture_names, yticklabels=gesture_names)
plt.title("Gesture Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

joblib.dump(clf_g, "gesture_classifier.joblib")


# ---------------------------------------------------------
# Train position classifier
# ---------------------------------------------------------
xtr, xte, ytr, yte = train_test_split(Xp, yp, test_size=0.2, stratify=yp)

clf_p = RandomForestClassifier(n_estimators=300)
clf_p.fit(xtr, ytr)
ypred = clf_p.predict(xte)

print("\nPOSITION CLASSIFICATION:")
print(classification_report(yte, ypred, target_names=position_names))

cm = confusion_matrix(yte, ypred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=position_names, yticklabels=position_names)
plt.title("Position Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

joblib.dump(clf_p, "position_classifier.joblib")

print("\n✔ Models saved!")
