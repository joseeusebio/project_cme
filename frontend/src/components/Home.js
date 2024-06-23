import React from 'react';
import { Typography, Box, Container, CssBaseline } from '@mui/material';
import { styled } from '@mui/system';

const BackgroundBox = styled(Box)(({ theme }) => ({
  backgroundColor: '#e0f2f1',
  minHeight: '100vh',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
}));

const StyledContainer = styled(Container)(({ theme }) => ({
  padding: theme.spacing(4),
  backgroundColor: '#ffffff',
  borderRadius: theme.spacing(1),
  boxShadow: '0 3px 5px rgba(0,0,0,0.2)',
}));

const Home = () => {
  return (
    <BackgroundBox>
      <StyledContainer component="main" maxWidth="md">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h4" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
            Bem-vindo ao MedTrace
          </Typography>
          <Typography component="h2" variant="h6" sx={{ mb: 2, color: 'secondary.main' }}>
            Central de Material e Esterilização
          </Typography>
          <Typography variant="body1">
            Esta é a página inicial do dashboard.
          </Typography>
        </Box>
      </StyledContainer>
    </BackgroundBox>
  );
};

export default Home;
