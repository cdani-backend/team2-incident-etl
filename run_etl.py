import sys

from sqlalchemy.exc import SQLAlchemyError

from config import get_engine, get_logger
from etl.extract import extract
from etl.transform import transform
from etl.validate import validate

def main():
    logger = get_logger()
    logger.info("=== Starting ETL ===")

    engine = get_engine()

    try:
        with engine.begin() as connection:
            extract(connection, logger)
            transform(connection, logger)
            passed = validate(connection, logger)
    except (SQLAlchemyError, ValueError) as e:
        logger.error(f"ETL FAILED: {e}", exc_info=True)
        sys.exit(1)

    if passed:
        logger.info("=== ETL completed successfully ===")
    else:
        logger.warning(
            "=== ETL completed with validation failures ==="
        )
        sys.exit(2)

if __name__ == "__main__":
    main()
