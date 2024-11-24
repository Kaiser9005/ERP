import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { Box, Typography, Paper } from '@mui/material';
import { Parcelle } from '../../types/production';
import { api } from "/home/user/ERP/src/services/api"
interface ParcelleMapProps {
  onParcelleSelect?: (parcelle: Parcelle) => void;
}

const ParcelleMap: React.FC<ParcelleMapProps> = ({ onParcelleSelect }) => {
  const [parcelles, setParcelles] = useState<Parcelle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchParcelles = async () => {
      try {
        const response = await api.get('/api/v1/production/parcelles');
        setParcelles(response.data);
      } catch (error) {
        console.error('Erreur lors du chargement des parcelles:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchParcelles();
  }, []);

  if (loading) {
    return <Typography>Chargement de la carte...</Typography>;
  }

  return (
    <Paper elevation={3} sx={{ p: 2, height: '500px' }}>
      <Box sx={{ height: '100%', width: '100%' }}>
        <MapContainer
          center={[4.0511, 9.7679]} // Coordonnées de Douala comme point central
          zoom={13}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {parcelles.map((parcelle) => (
            <Marker
              key={parcelle.id}
              position={[
                parcelle.coordonnees_gps.latitude,
                parcelle.coordonnees_gps.longitude
              ]}
              eventHandlers={{
                click: () => onParcelleSelect?.(parcelle)
              }}
            >
              <Popup>
                <Typography variant="subtitle1">
                  {parcelle.code} - {parcelle.culture_type}
                </Typography>
                <Typography variant="body2">
                  Surface: {parcelle.surface_hectares} ha
                </Typography>
                <Typography variant="body2">
                  Statut: {parcelle.statut}
                </Typography>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </Box>
    </Paper>
  );
};

export default ParcelleMap;
