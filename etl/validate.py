from sqlalchemy import text
from config import EXPECTED

def validate(connection, logger):
    logger.info("VALIDATE PHASE STARTING: running checks...")
    is_passed = True

    def check(label, actual, expected):
        nonlocal is_passed
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            is_passed = False
        logger.info(f"  [{status}] {label}: expected={expected}, actual={actual}")

    row_counts = connection.execute(
        text(
            "SELECT COUNT(*) AS total, COUNT(DISTINCT incident_id) AS uniq "
            "FROM team2.incident_response_mart"
        )
    ).one()
    check("total_rows", row_counts.total, EXPECTED["total_rows"])
    check("unique_incident_ids", row_counts.uniq, EXPECTED["unique_incident_ids"])

    status_counts = dict(
        connection.execute(
            text(
                "SELECT target_status, COUNT(*) FROM team2.incident_response_mart "
                "GROUP BY target_status"
            )
        ).all()
    )
    check("met_target", status_counts.get("Met", 0), EXPECTED["met_target"])
    check(
        "breached_target",
        status_counts.get("Breached", 0),
        EXPECTED["breached_target"],
    )

    open_count = connection.execute(
        text("SELECT COUNT(*) FROM team2.incident_response_mart WHERE is_open = 1")
    ).scalar()
    check("open_incidents", open_count, EXPECTED["open_incidents"])

    critical_count = connection.execute(
        text(
            "SELECT COUNT(*) FROM team2.incident_response_mart "
            "WHERE severity = 'Critical'"
        )
    ).scalar()
    check("critical_incidents", critical_count, EXPECTED["critical_incidents"])

    bad_rows = connection.execute(
        text(
            "SELECT COUNT(*) FROM team2.incident_response_mart "
            "WHERE response_delay_minutes < 0 OR target_minutes IS NULL"
        )
    ).scalar()
    check("negative_delay_or_null_target", bad_rows, 0)

    if is_passed:
        logger.info("VALIDATION FINISHED: all checks passed")
    else:
        logger.warning("VALIDATION FINISHED: one or more checks FAILED — review above")

    return is_passed