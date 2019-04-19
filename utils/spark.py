"""Spark Utility functions."""
import logging

from pyspark.sql import SparkSession


def get_or_create_spark(app_name: str = 'spark-themednet'):
    """Get or create SparkSession object.
    Documentation: https://bit.ly/2FcXS2p

    Returns:
        - SparkSession: instantiated spark session
    """
    spark = (
        SparkSession.builder
        .master('local[*]')
        .appName(app_name)
        .config('spark.sql.shuffle.partitions', '4')
        .config("spark.executor.memory", "1g")
        .config("spark.driver.memory", "4g")
        .getOrCreate()
    )

    # py4j logging level
    logging.getLogger('py4j').setLevel(logging.ERROR)
    # spark logging level
    spark.sparkContext.setLogLevel('ERROR')

    return spark