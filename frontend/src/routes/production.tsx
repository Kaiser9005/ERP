import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ProductionPage from '../components/production/ProductionPage';
import ParcelleForm from '../components/production/ParcelleForm';
import ParcelleDetails from '../components/production/ParcelleDetails';
import { IoTDashboard } from '../components/production/IoTDashboard';
import TableauMeteo from '../components/production/TableauMeteo';
import ProductionStats from '../components/production/ProductionStats';

const ProductionRoutes: React.FC = () => {
  return (
    <Routes>
      <Route index element={<ProductionPage />} />
      <Route path="parcelles/new" element={<ParcelleForm />} />
      <Route path="parcelles/:id" element={<ParcelleDetails />} />
      <Route path="parcelles/:id/edit" element={<ParcelleForm />} />
      <Route path="iot/:parcelleId" element={<IoTDashboard parcelleId={':parcelleId'} />} />
      <Route path="meteo" element={<TableauMeteo />} />
      <Route path="stats" element={<ProductionStats />} />
    </Routes>
  );
};

export default ProductionRoutes;
