# Exemples d'Utilisation RH Agricole

## Gestion des Compétences

### Création d'une Compétence

```typescript
import { createCompetence } from '@services/hr_agricole';

const nouvelleCompetence = await createCompetence({
  nom: "Conduite tracteur",
  description: "Conduite et manœuvre de tracteurs agricoles",
  niveau: "intermediaire",
  dateObtention: "2024-05-01",
  dateExpiration: "2026-05-01",
  employeId: "123"
});
```

### Liste des Compétences avec Filtrage

```typescript
import { rechercherCompetences } from '@services/hr_agricole';

const filtres = {
  niveau: "expert",
  statut: "actif",
  dateDebut: "2024-01-01",
  dateFin: "2024-12-31"
};

const tri = {
  champ: "nom",
  ordre: "asc"
};

const pagination = {
  page: 1,
  limite: 10
};

const { data, pagination: resultPagination } = await rechercherCompetences(
  filtres,
  tri,
  pagination
);
```

## Gestion des Certifications

### Ajout d'une Certification

```typescript
import { createCertification } from '@services/hr_agricole';

const nouvelleCertification = await createCertification({
  nom: "Permis tracteur",
  organisme: "CFPPA",
  dateObtention: "2024-05-01",
  dateExpiration: "2026-05-01",
  competenceId: "456",
  fichiers: ["certificat.pdf"]
});
```

### Vérification des Renouvellements

```typescript
import { 
  getCompetencesARenouveler,
  getCertificationsARenouveler 
} from '@services/hr_agricole';

// Compétences à renouveler dans les 30 jours
const competencesARenouveler = await getCompetencesARenouveler(30);

// Certifications à renouveler dans les 60 jours
const certificationsARenouveler = await getCertificationsARenouveler(60);
```

## Gestion des Affectations

### Création d'une Affectation

```typescript
import { createAffectation } from '@services/hr_agricole';

const nouvelleAffectation = await createAffectation({
  employeId: "123",
  parcelleId: "789",
  dateDebut: "2024-05-01",
  dateFin: "2024-05-31",
  type: "principale"
});
```

### Liste des Affectations par Parcelle

```typescript
import { getAffectationsParcelle } from '@services/hr_agricole';

const affectations = await getAffectationsParcelle("789");
```

## Statistiques

### Récupération des Statistiques

```typescript
import {
  getStatistiquesCompetences,
  getStatistiquesCertifications,
  getStatistiquesFormations,
  getStatistiquesConditionsTravail
} from '@services/hr_agricole';

// Statistiques des compétences
const statsCompetences = await getStatistiquesCompetences();

// Statistiques des certifications
const statsCertifications = await getStatistiquesCertifications();

// Statistiques des formations
const statsFormations = await getStatistiquesFormations();

// Statistiques des conditions de travail
const statsConditions = await getStatistiquesConditionsTravail(
  "2024-01-01",
  "2024-12-31"
);
```

## Gestion des Erreurs

```typescript
import { createCompetence } from '@services/hr_agricole';

try {
  const competence = await createCompetence({
    nom: "Conduite tracteur",
    description: "Conduite et manœuvre de tracteurs agricoles",
    niveau: "intermediaire",
    dateObtention: "2024-05-01",
    dateExpiration: "2026-05-01",
    employeId: "123"
  });
} catch (error) {
  if (error.response) {
    switch (error.response.status) {
      case 400:
        console.error("Erreur de validation:", error.response.data);
        break;
      case 401:
        console.error("Non authentifié");
        // Rediriger vers la page de connexion
        break;
      case 403:
        console.error("Non autorisé");
        break;
      case 404:
        console.error("Ressource non trouvée");
        break;
      default:
        console.error("Erreur serveur:", error.response.data);
    }
  }
}
```

## Utilisation dans un Composant React

```typescript
import { useState, useEffect } from 'react';
import { 
  getCompetencesEmploye,
  getStatistiquesCompetences 
} from '@services/hr_agricole';

export const CompetencesEmploye = ({ employeId }) => {
  const [competences, setCompetences] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [competencesData, statsData] = await Promise.all([
          getCompetencesEmploye(employeId),
          getStatistiquesCompetences()
        ]);
        setCompetences(competencesData);
        setStats(statsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [employeId]);

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <div>
      <h2>Compétences de l'employé</h2>
      <div>
        <h3>Statistiques</h3>
        <p>Total: {stats.total}</p>
        <p>À renouveler: {stats.aRenouveler}</p>
      </div>
      <ul>
        {competences.map(competence => (
          <li key={competence.id}>
            {competence.nom} - Niveau: {competence.niveau}
          </li>
        ))}
      </ul>
    </div>
  );
};
