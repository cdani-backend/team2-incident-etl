from config import get_engine
from sqlalchemy import text

engine = get_engine()
with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.scalar())