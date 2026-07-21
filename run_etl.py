# ============================================
# Sales Analytics Platform
# Master ETL Automation Pipeline
# ============================================

import subprocess
import time

from python.automation.reset_database import reset_database
from python.automation.validate_database import validate_database
from python.automation.logger import setup_logger


# ============================================
# Initialize Logger
# ============================================

logger = setup_logger()


# ============================================
# Start Timer
# ============================================

start_time = time.time()

print("=" * 70)
print("        SALES ANALYTICS MASTER ETL PIPELINE")
print("=" * 70)

logger.info("=" * 70)
logger.info("Sales Analytics ETL Pipeline Started")


# ============================================
# Step 1 : Reset Database
# ============================================

print("\nResetting Database...\n")

logger.info("Resetting Database")

success = reset_database()

if success:

    logger.info("Database Reset Successful")

else:

    logger.error("Database Reset Failed")

    print("Pipeline stopped because database reset failed.")

    exit()


# ============================================
# ETL Modules
# ============================================

scripts = [

    "python.etl.load_dim_customer",

    "python.etl.load_dim_product",

    "python.etl.load_dim_location",

    "python.etl.load_dim_ship_mode",

    "python.etl.load_dim_date",

    "python.etl.load_fact_sales"

]


# ============================================
# Execute ETL Modules
# ============================================

for script in scripts:

    print("\n" + "=" * 70)
    print(f"Running : {script}")
    print("=" * 70)

    logger.info(f"Running Module : {script}")

    result = subprocess.run(

        ["python", "-m", script],

        capture_output=True,

        text=True

    )

    # ----------------------------------------
    # Success
    # ----------------------------------------

    if result.returncode == 0:

        print("STATUS : SUCCESS\n")

        if result.stdout:

            print(result.stdout)

        logger.info(f"{script} Completed Successfully")

    # ----------------------------------------
    # Failure
    # ----------------------------------------

    else:

        print("STATUS : FAILED\n")

        if result.stderr:

            print(result.stderr)

        logger.error(f"{script} Failed")

        logger.error(result.stderr)

        print("\nPipeline Stopped.")

        logger.error("Pipeline Stopped")

        exit()


# ============================================
# Database Validation
# ============================================

print("\n")
print("=" * 70)
print("Running Database Validation")
print("=" * 70)

logger.info("Starting Database Validation")

validate_database()

logger.info("Database Validation Completed Successfully")


# ============================================
# Finish Pipeline
# ============================================

end_time = time.time()

execution_time = round(end_time - start_time, 2)

print("\n" + "=" * 70)
print("Pipeline Completed Successfully")
print(f"Execution Time : {execution_time} seconds")
print("=" * 70)

logger.info("Pipeline Completed Successfully")
logger.info(f"Total Execution Time : {execution_time} seconds")
logger.info("=" * 70)