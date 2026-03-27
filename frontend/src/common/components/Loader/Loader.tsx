import { CircularProgress } from "@mui/material";

export const Loader = () => {
  return (
    <div
      style={{
        minWidth: "100%",
        minHeight: "400px",
        verticalAlign: "middle",
        alignItems: "center",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <CircularProgress size={80} style={{ color: "#E95A1A" }} />
    </div>
  );
};
