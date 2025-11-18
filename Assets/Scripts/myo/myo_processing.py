import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn. preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer

# Arquivos e seus labels
arquivos = {
    "db/left.csv": 0,
    "db/center.csv": 1,
    "db/right.csv": 2
}

lista = []

# Carregando os dados
for caminho, label in arquivos.items():
    df = pd.read_csv(caminho)

    # Pegando o canal
    df = df[["CH_1"]]

    # Colocando o label
    df["label"] = label

    lista.append(df)

# db concatenada
db = pd.concat(lista, ignore_index=True)

# Verificando os dados antes da normalização
print(db)
print(db.describe())

# Divisão entre previsores e classe para normalização
x = db.iloc[:, 0].values # Apenas o canal x
y = db.iloc[:, 1].values  # Apenas o label

# print(x)
# print(y)

# Normalização dos dados
scaler = MinMaxScaler()
x_scaled = scaler.fit_transform(x.reshape(-1, 1))
db["CH_1"] = x_scaled

# Verificando os dados após a normalização
print(db.describe())

# Salvando a base de dados do canal x normalizada
db.to_csv("db/db_ch1.csv", index=False)