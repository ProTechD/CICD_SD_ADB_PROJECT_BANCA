# Databricks notebook source
# Databricks notebook source
dbutils.widgets.removeAll()

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F

# COMMAND ----------

# Widgets para parametrizar
dbutils.widgets.text("catalogo", "catalog_au")
dbutils.widgets.text("esquema_source", "bronze")
dbutils.widgets.text("esquema_sink", "silver")

# COMMAND ----------

catalogo = dbutils.widgets.get("catalogo")
esquema_source = dbutils.widgets.get("esquema_source")
esquema_sink = dbutils.widgets.get("esquema_sink")

# COMMAND ----------

# 1. Lectura de tablas Bronce
df_clientes = spark.table(f"{catalogo}.{esquema_source}.clientes")
df_cuentas = spark.table(f"{catalogo}.{esquema_source}.cuentas")
df_transacciones = spark.table(f"{catalogo}.{esquema_source}.transacciones")

# COMMAND ----------

# 2. Limpieza básica
df_clientes = df_clientes.dropna(how="all").filter(col("clienteid").isNotNull())
df_cuentas = df_cuentas.dropna(how="all").filter(col("cuentaid").isNotNull())
df_transacciones = df_transacciones.dropna(how="all").filter(col("transaccionid").isNotNull())

# COMMAND ----------

# 3. Enriquecimiento: categoría de saldo
def categoria_saldo(saldo):
    if saldo < 500:
        return "Bajo"
    elif 500 <= saldo < 2000:
        return "Medio"
    else:
        return "Alto"

saldo_udf = F.udf(categoria_saldo, StringType())
df_cuentas = df_cuentas.withColumn("categoria_saldo", saldo_udf("saldo"))

# COMMAND ----------

# 4. Join para crear Silver
df_silver = (df_transacciones.alias("t")
    .join(df_cuentas.alias("cu"), col("t.cuentaid") == col("cu.cuentaid"), "inner")
    .join(df_clientes.alias("c"), col("cu.clienteid") == col("c.clienteid"), "inner")
    .select(
        col("t.transaccionid"),
        col("c.clienteid"),
        concat(col("c.nombre"), lit(" "), col("c.apellido")).alias("nombrecompleto"),
        col("c.dni"),
        col("cu.cuentaid"),
        col("cu.tipocuenta"),
        col("t.fecha").alias("fechatransaccion"),
        col("t.tipo").alias("tipotransaccion"),
        col("t.monto"),
        col("c.ciudad")
    )
)

# COMMAND ----------

# 6. Escritura en Silver
df_silver.write.mode("overwrite").insertInto(f"{catalogo}.{esquema_sink}.transacciones")

# COMMAND ----------

#spark.table(f"{catalogo}.{esquema_sink}.transacciones").display()
