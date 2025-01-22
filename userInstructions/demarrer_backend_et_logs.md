## Instructions pour démarrer le backend et obtenir les logs

1.  **Démarrer le backend :**
    Ouvrez un terminal et exécutez la commande suivante pour démarrer le backend :
    ```bash
    uvicorn main:app --reload --port 8000
    ```
2.  **Tenter de créer le premier utilisateur administrateur :**
    Dans un autre terminal, exécutez le script suivant pour tenter de créer le premier utilisateur administrateur :
    ```bash
    python scripts/create_admin.py
    ```
3.  **Copier les logs :**
    Copiez tous les logs affichés dans le terminal où vous avez démarré le backend, y compris les messages d'erreur s'il y en a.
4.  **Fournir les logs :**
    Collez les logs dans votre prochaine réponse.

**Note :** Assurez-vous que le backend est en cours d'exécution avant d'exécuter le script `scripts/create_admin.py`.