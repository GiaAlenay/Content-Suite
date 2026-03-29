import { Box, Button, Stack, Typography } from "@mui/material";
import { IconPlus } from "@tabler/icons-react";
import { NoRawData } from "../components/NoData/NoRawData";
import { ErrorContent } from "../components/ErrorContent/ErrorContent";
import { Loader } from "../components/Loader/Loader";

interface Props {
  children: React.ReactNode;
  title: string;
  onPlusClick: () => void;
  isLoading: boolean;
  isError: boolean;
  isEmpty: boolean;
  errorMsg?: string;
  emptyLabel?: string;
}

export const MainContentLayout: React.FC<Props> = ({
  title,
  onPlusClick,
  children,
  isLoading,
  isError,
  errorMsg = "Ocurrió un error inesperado",
  isEmpty,
  emptyLabel = "datos",
}) => {
  const renderContent = () => {
    if (isLoading) return <Loader />;
    if (isError) return <ErrorContent msg={errorMsg} />;
    if (isEmpty) return <NoRawData itemsName={emptyLabel} />;
    return <>{children}</>;
  };

  return (
    <Box
      sx={{
        padding: "24px 32px",
        borderRadius: "8px",
        background: "#fff",
        border: "1px solid rgba(0, 0, 0, 0.12)",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
        minHeight: "96%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Stack
        className="column-base"
        spacing={3}
        sx={{ height: "100%", p: "24px" }}
      >
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography variant="h4" fontWeight="bold">
            {title}
          </Typography>
          <Button
            variant="contained"
            disabled={isLoading}
            onClick={onPlusClick}
            sx={{
              borderRadius: "50%",
              width: 48, // Simplificado
              height: 48,
              minWidth: 48,
              p: 0,
              "& .MuiButton-startIcon": { margin: 0 },
            }}
          >
            <IconPlus />
          </Button>
        </Stack>

        <Box sx={{ flex: 1, width: "100%" }}>{renderContent()}</Box>
      </Stack>
    </Box>
  );
};
