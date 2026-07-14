CREATE SCHEMA IF NOT EXISTS team2;

DROP TABLE IF EXISTS team2.incident_response_mart;

CREATE TABLE team2.incident_response_mart AS WITH base AS (
    SELECT
        f.incident_id,
        f.barangay_id,
        f.department_id,
        f.incident_type,
        f.incident_date,
        f.severity,
        f.response_minutes,
        f.status,
        f.source_channel,
        b.barangay_name,
        b.district,
        b.area_type,
        d.department_name,
        d.service_domain
    FROM fact_incident_report f
    JOIN dim_barangay AS b ON f.barangay_id = b.barangay_id
    JOIN dim_department AS d ON f.department_id = d.department_id
),

mapped AS (
    SELECT
        base.*,
        DATE_TRUNC('month', incident_date)::date AS incident_month,

        CASE severity
            WHEN 'Critical' THEN 15
            WHEN 'High' THEN 30
            WHEN 'Medium' THEN 45
            WHEN 'Low' THEN 60
        END AS target_minutes,

        CASE severity
            WHEN 'Critical' THEN 4
            WHEN 'High' THEN 3
            WHEN 'Medium' THEN 2
            WHEN 'Low' THEN 1
        END AS severity_weight,

         CASE WHEN status ILIKE 'open' THEN 1 ELSE 0 END AS is_open
    FROM base
)

SELECT
    incident_id,
    barangay_id,
    barangay_name,
    department_id,
    department_name,
    severity,
    incident_month,
    target_minutes,
    severity_weight,

    GREATEST(0, response_minutes - target_minutes) AS response_delay_minutes,

    CASE
        WHEN response_minutes <= target_minutes THEN 'Met'
        ELSE 'Breached'
    END AS target_status,

    CASE
        WHEN response_minutes <= target_minutes THEN 'On Time'
        WHEN response_minutes <= target_minutes * 2 THEN 'Minor Delay'
        WHEN response_minutes <= target_minutes * 4 THEN 'Major Delay'
        ELSE 'Severe Delay'
    END AS response_band,

    is_open,
    ROUND(
        (severity_weight
        * (response_minutes::numeric / target_minutes)
        + (is_open * 2))::numeric
    , 2) AS attention_score

FROM mapped;
