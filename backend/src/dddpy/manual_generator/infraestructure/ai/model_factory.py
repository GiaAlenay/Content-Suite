import os
from langchain_groq import ChatGroq

# from langchain_openai import ChatOpenAI # Por si quieres cambiar luego


def model_factory(model_type: str = "fast"):
    """
    Crea la instancia del LLM configurada con las API Keys y parámetros.
    """

    # Podrías manejar diferentes modelos según la necesidad (uno rápido para clasificar, uno potente para escribir)
    if model_type == "fast":
        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",  # Rápido y barato
            temperature=0.1,
            max_tokens=1024,
        )

    elif model_type == "creative":
        return ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile",  # Más potente para redactar el manual
            temperature=0.7,
        )

    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant"
    )
