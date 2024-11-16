export interface CashFlowData {
  labels: string[];
  recettes: number[];
  depenses: number[];
  solde: number[];
  previsions: number[];
  impact_meteo: number[];
}

export interface CashFlowResponse {
  data: CashFlowData;
  total_recettes: number;
  total_depenses: number;
  solde_final: number;
}
