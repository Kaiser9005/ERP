import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  fr: {
    translation: {
      commun: {
        periode: 'Période',
        periodes: {
          jour: 'Jour',
          semaine: 'Semaine',
          mois: 'Mois',
          annee: 'Année'
        },
        tous: 'Tous',
        exporter: 'Exporter',
        chargement: 'Chargement...',
        erreur: 'Une erreur est survenue',
        sansReference: 'Sans référence'
      },
      inventaire: {
        statistiques: 'Statistiques de l\'inventaire',
        valeurTotale: 'Valeur totale',
        tauxRotation: 'Taux de rotation',
        alertes: 'Alertes de stock',
        mouvements: {
          titre: 'Derniers Mouvements',
          types: {
            entree: 'Entrée en stock',
            sortie: 'Sortie de stock',
            transfert: 'Transfert'
          },
          filtres: {
            type: 'Type de mouvement',
            dateDebut: 'Date de début',
            dateFin: 'Date de fin',
            produit: 'Produit',
            recherche: 'Rechercher...'
          },
          colonnes: {
            date: 'Date',
            type: 'Type',
            produit: 'Produit',
            quantite: 'Quantité',
            reference: 'Référence',
            responsable: 'Responsable'
          },
          graphiques: {
            titre: 'Évolution des mouvements',
            entrees: 'Entrées',
            sorties: 'Sorties'
          },
          erreurChargement: 'Erreur lors du chargement des mouvements',
          aucunMouvement: 'Aucun mouvement récent à afficher'
        },
        produits: 'produits',
        entrees: 'Entrées',
        sorties: 'Sorties',
        quantite: 'Quantité',
        nombreProduits: 'Nombre de produits',
        categorie: 'Catégorie',
        categories: {
          intrant: 'Intrants',
          produit_fini: 'Produits finis',
          materiel: 'Matériel',
          fourniture: 'Fournitures'
        },
        graphiques: {
          mouvements: 'Mouvements de stock',
          stocksParCategorie: 'Stocks par catégorie'
        }
      }
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'fr',
    fallbackLng: 'fr',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
