const LOCALE = 'fr-FR';

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat(LOCALE, {
    style: 'currency',
    currency: 'XAF',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

export const formatDate = (date: string | Date): string => {
  if (!date) return '';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat(LOCALE, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(d);
};

export const formatDateTime = (date: string | Date): string => {
  if (!date) return '';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat(LOCALE, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(d);
};

export const formatNumber = (value: number, options?: Intl.NumberFormatOptions): string => {
  return new Intl.NumberFormat(LOCALE, options).format(value);
};

export const formatPercentage = (value: number): string => {
  return new Intl.NumberFormat(LOCALE, {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value / 100);
};

export const formatDecimal = (value: number, decimals: number = 2): string => {
  return new Intl.NumberFormat(LOCALE, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value);
};

export const parseDate = (dateStr: string): Date | null => {
  if (!dateStr) return null;
  
  const parts = dateStr.split('/');
  if (parts.length !== 3) return null;
  
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1;
  const year = parseInt(parts[2], 10);
  
  const date = new Date(year, month, day);
  return date.toString() === 'Invalid Date' ? null : date;
};

export const formatDateForAPI = (date: Date): string => {
  return date.toISOString().split('T')[0];
};

export const formatPeriode = (debut: string | Date, fin: string | Date): string => {
  return `${formatDate(debut)} - ${formatDate(fin)}`;
};

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

export const slugify = (text: string): string => {
  return text
    .toString()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w-]+/g, '')
    .replace(/--+/g, '-');
};

export const truncate = (text: string, length: number = 50): string => {
  if (!text || text.length <= length) return text;
  return `${text.substring(0, length)}...`;
};
