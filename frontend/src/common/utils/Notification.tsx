import Swal from "sweetalert2";
class NotificationService {
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
      timer: undefined,
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
