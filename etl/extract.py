from sqlalchemy import text
from config import SOURCE_TABLES

def extract(connection, logger):
    logger.info("EXTRACTION PHASE START: checking the source tables...")
    for table in SOURCE_TABLES:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.scalar()
        logger.info(f"  {table}: {count} rows")
        if count == 0:
            raise ValueError(f"Source table {table} is empty, aborting process...")
    logger.info("EXTRACTION PHASE FINISHED: all source tables present and populated")
