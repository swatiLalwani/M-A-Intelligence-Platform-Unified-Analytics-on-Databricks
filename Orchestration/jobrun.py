# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0
%restart_python

from databricks.sdk.service.jobs import JobSettings as Job


Incremental_Job_Update = Job.from_dict(
    {
        "name": "Incremental_Job_Update",
        "tasks": [
            {
                "task_key": "dim_processing_customers",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/swatilalwani342@gmail.com/Consolidated_pipeline/2_dimension_data_processing/1_customer_data_processing",
                    "base_parameters": {
                        "catalog": "fmcg",
                        "data_source": "customers",
                    },
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "dim_processing_products",
                "depends_on": [
                    {
                        "task_key": "dim_processing_customers",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/swatilalwani342@gmail.com/Consolidated_pipeline/2_dimension_data_processing/2_products_data_processing",
                    "base_parameters": {
                        "catalog": "fmcg",
                        "data_source": "products",
                    },
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "dim_processing_pricing",
                "depends_on": [
                    {
                        "task_key": "dim_processing_products",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/swatilalwani342@gmail.com/Consolidated_pipeline/2_dimension_data_processing/3_pricing_data_processing",
                    "base_parameters": {
                        "catalog": "fmcg",
                        "data_source": "gross_price",
                    },
                    "source": "WORKSPACE",
                },
            },
            {
                "task_key": "fact_processing_orders",
                "depends_on": [
                    {
                        "task_key": "dim_processing_pricing",
                    },
                ],
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/swatilalwani342@gmail.com/Consolidated_pipeline/3_fact_data_processing/2_incremental_load_fact",
                    "base_parameters": {
                        "catalog": "fmcg",
                        "data_source": "orders",
                    },
                    "source": "WORKSPACE",
                },
            },
        ],
        "queue": {
            "enabled": True,
        },
        "performance_target": "PERFORMANCE_OPTIMIZED",
    }
)

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
w.jobs.reset(new_settings=Incremental_Job_Update, job_id=1097669241771925)
# or create a new job using: w.jobs.create(**Incremental_Job_Update.as_shallow_dict())
