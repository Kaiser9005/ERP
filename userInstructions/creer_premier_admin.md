## Instructions pour créer le premier utilisateur administrateur

Le premier utilisateur administrateur doit être créé manuellement après le démarrage initial de l'application. Utilisez l'endpoint `/api/v1/auth/first-admin` pour cette création. Voici les étapes à suivre :

1. **Démarrer l'application backend :**
   ```bash
   python main.py
   ```

2. **Utiliser un client HTTP (comme Postman, Insomnia ou `curl`) pour envoyer une requête POST à l'endpoint `/api/v1/auth/first-admin` :**
   - L'URL complète sera probablement `http://localhost:8000/api/v1/auth/first-admin`.
   - La requête doit contenir les informations nécessaires pour créer le premier administrateur, conformément au schéma `FirstAdminCreate` :
     - `username`: Le nom d'utilisateur souhaité (par exemple, `admin`).
     - `email`: L'adresse email de l'administrateur.
     - `password`: Le mot de passe de l'administrateur.
     - `nom`: Le nom de famille de l'administrateur.
     - `prenom`: Le prénom de l'administrateur.

   **Exemple de requête avec `curl` :**
   ```bash
   curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "username": "admin",
           "email": "admin@example.com",
           "password": "votre_mot_de_passe",
           "nom": "Admin",
           "prenom": "Super"
         }' \
     http://localhost:8000/api/v1/auth/first-admin
   ```
   **Note :** Remplacez les valeurs par celles souhaitées.

3. **En cas d'erreur :**
   - Si vous recevez une erreur "Internal Server Error", vérifiez les logs du serveur pour plus de détails.
   - Les erreurs courantes incluent :
     * Email déjà utilisé
     * Username déjà utilisé
     * Champs manquants ou invalides

4. **Après avoir créé le premier administrateur :**
   - Vous pouvez vous connecter à l'application avec les identifiants fournis
   - Le système aura automatiquement créé un rôle ADMIN et l'aura associé à votre compte
   - Vous aurez tous les droits nécessaires pour gérer l'application

**Informations importantes :**

- Cet endpoint est spécifiquement conçu pour la création du tout premier administrateur. Après cela, la création d'autres utilisateurs nécessitera une authentification.
- Tous les champs sont obligatoires.
- Le mot de passe doit être suffisamment complexe (minimum 8 caractères, avec majuscules, minuscules et chiffres).
- L'email doit être valide et unique dans le système.
- Le username doit être unique dans le système.

**En cas de problème :**

1. Vérifiez que le serveur est bien démarré et accessible
2. Vérifiez que tous les champs requis sont présents dans la requête
3. Consultez les logs du serveur pour plus de détails sur l'erreur
4. Si le problème persiste, vous pouvez réinitialiser la base de données et réessayer

Pour plus d'informations sur la gestion des utilisateurs et des rôles après la création du premier admin, consultez la documentation complète de l'API.