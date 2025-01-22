## Instructions pour obtenir des clés API gratuites (pour le développement et les tests)

Étant donné que nous sommes en phase de développement et de tests, voici comment obtenir des clés API gratuites pour les différents services nécessaires.

### API Essentielles (MVP)

1. **OpenWeather API (OPENWEATHER_API_KEY)** :
   * Accédez à [OpenWeather](https://home.openweathermap.org/users/sign_up)
   * Créez un compte gratuit
   * Confirmez votre email
   * Dans votre tableau de bord, allez dans "API Keys"
   * Utilisez la clé par défaut ou générez-en une nouvelle
   * **Limitations du plan gratuit** :
     - 60 appels par minute
     - Données météo actuelles
     - Prévisions sur 5 jours
     - Suffisant pour le développement et les tests

2. **IoT Platform (IOT_API_KEY)** :
   * Option 1 - Simulateur IoT local :
     ```bash
     # Installation
     pip install iot-simulator
     
     # Lancement du simulateur
     python scripts/iot_simulator.py
     ```
   * Option 2 - ThingsBoard Community Edition :
     - Téléchargez [ThingsBoard CE](https://thingsboard.io/docs/user-guide/install/installation-options/)
     - Installation locale :
       ```bash
       docker run -it -p 9090:9090 -p 1883:1883 -p 5683:5683/udp thingsboard/tb-ce:latest
       ```
     - Accédez à http://localhost:9090
     - Identifiants par défaut : admin/admin
     - Créez des devices de test dans l'interface

### API Optionnelles (Développement futur)

### Fournisseur de cartes (MAP_PROVIDER_KEY) - OpenStreetMap avec Leaflet

Pour afficher des cartes dans votre application, nous utiliserons **OpenStreetMap**, qui est une initiative collaborative et gratuite. Pour l'intégration dans le frontend, nous utiliserons la librairie **Leaflet**, qui est open-source et ne nécessite pas de clé API pour les utilisations de base.

**Instructions :**

1. **Intégration dans le frontend :**  Vous n'avez pas besoin de clé API pour utiliser OpenStreetMap avec Leaflet. Dans vos composants React, vous pouvez directement utiliser les composants Leaflet pour afficher la carte. Voici un exemple d'intégration :

    ```typescript jsx
    import React from 'react';
    import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
    import 'leaflet/dist/leaflet.css';

    const position = [51.505, -0.09]; // Exemple de coordonnées

    function MyMap() {
      return (
        <MapContainer center={position} zoom={13} style={{ height: '300px', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          <Marker position={position}>
            <Popup>
              Ceci est un marqueur.
            </Popup>
          </Marker>
        </MapContainer>
      );
    }

    export default MyMap;
    ```

2. **Installation de Leaflet :** Assurez-vous d'avoir installé les dépendances nécessaires dans votre projet frontend :

    ```bash
    cd frontend
    npm install leaflet react-leaflet
    ```

### Fournisseur de stockage (STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY) - Stockage local pour le développement

Pour simuler le stockage de fichiers pendant le développement, nous pouvons utiliser le système de fichiers local. Cela ne nécessite pas de clés d'accès.

**Configuration du backend (FastAPI) :**

Vous devrez configurer votre backend pour enregistrer les fichiers localement. Voici un exemple de configuration possible :

1. **Créer un dossier de stockage :** Créez un dossier `local_storage` à la racine de votre projet backend.

2. **Configurer FastAPI pour le stockage local :**  Modifiez votre code backend pour enregistrer les fichiers dans ce dossier. Voici un exemple simplifié :

    ```python
    from fastapi import FastAPI, UploadFile, File
    import os

    app = FastAPI()

    @app.post("/uploadfile/")
    async def create_upload_file(file: UploadFile = File(...)):
        upload_folder = "local_storage"
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"filename": file.filename}
    ```

**Important :**

*   Le stockage local n'est **pas recommandé pour la production**. Il est destiné uniquement au développement et aux tests.
*   Pour la production, vous devrez configurer un véritable service de stockage cloud comme AWS S3, Google Cloud Storage ou Azure Blob Storage et obtenir les clés d'accès correspondantes.

En utilisant ces alternatives gratuites pour le développement, vous pouvez tester les fonctionnalités de votre ERP sans avoir besoin de clés API payantes pour le moment. N'oubliez pas de configurer correctement votre backend et votre frontend pour utiliser ces solutions.
