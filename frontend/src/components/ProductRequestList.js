import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
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
  IconButton
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon, CheckCircle as CheckCircleIcon, Pending as PendingIcon } from '@mui/icons-material';
import api from '../axiosConfig';

const ProductRequestList = () => {
  const [requests, setRequests] = useState([]);
  const [products, setProducts] = useState([]);
  const [open, setOpen] = useState(false);
  const [newRequest, setNewRequest] = useState({
    product: '',
    quantity: '',
    department: '',
    status: 'pending',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [editMode, setEditMode] = useState(false);
  const [currentRequestId, setCurrentRequestId] = useState(null);

  useEffect(() => {
    fetchRequests();
    fetchProducts();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await api.get('product-requests/');
      setRequests(response.data);
      setLoading(false);
    } catch (err) {
      setError("Failed to fetch requests");
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await api.get('products/');
      setProducts(response.data);
    } catch (err) {
      setError("Failed to fetch products");
    }
  };

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setErrorMessage('');
    setEditMode(false);
    setCurrentRequestId(null);
    setNewRequest({
      product: '',
      quantity: '',
      department: '',
      status: 'pending',
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewRequest({ ...newRequest, [name]: value });
  };

  const handleSave = async () => {
    const payload = { ...newRequest, quantity: parseInt(newRequest.quantity, 10) };
    try {
      if (editMode) {
        await api.patch(`product-requests/${currentRequestId}/update/`, payload);
      } else {
        await api.post('product-requests/create/', payload);
      }
      fetchRequests();
      handleClose();
    } catch (err) {
      setErrorMessage("Failed to save request");
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`product-requests/${id}/delete/`);
      fetchRequests();
    } catch (err) {
      setErrorMessage("Failed to delete request");
    }
  };

  const handleEdit = (request) => {
    setEditMode(true);
    setCurrentRequestId(request.id);
    setNewRequest({
      product: request.product,
      quantity: request.quantity,
      department: request.department,
      status: request.status,
    });
    setOpen(true);
  };

  const handleDistribute = async (id) => {
    try {
      await api.patch(`product-requests/${id}/distribute/`);
      fetchRequests();
    } catch (err) {
      setErrorMessage(err.response.data.detail || "Failed to distribute material");
    }
  };

  const renderStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return <PendingIcon color="warning" />;
      case 'completed':
        return <CheckCircleIcon color="success" />;
      default:
        return null;
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
        Requisições de Materiais
      </Typography>
      <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpen}>
        Nova Requisição
      </Button>
      {errorMessage && (
        <Typography color="error" variant="body2">
          {errorMessage}
        </Typography>
      )}
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Produto</TableCell>
              <TableCell>SKU</TableCell>
              <TableCell>Quantidade</TableCell>
              <TableCell>Departamento</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Data da Requisição</TableCell>
              <TableCell>Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {requests.length > 0 ? (
              requests.map((request) => (
                <TableRow key={request.id}>
                  <TableCell>{request.product_name}</TableCell>
                  <TableCell>{request.product_sku}</TableCell>
                  <TableCell>{request.quantity}</TableCell>
                  <TableCell>{request.department}</TableCell>
                  <TableCell>{renderStatusIcon(request.status)}</TableCell>
                  <TableCell>{request.request_date}</TableCell>
                  <TableCell>
                    <IconButton color="primary" onClick={() => handleEdit(request)} disabled={request.status === 'completed'}>
                      <EditIcon />
                    </IconButton>
                    <IconButton color="secondary" onClick={() => handleDelete(request.id)} disabled={request.status === 'completed'}>
                      <DeleteIcon />
                    </IconButton>
                    {request.status === 'pending' && (
                      <IconButton color="success" onClick={() => handleDistribute(request.id)}>
                        <CheckCircleIcon />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={7}>No data available</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{editMode ? 'Editar Requisição de Produto' : 'Nova Requisição de Produto'}</DialogTitle>
        <DialogContent>
          {errorMessage && (
            <Typography color="error" variant="body2">
              {errorMessage}
            </Typography>
          )}
          <FormControl fullWidth margin="dense">
            <InputLabel>Produto (Nome)</InputLabel>
            <Select
              name="product"
              value={newRequest.product}
              onChange={handleChange}
              label="Produto (Nome)"
            >
              {products.map((product) => (
                <MenuItem key={product.id} value={product.id}>
                  {product.name}
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
            value={newRequest.quantity}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="department"
            label="Departamento"
            type="text"
            fullWidth
            value={newRequest.department}
            onChange={handleChange}
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

export default ProductRequestList;
