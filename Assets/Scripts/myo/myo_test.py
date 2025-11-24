import multiprocessing
import numpy as np
import time
from pyomyo import Myo, emg_mode
from collections import deque
import joblib

# ============================================================
# Load trained models
# ============================================================
model_gesture = joblib.load("gesture_classifier.joblib")
model_position = joblib.load("position_classifier.joblib")

GESTURE_NAMES = ["POWER", "LATERAL", "POINTER", "OPEN", "TRIPOD"]
POSITION_NAMES = ["LEFT", "CENTER", "RIGHT"]

# ============================================================
# Feature extraction (must match TRAINING exactly)
# ============================================================
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


# ============================================================
# Worker: Myo process
# ============================================================
def worker(conn):
    m = Myo(mode=emg_mode.FILTERED)
    m.connect()

    def add_to_pipe(emg, movement):
        conn.send((time.time(), emg))

    m.add_emg_handler(add_to_pipe)

    print("Myo connected. Streaming...")

    while True:
        try:
            m.run()
        except Exception as e:
            print("Worker crashed:", e)
            break


# ============================================================
# MAIN REAL-TIME LOOP
# ============================================================
if __name__ == "__main__":

    # Start Myo in subprocess
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()

    print("\nEstimating sample rate...")
    ts_buffer = deque(maxlen=200)
    sample_rate = None
    start = time.time()

    # Estimate sample rate
    while sample_rate is None:
        if parent_conn.poll():
            t, _ = parent_conn.recv()
            ts_buffer.append(t)

            if time.time() - start >= 3:
                dt = np.diff(ts_buffer)
                sample_rate = 1.0 / np.median(dt)
                print(f"Sample Rate: {sample_rate:.2f} Hz")

    # Setup window
    WINDOW_MS = 300
    WINDOW_SIZE = int(sample_rate * WINDOW_MS / 1000)
    print(f"WINDOW_SIZE = {WINDOW_SIZE}")

    ring = deque(maxlen=WINDOW_SIZE)

    last_gesture = None
    last_position = None
    stab_g = stab_p = 0

    print("\n🔥 STARTED REAL-TIME CLASSIFICATION\n")

    try:
        while True:

            if parent_conn.poll():
                ts, emg = parent_conn.recv()
                ring.append(emg)

                if len(ring) == WINDOW_SIZE:

                    win = np.array(ring)
                    feats = extract_features_window(win).reshape(1, -1)

                    # Predict gesture + position
                    pred_g = model_gesture.predict(feats)[0]
                    pred_p = model_position.predict(feats)[0]

                    # Stability filter
                    if pred_g == last_gesture:
                        stab_g += 1
                    else:
                        stab_g = 0
                        last_gesture = pred_g

                    if pred_p == last_position:
                        stab_p += 1
                    else:
                        stab_p = 0
                        last_position = pred_p

                    if stab_g >= 3 and stab_p >= 3:
                        print(f">>> GESTURE: {GESTURE_NAMES[pred_g]}   POSITION: {POSITION_NAMES[pred_p]}")

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        p.terminate()
        p.join()
        print("Myo closed.")
