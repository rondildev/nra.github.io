"""
TP 1: Classification d'Images avec CNN
EST Guelmim - Intelligence Artificielle
Auteur: Nour Eddine AIT ABDALLAH

Objectif: Construire et entraîner un réseau de neurones convolutif pour 
classifier les images du dataset MNIST.
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Configuration
EPOCHS = 10
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.1

def load_and_prepare_data():
    """
    Charge le dataset MNIST et prépare les données
    """
    # Charger le dataset
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Normaliser les pixels [0, 1]
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    
    # Ajouter la dimension du canal
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    
    # Convertir les labels en one-hot encoding
    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)
    
    return (x_train, y_train), (x_test, y_test)

def build_cnn_model():
    """
    Construit l'architecture du CNN
    """
    model = models.Sequential([
        # Bloc de convolution 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        
        # Bloc de convolution 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Bloc de convolution 3
        layers.Conv2D(64, (3, 3), activation='relu'),
        
        # Couches denses
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    
    return model

def train_model(model, x_train, y_train):
    """
    Entraîne le modèle
    """
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    history = model.fit(
        x_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        verbose=1
    )
    
    return history

def evaluate_model(model, x_test, y_test):
    """
    Évalue le modèle sur les données de test
    """
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nPrécision sur l'ensemble de test: {test_accuracy:.4f}")
    print(f"Perte sur l'ensemble de test: {test_loss:.4f}")

def plot_training_history(history):
    """
    Affiche les courbes d'entraînement
    """
    plt.figure(figsize=(12, 4))
    
    # Précision
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Entraînement')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Précision du modèle')
    plt.xlabel('Époque')
    plt.ylabel('Précision')
    plt.legend()
    plt.grid(True)
    
    # Perte
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Entraînement')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Perte du modèle')
    plt.xlabel('Époque')
    plt.ylabel('Perte')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def predict_samples(model, x_test, y_test, num_samples=10):
    """
    Affiche quelques prédictions du modèle
    """
    predictions = model.predict(x_test[:num_samples])
    
    plt.figure(figsize=(15, 3))
    for i in range(num_samples):
        plt.subplot(1, num_samples, i + 1)
        plt.imshow(x_test[i].reshape(28, 28), cmap='gray')
        pred_label = np.argmax(predictions[i])
        true_label = np.argmax(y_test[i])
        color = 'green' if pred_label == true_label else 'red'
        plt.title(f'Prédit: {pred_label}\nRéel: {true_label}', color=color)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    """
    Fonction principale
    """
    print("=" * 50)
    print("Classification MNIST avec CNN")
    print("=" * 50)
    
    # Charger et préparer les données
    print("\n1. Chargement des données...")
    (x_train, y_train), (x_test, y_test) = load_and_prepare_data()
    print(f"   - Données d'entraînement: {x_train.shape}")
    print(f"   - Données de test: {x_test.shape}")
    
    # Construire le modèle
    print("\n2. Construction du modèle CNN...")
    model = build_cnn_model()
    model.summary()
    
    # Entraîner le modèle
    print("\n3. Entraînement du modèle...")
    history = train_model(model, x_train, y_train)
    
    # Évaluer le modèle
    print("\n4. Évaluation du modèle...")
    evaluate_model(model, x_test, y_test)
    
    # Afficher les résultats
    print("\n5. Visualisation des résultats...")
    plot_training_history(history)
    predict_samples(model, x_test, y_test)
    
    # Sauvegarder le modèle
    model.save('model_mnist_cnn.h5')
    print("\n✓ Modèle sauvegardé: model_mnist_cnn.h5")

if __name__ == "__main__":
    main()
