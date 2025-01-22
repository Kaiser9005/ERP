export interface Utilisateur {
  id: string;
  email: string;
  nom: string;
  prenom: string;
  role: string;
  permissions: string[];
}

export interface ContexteAuthType {
  utilisateur: Utilisateur | null;
  estAuthentifie: boolean;
  connexion: (nomUtilisateur: string, motDePasse: string) => Promise<void>;
  deconnexion: () => void;
}

export interface IdentifiantsConnexion {
  email: string;
  motDePasse: string;
}
