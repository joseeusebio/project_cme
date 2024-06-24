import React, { useEffect, useState } from 'react';
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
  FormControl
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  CheckCircle as CheckCircleIcon,
  HourglassEmpty as HourglassEmptyIcon,
  Cancel as CancelIcon
} from '@mui/icons-material';
import api from '../axiosConfig';

const ProductBatchStageList = () => {
  const [ordens, setOrdens] = useState([]);
  const [processos, setProcessos] = useState([]);
  const [batchStocks, setBatchStocks] = useState([]);
  const [openOrdemDialog, setOpenOrdemDialog] = useState(false);
  const [openProcessoDialog, setOpenProcessoDialog] = useState(false);
  const [openViewProcessosDialog, setOpenViewProcessosDialog] = useState(false);
  const [newOrdem, setNewOrdem] = useState({
    batch_stock: '',
    estimated_time_to_complete: '',
  });
  const [newProcesso, setNewProcesso] = useState({
    number_batch_stage: '',
    stage: '',
    quantity_done: '',
  });
  const [currentOrdemId, setCurrentOrdemId] = useState(null);
  const [stages, setStages] = useState([]);
  const [totalBatchQuantity, setTotalBatchQuantity] = useState(0);

  useEffect(() => {
    fetchOrdens();
    fetchBatchStocks();
  }, []);

  const fetchOrdens = async () => {
    const response = await api.get('batch-stages/');
    setOrdens(response.data);
  };

  const fetchBatchStocks = async () => {
    const response = await api.get('batch-stock/');
    setBatchStocks(response.data);
  };

  const fetchProcessos = async (ordemId) => {
    const response = await api.get(`process-batch-stages/?order_id=${ordemId}`);
    setProcessos(response.data);
  };

  const handleOpenOrdemDialog = () => {
    setOpenOrdemDialog(true);
  };

  const handleCloseOrdemDialog = () => {
    setOpenOrdemDialog(false);
    setNewOrdem({
      batch_stock: '',
      estimated_time_to_complete: '',
    });
  };

  const handleOpenProcessoDialog = async (ordemId) => {
    setCurrentOrdemId(ordemId);
    const ordem = ordens.find(o => o.id === ordemId);
    const batch = batchStocks.find(b => b.batch_number === ordem.batch_stock);
    const newStages = [];
    if (batch.needs_washing) newStages.push({ value: 'washing', label: 'Lavagem' });
    if (batch.needs_sterilization) newStages.push({ value: 'sterilization', label: 'Esterilização' });
    if (batch.needs_discard) newStages.push({ value: 'discard', label: 'Descarte' });
    if (newStages.length === 0) newStages.push({ value: 'distribution', label: 'Distribuição' });
    setStages(newStages);
    setTotalBatchQuantity(batch.quantity);
    setOpenProcessoDialog(true);
  };

  const handleCloseProcessoDialog = () => {
    setOpenProcessoDialog(false);
    setNewProcesso({
      number_batch_stage: '',
      stage: '',
      quantity_done: '',
    });
  };

  const handleOpenViewProcessosDialog = (ordemId) => {
    setCurrentOrdemId(ordemId);
    fetchProcessos(ordemId);
    setOpenViewProcessosDialog(true);
  };

  const handleCloseViewProcessosDialog = () => {
    setOpenViewProcessosDialog(false);
    setProcessos([]);
  };

  const handleSaveOrdem = async () => {
    const payload = {
      ...newOrdem,
      estimated_time_to_complete: convertToTimedelta(newOrdem.estimated_time_to_complete),
    };
    await api.post('batch-stages/create/', payload);
    fetchOrdens();
    handleCloseOrdemDialog();
  };

  const handleSaveProcesso = async () => {
    if (newProcesso.quantity_done > totalBatchQuantity) {
      alert("A quantidade realizada não pode exceder a quantidade total do lote.");
      return;
    }
    const payload = {
      ...newProcesso,
      number_batch_stage: currentOrdemId,
      user: localStorage.getItem('user_id'), 
      process_date: new Date().toISOString(), 
    };
    await api.post('process-batch-stages/create/', payload);
    fetchProcessos(currentOrdemId);
    fetchOrdens();
    handleCloseProcessoDialog();
  };

  const handleDeleteOrdem = async (stage_number) => {
    try {
      await api.delete(`batch-stages/${stage_number}/delete/`);
      fetchOrdens();
    } catch (error) {
      console.error("Error deleting order:", error);
    }
  };

  const handleDeleteProcesso = async (id) => {
    await api.delete(`process-batch-stages/${id}/delete/`);
    fetchProcessos(currentOrdemId);
  };

  const handleChangeOrdem = (e) => {
    const { name, value } = e.target;
    setNewOrdem({ ...newOrdem, [name]: value });
  };

  const handleChangeProcesso = (e) => {
    const { name, value } = e.target;
    setNewProcesso({ ...newProcesso, [name]: value });
  };

  const convertToTimedelta = (timeString) => {
    const [hours, minutes] = timeString.split(':').map(Number);
    return `${hours}:${minutes}:00`;
  };

  const renderStatusIcon = (status) => {
    switch (status) {
      case 'pending':
        return <HourglassEmptyIcon color="warning" />;
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'not_needed':
        return <CancelIcon color="disabled" />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Ordem de Tratamento
      </Typography>
      <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpenOrdemDialog}>
        Nova Ordem de Tratamento
      </Button>
      <TableContainer sx={{ marginTop: 2 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Order Number</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Tempo Estimado para Completar</TableCell>
              <TableCell>Data de Conclusão</TableCell>
              <TableCell>Quantidade Total do Lote</TableCell>
              <TableCell>Lavagem</TableCell>
              <TableCell>Esterilização</TableCell>
              <TableCell>Descarte</TableCell>
              <TableCell>Distribuição</TableCell>
              <TableCell>Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {ordens.map((ordem) => (
              <TableRow key={ordem.stage_number}>
                <TableCell>{ordem.stage_number}</TableCell>
                <TableCell>{ordem.stage_status}</TableCell>
                <TableCell>{ordem.estimated_time_to_complete}</TableCell>
                <TableCell>{ordem.completion_date}</TableCell>
                <TableCell>{batchStocks.find(batch => batch.batch_number === ordem.batch_stock)?.quantity}</TableCell>
                <TableCell>{renderStatusIcon(ordem.washing_status)}</TableCell>
                <TableCell>{renderStatusIcon(ordem.sterilization_status)}</TableCell>
                <TableCell>{renderStatusIcon(ordem.discard_status)}</TableCell>
                <TableCell>{renderStatusIcon(ordem.distribution_status)}</TableCell>
                <TableCell>
                  <IconButton color="secondary" onClick={() => handleDeleteOrdem(ordem.stage_number)}>
                    <DeleteIcon />
                  </IconButton>
                  <IconButton color="primary" onClick={() => handleOpenProcessoDialog(ordem.id)}>
                    <AddIcon />
                  </IconButton>
                  <IconButton color="default" onClick={() => handleOpenViewProcessosDialog(ordem.id)}>
                    <VisibilityIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Dialog open={openOrdemDialog} onClose={handleCloseOrdemDialog}>
        <DialogTitle>Nova Ordem de Tratamento</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="dense">
            <InputLabel>Lote</InputLabel>
            <Select
              name="batch_stock"
              value={newOrdem.batch_stock}
              onChange={handleChangeOrdem}
              label="Lote"
            >
              {batchStocks.map((batch) => (
                <MenuItem key={batch.batch_number} value={batch.batch_number}>
                  Lote:{batch.batch_number} - SKU:{batch.product_sku}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            name="estimated_time_to_complete"
            label="Tempo Estimado para Completar (HH:MM)"
            type="text"
            fullWidth
            value={newOrdem.estimated_time_to_complete}
            onChange={handleChangeOrdem}
            placeholder="00:00"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseOrdemDialog} color="primary">
            Cancelar
          </Button>
          <Button onClick={handleSaveOrdem} color="primary">
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={openProcessoDialog} onClose={handleCloseProcessoDialog}>
        <DialogTitle>Novo Processo</DialogTitle>
        <DialogContent>
          <FormControl fullWidth margin="dense">
            <InputLabel>Fase</InputLabel>
            <Select
              name="stage"
              value={newProcesso.stage}
              onChange={handleChangeProcesso}
              label="Fase"
            >
              {stages.map((stage) => (
                <MenuItem key={stage.value} value={stage.value}>
                  {stage.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            name="quantity_done"
            label={`Quantidade Realizada (Total do Lote: ${totalBatchQuantity})`}
            type="number"
            fullWidth
            value={newProcesso.quantity_done}
            onChange={handleChangeProcesso}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseProcessoDialog} color="primary">
            Cancelar
          </Button>
          <Button onClick={handleSaveProcesso} color="primary">
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={openViewProcessosDialog} onClose={handleCloseViewProcessosDialog}>
        <DialogTitle>Processos da Ordem</DialogTitle>
        <DialogContent>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Usuário</TableCell>
                  <TableCell>Data do Processo</TableCell>
                  <TableCell>Quantidade Realizada</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {processos.map((processo) => (
                  <TableRow key={processo.id}>
                    <TableCell>{processo.user}</TableCell>
                    <TableCell>{processo.process_date}</TableCell>
                    <TableCell>{processo.quantity_done}</TableCell>
                    <TableCell>
                      <IconButton color="secondary" onClick={() => handleDeleteProcesso(processo.id)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseViewProcessosDialog} color="primary">
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProductBatchStageList;
