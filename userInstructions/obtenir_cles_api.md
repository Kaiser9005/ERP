## Instructions pour obtenir les clés API

Pour le bon fonctionnement de l'ERP, certaines clés API sont nécessaires. Les clés OpenWeather et IoT sont essentielles pour le MVP, tandis que les autres sont optionnelles pour le développement initial.

### Clés API Essentielles (MVP)

1. **OpenWeather API (OPENWEATHER_API_KEY)** :
    * Accédez à [OpenWeather](https://openweathermap.org/api)
    * Cliquez sur "Subscribe" dans le menu principal
    * Sélectionnez le plan gratuit "Current Weather Data"
    * Créez un compte et confirmez votre email
    * Accédez à "My API Keys" dans votre tableau de bord
    * Copiez votre clé API
    * Temps d'activation : ~2 heures après création

2. **IoT Platform API (IOT_API_KEY)** :
    * Accédez à [ThingsBoard](https://thingsboard.io/) (plateforme IoT recommandée)
    * Créez un compte gratuit
    * Dans le tableau de bord, allez dans "Devices"
    * Créez un nouveau device pour chaque type de capteur :
        - TEMP001 (température)
        - HUM001 (humidité)
        - RAIN001 (pluviométrie)
    * Pour chaque device :
        - Notez l'Access Token généré
        - Configurez les attributs selon le type de capteur
    * Combinez les tokens dans un fichier JSON et encodez-le en base64
    * Utilisez cette chaîne encodée comme IOT_API_KEY

### Clés API Optionnelles (Développement futur)

1. **Fournisseur de cartes (MAP_PROVIDER_KEY)** :
    *   Choisissez un fournisseur de services de cartographie comme OpenLayers, Leaflet ou Mapbox.
    *   Consultez la documentation du fournisseur choisi pour créer un compte et obtenir une clé API.

2. **Fournisseur de stockage (STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY)** :
    *   Si vous utilisez un service de stockage cloud comme AWS S3, Google Cloud Storage ou Azure Blob Storage :
        *   Créez un compte sur la plateforme choisie.
        *   Créez un bucket (espace de stockage).
        *   Générez des clés d'accès (Access Key ID et Secret Access Key) pour votre bucket.

3. **API de taux de change (EXCHANGE_RATE_API_KEY)** :
    *   Inscrivez-vous à un service d'API de taux de change comme :
        *   [https://exchangerate-api.com/](https://exchangerate-api.com/)
        *   [https://www.currencyconverterapi.com/](https://www.currencyconverterapi.com/)
        *   Consultez la documentation du service choisi pour obtenir votre clé API.

4. **API IoT (si applicable)** :
    *   Si votre ERP intègre des fonctionnalités IoT, identifiez le fournisseur de votre plateforme IoT.
    *   Suivez les instructions de ce fournisseur pour créer un projet/appareil et obtenir les clés API nécessaires.

**Note importante** : Conservez ces clés en sécurité et ne les partagez pas publiquement.

Une fois que vous avez obtenu ces clés, mettez à jour le fichier `.env` à la racine du projet avec les valeurs correspondantes. Par exemple :

```env
MAP_PROVIDER_KEY=votre_cle_fournisseur_cartes
STORAGE_ACCESS_KEY=votre_cle_acces_stockage
STORAGE_SECRET_KEY=votre_cle_secrete_stockage
EXCHANGE_RATE_API_KEY=votre_cle_api_taux_de_change
OPENWEATHER_API_KEY=votre_clé_api_météo (déja configuré)
IOT_API_KEY=votre_clé_api_iot
