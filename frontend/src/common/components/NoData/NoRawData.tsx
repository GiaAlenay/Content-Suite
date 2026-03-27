import { IconAlertTriangle } from "@tabler/icons-react";

export const NoRawData = ({ itemsName }: { itemsName: string }) => {
  return (
    <div
      style={{
        minWidth: "100%",
        minHeight: "400px%",
        verticalAlign: "middle",
        alignItems: "center",
        display: "flex",
        flexDirection: "column",
        gap: 10,
        justifyContent: "center",
      }}
    >
      <IconAlertTriangle
        color="#d32f2f"
        size={50}
        style={{ marginRight: 10 }}
      />
      <span>Aun no hay {itemsName} registradas para mostrar.</span>
    </div>
  );
};
