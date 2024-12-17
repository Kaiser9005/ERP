# Erreurs de type TS2345

Ce fichier liste les erreurs de type TS2345 rencontrées lors du build du frontend.

## Description de l'erreur

TS2345: Argument of type ... is not assignable to parameter of type ...

## Liste des erreurs

- src/components/comptabilite/JournauxList.tsx:57:20 - error TS2345: Argument of type '(ecritures: any) => unknown' is not assignable to parameter of type 'SetStateAction<EcritureComptable[]>'.
  Type '(ecritures: any) => unknown' is not assignable to type '(prevState: EcritureComptable[]) => EcritureComptable[]'.
    Type 'unknown' is not assignable to type 'EcritureComptable[]'.

  57       setEcritures(data?.ecritures || []);
                      ~~~~~~~~~~~~~~~~~~~~~

- src/components/comptabilite/JournauxList.tsx:74:22 - error TS2345: Argument of type '(ecritures: any) => unknown' is not assignable to parameter of type 'SetStateAction<EcritureComptable[]>'.
  Type '(ecritures: any) => unknown' is not assignable to type '(prevState: EcritureComptable[]) => EcritureComptable[]'.
    Type 'unknown' is not assignable to type 'EcritureComptable[]'.

  74         setEcritures(data?.ecritures || []);
                        ~~~~~~~~~~~~~~~~~~~~~

- src/components/documents/DocumentList.tsx:57:29 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'void'.

  57       deleteMutation.mutate(id);
                               ~~

- src/components/documents/DocumentUploadDialog.tsx:63:23 - error TS2345: Argument of type 'FormData' is not assignable to parameter of type 'void'.

  63       mutation.mutate(formData);
                           ~~~~~~~~

- src/components/finance/__tests__/AnalyseBudget.test.tsx:62:44 - error TS2345: Argument of type '{ total_prevu: number; total_realise: number; categories: { Équipement: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; Personnel: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; }; impact_meteo: { ...; }; recommandations: string[]; }' is not assignable to parameter of type 'AnalyseBudgetaire | Promise<AnalyseBudgetaire>'.
  Type '{ total_prevu: number; total_realise: number; categories: { Équipement: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; Personnel: { prevu: number; realise: number; ecart: number; ecart_pourcentage: number; }; }; impact_meteo: { ...; }; recommandations: string[]; }' is missing the following properties from type 'AnalyseBudgetaire': periode total alertes

  62     mockGetAnalyseBudget.mockResolvedValue(mockAnalyse);
                                                ~~~~~~~~~~~

- src/components/finance/__tests__/AnalyseBudget.test.tsx:137:48 - error TS2345: Argument of type '{ total_prevu: number; total_realise: number; categories: {}; impact_meteo: { score: number; facteurs: never[]; projections: {}; }; recommandations: never[]; }' is not assignable to parameter of type 'AnalyseBudgetaire | Promise<AnalyseBudgetaire>'.
  Type '{ total_prevu: number; total_realise: number; categories: {}; impact_meteo: { score: number; facteurs: never[]; projections: {}; }; recommandations: never[]; }' is missing the following properties from type 'AnalyseBudgetaire': periode total alertes

  137     mockGetAnalyseBudget.mockResolvedValueOnce(emptyAnalyse);
                                                   ~~~~~~~~~~~~

- src/components/finance/__tests__/GraphiqueTresorerie.test.tsx:25:48 - error TS2345: Argument of type '{ labels: string[]; recettes: number[]; depenses: number[]; }' is not assignable to parameter of type 'DonneesTresorerie | Promise<DonneesTresorerie>'.

  25     mockGetDonneesTresorerie.mockResolvedValue(mockData);
                                                   ~~~~~~~~

- src/components/finance/__tests__/ListeTransactions.test.tsx:43:43 - error TS2345: Argument of type '{ id: string; date: string; reference: string; description: string; montant: number; type: TypeTransaction; statut: StatutTransaction; categorie: string; }[]' is not assignable to parameter of type 'TransactionListResponse | Promise<TransactionListResponse>'.

  43     mockGetTransactions.mockResolvedValue(mockTransactions);
                                               ~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/ListeTransactions.test.tsx:89:47 - error TS2345: Argument of type 'never[]' is not assignable to parameter of type 'TransactionListResponse | Promise<TransactionListResponse>'.

  89     mockGetTransactions.mockResolvedValueOnce([]);
                                                   ~~

- src/components/finance/TransactionForm.tsx:94:83 - error TS2345: Argument of type '{ date_transaction: string; compte_source?: string; compte_destination?: string; }' is not assignable to parameter of type 'TransactionFormData'.
  Type '{ date_transaction: string; compte_source?: string | undefined; compte_destination?: string | undefined; }' is missing the following properties from type 'TransactionFormData': reference type_transaction categorie montant

  94       return isEdit ? updateTransaction(id! transactionData) : createTransaction(transactionData);
                                                                                       ~~~~~~~~~~~~~~~

- src/components/finance/TransactionForm.tsx:105:21 - error TS2345: Argument of type 'TransactionFormData' is not assignable to parameter of type 'void'.

  105     mutation.mutate(data);
                          ~~~~

- src/components/inventaire/DialogueMouvementStock.tsx:117:23 - error TS2345: Argument of type '{ type_mouvement: TypeMouvement; quantite: number; reference_document: string; cout_unitaire?: number; notes?: string; produit_id: string; }' is not assignable to parameter of type 'Omit<MouvementStock "id" | "date_mouvement">'.
  Property 'responsable_id' is missing in type '{ type_mouvement: TypeMouvement; quantite: number; reference_document: string; cout_unitaire?: number; notes?: string; produit_id: string; }' but required in type 'Omit<MouvementStock "id" | "date_mouvement">'.

  117       mutation.mutate({
                            ~
  118         produit_id: productId
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  119         ...data
      ~~~~~~~~~~~~~~~
  120       });
      ~~~~~~~
