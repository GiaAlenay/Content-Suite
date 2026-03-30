export const formatDateToSpanish = (dateString: string | undefined | null): string => {
  if (!dateString) return "Fecha no disponible";

  const date = new Date(dateString);

  if (isNaN(date.getTime())) return "-";

  const formatter = new Intl.DateTimeFormat('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });


  const parts = formatter.formatToParts(date);
  const day = parts.find(p => p.type === 'day')?.value;
  const month = parts.find(p => p.type === 'month')?.value;
  const year = parts.find(p => p.type === 'year')?.value;

  const capitalizedMonth = month ? month.charAt(0).toUpperCase() + month.slice(1) : "";

  return `${day} de ${capitalizedMonth} ${year}`;
};