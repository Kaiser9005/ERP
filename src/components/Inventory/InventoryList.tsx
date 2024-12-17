import React from 'react';

interface Product {
  id: number;
  name: string;
  price: number;
}

const InventoryList: React.FC = () => {
  const products: Product[] = [
    { id: 1, name: 'Product 1', price: 100 },
    { id: 2, name: 'Product 2', price: 200 }
  ];

  return (
    <div>
      {products.map((product) => (
        <div key={product.id}>
          <p>{product.name}</p>
          <p>{product.price}</p>
        </div>
      ))}
    </div>
  );
};

export default InventoryList;
