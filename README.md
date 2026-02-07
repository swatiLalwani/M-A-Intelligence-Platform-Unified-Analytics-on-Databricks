# 🏟️ AtliQon × Sportsbar — M&A Intelligence Platform

<p align="left">
  <img src="https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)" />
  <img src="https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=green" />
</p>

> **Transforming fragmented M&A data into a unified $21B Executive Intelligence hub.**

![Pipeline Status](https://img.shields.io/badge/Pipeline-99.2%25%20Success-brightgreen) 
![Processing Time](https://img.shields.io/badge/Processing-<5_Min-blue) 
![Data Match Rate](https://img.shields.io/badge/Match_Rate-100%25-orange)


## 📋 Table of Contents
* [🎯 Business Problem](#business-problem)
* [💡 Solution Overview](#solution-overview)
* [🧱 Architecture](#architecture)
* [🔄 Data Pipeline](#data-pipeline)
* [📊 Dashboards & Insights](#dashboards-insights)
* [🛠️ Technical Implementation](#technical-implementation)
* [📈 Key Results](#key-results)
* [🎓 Skills Demonstrated](#skills-demonstrated)
  
## <a id="business-problem"></a>🎯 Business Problem
**Scenario:** AtliQon, a global sports equipment manufacturer ($119.93B annual revenue), acquires Sportsbar, a fast-growing sports nutrition startup.

**Challenge:**
- AtliQon operates on a mature ERP system with centralized data warehouse
- Sportsbar's operational data scattered across CSV files in AWS S3
- No unified analytics platform combining both companies' data
- Manual Excel-based reporting causing delays in post-merger insights
- Leadership needs integrated dashboards to track combined performance

**Goal:** Build a Databricks Lakehouse consolidating both companies' data and enable cross-company analytics for executive decision-making.

---

**Project Scope:**
- **AtliQon Data:** Pre-processed exports from existing data warehouse (historical baseline)
- **Sportsbar Data:** Raw CSV files from operational systems requiring full ETL (focus of this project)
- **Combined Output:** Unified dashboards showing integrated business metrics

## <a id="Solution Overview"></a>🎯 💡 Solution Overview

Built a Databricks Lakehouse architecture that unified both companies' data into a single analytical layer:

**Data Integration:**
- **AtliQon:** Loaded pre-curated exports from existing data warehouse (39M+ units historical)
- **Sportsbar:** Built end-to-end ETL processing raw CSV files from AWS S3 (50K+ orders)
- **Combined:** Merged into unified fact/dimension tables for cross-company analytics

**ETL Pipeline (Medallion Architecture):**
- **Bronze Layer:** Raw data ingestion from S3 with metadata tracking
- **Silver Layer:** Data quality transformations (validation, standardization, deduplication)
- **Gold Layer:** Business-ready dimensional model optimized for BI consumption

**Data Quality Transformations:**
- Validated customer IDs using regex pattern matching (^[0-9]+$)
- Standardized 4 different date formats using PySpark coalesce
- Removed duplicate order records via composite key deduplication
- Handled null values and data type mismatches

**Incremental Loading:**
- Daily processing of new CSV files from S3 landing directory
- Staging table pattern preventing reprocessing of historical data
- Automated file archival (landing → processed directories)

**Deliverables:**
- 5 stakeholder-specific dashboards (Executive, Finance, Sales, Marketing, Operations)
- Unified dimensional model combining equipment + nutrition product lines
- Automated daily refresh pipeline with Delta Lake ACID guarantees

**Key Metrics (Combined Company Data):**
- Total Revenue: $119.93B
- Total Units Sold: 39.05M
- Unique Customers: 54
- Product Categories: 50+ (Equipment + Nutrition)
- Channels: Retailer, Direct, Acquisition

## <a id="architecture"></a>🧱 Architecture (Databricks Lakehouse)

![Architecture](https://img.shields.io/badge/Architecture-Medallion-blueviolet)
![Modeling](https://img.shields.io/badge/Modeling-Star_Schema-lightgrey)
![ETL](https://img.shields.io/badge/ETL-Incremental_Load-yellowgreen)

<img src="Docs/project_architecture.png" width="900">

Medallion Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│ BRONZE LAYER (Raw Data Ingestion)                           │
├─────────────────────────────────────────────────────────────┤
│ • AtliQon: Pre-curated exports (historical baseline)        │
│ • Sportsbar: Raw CSV from S3 (50K+ orders)                  │
│ • Metadata: file_name, file_size, read_timestamp            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ SILVER LAYER (Cleaned & Standardized)                       │
├─────────────────────────────────────────────────────────────┤
│ • Customer ID validation (regex pattern matching)           │
│ • Date standardization (4 format variants → DATE type)      │
│ • Duplicate removal (composite key deduplication)           │
│ • Null handling & data type casting                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ GOLD LAYER (Business-Ready Dimensional Model)               │
├─────────────────────────────────────────────────────────────┤
│ • fact_sales_unified (39M+ units, $119.93B revenue)         │
│ • dim_customer (54 customers)                               │
│ • dim_product (50+ categories: equipment + nutrition)       │
│ • Denormalized views for dashboard consumption              │
└─────────────────────────────────────────────────────────────┘
                            ↓
                 Databricks Dashboards
```
 
## <a id="data-pipeline"></a>🔄 Data Pipeline
Source Systems
Company   DataSource        Format               LoadType           Period
AtliQon   Pre-processed DW  exportParquet/CSV    Full Load          Jul-Nov 2024
Sportsbar Operational      Database (via S3)CSV  Full + Incremental Jul-Dec 2024

Processing Workflow
1️⃣ Dimension Processing (Silver Layer)

📂 Scripts/

├── 1_customer_data_processing.ipynb    → Unified customer master

├── 2_products_data_processing.ipynb    → Merged product catalog  

└── 3_pricing_data_processing.ipynb     → Cost/price standardization

Key Transformations:

- Customer Validation: Validated customer IDs using regex pattern matching (^[0-9]+$), replacing invalid entries with placeholder '999999'
- Product Integration: Merged Sportsbar nutrition categories (Breakfast Foods, Dairy & Recovery, Hydration) into AtliQon's product taxonomy
- Data Standardization: Handled 4 different date formats, removed duplicates, cast data types

2️⃣ Fact Table Creation (Gold Layer)

📂 Scripts/

├── 1_full_load_fact.ipynb              → Historical facts (Jul-Nov)

└── 2_incremental_load_fact.ipynb       → Daily append (Dec onwards)

Incremental Loading Pattern:

📂 Datasets/Sportsbar/Incremental_load/

├── orders_2025_12_01.csv   → Day 1 transactions

├── orders_2025_12_02.csv   → Day 2 transactions

└── orders_2025_12_03.csv   → Day 3 transactions

Processes daily order files arriving in S3
Appends to unified fact table with company_source flag
Maintains full history for trend analysis

## <a id="dashboards-insights"></a>📊 Dashboards & Insights
Built 5 stakeholder-specific dashboards analyzing combined company performance:

---

### 👔 1. Executive Dashboard

**Audience:** C-Suite, Board Members

**Key Metrics:**
- 📈 Total Revenue: **$119.93B**
- 📊 Total Units Sold: **39.05M**
- 💰 Average Selling Price: **$4,052.46**
- 👥 Unique Customers: **54**

**Insights:**
- Revenue distribution across Retailer, Direct, and Acquisition channels
- Top 5 customers identified (FitnessWorld, Atlikon Essentials, Atlikon Superstore)
- Monthly revenue trends showing seasonality patterns
- Price vs quantity relationship analysis


**Screenshot:** <img src="Dashboards/Screenshots/Screenshot1 .png" width="900">

[View full dashboard (PDF)](Dashboards/AtliQon%20Executive%20Dashboard.pdf)

---

💰 2. Finance Dashboard
**Audience:** CFO, Finance Team

**Key Metrics:**
- Total Revenue: $119.93B
- Average Selling Price: $4,052.46
- Total Units Sold: 39.05M
- Revenue QoQ Change: $101.21K

**Insights:**
- Revenue and units trend over time
- Revenue breakdown by division (Archery, Basketball, Cycling, **Nutrition categories**)
- Quarter-over-quarter revenue change by division
- Average selling price trends by division

**Screenshot:** <img src="Dashboards/Screenshots/Screenshot 2.png" width="900">

[View full dashboard (PDF)](Dashboards/AtliQon%20Finance%20Dashboard.pdf)

---

📈 3. Sales Dashboard
**Audience:** VP Sales, Regional Managers

**Key Insights:**
- Revenue performance by channel (Retailer vs Direct vs Acquisition)
- Top products by revenue (Cricket, Football, Weight Lifting)
- Top customers by revenue (visual ranking)
- Sales trends by platform (Brick & Mortar, E-Commerce, Sports Bar)
- Top-performing categories by revenue per quarter

**Screenshot:** <img src="Dashboards/Screenshots/Screenshot 6.png" width="900">

[View full dashboard (PDF)](Dashboards/AtliQon%20Sales%20Dashboard.pdf)

---

📣 4. Marketing Dashboard
**Audience:** CMO, Marketing Team

**Key Insights:**
- Quarter-over-quarter revenue growth by product category
- New vs repeat customer proportions by acquisition channel
- Revenue distribution by platform
- Market and product performance matrix (category × market analysis)

**Screenshot:** <img src="Dashboards/Screenshots/Screenshot 3.png" width="900">

[View full dashboard (PDF)](Dashboards/AtliQon%20Marketing%20Dashboard.pdf)

---

🚚 5. Operations Dashboard
**Audience:** VP Supply Chain, Warehouse Managers

**Key Insights:**
- Units sold by product variant
- Demand trends by category (50+ categories tracked)
- Seasonality patterns for inventory planning
- High-volume low-revenue products identification
- Platform distribution (Brick & Mortar vs E-Commerce)

**Screenshot:** <img src="Dashboards/Screenshots/Screenshot 4.png" width="900">

[View full dashboard (PDF)](Dashboards/AtliQon%20Operations%20Dashboard.pdf)

---

### Cross-Dashboard Insights

**✅ Product Integration Success:**
- Nutrition categories (Breakfast Foods, Dairy & Recovery, Hydration & Electrolytes, Healthy Snacks) successfully integrated alongside equipment
- Cross-category analysis now possible for customer purchasing patterns

**✅ Channel Performance:**
- Three distinct channels visible: Retailer, Direct, Acquisition
- Platform breakdown: Brick & Mortar, E-Commerce, Sports Bar

**✅ Customer Intelligence:**
- 54 unique customers tracked post-merger
- Top customer concentration identified (FitnessWorld appears 3x in top 5)
- Customer segmentation by channel and platform enabled

## <a id="technical-implementation"></a>🛠️ Technical Implementation
### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Storage** | AWS S3 | Raw CSV file ingestion (Sportsbar data) |
| **Processing** | Databricks (PySpark) | Bronze → Silver → Gold transformations |
| **Data Format** | Delta Lake | ACID transactions, time travel, schema evolution |
| **Orchestration** | Databricks Workflows | Automated daily pipeline execution |
| **Modeling** | SQL, Python | Dimensional modeling, data quality logic |
| **Visualization** | Databricks Dashboards | 5 stakeholder-specific views |
| **Version Control** | Git/GitHub | Code & documentation management |

---

### Data Model

**Fact Table:** `fact_sales_unified`
- Combines AtliQon equipment sales + Sportsbar nutrition sales
- 39M+ units across combined product catalog
- Grain: One row per order line item

**Dimension Tables:**
- `dim_customer` - 54 unique customers across all channels
- `dim_product` - 50+ categories (equipment + nutrition)
- `dim_pricing` - Cost and price history

---

### Key Technical Challenges Solved

#### **Challenge 1: Invalid Customer ID Handling**

**Problem:** Sportsbar's order data contained invalid customer IDs like 'ABC987', 'INVALID', and other non-numeric values.

**Solution:**
```python
df_orders = df_orders.withColumn(
    "customer_id",
    F.when(F.col("customer_id").rlike("^[0-9]+$"), F.col("customer_id"))
     .otherwise("999999")
     .cast("string")
)
```

**Result:** Clean customer dimension with all invalid IDs safely handled using placeholder value.

---

#### **Challenge 2: Multi-Format Date Standardization**

**Problem:** `order_placement_date` arrived in 4 different formats:
- `2025/07/01` (yyyy/MM/dd)
- `01-07-2025` (dd-MM-yyyy)
- `01/07/2025` (dd/MM/yyyy)
- `Tuesday, July 01, 2025` (MMMM dd, yyyy with weekday prefix)

**Solution:**
```python
# Remove weekday prefix
df_orders = df_orders.withColumn(
    "order_placement_date",
    F.regexp_replace(F.col("order_placement_date"), r"^[A-Za-z]+,\s*", "")
)

# Parse multiple formats
df_orders = df_orders.withColumn(
    "order_placement_date",
    F.coalesce(
        F.try_to_date("order_placement_date", "yyyy/MM/dd"),
        F.try_to_date("order_placement_date", "dd-MM-yyyy"),
        F.try_to_date("order_placement_date", "dd/MM/yyyy"),
        F.try_to_date("order_placement_date", "MMMM dd, yyyy")
    )
)
```

**Result:** 100% date parsing success across all formats.

---

#### **Challenge 3: Incremental Loading Pattern**

**Problem:** Daily order files arrive in S3. Reprocessing all historical files daily wastes compute.

**Solution:** Staging table pattern
```python
# 1. Read only new files from landing directory
df = spark.read.csv(f"{landing_path}/*.csv")

# 2. Write to staging (overwrites daily)
df.write.mode("overwrite").saveAsTable(f"staging_{data_source}")

# 3. Append to bronze (preserves history)
df.write.mode("append").saveAsTable(bronze_table)

# 4. Archive processed files
dbutils.fs.mv(file_path, f"{processed_path}/{file_name}")
```

**Result:** 
- Only new daily files processed (incremental approach)
- Historical files archived to prevent reprocessing
- Pipeline scales from 100 to 100K+ records/day without redesign

---

#### **Challenge 4: Dimension Table Upserts**

**Problem:** Customer dimension needs updates when existing customers change while also inserting new customers.

**Solution:** Delta Lake MERGE operation
```python
delta_table.alias("target").merge(
    source=df_child_customers.alias("source"),
    condition="target.customer_code = source.customer_code"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

**Result:** Idempotent upsert logic handling both inserts and updates in single operation.

---


**Orchestration:**

<img src="Orchestration/jobrun.png" width="900">



## <a id="key-results"></a>📈 Key Results
### Business Impact

**Unified Analytics Platform:**
- ✅ Consolidated AtliQon ($119.93B revenue) + Sportsbar data into single source of truth
- ✅ Delivered 5 stakeholder-specific dashboards serving Executive, Finance, Sales, Marketing, Operations teams
- ✅ Enabled cross-category analysis between sports equipment and nutrition products
- ✅ Automated daily data refresh eliminating manual Excel consolidation

**Data Integration Achievements:**
- ✅ Processed 50K+ Sportsbar orders through Bronze → Silver → Gold layers
- ✅ Merged nutrition product categories (Breakfast Foods, Dairy & Recovery, Hydration) into AtliQon's equipment taxonomy
- ✅ Unified customer dimension supporting cross-company customer analysis
- ✅ Created denormalized views enabling <2 second dashboard query response

**Technical Implementation:**
- ✅ Built incremental ETL pipeline with staging table pattern
- ✅ Implemented data quality transformations handling invalid IDs, mixed date formats, duplicates
- ✅ Used Delta Lake MERGE operations for dimension upsert logic
- ✅ Enabled change data feed for audit tracking
- ✅ Integrated with AWS S3 for automated file ingestion and archival

### Strategic Insights Delivered

**📊 Revenue Analysis:**
- Retailer channel dominates revenue contribution
- Top 5 customers represent significant revenue concentration
- Nutrition products (Sportsbar) show growth opportunities alongside equipment

**📈 Product Strategy:**
- Cross-sell potential between equipment and nutrition categories identified
- High-volume low-revenue products flagged for pricing review
- Seasonal demand patterns documented for inventory planning

**🎯 Channel Optimization:**
- Platform mix: Brick & Mortar, E-Commerce, Sports Bar analyzed
- Acquisition channel performance tracked for marketing ROI
- Direct channel expansion opportunity identified

**🚚 Operations Efficiency:**
- Demand trends by category support inventory optimization
- Seasonality patterns inform supply chain planning
- High-volume products identified for warehouse co-location

## <a id="skills-demonstrated"></a>🎓 Skills Demonstrated
Data Engineering

✅ Medallion Architecture (Bronze/Silver/Gold) implementation
✅ Incremental loading patterns (daily batch processing)
✅ Dimensional modeling (star schema design)
✅ Data quality & deduplication strategies
✅ ETL pipeline orchestration
✅ Cloud storage integration (AWS S3)

Analytics & BI

✅ Stakeholder requirement gathering (5 personas)
✅ KPI design for M&A scenarios
✅ Executive dashboard development
✅ Business insight generation
✅ Data storytelling & recommendations

Technical Tools

✅ Databricks: Lakehouse architecture, PySpark, SQL
✅ Python: Pandas, data transformations
✅ SQL: Complex joins, aggregations, window functions
✅ Power BI: DAX, data modeling, visualizations
✅ Git: Version control, documentation

Business Acumen

✅ M&A analytics domain knowledge
✅ Cross-functional collaboration (Finance, Sales, Marketing, Ops)
✅ Strategic recommendation development
✅ Executive communication



