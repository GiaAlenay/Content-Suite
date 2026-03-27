import { IconAlertCircle } from "@tabler/icons-react";

export const ErrorContent = ({ msg }: { msg: string }) => {
  return (
    <div
      style={{
        minWidth: "100%",
        minHeight: "400px",
        verticalAlign: "middle",
        alignItems: "center",
        display: "flex",
        flexDirection: "column",
        gap: 10,
        justifyContent: "center",
      }}
    >
      <IconAlertCircle color="#d32f2f" size={50} style={{ marginRight: 10 }} />

      <span>{msg}</span>
    </div>
  );
};
