# Configuration des Environnements GitHub Actions

Ce guide explique comment utiliser le script de configuration automatique des environnements GitHub Actions.

## Prérequis

1. Python 3.8+
2. Packages Python requis :
   ```bash
   pip install pyyaml requests pynacl
   ```
3. Token GitHub avec les permissions suivantes :
   - `repo`
   - `workflow`
   - `admin:org`

## Configuration

### 1. Token GitHub

1. Allez sur GitHub.com > Settings > Developer settings > Personal access tokens
2. Cliquez sur "Generate new token (classic)"
3. Donnez un nom descriptif (ex: "ERP CI/CD Setup")
4. Sélectionnez les scopes requis :
   - `repo` (tous)
   - `workflow`
   - `admin:org`
5. Copiez le token généré

### 2. Configuration des Environnements

Le fichier `.github/environments.yml` définit la configuration de chaque environnement :

```yaml
development:
  variables:
    VITE_API_URL: "http://localhost:8000"
  required_secrets:
    - VITE_WEATHER_API_KEY
    - OPENWEATHER_API_KEY

staging:
  variables:
    VITE_API_URL: "https://api.staging.erp-agricole.com"
  required_secrets:
    - VITE_WEATHER_API_KEY
    - AWS_ACCESS_KEY_ID
```

## Utilisation

### 1. Configuration du Token

```bash
export GITHUB_TOKEN=votre_token_github
```

### 2. Exécution du Script

```bash
python scripts/setup_github_environments.py
```

Le script va :
1. Lire la configuration depuis `.github/environments.yml`
2. Créer/mettre à jour les environnements sur GitHub
3. Configurer les variables d'environnement
4. Configurer les règles de protection

## Structure de Configuration

### Variables d'Environnement

```yaml
environment_name:
  variables:
    VAR_NAME: "value"
```

### Secrets Requis

```yaml
environment_name:
  required_secrets:
    - SECRET_NAME
```

### Règles de Protection

```yaml
environment_name:
  deployment_protection_rules:
    wait_timer: 30
    required_approvals: 2
```

### Branches Autorisées

```yaml
environment_name:
  deployment_branch_policy:
    protected_branches: true
    custom_branches:
      - "feature/*"
```

## Vérification

Après l'exécution du script, vérifiez :

1. Sur GitHub > Repository > Settings > Environments
   - Les environnements sont créés
   - Les variables sont configurées
   - Les règles de protection sont appliquées

2. Dans GitHub Actions
   - Les workflows peuvent accéder aux environnements
   - Les secrets sont disponibles
   - Les déploiements respectent les règles

## Dépannage

### Erreurs Communes

1. **Token Invalid**
   ```
   Erreur: GITHUB_TOKEN n'est pas défini
   ```
   Solution: Exportez le token avec les bonnes permissions

2. **Permission Denied**
   ```
   Erreur lors de la création de l'environnement
   ```
   Solution: Vérifiez les permissions du token

3. **Configuration Invalid**
   ```
   Erreur: Fichier de configuration non trouvé
   ```
   Solution: Vérifiez le chemin vers environments.yml

### Logs

Le script génère des logs détaillés :
- Création/mise à jour des environnements
- Configuration des variables
- Erreurs rencontrées

## Maintenance

### Mise à Jour des Configurations

1. Modifiez `.github/environments.yml`
2. Réexécutez le script
3. Les modifications seront appliquées

### Rotation des Secrets

1. Générez les nouveaux secrets
2. Mettez à jour les secrets dans GitHub
3. Mettez à jour la documentation

## Sécurité

- Ne stockez jamais de secrets dans environments.yml
- Utilisez des tokens avec les permissions minimales
- Activez la protection des branches
- Configurez les approbations requises

## Support

Pour toute question ou problème :
1. Consultez les logs du script
2. Vérifiez la documentation GitHub Actions
3. Contactez l'équipe DevOps