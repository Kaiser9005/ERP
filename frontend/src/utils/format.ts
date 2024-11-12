/**
 * Formate un nombre en devise XAF
 * @param amount - Montant à formater
 * @returns Chaîne formatée (ex: "1 000 000 XAF")
 */
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'XAF',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

/**
 * Formate un pourcentage
 * @param value - Valeur à formater
 * @param decimals - Nombre de décimales (défaut: 1)
 * @returns Chaîne formatée (ex: "10,5%")
 */
export const formatPercentage = (value: number, decimals: number = 1): string => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value / 100);
};

/**
 * Formate une date au format local
 * @param date - Date à formater
 * @returns Chaîne formatée (ex: "01/01/2024")
 */
export const formatDate = (date: string | Date): string => {
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(typeof date === 'string' ? new Date(date) : date);
};

/**
 * Formate un montant en texte
 * @param amount - Montant à convertir
 * @returns Montant en lettres (ex: "Un million cinq cent mille francs CFA")
 */
export const amountToText = (amount: number): string => {
  const units = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf'];
  const teens = ['dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf'];
  const tens = ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante-dix', 'quatre-vingt', 'quatre-vingt-dix'];
  
  const convertLessThanThousand = (n: number): string => {
    if (n === 0) return '';
    
    let result = '';
    
    // Centaines
    if (n >= 100) {
      result += (n >= 200 ? units[Math.floor(n / 100)] + ' ' : '') + 'cent ';
      n %= 100;
    }
    
    // Dizaines et unités
    if (n >= 10 && n < 20) {
      result += teens[n - 10];
    } else {
      const ten = Math.floor(n / 10);
      const unit = n % 10;
      
      if (ten > 0) {
        result += tens[ten];
        if (unit > 0) {
          result += '-' + units[unit];
        }
      } else if (unit > 0) {
        result += units[unit];
      }
    }
    
    return result.trim();
  };
  
  if (amount === 0) return 'zéro franc CFA';
  
  const billions = Math.floor(amount / 1000000000);
  const millions = Math.floor((amount % 1000000000) / 1000000);
  const thousands = Math.floor((amount % 1000000) / 1000);
  const remainder = amount % 1000;
  
  let result = '';
  
  if (billions > 0) {
    result += (billions > 1 ? convertLessThanThousand(billions) + ' milliards ' : 'un milliard ');
  }
  
  if (millions > 0) {
    result += (millions > 1 ? convertLessThanThousand(millions) + ' millions ' : 'un million ');
  }
  
  if (thousands > 0) {
    result += (thousands > 1 ? convertLessThanThousand(thousands) + ' mille ' : 'mille ');
  }
  
  if (remainder > 0) {
    result += convertLessThanThousand(remainder);
  }
  
  return result.trim() + ' francs CFA';
};
