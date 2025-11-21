import multiprocessing
import pandas as pd
import time
from pyomyo import Myo, emg_mode
from collections import deque
import os
import winsound
import cv2  # NEW: to display images

# Gesture list + corresponding images
gestures = {
    "POWER": "img/power.png",
    "LATERAL": "img/lateral.png",
    "POINTER": "img/point.png",
    "OPEN": "img/open.png",
    "TRIPOD": "img/tripod.png"
}

REST_IMAGE = "img/rest.png"

# ===========================================================
# Worker process to handle Myo EMG streaming
# ===========================================================
def worker(conn):
    m = Myo(mode=emg_mode.FILTERED)
    m.connect()

    def add_to_pipe(emg, movement):
        conn.send((time.time(), emg))

    m.set_leds([128, 0, 0], [128, 0, 0])
    m.vibrate(1)
    m.add_emg_handler(add_to_pipe)

    print("Myo connected. Collecting...")

    while True:
        try:
            m.run()
        except Exception as e:
            print("Worker stopped:", e)
            break


# ===========================================================
# Function to display gesture image
# ===========================================================
def show_image(image_path, window_name="Gesture", width=500, height=500):
    img = cv2.imread(image_path)
    if img is not None:
        img = cv2.resize(img, (width, height))   # <-- SET SIZE HERE
        cv2.imshow(window_name, img)
        cv2.waitKey(1)
    else:
        print(f"⚠️ ERROR: Could not load image: {image_path}")


# ===========================================================
# MAIN PROGRAM
# ===========================================================
if __name__ == "__main__":

    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()

    emg_data = []

    print("Estimating sample rate...")
    monitor = deque(maxlen=200)

    start_time = time.time()
    fixed_sample_rate = None

    # Estimate sample rate first
    while fixed_sample_rate is None:
        if parent_conn.poll():
            t, _ = parent_conn.recv()
            monitor.append(t)

            if time.time() - start_time >= 3:
                duration = monitor[-1] - monitor[0]
                fixed_sample_rate = len(monitor) / duration
                print(f"✔ Estimated Sample Rate: {fixed_sample_rate:.2f} Hz")
                storage_interval = 1.0 / fixed_sample_rate
                last_save = t

    # Protocol parameters
    GRASP_TIME = 5
    REST_TIME = 3
    AUDIO_ADVANCE = 0.250
    CYCLES_PER_GESTURE = 5  # 5 cycles per gesture

    print("\n===============================")
    print("     PROTOCOL STARTED")
    print("===============================\n")

    try:

        for current_gesture, image_path in gestures.items():

            print("\n=========================================")
            print(f"👉 NEXT GESTURE: {current_gesture}")
            print("=========================================\n")

            cycle = 0
            state = "REST"
            state_end_time = time.time() + REST_TIME

            while cycle < CYCLES_PER_GESTURE:

                now = time.time()

                # REST → GRASP or GRASP → REST transition
                if now >= state_end_time:

                    if state == "REST":

                        # Show gesture image BEFORE GRASP
                        show_image(image_path)

                        # Audio cue 250 ms before starting GRASP
                        winsound.Beep(1000, 250)
                        print("👉 Starting grasp in 250 ms...")
                        time.sleep(AUDIO_ADVANCE)

                        state = current_gesture
                        print(f"✊ {current_gesture} — Hold for {GRASP_TIME} seconds!")

                        now = time.time()
                        state_end_time = now + GRASP_TIME

                    else:
                        # End of grasp
                        winsound.Beep(800, 200)
                        print("🔔 End of grasp!")

                        state = "REST"
                        cycle += 1
                        print(f"🟦 Resting for {REST_TIME}s...  ({cycle}/{CYCLES_PER_GESTURE})")

                        # Show REST image
                        show_image(REST_IMAGE)

                        now = time.time()
                        state_end_time = now + REST_TIME

                # Receive EMG and store
                if parent_conn.poll():
                    timestamp, emg = parent_conn.recv()
                    if timestamp - last_save >= storage_interval:
                        emg_data.append([timestamp] + list(emg) + [state])
                        last_save = timestamp

            print("\n✔ COMPLETED gesture:", current_gesture)

        print("\n🎉 ALL GESTURES COMPLETED SUCCESSFULLY!")

    except KeyboardInterrupt:
        print("\nCollection interrupted by user.")

    finally:
        print("\nShutting down Myo...")
        p.terminate()
        p.join()

        df = pd.DataFrame(
            emg_data,
            columns=["Timestamp"] + [f"CH_{i+1}" for i in range(8)] + ["State"]
        )

        os.makedirs("db", exist_ok=True)
        df.to_csv("db/left_full_gestures.csv", index=False)

        print("\n✔ File saved to: db/left_full_gestures.csv")

        cv2.destroyAllWindows()
