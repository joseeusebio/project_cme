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

  useEffect(() => {
    fetchTotalStocks();
  }, []);

  const fetchTotalStocks = async () => {
    const response = await api.get('total-stock/');
    setTotalStocks(response.data);
  };

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Saldo Total de Produtos
      </Typography>
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Produto</TableCell>
              <TableCell>Saldo Total</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {totalStocks.map((totalStock) => (
              <TableRow key={totalStock.product.id}>
                <TableCell>{totalStock.product.name}</TableCell>
                <TableCell>{totalStock.total_quantity}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ProductTotalStockList;
