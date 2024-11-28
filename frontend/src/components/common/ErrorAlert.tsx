import React from 'react';
import { Alert, AlertTitle } from '@mui/material';

interface ErrorAlertProps {
  message: string;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({ message }) => {
  return (
    <Alert 
      severity="error"
      role="alert"
      aria-live="assertive"
    >
      <AlertTitle>Erreur</AlertTitle>
      {message}
    </Alert>
  );
};

export default ErrorAlert;
