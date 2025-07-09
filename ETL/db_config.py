# db_config.py

import os
from sqlalchemy import create_engine
from config import settings

# Cargar variables desde .env
def get_engine():
    url = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    return create_engine(url)   

# Verificación (opcional)
if __name__ == "__main__":
    from sqlalchemy import text

    try:
        engine = get_engine()
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version();")).fetchone()
            print("✅ Conexión exitosa a PostgreSQL")
            print("Versión:", version[0])
    except Exception as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)