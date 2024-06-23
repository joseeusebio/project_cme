import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import api from '../axiosConfig';

const conditions = [
  { value: 'new', label: 'New' },
  { value: 'used', label: 'Used' },
  { value: 'damaged', label: 'Damaged' },
];

const ProductBatchStockList = () => {
  const [batchStocks, setBatchStocks] = useState([]);
  const [open, setOpen] = useState(false);
  const [products, setProducts] = useState([]);
  const [newBatchStock, setNewBatchStock] = useState({
    product: '',
    quantity: '',
    expiration_date: '',
    condition: 'new',
    needs_washing: true,
    needs_sterilization: true,
  });

  useEffect(() => {
    fetchBatchStocks();
    fetchProducts();
  }, []);

  const fetchBatchStocks = async () => {
    const response = await api.get('batch-stock/');
    setBatchStocks(response.data);
  };

  const fetchProducts = async () => {
    const response = await api.get('products/');
    setProducts(response.data);
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setNewBatchStock({
      product: '',
      quantity: '',
      expiration_date: '',
      condition: 'new',
      needs_washing: true,
      needs_sterilization: true,
    });
  };

  const handleSave = async () => {
    const payload = { ...newBatchStock };
    if (!payload.expiration_date) {
      delete payload.expiration_date;
    }
    await api.post('batch-stocks/create/', payload);
    fetchBatchStocks();
    handleClose();
  };

  const handleDelete = async (id) => {
    await api.delete(`batch-stocks/${id}/`);
    fetchBatchStocks();
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewBatchStock({
      ...newBatchStock,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Recebimento de Materiais
      </Typography>
      <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpen}>
        Novo Recebimento
      </Button>
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Produto (SKU)</TableCell>
              <TableCell>Número do Lote</TableCell>
              <TableCell>Quantidade</TableCell>
              <TableCell>Data de Expiração</TableCell>
              <TableCell>Data de Entrada</TableCell>
              <TableCell>Última Atualização</TableCell>
              <TableCell>Condição</TableCell>
              <TableCell>Necessita Lavagem</TableCell>
              <TableCell>Necessita Esterilização</TableCell>
              <TableCell>Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {batchStocks.map((batchStock) => (
              <TableRow key={batchStock.id}>
                <TableCell>{batchStock.product_sku}</TableCell>
                <TableCell>{batchStock.batch_number}</TableCell>
                <TableCell>{batchStock.quantity}</TableCell>
                <TableCell>{batchStock.expiration_date}</TableCell>
                <TableCell>{batchStock.entry_date}</TableCell>
                <TableCell>{batchStock.last_updated}</TableCell>
                <TableCell>{batchStock.condition}</TableCell>
                <TableCell>{batchStock.needs_washing ? 'Sim' : 'Não'}</TableCell>
                <TableCell>{batchStock.needs_sterilization ? 'Sim' : 'Não'}</TableCell>
                <TableCell>
                  <IconButton color="secondary" onClick={() => handleDelete(batchStock.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Novo Recebimento</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="dense">
            <InputLabel>Produto (SKU)</InputLabel>
            <Select
              name="product"
              value={newBatchStock.product}
              onChange={handleChange}
              label="Produto (SKU)"
            >
              {products.map((product) => (
                <MenuItem key={product.sku} value={product.sku}>
                  {product.sku} | {product.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            name="quantity"
            label="Quantidade"
            type="number"
            fullWidth
            value={newBatchStock.quantity}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="expiration_date"
            label="Data de Expiração"
            type="date"
            fullWidth
            value={newBatchStock.expiration_date}
            onChange={handleChange}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>Condição</InputLabel>
            <Select
              name="condition"
              value={newBatchStock.condition}
              onChange={handleChange}
              label="Condição"
            >
              {conditions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControlLabel
            control={
              <Checkbox
                checked={newBatchStock.needs_washing}
                onChange={handleChange}
                name="needs_washing"
                color="primary"
              />
            }
            label="Necessita Lavagem"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={newBatchStock.needs_sterilization}
                onChange={handleChange}
                name="needs_sterilization"
                color="primary"
              />
            }
            label="Necessita Esterilização"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancelar
          </Button>
          <Button onClick={handleSave} color="primary">
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProductBatchStockList;
