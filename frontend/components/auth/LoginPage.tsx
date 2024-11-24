import React from 'react'
import { Box, Card, CardContent, Typography } from '@mui/material'

const LoginPage: React.FC = () => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 3,
      }}
    >
      <Card>
        <CardContent>
          <Typography variant="h4" component="h1" gutterBottom>
            FOFAL ERP
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Connexion en cours de développement...
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}

export default LoginPage