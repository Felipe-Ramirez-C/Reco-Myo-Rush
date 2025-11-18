import pandas as pd
import matplotlib.pyplot as plt

# --- arquivos CSV ---
files = [
    "db/left.csv",
    "db/center.csv",
    "db/right.csv"
]

# --- nomes dos canais ---
channels = ["CH_1","CH_2","CH_3","CH_4","CH_5","CH_6","CH_7","CH_8"]

# --- figura ---
fig, axes = plt.subplots(
    nrows=8, ncols=3, 
    figsize=(12, 16), 
    sharex=True, sharey=True
)

for col, file in enumerate(files):
    df = pd.read_csv(file)

    for row, ch in enumerate(channels):
        ax = axes[row, col]
        ax.plot(df["Timestamp"], df[ch], linewidth=0.8)

        # Nome do canal na esquerda
        if col == 0:
            ax.set_ylabel(ch)

        # Nome do arquivo no topo
        if row == 0:
            ax.set_title(file)

# Ajuste de layout
plt.tight_layout()
plt.show()
