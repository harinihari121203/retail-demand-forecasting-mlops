# Databricks notebook source
from pyspark.sql.functions import *

inventory_df = (
    sales_df
    .select(
        "Store",
        "Date",
        "Sales"
    )

    .withColumn(
        "InventoryMultiplier",
        rand(seed=42) * 1.0 + 0.5
    )

    .withColumn(
        "InventoryOnHand",
        round(
            col("Sales") * col("InventoryMultiplier"),
            0
        )
    )

    .withColumn(
        "SafetyStock",
        round(
            col("Sales") * 0.20,
            0
        )
    )

    .withColumn(
        "ReorderPoint",
        col("SafetyStock") * 2
    )

    .withColumn(
        "StockoutFlag",
        when(
            col("InventoryOnHand") < col("Sales"),
            1
        ).otherwise(0)
    )

    .withColumn(
        "InventoryCoverage",
        round(
            col("InventoryOnHand") /
            when(col("Sales") == 0, 1)
            .otherwise(col("Sales")),
            2
        )
    )

    .drop("InventoryMultiplier")
)

# COMMAND ----------

inventory_df.groupBy(
    "StockoutFlag"
).count().display()

# COMMAND ----------

inventory_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(
        "retail_catalog.silver.inventory_clean"
    )

# COMMAND ----------

inventory_df.groupBy("StockoutFlag").count().display()