# LOTA - Learns On The Air

**TRXsimulator.py** est un simulateur interactif d'émetteur-récepteur radioamateur conçu à des fins éducatives. Il fournit une interface réaliste pour apprendre et pratiquer les opérations radioamateur sans nécessiter d'équipement radio réel.

🌐 **Site web** : [https://lota.r-e-f.org/](https://lota.r-e-f.org/)

## Fonctionnalités

### 🎛️ Simulation complète d'émetteur-récepteur
- **Bandes radioamateur multiples** : 10m (28,000-29,700 MHz), 2m (144,000-146,000 MHz), 70cm (430,000-440,000 MHz)
- **Modes de fonctionnement** : FM, USB, LSB, CW
- **S-mètre réaliste** : Indication visuelle de la force du signal avec affichage à aiguille analogique
- **PTT (Push-to-Talk)** : Contrôle de transmission simulé
- **Contrôles de volume et squelch** : Réglages audio ajustables

### 📡 Expérience radioamateur authentique
- **Contrôle de fréquence** : Sélection précise de fréquence avec pas appropriés (12,5kHz pour 2m, 1kHz pour les autres)
- **Commutation de bandes** : Changement facile entre les bandes radioamateur
- **Indicateurs TX/RX** : Retour visuel pour les états d'émission et de réception
- **Simulation de signaux** : Variations réalistes du niveau de signal et fonctionnement du squelch

## Installation

### Prérequis
- Python 3.6 ou supérieur
- tkinter (généralement inclus avec Python)

### Configuration
1. Clonez le dépôt :
   ```bash
   git clone [url-du-dépôt]
   cd LOTA
   ```

2. Lancez le simulateur :
   ```bash
   python TRXsimulator.py
   ```

Aucune dépendance supplémentaire n'est requise car le simulateur utilise uniquement les modules de la bibliothèque standard Python.

## Utilisation

### Premiers pas
1. Lancez l'application en exécutant `TRXsimulator.py`
2. Sélectionnez la bande radioamateur désirée dans le menu déroulant
3. Ajustez la fréquence à l'aide du curseur de contrôle
4. Choisissez votre mode de fonctionnement (FM, USB, LSB ou CW)
5. Réglez les niveaux de volume et de squelch selon vos besoins
6. Utilisez le bouton PTT pour simuler la transmission

### Contrôles
- **Sélecteur de bande** : Choisissez entre les bandes 10m, 2m et 70cm
- **Curseur de fréquence** : Accordez sur la bande sélectionnée
- **Sélection de mode** : Basculez entre différents modes de modulation
- **Contrôle du volume** : Ajustez le niveau audio du récepteur
- **Contrôle du squelch** : Définissez le seuil de bruit pour la détection de signal
- **Bouton PTT** : Appuyez et maintenez pour simuler la transmission

### Indicateurs visuels
- **S-mètre** : Affiche la force du signal avec un mouvement d'aiguille réaliste
- **Indicateur RX** : Vert lors de la réception de signaux au-dessus du seuil de squelch
- **Indicateur TX** : Rouge lors de la transmission (PTT actif)

## Objectif éducatif

LOTA est conçu pour aider les radioamateurs et étudiants à :
- Apprendre les procédures d'exploitation radio appropriées
- Comprendre l'attribution des fréquences et les plans de bandes
- Pratiquer avec différents modes de fonctionnement
- Se familiariser avec les contrôles d'émetteur-récepteur
- Développer la mémoire musculaire pour les opérations radio

## Détails techniques

### Architecture
- Construit avec Python et tkinter pour la compatibilité multiplateforme
- Conception multi-thread pour une simulation fluide en temps réel
- Widget S-mètre personnalisé avec graphiques de style analogique
- Simulation de signal réaliste avec variations aléatoires

### Pas de fréquence
- **Bande 2m** : Pas de 12,5 kHz (typique pour les opérations VHF/UHF)
- **Autres bandes** : Pas de 1 kHz (typique pour les opérations HF)

## Contribution

Nous accueillons les contributions pour améliorer LOTA ! N'hésitez pas à :
- Signaler des bogues ou suggérer des fonctionnalités
- Soumettre des pull requests avec des améliorations
- Partager vos retours d'utilisation éducative

## Licence

Ce projet est sous licence GNU Lesser General Public License v2.1 (LGPL-2.1). Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## À propos

LOTA (Learns On The Air) est un projet éducatif visant à soutenir l'éducation et la formation radioamateur. Le simulateur offre un moyen sûr et économique d'apprendre les opérations radio avant de travailler avec un équipement réel.

Pour plus d'informations et de mises à jour, visitez : [https://lota.r-e-f.org/](https://lota.r-e-f.org/)

---

**73 !** (Meilleurs vœux selon la tradition radioamateur)
