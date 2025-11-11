import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle

if __name__ == "__main__":
    # Importando a base de dados
    db = pd.read_csv('Assets/Scripts/myo/right_myo.csv')

    db['default'] = 1

    # Visualizando as primeiras linhas da base de dados
    # print(db.head())

    # Verificando informações gerais da base de dados
    # print(db.describe())

    # Verificando se existem valores nulos na base de dados
    # print(db.isnull().sum())

    x = db.iloc[:, 1:9]
    y = db.iloc[:, 9]
    # print(x.head())
    # print(y.head())

    #scalar_standard = StandardScaler()
    #x_scaled = scalar_standard.fit_transform(x)

    # Divisão entre treino e teste
    # x_train, x_test, y_train, y_test = train_test_split(
    #     x_scaled, y, test_size=0.25, random_state=0
    # ) 
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=0
    )

    print(x_train.shape, x_test.shape)
    print(y_train.shape, y_test.shape)

    # Salvando a base de dados tratada em pickle
    with open('Assets/Scripts/myo/right_myo.pkl', mode = 'wb') as f:
        pickle.dump([x_train, y_train, x_test, y_test], f)