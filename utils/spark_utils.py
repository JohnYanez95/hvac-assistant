"""spark_utils.py - Spark session management for HVAC Assistant"""

from pyspark.sql import SparkSession
from .config_loader import get_spark_config


def construct_spark_session(app_name: str = "HVAC-Assistant") -> SparkSession:
    """Construct a Spark session with configuration from config.yaml
    
    Args:
        app_name: Name for the Spark application
        
    Returns:
        Configured SparkSession instance
    """
    config = get_spark_config()
    
    # Use config values with fallbacks
    local_threads = config.get('local_threads', 6)
    executor_memory = config.get('executor_memory', '16g')
    driver_memory = config.get('driver_memory', '32g')
    shuffle_partitions = config.get('shuffle_partitions', 216)
    log_level = config.get('log_level', 'WARN')
    
    spark = (
        SparkSession.builder.appName(app_name)
        .master(f"local[{local_threads}]")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.executor.memory", executor_memory)
        .config("spark.driver.memory", driver_memory)
        .config("spark.sql.adaptive.enabled", "false")
        .config("spark.sql.shuffle.partitions", str(shuffle_partitions))
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        # Additional configs for text processing
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel(log_level)
    return spark


def stop_spark_session(spark: SparkSession) -> None:
    """Safely stop a Spark session
    
    Args:
        spark: SparkSession to stop
    """
    if spark:
        spark.stop()


def get_spark_context_info(spark: SparkSession) -> dict:
    """Get information about the current Spark context
    
    Args:
        spark: Active SparkSession
        
    Returns:
        Dictionary with Spark context information
    """
    sc = spark.sparkContext
    return {
        "application_name": sc.appName,
        "application_id": sc.applicationId,
        "master": sc.master,
        "spark_version": sc.version,
        "default_parallelism": sc.defaultParallelism,
        "python_version": sc.pythonVer
    }