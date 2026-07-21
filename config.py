import datetime
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).parent
LOG_DIR = PROJECT_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)

SQL_DIR = PROJECT_ROOT / 'sql'
BUILD_SQL_PATH = SQL_DIR / 'build_incident_response_mart.sql'

SOURCE_TABLES = ["fact_incident_report", "dim_barangay", "dim_department"]

EXPECTED = {
    "total_rows": 180,
    "unique_incident_ids": 180,
    "met_target": 38,
    "breached_target": 142,
    "open_incidents": 63,
    "critical_incidents": 12
}

def load_env():
    load_dotenv(PROJECT_ROOT / '.env')
    required = ["DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        sys.exit(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Copy .env.example to .env and fill in your credentials."
        )
    return {v: os.getenv(v) for v in required}

def get_engine():
    credentials = load_env()
    connection_string = (
        f"postgresql+psycopg2://{credentials['DB_USER']}:{credentials['DB_PASS']}"
        f"@{credentials['DB_HOST']}:{credentials['DB_PORT']}/{credentials['DB_NAME']}"
    )
    return create_engine(connection_string)

def get_logger():
    logger = logging.getLogger('incident_response_mart_etl')
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    log_file = LOG_DIR / f"etl_incident_response_mart_{datetime.datetime.now():%Y%m%d_%H%M%S}.log"

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(f"Log file: {log_file}")
    return logger


