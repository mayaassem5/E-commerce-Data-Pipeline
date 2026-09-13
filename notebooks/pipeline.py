import pandas as pd
import subprocess
import os
from pathlib import Path

# Step 1: Read raw CSV
print("Step 1: Reading raw data...")
df = pd.read_csv("ecommerce_orders_raw.csv")
print(f"  Loaded {len(df)} rows")

# Step 2: Clean
print("Step 2: Cleaning...")
df = df.drop_duplicates(subset=["order_id"], keep="first")
df["customer_name"] = df["customer_name"].str.title().str.strip()
df["city"] = df["city"].str.title().str.strip()
df["quantity"] = df["quantity"].fillna(df["quantity"].median()).astype(int)
df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
df["email"] = df["email"].fillna("unknown@example.com")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["total_amount"] = df["quantity"] * df["unit_price"]
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
print(f"  After cleaning: {len(df)} rows")

# Step 3: Save outputs
print("Step 3: Saving cleaned data...")
output_dir = Path("../results")
output_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(output_dir / "cleaned_orders.csv", index=False)
df.to_parquet(output_dir / "cleaned_orders.parquet", index=False)

# Step 4: Load to PostgreSQL
print("Step 4: Loading to PostgreSQL...")
from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:edb123@localhost:5432/ecommerce")

# Load customers after removing duplicate customer IDs.
customers = df[["customer_id", "customer_name", "email", "city"]].drop_duplicates(
    subset="customer_id"
)
customers.to_sql("customers", engine, if_exists="append", index=False)

# Load cleaned order records.
orders = df[[
    "order_id", "customer_id", "product", "quantity", "unit_price",
    "total_amount", "order_date", "payment_method", "status"
]]
orders.to_sql("orders", engine, if_exists="append", index=False)

# Step 5: Upload to HDFS
print("Step 5: Uploading to HDFS...")
subprocess.run(["docker", "cp", str(output_dir / "cleaned_orders.parquet"), "namenode:/tmp/"])
subprocess.run(["docker", "exec", "namenode", "hdfs", "dfs", "-put", "-f",
                 "/tmp/cleaned_orders.parquet", "/data/silver/orders/"])

print("Pipeline complete!")