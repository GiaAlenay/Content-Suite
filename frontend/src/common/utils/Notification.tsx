class NotificationService {
  static notifyError(message: string): void {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: message,
      confirmButtonText: "Aceptar",
      confirmButtonColor: "#E95A1A",
    });
  }

  static showSuccessAlertAndAction(msg: string, ejecutar: () => void): void {
    Swal.fire({
      title: "Éxito",
      text: msg,
      icon: "success",
      showCancelButton: true,
      showConfirmButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Aceptar",
    }).then((result) => {
      if (result.isConfirmed) {
        ejecutar();
      }
    });
  }

  static showSuccessAlertAndDoubleAction(
    msg: string,
    ejecutar: () => void,
    cancelar?: () => void,
  ): void {
    Swal.fire({
      title: "Éxito",
      text: msg,
      icon: "success",
      showCancelButton: true,
      showConfirmButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Aceptar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        ejecutar();
      } else if (result.dismiss === Swal.DismissReason.cancel && cancelar) {
        cancelar();
      }
    });
  }

  static showSuccessAlert(msg: string, ejecutar?: () => void): void {
    if (ejecutar) {
      console.log("Se ejecutará la acción.");
      Swal.fire({
        title: "Éxito",
        text: msg,
        icon: "success",
        showConfirmButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Aceptar",
      }).then(() => {
        ejecutar();
      });
    } else {
      console.log("No hay acción a ejecutar.");
      Swal.fire({
        title: "Éxito",
        text: msg,
        icon: "success",
        showConfirmButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Aceptar",
      });
    }
  }
  static showSuccessAlertPersonalizado(
    title: string,
    msg: string,
    accion?: () => void,
  ) {
    Swal.fire({
      title: title,
      text: msg,
      icon: "success",
      showConfirmButton: !!accion,
      confirmButtonText: "OK",
      timer: accion ? undefined : 1200,
      width: "512px",
      padding: "0px 30px 30px 30px",
      customClass: {
        popup: "my-swal-popup",
        confirmButton: accion ? "my-custom-button" : "",
      },
    }).then((result) => {
      if (accion && result.isConfirmed) {
        accion();
      }
    });
  }

  static showErrorssAlertPersonalizado(
    title: string,
    msg: string,
    accion?: () => void,
  ) {
    Swal.fire({
      title: title,
      text: msg,
      icon: "error",
      showConfirmButton: !!accion,
      confirmButtonText: "OK",
      timer: accion ? undefined : 1200,
      width: "512px",
      padding: "0px 30px 30px 30px",
      customClass: {
        popup: "my-swal-popup",
        confirmButton: accion ? "my-custom-button" : "",
      },
    }).then((result) => {
      if (accion && result.isConfirmed) {
        accion();
      }
    });
  }

  static notifyWarning(message: string): void {
    Swal.fire({
      icon: "warning",
      title: "Advertencia",
      text: message,
      confirmButtonText: "Aceptar",
      confirmButtonColor: "#E95A1A",
    });
  }
}

export default NotificationService;
