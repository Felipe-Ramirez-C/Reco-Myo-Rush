import pickle
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurações
WINDOW_SIZE = 15  # mesmo valor usado no script de inferência

# Caminhos
path = os.path.abspath(os.getcwd())
db_path = os.path.join(path, "db")

# Garante que a pasta db existe
os.makedirs(db_path, exist_ok=True)

# Função de extração de features
def extract_features(window):
    window = np.array(window)
    mean = np.mean(window, axis=0)
    std = np.std(window, axis=0)
    maximum = np.max(window, axis=0)
    minimum = np.min(window, axis=0)
    return np.concatenate([mean, std, maximum, minimum])

# Função para carregar e processar dados
def load_and_process(file_path, label):
    with open(file_path, 'rb') as f:
        x_train, y_train, x_test, y_test = pickle.load(f)

    x_all = np.concatenate((x_train, x_test), axis=0)
    y_all = np.full(len(x_all), label)

    features, labels = [], []
    for i in range(len(x_all) - WINDOW_SIZE):
        window = x_all[i:i + WINDOW_SIZE]
        feat = extract_features(window)
        features.append(feat)
        labels.append(label)

    return np.array(features), np.array(labels)

# Carregar e processar os dois conjuntos de dados
x_one, y_one = load_and_process(os.path.join(db_path, 'open.pkl'), 1)
x_two, y_two = load_and_process(os.path.join(db_path, 'close.pkl'), 2)
x_three, y_three = load_and_process(os.path.join(db_path, 'positive.pkl'), 3)

# Combinar os dados
X = np.concatenate([x_one, x_two, x_three])
y = np.concatenate([y_one, y_two, y_three])
# Dividir em treino e teste
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestClassifier(random_state=42)
model.fit(x_train, y_train)

# Avaliação
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia: {accuracy:.2f}")
print(classification_report(y_test, y_pred, target_names=['One (1)', 'Two (2)', 'Three (3)']))

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred, labels=[1, 2, 3])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['One', 'Two', 'Three'],
            yticklabels=['One', 'Two', 'Three'])
plt.title("Matriz de Confusão")
plt.xlabel("Predição")
plt.ylabel("Real")
plt.tight_layout()
plt.show()

# Salvar modelo treinado
model_path = os.path.join(db_path, 'best_RF.joblib')
joblib.dump(model, model_path)

print(f"✅ Modelo salvo em: {model_path}")