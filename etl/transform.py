from sqlalchemy import text
from config import BUILD_SQL_PATH

def transform(connection, logger):
    logger.info("TRANSFORM PHASE START: rebuilding team2.incident_response_mart...")
    sql = BUILD_SQL_PATH.read_text()
    connection.execute(text(sql))
    logger.info("TRANSFORM PHASE FINISHED: rebuilding complete...")
