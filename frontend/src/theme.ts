import {  createTheme } from "@mui/material/styles";
export const theme = createTheme({
  typography: {
    fontFamily: 'Lato, "Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textAlign: "center",
          borderRadius: "4px", // Bordes consistentes con tus inputs de 48px
          textTransform: "none", // Quita las mayúsculas forzadas si prefieres control total
        },
        contained: {
          backgroundColor: "#E95A1A",
          color: "#fff",
          "&:hover": {
            backgroundColor: "#D14D14", // Un tono un poco más oscuro para el hover
          },
          // Asegura que no cambie el color si está deshabilitado
          "&.Mui-disabled": {
            backgroundColor: "rgba(0, 0, 0, 0.12)",
          },
        },

        outlined: {
          border: "1px solid #E95A1A",
          backgroundColor: "#fff",
          color: "#E95A1A",
          "&:hover": {
            backgroundColor: "#fff",
          },
          "&.Mui-disabled": {
            backgroundColor: "rgba(0, 0, 0, 0.12)",
          },
        },
      },
    },
    MuiTextField: {
      defaultProps: {
        // 1. Quitamos el margen "normal" por defecto
        margin: "none",
        variant: "outlined",
        fullWidth: true,
      },
      styleOverrides: {
        root: {
          // 2. Quitamos cualquier margen remanente de las clases de MUI
          marginTop: 0,
          marginBottom: 0,
          // 3. ¡Ojo aquí! Si pones max-height al root, el 'helperText' (el error)
          // se cortará o se encimará porque el root envuelve TODO el componente.
          // Es mejor dejar que el root crezca y limitar solo el Input.
        },
      },
    },

    MuiTable: {
      styleOverrides: {
        root: {
          fontFamily: "Lato, sans-serif",
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          fontFamily: "Lato, sans-serif",
        },
      },
    },
    MuiTableBody: {
      styleOverrides: {
        root: {
          fontFamily: "Lato, sans-serif",
          "& > tr:last-of-type > td, & > tr:last-of-type > th": {
            borderBottom: "none",
          },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          fontFamily: "Lato, sans-serif",
        },
      },
    },
    MuiCheckbox: {
      styleOverrides: {
        root: {
          color: "#D9D9D9",
          "&.Mui-checked": {
            color: "#E95A1A",
          },
        },
      },
    },
    MuiFormControlLabel: {
      styleOverrides: {
        label: {
          fontSize: "12px",
          fontFamily: "'Lato', sans-serif;",
          // color: "#333",
        },
        root: {
          fontSize: "12px",
          display: "flex",
          alignItems: "center",
          verticalAlign: "middle",
          "& .MuiTypography-root": {
            fontSize: "12px",
            padding: "4px 8px",
            borderRadius: "4px",
            transition: "background-color 0.3s ease-in-out",
          },
          "& .Mui-checked + .MuiTypography-root": {
            // backgroundColor: "#E95A1A",
            // color: "#fff",
          },
        },
      },
    },
    MuiMenuList: {
      styleOverrides: {
        root: {
          padding: "5px",
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          fontFamily: '"Lato", sans-serif',
          fontWeight: 400,
          fontSize: "14px",
          lineHeight: "140%",
          letterSpacing: "-2%",
          padding: "5px 5px !important",
          justifyContent: "left",
          alignItems: "left",
          "&.Mui-selected": {
            backgroundColor: "#FCEBE3 !important",
          },
          "& .MuiButtonBase-root ": {
            display: "flex  !important'",
          },
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          height: "48px", // Altura fija global
          borderRadius: "8px",
          input: {
            boxSizing: "border-box",
            padding: "10px 14px !important",
            outline: "0 !important",
          },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#E95A1A !important",
          },
          "& .MuiOutlinedInput-notchedOutline": {
            border: "1px solid #c0c0c0ff",
          },
          "& .MuiOutlinedInput-input": {
            // border: "none !important",
            padding: "10px 14px",
            fontStyle: "normal !important",
            color: "#808080",
            fontFamily: "'Barlow', sans-serif",
            fontWeight: 400,
            fontSize: "12px",
            "&::placeholder": {
              color: "#808080",
              fontStyle: "normal",
              fontFamily: "'Barlow', sans-serif",
              fontWeight: 400,
              fontSize: "12px",
            },
          },

          "& .MuiOutlinedInput-inputMultiline": {
            height: "auto",
            minHeight: "100px",
            lineHeight: "1.5",

            padding: "0px !important",
          },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          height: "40px",
          "& .MuiSelect-select": {
            height: "40px",
            display: "flex",
            alignItems: "center",
          },
        },
      },
    },
    MuiTablePagination: {
      styleOverrides: {
        root: {
          fontFamily: "Barlow, sans-serif",
          fontWeight: 400,
          fontSize: "12px",
          lineHeight: "140%",
          letterSpacing: "0%",
        },
        selectLabel: {
          fontFamily: "Barlow, sans-serif",
          fontSize: "12px",
        },
        displayedRows: {
          fontFamily: "Barlow, sans-serif",
          fontSize: "12px",
        },
      },
    },
    MuiRadio: {
      styleOverrides: {
        root: {
          color: "#808080",
          "&.Mui-checked": {
            color: "#E95A1A",
          },
          "& .MuiSvgIcon-root": {
            fontSize: "20px",
          },
        },
      },
    },
  },
});