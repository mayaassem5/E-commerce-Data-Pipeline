# E-Commerce Orders Data Pipeline

This project analyzes and processes raw e-commerce order data with Python and pandas. It includes data-quality checks, cleaning, business aggregations, visualizations, file exports, PostgreSQL loading, and HDFS upload.

## Project Structure

```text
homework_mayaAssem/
├── notebooks/
│   ├── ecommerce_orders_raw.csv
│   ├── part1_pandas.ipynb
│   └── pipeline.py
├── results/
│   ├── cleaned_orders.csv
│   ├── cleaned_orders.parquet
│   └── city_revenue.csv
├── screenshots/
└── sql/
```

## Notebook Analysis

`notebooks/part1_pandas.ipynb` contains the exploratory analysis and data preparation workflow:

- Inspects dimensions, data types, missing values, duplicates, and descriptive statistics.
- Removes duplicate orders using `order_id`.
- Standardizes customer names and city names.
- Fills missing quantity, unit price, and email values.
- Converts `order_date` to a datetime column.
- Creates `total_amount`, `order_year`, and `order_month` fields.
- Summarizes revenue, order volume, customers, payment methods, and order statuses.
- Produces a four-panel dashboard of key business metrics.
- Exports cleaned data and city revenue results.

## Automated Pipeline

`notebooks/pipeline.py` runs the main workflow from start to finish:

1. Reads the raw CSV file.
2. Cleans and enriches the data.
3. Saves CSV and Parquet files to `results/`.
4. Loads customer and order data into PostgreSQL.
5. Uploads the Parquet file to HDFS through Docker.

Run it from the `notebooks` directory so the relative file paths resolve correctly:

```powershell
cd notebooks
python pipeline.py
```

## Requirements

Install the Python dependencies in the environment used by the notebook or pipeline:

```powershell
pip install pandas pyarrow sqlalchemy psycopg2-binary
```

The PostgreSQL step expects a local database with these connection details:

```text
Host: localhost
Port: 5432
Database: ecommerce
User: postgres
```

The HDFS step expects Docker to be running with a container named `namenode` and the target HDFS directory available:

```text
/data/silver/orders/
```

If PostgreSQL or Docker/HDFS is not configured, the analysis and local file-export portions can still be run independently from the notebook.

## Outputs

The project writes the following files to `results/`:

- `cleaned_orders.csv`: cleaned orders in CSV format.
- `cleaned_orders.parquet`: cleaned orders in columnar Parquet format.
- `city_revenue.csv`: revenue totals for the top cities.

## Notes

The PostgreSQL connection string in `pipeline.py` is configured for the local assessment environment. For shared or production use, replace hard-coded credentials with environment variables or another secure configuration method.
