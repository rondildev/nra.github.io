# TP 1: Classification d'Images avec CNN

## Objectif
Construire et entraîner un réseau de neurones convolutif (CNN) pour classifier les images du dataset MNIST (chiffres manuscrits 0-9).

## Prérequis
```bash
pip install tensorflow numpy matplotlib
```

## Contenu du TP

### Partie 1: Chargement et Préparation des Données
- Charger le dataset MNIST (70 000 images)
- Normaliser les pixels [0, 1]
- Ajouter la dimension du canal (28x28x1)
- Conversion des labels en one-hot encoding

### Partie 2: Architecture du CNN
Le modèle se compose de:
- **Bloc 1**: Conv2D(32 filtres) → MaxPool → Dropout
- **Bloc 2**: Conv2D(64 filtres) → MaxPool → Dropout
- **Bloc 3**: Conv2D(64 filtres) → Flatten
- **Couches denses**: Dense(64) → Dropout(0.5) → Dense(10 softmax)

### Partie 3: Entraînement
- Optimiseur: Adam
- Loss: Categorical Crossentropy
- Épochs: 10
- Batch Size: 128
- Validation Split: 10%

### Partie 4: Évaluation
- Évaluer sur l'ensemble de test
- Afficher les courbes d'entraînement
- Tester quelques prédictions

## Exécution
```bash
python TP1_CNN_ImageClassification.py
```

## Résultats attendus
- Précision sur test: ~99%
- Temps d'entraînement: ~2-5 minutes

## Questions à explorer
1. Pourquoi utiliser Conv2D au lieu de Dense?
2. Quel est l'effet du Dropout?
3. Comment améliorer la précision?
4. Quel est le rôle de MaxPooling?

## Améliorations possibles
- Data Augmentation (rotations, flips)
- Batch Normalization
- Learning Rate Scheduling
- Différentes architectures (ResNet, VGG)
