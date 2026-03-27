import {
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import { useState } from "react";
// import Swal from "sweetalert2";
import { IconAlertCircle } from "@tabler/icons-react";
// import { GlobalContext } from "../../../../../components/auth/GlobalContext";
// import { validateEnProgresoOS } from "../../../../itinerario/itinerarioEdit/TableItnerarioEdit/Table/Collapsible/querys/validateEnProgresoOSS";
// import { deleteOs } from "../../../files/api/delete-os";
// import { deleteOsTickets } from "../../../files/api/delete-os-tickets";

const ConfirmDelete = ({
  open,
  onClose,
  itemId,
}: {
  open: boolean;
  onClose: () => void;
  itemId: string;
}) => {
  //   const UserGlobalContext = useContext(GlobalContext);
  const [isLoading, setIsLoading] = useState(false);

  //   let { user } = UserGlobalContext.userState;

  //   const usuario = user
  //     ? `${user.storage?.nombre || ''} ${user.storage.apellido || ''}`.trim()
  //     : 'Usuario desconocido';

  //   useEffect(() => {
  //     const dataWithSameNumOS = dataAll.filter(
  //       (item) => item.numOS === data.numOS
  //     );
  //     setDataSelect(dataWithSameNumOS);
  //   }, [data]);

  const deleteOS = async (itemId: string) => {
    console.log(itemId);
    // const osPagadas = dataArray.filter((data) => data.estadoOS !== 'CONFIRMED');
    // if (osPagadas.length > 0) {
    //   Swal.fire({
    //     icon: 'warning',
    //     title: 'Eliminación De OS Cancelada',
    //     text: 'Una o más OS están en estado "EN PROCESO" y no pueden ser eliminadas.',
    //     confirmButtonText: 'Entendido',
    //   });
    //   setIsLoading(false);
    //   onClose();
    //   return;
    // }
    // const servicesId = dataArray.map((data) => data.id);
    // const existeOSActividad = await validateEnProgresoOS(servicesId);
    // if (existeOSActividad) {
    //   Swal.fire({
    //     icon: 'warning',
    //     title: 'Eliminación De OS Cancelada',
    //     text: 'Una o más OS están en estado "EN PROCESO" y no pueden ser eliminadas.',
    //     confirmButtonText: 'Entendido',
    //   });
    //   setIsLoading(false);
    //   onClose();
    //   return;
    // }
    // const promesasDeleteOS = dataArray.map(async (servicio) => {
    //   console.log(servicio);
    //   if (servicio.tipoServicio === 'TICKET')
    //     return deleteOsTickets({
    //       idService: servicio.id,
    //       numOS: Number(servicio.numOS),
    //       user: usuario,
    //     });
    //   else
    //     return deleteOs({
    //       id: servicio.id,
    //       user: usuario,
    //     });
    // });
    // const results = await Promise.all(promesasDeleteOS);
    // console.log('results');
    // console.log(results);
    // setChange(!change);
    // const successfulDeletes = results.filter((result) => result).length;
    // const unsuccessfulDeletes = dataArray.length - successfulDeletes;
    // if (successfulDeletes > 0) {
    //   Swal.fire({
    //     position: 'top-end',
    //     icon: 'success',
    //     title: `${successfulDeletes} Proceso(s) Exitoso(s)`,
    //     showConfirmButton: false,
    //     timer: 2000,
    //   });
    // }
    // if (unsuccessfulDeletes > 0) {
    //   Swal.fire({
    //     position: 'top-end',
    //     icon: 'error',
    //     title: `${unsuccessfulDeletes} error(es)`,
    //     showConfirmButton: false,
    //     timer: 2000,
    //   });
    // }
    // setChange(!change);
    // setIsLoading(false);
    // onClose();
    // return dataArray;
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDialog-paper": {
          width: "512px !important",
          gap: "22px",
          padding: "30px 30px 70px 30px",
        },
      }}
    >
      <DialogTitle
        style={{ padding: "0" }}
        className="dialog-title confirm-cont column-base div-center"
      >
        <IconAlertCircle size={88} color="#fdc560" />
        <h4
          style={{
            paddingTop: "0",
            fontWeight: "600px",
            fontSize: "30px",

            fontStyle: "Normal",
          }}
        >
          ¿Estás seguro de eliminar la OS?
        </h4>
      </DialogTitle>
      <DialogContent style={{ padding: "0", textAlign: "center" }}>
        <span style={{ fontSize: "18px" }}>
          Esta acción no se puede deshacer.
        </span>
      </DialogContent>

      <DialogActions
        style={{ padding: "0", justifyContent: "center", gap: "30px" }}
      >
        <button
          className="btn-base btn-full-orange "
          onClick={() => {
            setIsLoading(true);
            deleteOS(itemId);
          }}
          style={{ minWidth: "95px" }}
        >
          {isLoading ? (
            <div className="loadingBtn">
              <CircularProgress size={20} style={{ color: "#FFFFFF" }} />
            </div>
          ) : (
            <>Si, eliminar</>
          )}
        </button>
        <button
          className="btn-base btn-lines-orange "
          onClick={onClose}
          style={{ minWidth: "95px" }}
        >
          Cancelar
        </button>
      </DialogActions>
    </Dialog>
  );
};

export default ConfirmDelete;
