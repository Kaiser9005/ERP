# Erreurs de type TS2559

Ce fichier liste les erreurs de type TS2559 rencontrées lors du build du frontend.

## Description de l'erreur

TS2559: Type ... has no properties in common with type ...

## Liste des erreurs

- src/components/finance/TransactionForm.tsx:64:5 - error TS2554: Expected 1-2 arguments but got 3.

  64     { enabled: isEdit }
       ~~~~~~~~~~~~~~~~~~~

- src/components/finance/TransactionForm.tsx:89:5 - error TS2559: Type '(data: TransactionFormData) => Promise<Transaction>' has no properties in common with type 'UseMutationOptions<unknown Error void unknown>'.

  89     (data: TransactionFormData) => {
         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/TransactionForm.tsx:94:46 - error TS2559: Type '{ date_transaction: string; compte_source?: string | undefined; compte_destination?: string | undefined; }' has no properties in common with type 'Partial<TransactionFormData>'.

  94       return isEdit ? updateTransaction(id! transactionData) : createTransaction(transactionData);
                                                  ~~~~~~~~~~~~~~~

- src/components/finance/TransactionForm.tsx:98:39 - error TS2559: Type 'string[]' has no properties in common with type 'InvalidateQueryFilters'.

  98         queryClient.invalidateQueries(['transactions']);
                                           ~~~~~~~~~~~~~~~~

- src/components/finance/TransactionForm.tsx:105:21 - error TS2345: Argument of type 'TransactionFormData' is not assignable to parameter of type 'void'.

  105     mutation.mutate(data);
                          ~~~~

- src/components/parametrage/__tests__/ParametrageLayout.test.tsx:41:8 - error TS2559: Type '{ children: Element; }' has no properties in common with type 'IntrinsicAttributes'.

  41       <ParametrageLayout>
            ~~~~~~~~~~~~~~~~~
