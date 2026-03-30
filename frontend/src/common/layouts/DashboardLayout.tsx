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
import { IconRobot } from "@tabler/icons-react";
import { Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/useAuth";
import { useEffect, useState } from "react";
import NotificationService from "../utils/Notification";

const drawerWidth = 240;

export const DashboardLayout = () => {
  const { signOut, user } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    console.log({ user });
  }, [user]);

  const handleLogOut = async () => {
    console.log("esta en logout");
    setIsLoading(true);

    try {
      await signOut();

      navigate("/brands");
    } catch (error: any) {
      NotificationService.showErrorssAlertPersonalizado(
        "Error",
        error.message || "Ocurrió un error al cerrar sesión",
      );
    } finally {
      setIsLoading(false);
    }
  };
  const enruter = [
    {
      name: "Marcas",
      route: "brands",
    },
    {
      name: "Espacio Creativo",
      route: "creative-engine",
    },
    {
      name: "Auditoria",
      route: "governance",
    },
  ];
  const handleRouter = (name: string) => {
    return enruter.find((r) => r.name === name)?.route ?? "";
  };

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
            backgroundColor: "#121212",
            color: "#ffffff",
            borderRight: "1px solid #333",
          },
        }}
      >
        <Box
          sx={{
            p: 2,
            display: "flex",
            flexDirection: "row",
            gap: "8px",
            justifyContent: "flex-start",
            verticalAlign: "middle",
          }}
        >
          <IconRobot size={24} />

          <Typography variant="h6">Menu</Typography>
        </Box>

        <Divider sx={{ backgroundColor: "rgba(24, 24, 24, 0.12)" }} />

        <List>
          {enruter.map((text) => (
            <ListItem key={text.name} disablePadding>
              <ListItemButton
                onClick={() => navigate(`/${handleRouter(text.name)}`)}
                sx={{
                  "&:hover": {
                    backgroundColor: "rgba(255, 255, 255, 0.08)",
                  },
                }}
              >
                <ListItemText primary={text.name} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>

        <Box sx={{ mt: "auto", p: 2 }}>
          <Divider
            sx={{ backgroundColor: "rgba(255, 255, 255, 0.12)", mb: 2 }}
          />
          <Typography variant="body2" sx={{ opacity: 0.7 }}>
            {user?.email}
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.7 }}>
            {user?.user_metadata?.full_name ?? "-"}
          </Typography>
          <Button
            fullWidth
            disabled={isLoading}
            variant="outlined"
            onClick={handleLogOut}
            sx={{
              mt: 1,
              color: "white",
              backgroundColor: "rgba(255, 255, 255, 0.05)",
              borderColor: "rgba(255, 255, 255, 0.5)",
              "&:hover": {
                borderColor: "white",
                backgroundColor: "rgba(26, 25, 25, 0.05)",
              },
            }}
          >
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
