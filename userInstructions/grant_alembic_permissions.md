## Instructions pour accorder les permissions sur la table alembic_version

L'utilisateur `jjifdm` ne dispose pas des permissions nécessaires pour accéder à la table `alembic_version`. Pour résoudre ce problème, vous devez vous connecter à la base de données PostgreSQL en tant qu'utilisateur disposant des privilèges suffisants (par exemple, l'utilisateur `postgres`) et exécuter la commande SQL suivante :

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE alembic_version TO jjifdm;
```

Cette commande accordera les permissions `SELECT`, `INSERT`, `UPDATE`, et `DELETE` sur la table `alembic_version` à l'utilisateur `jjifdm`.

Après avoir exécuté cette commande, réessayez de créer le premier utilisateur administrateur.