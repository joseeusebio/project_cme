import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Link, useHistory } from 'react-router-dom';
import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, AppBar, Typography, Box, Button, Avatar } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import InventoryIcon from '@mui/icons-material/Inventory';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';
import AssignmentIcon from '@mui/icons-material/Assignment';
import Home from './Home';
import ProductList from './ProductList';
import ProductTotalStockList from './ProductTotalStockList'; 
import ProductBatchStockList from './ProductBatchStockList'; 
import ProductBatchStageList from './ProductBatchStageList'; 
import api from '../axiosConfig';

const drawerWidth = 240;

const Dashboard = () => {
  const history = useHistory();
  const [userName, setUserName] = useState('');

  useEffect(() => {
    fetchUserName();
  }, []);

  const fetchUserName = async () => {
    try {
      const response = await api.get('api/user/');
      setUserName(response.data.name);
    } catch (error) {
      console.error('Failed to fetch user name:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];
    history.push('/login');
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h6" noWrap component="div">
            MedTrace Dashboard
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            {userName && (
              <Typography variant="h6" component="span" sx={{ marginRight: 2 }}>
                Bem-vindo, {userName}
              </Typography>
            )}
            <Button variant="contained" color="secondary" onClick={handleLogout}>
              Logout
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar>
          <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
            <MedicalServicesIcon />
          </Avatar>
          <Typography variant="h6" noWrap component="div">
            MedTrace
          </Typography>
        </Toolbar>
        <Box sx={{ overflow: 'auto' }}>
          <List>
            <ListItemButton component={Link} to="/">
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Home" />
            </ListItemButton>
            <ListItemButton component={Link} to="/produtos">
              <ListItemIcon>
                <InventoryIcon />
              </ListItemIcon>
              <ListItemText primary="Produtos" />
            </ListItemButton>
            <ListItemButton component={Link} to="/total-stock">
              <ListItemIcon>
                <InventoryIcon />
              </ListItemIcon>
              <ListItemText primary="Saldo Total" />
            </ListItemButton>
            <ListItemButton component={Link} to="/batch-stock">
              <ListItemIcon>
                <MedicalServicesIcon />
              </ListItemIcon>
              <ListItemText primary="Recebimento de Materiais" />
            </ListItemButton>
            <ListItemButton component={Link} to="/batch-stage">
              <ListItemIcon>
                <AssignmentIcon />
              </ListItemIcon>
              <ListItemText primary="Ordem de Tratamento" />
            </ListItemButton>
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}>
        <Toolbar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/produtos" component={ProductList} />
          <Route path="/total-stock" component={ProductTotalStockList} />
          <Route path="/batch-stock" component={ProductBatchStockList} />
          <Route path="/batch-stage" component={ProductBatchStageList} />
        </Switch>
      </Box>
    </Box>
  );
};

export default Dashboard;
