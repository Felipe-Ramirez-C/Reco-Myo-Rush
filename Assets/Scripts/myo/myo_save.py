import multiprocessing
import numpy as np
import pandas as pd
import time
from pyomyo import Myo, emg_mode
from collections import deque
import os

# Worker que coleta os dados e envia pelo Pipe
def worker(conn):
    m = Myo(mode=emg_mode.PREPROCESSED)
    m.connect()

    def add_to_pipe(emg, movement):
        conn.send((time.time(), emg))

    m.set_leds([128, 0, 0], [128, 0, 0])
    m.vibrate(1)
    m.add_emg_handler(add_to_pipe)

    print("Myo conectado. Coletando dados EMG...")
    while True:
        try:
            m.run()
        except Exception as e:
            print("Worker parado:", e)
            break

# Programa principal
if __name__ == '__main__':
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=worker, args=(child_conn,))
    p.start()

    emg_data = []
    monitor = deque(maxlen=100)
    fixed_sample_rate = None
    CALIBRATION_DURATION = 5
    last_stored_time = None
    print("Pressione Ctrl+C para parar a coleta")

    try:
        start_time = time.time()

        while True:
            if parent_conn.poll():
                timestamp, emg = parent_conn.recv()

                if fixed_sample_rate is None:
                    monitor.append(timestamp)
                    if time.time() - start_time >= CALIBRATION_DURATION:
                        duration = monitor[-1] - monitor[0]
                        rate = len(monitor) / duration if duration > 0 else 0
                        fixed_sample_rate = rate
                        print(f"Sample rate estimado: {rate:.2f} Hz")
                        storage_interval = 1.0 / rate
                        last_stored_time = timestamp
                    continue

                if last_stored_time is None or timestamp - last_stored_time >= storage_interval:
                    row = [timestamp] + list(emg)
                    print("Armazenando:", row)
                    emg_data.append(row)
                    last_stored_time = timestamp

    except KeyboardInterrupt:
        print("\nParando coleta...")
        path = os.path.abspath(os.getcwd())
        path_to_save = path + "/db/positive.csv"
        p.terminate()
        p.join()

        df = pd.DataFrame(emg_data, columns=["Timestamp"] + [f"CH_{i+1}" for i in range(8)])
        os.makedirs(os.path.dirname(path_to_save), exist_ok=True) # Cria o diretório se não existir
        df.to_csv(path_to_save, index=False)
        print("Salvo com sucesso")
