# myo_processing.py
import os
import numpy as np
import pandas as pd
from collections import Counter
import pickle

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
DATASETS = {
    "LEFT":   "db/left_full_gestures_00.csv",
    "CENTER": "db/center_full_gestures_00.csv",
    "RIGHT":  "db/right_full_gestures_00.csv"
}

gesture_map = {
    "POWER": 0,
    "LATERAL": 1,
    "POINTER": 2,
    "OPEN": 3,
    "TRIPOD": 4
}

position_map = {
    "LEFT": 0,
    "CENTER": 1,
    "RIGHT": 2
}

channels = [f"CH_{i}" for i in range(1, 9)]


# -------------------------------------------------------------------
# Feature extraction
# -------------------------------------------------------------------
def rms(x): return np.sqrt(np.mean(x**2))
def mav(x): return np.mean(np.abs(x))
def wl(x): return np.sum(np.abs(np.diff(x)))
def zc(x, thresh=5): return np.sum(((x[:-1] * x[1:]) < 0) & (np.abs(x[:-1]-x[1:])>=thresh))
def ssc(x, thresh=5):
    d = np.diff(x)
    return np.sum(((d[:-1] * d[1:]) < 0) & (np.abs(d[:-1]-d[1:]) >= thresh))

def extract_features_window(win):
    feats = []
    for c in range(win.shape[1]):
        x = win[:, c]
        feats += [
            rms(x), mav(x), np.std(x), np.var(x),
            np.max(x), np.min(x), np.ptp(x),
            wl(x), zc(x), ssc(x)
        ]
    return np.array(feats)


# -------------------------------------------------------------------
# Processing function
# -------------------------------------------------------------------
X_gesture, y_gesture = [], []
X_position, y_position = [], []

for pos_name, filepath in DATASETS.items():

    print(f"Loading: {filepath}")
    df = pd.read_csv(filepath)

    # remove rest periods
    df = df[df["State"] != "REST"].reset_index(drop=True)

    g_label = df["State"].map(gesture_map).values
    p_label = position_map[pos_name]

    ts = df["Timestamp"].values
    sr = 1 / np.median(np.diff(ts))
    WINDOW_SIZE = int(sr * 0.30)
    STEP = WINDOW_SIZE // 2

    data = df[channels].values

    for start in range(0, len(df)-WINDOW_SIZE, STEP):
        win = data[start:start+WINDOW_SIZE]
        win_labels = g_label[start:start+WINDOW_SIZE]
        maj = Counter(win_labels).most_common(1)[0][0]

        feats = extract_features_window(win)

        X_gesture.append(feats)
        y_gesture.append(maj)

        X_position.append(feats)
        y_position.append(p_label)


# Convert to numpy
X_gesture = np.array(X_gesture)
y_gesture = np.array(y_gesture)
X_position = np.array(X_position)
y_position = np.array(y_position)

print("Final gesture dataset:", X_gesture.shape, y_gesture.shape)
print("Final position dataset:", X_position.shape, y_position.shape)

# -------------------------------------------------------------------
# SAVE TO .pkl
# -------------------------------------------------------------------
os.makedirs("processed", exist_ok=True)

with open("processed/processed_data.pkl", "wb") as f:
    pickle.dump((X_gesture, y_gesture, X_position, y_position), f)

print("\n✔ Saved processed_data.pkl")
