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
        exporter: 'Exporter'
      },
      inventaire: {
        statistiques: 'Statistiques de l\'inventaire',
        valeurTotale: 'Valeur totale',
        tauxRotation: 'Taux de rotation',
        alertes: 'Alertes de stock',
        mouvements: 'Mouvements',
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
