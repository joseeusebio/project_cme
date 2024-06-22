import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, AppBar, Typography, Box } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import InventoryIcon from '@mui/icons-material/Inventory';
import Home from './Home';
import ProductPage from './ProductPage'; 
const drawerWidth = 240;

const Dashboard = () => {
  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <AppBar position="fixed" sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              MedTrace Dashboard
            </Typography>
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
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>
            <List>
              <ListItemButton component={Link} to="/">
                <ListItemIcon>
                  <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Home" />
              </ListItemButton>
              <ListItemButton component={Link} to="/cadastro-produto">
                <ListItemIcon>
                  <InventoryIcon />
                </ListItemIcon>
                <ListItemText primary="Cadastro Produto" />
              </ListItemButton>
            </List>
          </Box>
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}>
          <Toolbar />
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/cadastro-produto" component={ProductPage} />
          </Switch>
        </Box>
      </Box>
    </Router>
  );
};

export default Dashboard;
