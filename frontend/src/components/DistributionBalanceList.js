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

const DistributionBalanceList = () => {
  const [distributionBalances, setDistributionBalances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDistributionBalances();
  }, []);

  const fetchDistributionBalances = async () => {
    try {
      const response = await api.get('distribution-balance/');
      setDistributionBalances(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to fetch distribution balances");
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
        Saldo a Distribuir
      </Typography>
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Produto (Nome)</TableCell>
              <TableCell>SKU</TableCell>
              <TableCell>Saldo a Distribuir</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {distributionBalances.length > 0 ? (
              distributionBalances.map((distributionBalance, index) => (
                <TableRow key={index}>
                  <TableCell>{distributionBalance.product_name}</TableCell>
                  <TableCell>{distributionBalance.product_sku}</TableCell>
                  <TableCell>{distributionBalance.total_quantity}</TableCell>
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

export default DistributionBalanceList;
