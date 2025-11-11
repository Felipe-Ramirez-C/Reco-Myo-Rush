import pickle
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

WINDOW_SIZE = 15  # mesmo valor usado no script de inferência

def extract_features(window):
    window = np.array(window)
    mean = np.mean(window, axis=0)
    std = np.std(window, axis=0)
    maximum = np.max(window, axis=0)
    minimum = np.min(window, axis=0)
    return np.concatenate([mean, std, maximum, minimum])

def load_and_process(file_path, label):
    with open(file_path, 'rb') as f:
        x_train, y_train, x_test, y_test = pickle.load(f)
        x_all = np.concatenate((x_train, x_test), axis=0)
        y_all = np.full(len(x_all), label)

    features = []
    labels = []
    for i in range(len(x_all) - WINDOW_SIZE):
        window = x_all[i:i+WINDOW_SIZE]
        feat = extract_features(window)
        features.append(feat)
        labels.append(label)
    
    return np.array(features), np.array(labels)

# Carregar e processar dados
X_left, y_left = load_and_process('Assets/Scripts/myo/left_myo.pkl', -1)
X_center, y_center = load_and_process('Assets/Scripts/myo/center_myo.pkl', 0)
X_right, y_right = load_and_process('Assets/Scripts/myo/right_myo.pkl', 1)

# Combinar
X = np.concatenate([X_left, X_center, X_right])
y = np.concatenate([y_left, y_center, y_right])

# Dividir
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia: {accuracy:.2f}")

print(classification_report(y_test, y_pred, target_names=['Left (-1)', 'Center (0)', 'Right (1)']))

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred, labels=[-1, 0, 1])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Left', 'Center', 'Right'],
            yticklabels=['Left', 'Center', 'Right'])
plt.title("Matriz de Confusão")
plt.xlabel("Predição")
plt.ylabel("Real")
plt.tight_layout()
plt.show()

# Salvar modelo treinado
joblib.dump(model, 'Assets/Scripts/myo/best_RF.joblib')
