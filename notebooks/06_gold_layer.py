# Databricks notebook source
sales_df = spark.table(
    "retail_catalog.silver.sales_clean"
)

store_df = spark.table(
    "retail_catalog.silver.store_clean"
)

weather_df = spark.table(
    "retail_catalog.silver.weather_clean"
)

inventory_df = spark.table(
    "retail_catalog.silver.inventory_clean"
)

# COMMAND ----------

gold_df = (
    sales_df.alias("s")
    .join(
        store_df.alias("st"),
        on="Store",
        how="left"
    )
)

# COMMAND ----------

gold_df = gold_df.join(
    weather_df.select(
        "Date",
        "temperature",
        "humidity",
        "rainfall",
        "weather_condition"
    ),
    on="Date",
    how="left"
)

# COMMAND ----------

gold_df = (
    gold_df
    .join(
        inventory_df.select(
            "Store",
            "Date",
            "InventoryOnHand",
            "SafetyStock",
            "ReorderPoint",
            "StockoutFlag",
            "InventoryCoverage"
        ),
        ["Store","Date"],
        "left"
    )
)

# COMMAND ----------

print(gold_df.count())

# COMMAND ----------

gold_df = gold_df.drop(
    "StoreType",
    "Assortment"
)

# COMMAND ----------

print(len(gold_df.columns))

# COMMAND ----------

print(gold_df.printSchema())