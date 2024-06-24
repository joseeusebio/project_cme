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
  NotInterested as NotStartedIcon,
  Cancel as CancelIcon,
  Pending as PendingIcon
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
  });
  const [currentOrdemId, setCurrentOrdemId] = useState(null);
  const [stages, setStages] = useState([]);
  const [totalBatchQuantity, setTotalBatchQuantity] = useState(0);
  const [errorMessage, setErrorMessage] = useState('');

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
    const response = await api.get(`process-batch-stages/order/${ordemId}/`);
    setProcessos(response.data);
  };

  const handleOpenOrdemDialog = () => {
    setOpenOrdemDialog(true);
  };

  const handleCloseOrdemDialog = () => {
    setOpenOrdemDialog(false);
    setErrorMessage('');
    setNewOrdem({
      batch_stock: '',
      estimated_time_to_complete: '',
    });
  };

  const handleOpenProcessoDialog = async (ordemId) => {
    setCurrentOrdemId(ordemId);
    const ordem = ordens.find(o => o.id === ordemId);
    if (ordem.stage_status === 'completed') {
      setErrorMessage("A ordem de tratamento foi concluída e não pode receber novos processos.");
      return;
    }
    const pendingStages = [];
    if (ordem.washing_status === 'pending') pendingStages.push({ value: 'lavagem', label: 'Lavagem' });
    if (ordem.sterilization_status === 'pending') pendingStages.push({ value: 'esterilizacao', label: 'Esterilização' });
    if (ordem.discard_status === 'pending') pendingStages.push({ value: 'descarte', label: 'Descarte' });
    if (ordem.distribution_status === 'pending') pendingStages.push({ value: 'distribuicao', label: 'Distribuição' });
    setStages(pendingStages);
    const batch = batchStocks.find(b => b.batch_number === ordem.batch_stock);
    setTotalBatchQuantity(batch.quantity);
    setOpenProcessoDialog(true);
  };

  const handleCloseProcessoDialog = () => {
    setOpenProcessoDialog(false);
    setNewProcesso({
      number_batch_stage: '',
      stage: '',
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

    try {
      await api.post('batch-stages/create/', payload);
      fetchOrdens();
      handleCloseOrdemDialog();
    } catch (error) {
      if (error.response && error.response.data) {
        setErrorMessage(error.response.data.detail || 'Erro ao criar a ordem de tratamento');
      } else {
        setErrorMessage('Erro ao criar a ordem de tratamento');
      }
    }
  };

  const handleSaveProcesso = async () => {
    const ordem = ordens.find(o => o.id === currentOrdemId);
    if (!ordem) {
      alert("Ordem de tratamento não encontrada.");
      return;
    }
    const userId = localStorage.getItem('user_id');
    const payload = {
      ...newProcesso,
      number_batch_stage: ordem.stage_number,
      processed_by: userId,
      process_date: new Date().toISOString(), 
    };
    try {
      await api.post('process-batch-stages/create/', payload);
      fetchProcessos(currentOrdemId);
      fetchOrdens(); 
      handleCloseProcessoDialog();
    } catch (error) {
      if (error.response && error.response.data) {
        setErrorMessage(error.response.data.detail || 'Erro ao criar o processo');
      } else {
        setErrorMessage('Erro ao criar o processo');
      }
    }
  };

  const handleDeleteOrdem = async (stage_number) => {
    try {
      await api.delete(`batch-stages/${stage_number}/delete/`);
      fetchOrdens();
    } catch (error) {
      if (error.response && error.response.data) {
        setErrorMessage(error.response.data.detail || 'Erro ao deletar a ordem de tratamento');
      } else {
        setErrorMessage('Erro ao deletar a ordem de tratamento');
      }
    }
  };

  const handleDeleteProcesso = async (id) => {
    try {
      await api.delete(`process-batch-stages/${id}/delete/`);
      fetchProcessos(currentOrdemId);
    } catch (error) {
      if (error.response && error.response.data) {
        setErrorMessage(error.response.data.detail || 'Não é possível excluir processos de uma ordem de tratamento concluída.');
      } else {
        setErrorMessage('Erro ao deletar o processo');
      }
    }
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
        return <PendingIcon color="warning" />;
      case 'completed':
        return <CheckCircleIcon color="success" />;
      case 'not_needed':
        return <CancelIcon color="disabled" />;
      case 'not_started':
        return <NotStartedIcon color="disabled" />;
      default:
        return null;
    }
  };

  const renderStatusText = (status) => {
    switch (status) {
      case 'not_started':
        return 'Não Iniciado';
      case 'in_process':
        return 'Em Processo';
      case 'completed':
        return 'Concluído';
      case 'pending':
        return 'Pendente';
      case 'not_needed':
        return 'Não Necessário';
      default:
        return status;
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
              <TableCell>Tempo Estimado</TableCell>
              <TableCell>Data de Conclusão</TableCell>
              <TableCell>Lote Associado</TableCell>
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
                <TableCell>{renderStatusText(ordem.stage_status)}</TableCell>
                <TableCell>{ordem.estimated_time_to_complete}</TableCell>
                <TableCell>{ordem.completion_date}</TableCell>
                <TableCell>{ordem.batch_stock}</TableCell>
                <TableCell>{batchStocks.find(batch => batch.batch_number === ordem.batch_stock)?.quantity}</TableCell>
                <TableCell>{renderStatusIcon(ordem.washing_status)}</TableCell>
                <TableCell>{renderStatusIcon(ordem.sterilization_status)}</TableCell>
                <TableCell>{renderStatusIcon(ordem.discard_status)}</TableCell>
                <TableCell>{renderStatusIcon(ordem.distribution_status)}</TableCell>
                <TableCell>
                  <IconButton color="secondary" onClick={() => handleDeleteOrdem(ordem.stage_number)} disabled={ordem.stage_status === 'completed'}>
                    <DeleteIcon />
                  </IconButton>
                  <IconButton color="primary" onClick={() => handleOpenProcessoDialog(ordem.id)} disabled={ordem.stage_status === 'completed'}>
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
              {errorMessage && (
                  <Typography color="error" variant="body2">
                      {errorMessage}
                  </Typography>
              )}
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
          {errorMessage && (
            <Typography color="error" variant="body2">
              {errorMessage}
            </Typography>
          )}
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
          {errorMessage && (
            <Typography color="error" variant="body2">
              {errorMessage}
            </Typography>
          )}
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Usuário</TableCell>
                  <TableCell>Data do Processo</TableCell>
                  <TableCell>Fase</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {processos.map((processo) => (
                  <TableRow key={processo.id}>
                    <TableCell>{processo.user_name}</TableCell>
                    <TableCell>{processo.process_date}</TableCell>
                    <TableCell>{processo.stage}</TableCell>
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
