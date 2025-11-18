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