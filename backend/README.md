# Content-Suite

source venv/Scripts/activate

pip install -r requirements.txt
pip freeze > requirements.txt

uvicorn main:app --reload

"Sistema Multi-Agente con RAG."

"Arquitectura de Agentes Cognitivos"

"patrón "Manager-Worker"" ---> el Agente Orquestador decide dinámicamente qué hacer.

RAG (Retrieval Augmented Generation): Es la técnica para que la IA lea tus tablas de vectores.

Arquitectura de Agentes: Es la estructura donde delegas decisiones a "expertos" (Arquitecto, Auditor) en lugar de escribir 50 if/else.
