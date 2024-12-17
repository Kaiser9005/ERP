# Erreurs de type TS2561

Ce fichier liste les erreurs de type TS2561 rencontrées lors du build du frontend.

## Description de l'erreur

TS2561: Object literal may only specify known properties but ... does not exist in type ...

## Liste des erreurs

- src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:31:5 - error TS2561: Object literal may only specify known properties but 'responsable' does not exist in type 'MouvementStock'. Did you mean to write 'responsable_id'?

  31     responsable: {
         ~~~~~~~~~~~

- src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:55:5 - error TS2561: Object literal may only specify known properties but 'responsable' does not exist in type 'MouvementStock'. Did you mean to write 'responsable_id'?

  55     responsable: {
         ~~~~~~~~~~~
