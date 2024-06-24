import React, { useEffect, useState } from 'react';
import api from '../axiosConfig';
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
  Alert
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

const categories = [
  { value: 'surgical', label: 'Surgical - Instrumentos Cirúrgicos' },
  { value: 'imaging', label: 'Imaging - Equipamentos de Visualização' },
  { value: 'anesthesia', label: 'Anesthesia - Dispositivos de Anestesia' },
  { value: 'catheterization', label: 'Catheterization - Material de Cateterização e Drenagem' },
  { value: 'dental', label: 'Dental - Instrumental Odontológico' },
  { value: 'containers', label: 'Containers - Recipientes e Acessórios' },
  { value: 'obstetric', label: 'Obstetric - Instrumental para Parto' },
  { value: 'ppe', label: 'PPE - Equipamento de Proteção Individual (Personal Protective Equipment)' },
];

const units = [
  { value: 'pc', label: 'Peça' },
  { value: 'set', label: 'Conjunto' },
  { value: 'unit', label: 'Unidade' },
  { value: 'pk', label: 'Pacote' },
  { value: 'box', label: 'Caixa' },
];

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [open, setOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    const response = await api.get('products/');
    setProducts(response.data);
  };

  const handleOpen = (product = null) => {
    setEditingProduct(product);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingProduct(null);
    setError(null);
  };

  const handleSave = async () => {
    try {
      if (editingProduct.id) {
        await api.patch(`products/${editingProduct.sku}/update/`, editingProduct);
      } else {
        await api.post('products/create/', editingProduct);
      }
      fetchProducts();
      handleClose();
    } catch (error) {
      setError('Erro ao salvar o produto.');
    }
  };

  const handleDelete = async (sku) => {
    try {
      await api.delete(`products/${sku}/delete/`);
      fetchProducts();
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error);
      } else {
        setError('Erro ao deletar o produto.');
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditingProduct({ ...editingProduct, [name]: value });
  };

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Produtos
      </Typography>
      {error && <Alert severity="error">{error}</Alert>}
      <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={() => handleOpen()}>
        Adicionar Produto
      </Button>
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Descrição</TableCell>
              <TableCell>SKU</TableCell>
              <TableCell>Categoria</TableCell>
              <TableCell>Fabricante</TableCell>
              <TableCell>Unidade</TableCell>
              <TableCell>Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {products.map((product) => (
              <TableRow key={product.id}>
                <TableCell>{product.name}</TableCell>
                <TableCell>{product.description}</TableCell>
                <TableCell>{product.sku}</TableCell>
                <TableCell>{product.category}</TableCell>
                <TableCell>{product.manufacturer}</TableCell>
                <TableCell>{product.unit}</TableCell>
                <TableCell>
                  <IconButton color="primary" onClick={() => handleOpen(product)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton color="secondary" onClick={() => handleDelete(product.sku)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{editingProduct?.id ? 'Editar Produto' : 'Adicionar Produto'}</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            name="name"
            label="Nome"
            type="text"
            fullWidth
            value={editingProduct?.name || ''}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="description"
            label="Descrição"
            type="text"
            fullWidth
            value={editingProduct?.description || ''}
            onChange={handleChange}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>Categoria</InputLabel>
            <Select
              name="category"
              value={editingProduct?.category || ''}
              onChange={handleChange}
              label="Categoria"
            >
              {categories.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            name="manufacturer"
            label="Fabricante"
            type="text"
            fullWidth
            value={editingProduct?.manufacturer || ''}
            onChange={handleChange}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>Unidade</InputLabel>
            <Select
              name="unit"
              value={editingProduct?.unit || ''}
              onChange={handleChange}
              label="Unidade"
            >
              {units.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
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

export default ProductList;
