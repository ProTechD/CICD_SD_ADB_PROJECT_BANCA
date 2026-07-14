# CICD_SD_ADB_PROJECT_BANCA  
## 🧠 Proyecto de Ingesta y Transformación de Datos

Este proyecto implementa un flujo **ETL bancario** en **Azure Databricks**, siguiendo la arquitectura de capas **Bronze–Silver–Gold** y aplicando prácticas de **CI/CD** con GitHub Actions.  
El objetivo es demostrar cómo ingerir datos desde archivos CSV, transformarlos con PySpark y SQL, y cargarlos en tablas Delta optimizadas para análisis y visualización.

---

## 🚀 Funcionalidades
- Ingesta de datos desde archivos CSV (clientes, cuentas, transacciones).  
- Transformación y limpieza de datos con **PySpark** y **Databricks SQL**.  
- Carga en tablas Delta para análisis en la capa Gold.  
- Uso de **dbutils** para parametrización y gestión de secretos.  
- Automatización de despliegues con **GitHub Actions**.  
- Dashboard bancario para visualizar métricas de clientes y transacciones.  

---

## 🏗️ Arquitectura
La solución sigue la arquitectura **Medallion** (Bronze–Silver–Gold):

- **Bronze**: Ingesta de datos crudos desde archivos CSV (`clientes.csv`, `cuentas.csv`, `transacciones.csv`).  
- **Silver**: Transformación y enriquecimiento de datos, uniendo clientes, cuentas y transacciones para obtener vistas detalladas.  
- **Gold**: Tablas analíticas optimizadas para reportes, como `resumenclientes`, que consolida métricas por cliente.  

Además:  
- Se configuraron **External Locations** en ADLS (`exlt-raw`, `exlt-bronze`, `exlt-silver`, `exlt-golden`).  
- Se creó el catálogo `catalog_au` con esquemas `raw`, `bronze`, `silver`, `golden`.  
- Se aplicaron **grants y permisos** para usuarios y roles (`Analists`, `Devs`, cuentas específicas).  

<img width="1536" height="1024" alt="Arquitectura" src="https://github.com/user-attachments/assets/f37e9707-bf48-423d-822f-6e733c457851" />


---

## 📊 Dashboard
El proyecto incluye un **Dashboard Bancario de Clientes** (`Dashboard Bancario de Clientes.lvdash.json`) que permite visualizar:  
- Total de transacciones por cliente.  
- Monto promedio de operaciones.  
- Distribución de clientes por ciudad.  
- Ranking de clientes por volumen de transacciones.  

<img width="1096" height="813" alt="Dashboard_databricks" src="https://github.com/ProTechD/CICD_SD_ADB_PROJECT_BANCA/blob/main/Dashboard/Dashboard_databricks.png" />

---

## 📂 Scripts del Proceso
Los notebooks y scripts en la carpeta **Proceso/** implementan cada etapa del pipeline:

1. **1.Preparacion_Ambiente.sql**  
   - Configura external locations en ADLS.  
   - Crea catálogo y esquemas (`raw`, `bronze`, `silver`, `golden`).  
   - Define tablas Delta para cada capa.  

2. **2.Ingest_clientes_data.py**  
   - Lee `clientes.csv` desde ADLS.  
   - Aplica esquema con tipos correctos.  
   - Renombra columnas y carga en `catalog_au.bronze.clientes`.  

3. **2.Ingest_cuentas_data.py**  
   - Lee `cuentas.csv`.  
   - Aplica esquema y transforma nombres de columnas.  
   - Inserta en `catalog_au.bronze.cuentas`.  

4. **2.Ingest_transacciones_data.py**  
   - Lee `transacciones.csv`.  
   - Aplica esquema y selecciona columnas relevantes.  
   - Inserta en `catalog_au.bronze.transacciones`.  

5. **3.Transform.py**  
   - Une clientes, cuentas y transacciones.  
   - Genera vista detallada en `catalog_au.silver.transacciones`.  

6. **4.Load.py**  
   - Agrega métricas por cliente (conteo, suma y promedio de montos).  
   - Carga resultados en `catalog_au.golden.resumenclientes`.  

7. **5.Accesos.ipynb**  
   - Define permisos y grants sobre catálogos, esquemas y tablas.  
   - Asigna privilegios de lectura/escritura a usuarios y roles.  

---

## ⚙️ CI/CD con GitHub Actions
El archivo `.github/workflows/deploy-notebook.yml` automatiza:  
- Exportación de notebooks desde el workspace origen.  
- Importación en el workspace destino.  
- Creación de un workflow en Databricks (`WF_ADB`) con tareas encadenadas:  
  - Preparación de ambiente → Ingesta → Transformación → Load → Grants.  
- Ejecución automática en un cluster existente (`cluster_SD`).  
- Monitoreo y validación de la ejecución.  

<img width="915" height="852" alt="Pre_commit" src="https://github.com/ProTechD/CICD_SD_ADB_PROJECT_BANCA/blob/main/Evidencias/Pre_commit.png" />
<img width="1891" height="827" alt="Deploy" src="https://github.com/ProTechD/CICD_SD_ADB_PROJECT_BANCA/blob/main/Evidencias/Deploy.png" />


---

## 🚀 Ejecución
1. Preparar ambiente (`1.Preparacion_Ambiente.sql`).  
2. Ingestar datasets (`2.Ingest_*`).  
3. Transformar datos (`3.Transform.py`).  
4. Cargar métricas (`4.Load.py`).  
5. Configurar accesos (`5.Accesos.ipynb`).  
6. Visualizar resultados en el Dashboard.  

<img width="1911" height="769" alt="WorkFlow_run_ok" src="https://github.com/ProTechD/CICD_SD_ADB_PROJECT_BANCA/blob/main/Evidencias/WorkFlow_run_ok.png" />
