# Configuration des Secrets pour le CI/CD

Ce document explique comment configurer les secrets nécessaires pour le pipeline CI/CD de l'ERP agricole.

## Secrets Requis

### Secrets GitHub Actions

Ces secrets doivent être configurés dans les paramètres du repository GitHub sous "Settings > Secrets and variables > Actions":

1. **API Keys**
   ```
   VITE_WEATHER_API_KEY=votre_clé_openweather
   OPENWEATHER_API_KEY=votre_clé_openweather
   IOT_API_KEY=votre_clé_iot_encodée_base64
   ```

2. **AWS Credentials** (pour le déploiement)
   ```
   AWS_ACCESS_KEY_ID=votre_access_key_id
   AWS_SECRET_ACCESS_KEY=votre_secret_access_key
   ```

3. **Sentry** (pour le monitoring)
   ```
   SENTRY_AUTH_TOKEN=votre_token_sentry
   ```

## Instructions de Configuration

1. Accédez aux paramètres de votre repository GitHub
2. Naviguez vers "Settings > Secrets and variables > Actions"
3. Cliquez sur "New repository secret"
4. Ajoutez chaque secret avec son nom et sa valeur

### Exemple pour OpenWeather API

1. Allez sur [OpenWeather](https://openweathermap.org/api)
2. Créez un compte ou connectez-vous
3. Copiez votre clé API
4. Créez deux secrets dans GitHub :
   - `VITE_WEATHER_API_KEY` avec la clé
   - `OPENWEATHER_API_KEY` avec la même clé

### Exemple pour AWS

1. Allez sur [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Créez un nouvel utilisateur IAM avec les permissions ECS et ECR
3. Générez les clés d'accès
4. Créez les secrets dans GitHub :
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### Exemple pour Sentry

1. Allez sur [Sentry](https://sentry.io)
2. Accédez aux paramètres de votre organisation
3. Générez un token d'authentification
4. Créez le secret `SENTRY_AUTH_TOKEN` dans GitHub

## Vérification

Pour vérifier que vos secrets sont correctement configurés :

1. Allez dans l'onglet "Actions" de votre repository
2. Lancez manuellement le workflow CI
3. Vérifiez que toutes les étapes passent sans erreur de secret

## Sécurité

- Ne partagez jamais ces secrets en dehors de GitHub Actions
- Ne les exposez pas dans les logs
- Faites une rotation régulière des clés
- Utilisez des permissions minimales pour chaque service

## Environnements

Les secrets peuvent être différents selon l'environnement :

- **Development** : Utilisé pour les branches de feature
- **Staging** : Utilisé pour la branche develop
- **Production** : Utilisé pour la branche main

Configurez des secrets différents pour chaque environnement dans les paramètres GitHub.

## Dépannage

Si vous rencontrez des erreurs liées aux secrets :

1. Vérifiez que le secret existe dans GitHub
2. Vérifiez que le nom du secret est correct dans le workflow
3. Vérifiez que le secret a la bonne valeur
4. Vérifiez les permissions du workflow

## Maintenance

- Faites une rotation des secrets tous les 90 jours
- Documentez chaque changement de secret
- Testez après chaque rotation
- Gardez une liste des personnes ayant accès aux secrets

## Contact

Pour toute question sur la configuration des secrets :
- Contactez l'équipe DevOps
- Ouvrez une issue avec le label `secrets-config`