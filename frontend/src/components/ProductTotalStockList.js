import React, { useEffect, useState } from 'react';
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from '@mui/material';
import api from '../axiosConfig';

const ProductTotalStockList = () => {
  const [totalStocks, setTotalStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTotalStocks();
  }, []);

  const fetchTotalStocks = async () => {
    try {
      const response = await api.get('total-stock/');
      setTotalStocks(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to fetch total stocks");
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography variant="h6">Loading...</Typography>;
  }

  if (error) {
    return <Typography variant="h6" color="error">{error}</Typography>;
  }

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Saldo Total de Produtos
      </Typography>
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Produto (Nome)</TableCell>
              <TableCell>SKU</TableCell>
              <TableCell>Saldo Total</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {totalStocks.length > 0 ? (
              totalStocks.map((totalStock, index) => (
                <TableRow key={index}>
                  <TableCell>{totalStock.product_name}</TableCell>
                  <TableCell>{totalStock.product_sku}</TableCell>
                  <TableCell>{totalStock.total_quantity}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3}>No data available</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ProductTotalStockList;
