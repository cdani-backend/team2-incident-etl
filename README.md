## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd team2-incident-etl
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

If the project has a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the required dependencies used by the project.

### 4. Run the ETL Pipeline

```bash
python tests/run_etl.py
```

Or, depending on the project entry point:

```bash
python tests/main.py
```

### 5. Run Sanity Checks

```bash
python tests/sanity.py
```

## 🔄 ETL Workflow

The expected workflow is:

1. **Extract** raw incident data.
2. **Transform** and clean the extracted data.
3. **Validate** the transformed records.
4. **Load** the validated data into the target data mart.
5. **Run sanity checks** to verify the pipeline results.

## 📊 Incident Response Data Mart

The data mart is designed to support analysis of incident response data, including potential metrics such as:

* Incident volume
* Incident status
* Priority levels
* Response times
* Resolution times
* SLA compliance
* Incident categories
* Geographic or organizational breakdowns

The exact metrics depend on the business rules and schema defined in the ETL pipeline and SQL data mart script.

# Team 2 Incident ETL

An ETL (Extract, Transform, Load) pipeline for processing incident data and building an incident response data mart for analysis and reporting.

## 📁 Project Structure

```text
team2-incident-etl/
│
├── etl/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── validate.py
│
├── sql/
│   └── build_incident_response_mart.sql
│
├── tests/
│   ├── .gitignore
│   ├── config.py
│   ├── main.py
│   ├── run_etl.py
│   └── sanity.py
│
└── README.md
```

## 🎯 Project Overview

The **Team 2 Incident ETL** project is designed to extract incident data, transform it into a standardized format, validate data quality, and prepare it for loading into an incident response data mart.

The pipeline follows a standard ETL workflow:

```text
Source Data
    │
    ▼
Extract
    │
    ▼
Transform
    │
    ▼
Validate
    │
    ▼
Load / Data Mart
```

## ⚙️ ETL Components

### Extract

`etl/extract.py`

Responsible for retrieving incident data from the source system.

Typical responsibilities include:

* Reading source data
* Connecting to data sources
* Extracting raw incident records
* Preparing data for transformation

### Transform

`etl/transform.py`

Responsible for cleaning and transforming the extracted data.

Typical operations include:

* Standardizing data formats
* Cleaning missing or invalid values
* Transforming incident attributes
* Applying business rules
* Preparing data for the target data mart

### Validate

`etl/validate.py`

Responsible for checking data quality and ensuring that the transformed data meets expected requirements.

Validation may include:

* Required field checks
* Data type validation
* Duplicate detection
* Business rule validation
* Record count checks

## 🗄️ SQL Data Mart

The SQL script used to build the incident response data mart is located at:

```text
sql/build_incident_response_mart.sql
```

This script is responsible for creating and/or populating the data mart used for incident response analysis and reporting.

## 🧪 Testing and Execution

The `tests/` directory contains scripts used to run and verify the ETL pipeline.

### Available Scripts

| File         | Description                                           |
| ------------ | ----------------------------------------------------- |
| `config.py`  | Project configuration settings                        |
| `main.py`    | Main application or pipeline entry point              |
| `run_etl.py` | Runs the ETL workflow                                 |
| `sanity.py`  | Performs basic sanity checks on the pipeline and data |


## 🛠️ Technology Stack

* **Python** — ETL processing and validation
* **SQL** — Data mart creation and transformation
* **Git/GitHub** — Version control and collaboration

## 👥 Team 2

This project was developed by **Team 2** as part of a collaborative data engineering / ETL project.

## 📌 Future Improvements

Potential future enhancements include:

* Add automated unit tests
* Add logging and error handling
* Add data quality reports
* Add automated ETL scheduling
* Add Docker support
* Add CI/CD using GitHub Actions
* Add documentation for database configuration
* Add pipeline monitoring

## 📄 License

This project is intended for educational and collaborative development purposes.
