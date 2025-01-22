## Réexécuter le script de création de l'administrateur et observer la sortie du backend

Pour diagnostiquer l'erreur de création du premier utilisateur administrateur, veuillez suivre les étapes suivantes :

1. **Assurez-vous que le backend est en cours d'exécution.** Si ce n'est pas le cas, démarrez-le.
2. **Ouvrez un nouveau terminal** dans le répertoire racine du projet (`/Users/cherylmaevahfodjo/ERP/ERP`).
3. **Exécutez la commande suivante** pour lancer le script de création de l'administrateur :

   ```bash
   python scripts/create_admin.py
   ```

4. **Observez attentivement la sortie standard (le texte affiché dans le terminal) du backend.**  Recherchez les messages de log qui commencent par `create_first_admin:`. Ces messages fourniront des informations sur le déroulement de la création de l'utilisateur et les éventuelles erreurs rencontrées.

Veuillez fournir la sortie du backend après avoir exécuté le script.