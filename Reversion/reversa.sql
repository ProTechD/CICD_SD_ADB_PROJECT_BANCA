-- Databricks notebook source
-- MAGIC %python
-- MAGIC dbutils.widgets.removeAll()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.widgets.text("storageName","adlsmartdata1207")
-- MAGIC dbutils.widgets.text("catalogo","catalog_au")

-- COMMAND ----------

-- MAGIC %python
-- MAGIC storageName = dbutils.widgets.get("storageName")
-- MAGIC catalogo = dbutils.widgets.get("catalogo")
-- MAGIC
-- MAGIC rutaBronze = f"abfss://bronze@{storageName}.dfs.core.windows.net"
-- MAGIC rutaSilver = f"abfss://silver@{storageName}.dfs.core.windows.net"
-- MAGIC rutaGolden = f"abfss://golden@{storageName}.dfs.core.windows.net"

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Rerversa Capa Bronze

-- COMMAND ----------

-- DROP TABLES
DROP TABLE IF EXISTS ${catalogo}.bronze.clientes;
DROP TABLE IF EXISTS ${catalogo}.bronze.cuentas;
DROP TABLE IF EXISTS ${catalogo}.bronze.transacciones;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC ## REMOVE DATA (Bronze)
-- MAGIC dbutils.fs.rm(f"{rutaBronze}/clientes", True)
-- MAGIC dbutils.fs.rm(f"{rutaBronze}/cuentas", True)
-- MAGIC dbutils.fs.rm(f"{rutaBronze}/transacciones", True)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Rerversa Capa Silver

-- COMMAND ----------

-- DROP TABLES
DROP TABLE IF EXISTS ${catalogo}.silver.transacciones;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC # REMOVE DATA (Silver)
-- MAGIC dbutils.fs.rm(f"{rutaSilver}/transacciones", True)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Rerversa Capa Golden

-- COMMAND ----------

-- DROP TABLES
DROP TABLE IF EXISTS ${catalogo}.golden.resumenclientes;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC # REMOVE DATA (Golden)
-- MAGIC dbutils.fs.rm(f"{rutaGolden}/resumenclientes", True)
