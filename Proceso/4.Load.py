# Databricks notebook source
dbutils.widgets.removeAll()

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F

# COMMAND ----------

# Widgets para parametrizar
dbutils.widgets.text("catalogo", "catalog_au")
dbutils.widgets.text("esquema_source", "silver")
dbutils.widgets.text("esquema_sink", "golden")

# COMMAND ----------

catalogo = dbutils.widgets.get("catalogo")
esquema_source = dbutils.widgets.get("esquema_source")
esquema_sink = dbutils.widgets.get("esquema_sink")

# COMMAND ----------

# 1. Lectura de tabla Silver
df_silver_transacciones = spark.table(f"{catalogo}.{esquema_source}.transacciones")

# COMMAND ----------

# 2. Agregación para Golden
df_resumen = df_silver_transacciones.groupBy(
    col("clienteid"),
    col("nombrecompleto"),
    col("ciudad")
).agg(
    F.count("transaccionid").alias("totaltransacciones"),
    F.sum("monto").alias("totalmonto"),
    F.avg("monto").alias("promediomonto")
).orderBy(col("totalmonto").desc())

# COMMAND ----------

# 3. Escritura en Golden
df_resumen.write.mode("overwrite").insertInto(f"{catalogo}.{esquema_sink}.resumenclientes")

# COMMAND ----------

spark.table(f"{catalogo}.{esquema_sink}.resumenclientes").display()
