import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="lg">
        <Toolbar>
          <PictureAsPdfIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            PDF Task Processor
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar; 