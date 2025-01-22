# Standardisation des Noms dans les Modèles

## Principes Généraux

1. Utiliser le français de manière cohérente pour :
   - Noms de tables
   - Noms de colonnes
   - Noms de relations
   - Noms de classes
2. Garder la même convention de nommage dans tous les fichiers
3. Éviter le mélange français/anglais

## Incohérences Identifiées

### Tables et Modèles

1. **Problème** : Mélange "employees" et "employes"
   - **Correction** : Utiliser "employes" partout
   - **Fichiers concernés** :
     * models/hr_formation.py
     * models/hr.py

2. **Problème** : Mélange "Employee" et "Employe"
   - **Correction** : Utiliser "Employe" partout
   - **Fichiers concernés** :
     * models/hr_formation.py
     * models/task.py

### Relations

1. **Task-Employe**
   - **Actuel** :
     * Task : `assignee = relationship("Employe", back_populates="assigned_tasks")`
     * Employe : `taches_assignees = relationship("Task", back_populates="assignee")`
   - **Correction** :
     * Task : `responsable = relationship("Employe", back_populates="taches_assignees")`
     * Employe : `taches_assignees = relationship("Task", back_populates="responsable")`

2. **Formation-Employe**
   - **Actuel** :
     * Formation : `employes = relationship("Employe", secondary="participations_formation", backref="formations")`
     * ParticipationFormation : `employee = relationship("Employee", backref="participations_formations")`
   - **Correction** :
     * Formation : `employes = relationship("Employe", secondary="participations_formation", backref="formations")`
     * ParticipationFormation : `employe = relationship("Employe", backref="participations_formations")`

3. **Evaluation-Employe**
   - **Actuel** :
     * `employee = relationship("Employee", foreign_keys=[employee_id], backref="evaluations_recues")`
     * `evaluateur = relationship("Employee", foreign_keys=[evaluateur_id], backref="evaluations_donnees")`
   - **Correction** :
     * `employe = relationship("Employe", foreign_keys=[employe_id], backref="evaluations_recues")`
     * `evaluateur = relationship("Employe", foreign_keys=[evaluateur_id], backref="evaluations_donnees")`

### Colonnes

1. **Problème** : Mélange "employee_id" et "employe_id"
   - **Correction** : Utiliser "employe_id" partout
   - **Fichiers concernés** :
     * models/hr_formation.py
     * models/hr_agricole.py

## Plan de Correction

1. Mettre à jour les modèles dans l'ordre suivant :
   - models/hr.py (modèle de base Employe)
   - models/task.py (relations avec Employe)
   - models/hr_formation.py (formations et évaluations)
   - models/hr_agricole.py (compétences et certifications)

2. Mettre à jour les migrations Alembic pour refléter ces changements

3. Mettre à jour les schémas Pydantic correspondants

4. Mettre à jour les tests pour utiliser les nouveaux noms

## Impact sur la Base de Données

Ces changements nécessiteront :
1. Une migration de la base de données
2. Une mise à jour des données existantes
3. Une mise à jour des contraintes de clés étrangères

## Recommandations

1. Effectuer ces changements dans une branche dédiée
2. Tester chaque modification individuellement
3. Prévoir une stratégie de rollback en cas de problème
4. Documenter tous les changements dans changes.md