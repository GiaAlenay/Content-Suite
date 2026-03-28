import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Divider,
  Typography,
  Button,
} from "@mui/material";
import { Outlet, useNavigate } from "react-router-dom";

const drawerWidth = 240;

export const DashboardLayout = () => {
  const navigate = useNavigate();

  return (
    <Box sx={{ display: "flex" }}>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" fontWeight="bold">
            Menu
          </Typography>
        </Box>
        <Divider />

        <List>
          <ListItem disablePadding>
            <ListItemButton onClick={() => navigate("/brands")}>
              <ListItemText primary="Brands" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton onClick={() => navigate("/creative-engine")}>
              <ListItemText primary="Creative Engine" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton onClick={() => navigate("/governance")}>
              <ListItemText primary="Governance" />
            </ListItemButton>
          </ListItem>
        </List>

        <Box sx={{ mt: "auto", p: 2 }}>
          <Divider />
          <Typography variant="body2" sx={{ mt: 2, mb: 1 }}>
            User: <strong>gianella@example.com</strong>
          </Typography>
          <Button fullWidth variant="outlined">
            Cerrar Sesión
          </Button>
        </Box>
      </Drawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          minHeight: "100vh",
          background: "#e7e1e1",
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};
