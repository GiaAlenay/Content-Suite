import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()


def get_supabase_client() -> Client:
    """
    Inicializa el cliente oficial de Supabase.
    Requiere SUPABASE_URL y SUPABASE_SERVICE_KEY en el .env
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise ValueError("Faltan las credenciales de Supabase en el archivo .env")

    client = create_client(url, key)
    print("client supabase")
    print(client)
    return client


supabase: Client = get_supabase_client()
