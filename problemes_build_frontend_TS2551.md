# Erreurs de type TS2551

Ce fichier liste les erreurs de type TS2551 rencontrées lors du build du frontend.

## Description de l'erreur

TS2551: Property ... does not exist on type ... Did you mean ...?

## Liste des erreurs

- src/components/finance/TransactionDetails.tsx:186:24 - error TS2551: Property 'validee_par_id' does not exist on type 'Transaction'. Did you mean 'validee_par'?

  186           {transaction.validee_par_id && (
                             ~~~~~~~~~~~~~~

- src/components/finance/TransactionDetails.tsx:193:32 - error TS2551: Property 'validee_par_id' does not exist on type 'Transaction'. Did you mean 'validee_par'?

  193                   {transaction.validee_par_id.nom} {transaction.validee_par_id.prenom}
                                    ~~~~~~~~~~~~~~

- src/components/finance/TransactionDetails.tsx:193:65 - error TS2551: Property 'validee_par_id' does not exist on type 'Transaction'. Did you mean 'validee_par'?

  193                   {transaction.validee_par_id.nom} {transaction.validee_par_id.prenom}
                                                                     ~~~~~~~~~~~~~~
