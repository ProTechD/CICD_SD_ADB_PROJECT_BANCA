-- Databricks notebook source
-- MAGIC %python
-- MAGIC dbutils.widgets.removeAll()

-- COMMAND ----------

create widget text storageName default "adlsmartdata1207";

-- COMMAND ----------

-- MAGIC %python
-- MAGIC storageName = dbutils.widgets.get("storageName")

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-metastore`
URL 'abfss://metastore@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `credential`)
COMMENT 'Ubicación externa para las tablas raw del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-raw`
URL 'abfss://raw@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `credential`)
COMMENT 'Ubicación externa para las tablas raw del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-bronze`
URL 'abfss://bronze@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `credential`)
COMMENT 'Ubicación externa para las tablas bronze del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-silver`
URL 'abfss://silver@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `credential`)
COMMENT 'Ubicación externa para las tablas silver del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-golden`
URL 'abfss://golden@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL `credential`)
COMMENT 'Ubicación externa para las tablas golden del Data Lake';

-- COMMAND ----------

DROP CATALOG IF EXISTS catalog_au CASCADE;

-- COMMAND ----------

CREATE CATALOG IF NOT EXISTS catalog_au
MANAGED LOCATION 'abfss://metastore@${storageName}.dfs.core.windows.net/'
COMMENT 'Catalogo para la arquitectura medallion del ambiente de dev';

-- COMMAND ----------

DROP SCHEMA IF EXISTS catalog_au.raw;
DROP SCHEMA IF EXISTS catalog_au.bronze;
DROP SCHEMA IF EXISTS catalog_au.silver;
DROP SCHEMA IF EXISTS catalog_au.golden;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.fs.rm(f"abfss://bronze@{storageName}.dfs.core.windows.net/",True)
-- MAGIC dbutils.fs.rm(f"abfss://silver@{storageName}.dfs.core.windows.net/",True)
-- MAGIC dbutils.fs.rm(f"abfss://golden@{storageName}.dfs.core.windows.net/",True)

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS catalog_au.raw;
CREATE SCHEMA IF NOT EXISTS catalog_au.bronze;
CREATE SCHEMA IF NOT EXISTS catalog_au.silver;
CREATE SCHEMA IF NOT EXISTS catalog_au.golden;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Tablas Bronze

-- COMMAND ----------

-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS catalog_au.bronze.clientes (
    clienteid integer,
    nombre string,
    apellido string,
    dni string,
    fechanacimiento date,
    ciudad string
)
USING DELTA
LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/clientes"

-- COMMAND ----------

-- Tabla de Cuentas
CREATE TABLE IF NOT EXISTS catalog_au.bronze.cuentas (
    cuentaid integer,
    clienteid integer,
    tipocuenta string, -- ej: ahorros, corriente
    fechaapertura date,
    saldo double
)
USING DELTA
LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/cuentas"

-- COMMAND ----------

-- Tabla de Transacciones
CREATE TABLE IF NOT EXISTS catalog_au.bronze.transacciones (
    transaccionid integer,
    cuentaid integer,
    fecha date,
    tipo string, -- ej: deposito, retiro, transferencia
    monto double
)
USING DELTA
LOCATION "abfss://bronze@${storageName}.dfs.core.windows.net/transacciones"

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Tablas Silver

-- COMMAND ----------

-- Tabla Silver: Vista detallada de transacciones con cliente y cuenta
CREATE TABLE IF NOT EXISTS catalog_au.silver.transacciones (
    transaccionid integer,
    clienteid integer,
    nombrecompleto string,
    dni string,
    cuentaid integer,
    tipocuenta string,
    fechatransaccion date,
    tipotransaccion string,
    monto double,
    ciudad string
)
USING DELTA
LOCATION "abfss://silver@${storageName}.dfs.core.windows.net/transacciones"

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ###Tablas Golden

-- COMMAND ----------

-- Tabla Gold: Resumen de actividad por cliente
CREATE TABLE IF NOT EXISTS catalog_au.golden.resumenclientes (
    clienteid integer,
    nombrecompleto string,
    ciudad string,
    totaltransacciones integer,
    totalmonto double,
    promediomonto double
)
USING DELTA
LOCATION "abfss://golden@${storageName}.dfs.core.windows.net/resumenclientes"
