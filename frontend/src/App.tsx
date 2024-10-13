import 'leaflet/dist/leaflet.css';
import { MapView } from './components/MapView/MapView';
import { Modal, Box, Button, Typography, FormGroup, FormControlLabel, Checkbox } from '@mui/material';
import { useUserStore } from './state/State';
import { useEffect } from 'react';

const App = () => {
  const isModalOpen = useUserStore((state) => state.isModalOpen);
  const openModal = useUserStore((state) => state.openModal);
  const closeModal = useUserStore((state) => state.closeModal);
  const showMuseos = useUserStore((state) => state.showMuseos);
  const showMonumentos = useUserStore((state) => state.showMonumentos);
  const showIglesias = useUserStore((state) => state.showIglesias);
  const setShowMuseos = useUserStore((state) => state.setShowMuseos);
  const setShowMonumentos = useUserStore((state) => state.setShowMonumentos);
  const setShowIglesias = useUserStore((state) => state.setShowIglesias);

  useEffect(() => {
    openModal();
  }, [openModal]);

  return (
    <div style={{ height: "100vh" }}>
      <Button
        variant="contained"
        color="primary"
        onClick={openModal}
        style={{ position: 'absolute', zIndex: 1000 }}
      >
        Abrir Modal
      </Button>

      <MapView />

      <Modal
        open={isModalOpen}
        onClose={closeModal}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: 400,
            bgcolor: 'background.paper',
            boxShadow: 24,
            p: 4,
            borderRadius: 2,
          }}
        >
          <Typography id="modal-title" variant="h6" component="h2">
            Configuración de Marcadores
          </Typography>
          <FormGroup>
            <FormControlLabel
              control={<Checkbox />}
              label="Mostrar Museos"
              onChange={() => setShowMuseos(!showMuseos)}
              checked={showMuseos}
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Mostrar Monumentos"
              onChange={() => setShowMonumentos(!showMonumentos)}
              checked={showMonumentos}
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Mostrar Iglesias"
              onChange={() => setShowIglesias(!showIglesias)}
              checked={showIglesias}
            />
            <FormControlLabel
              control={<Checkbox />}
              label="Mostrar Parques"
            />
          </FormGroup>
          <Button onClick={closeModal} variant="contained" color="primary" sx={{ mt: 3 }}>
            Cerrar
          </Button>
        </Box>
      </Modal>
    </div>
  );
}

export default App;
