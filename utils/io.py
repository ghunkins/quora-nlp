"""Data loading utility."""
from functools import reduce
from typing import Optional, Callable, List, Union

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit
from IPython.core.display import display

from .spark import get_or_create_spark


class SparkIO:
    """Spark I/O Utility class."""

    def __init__(self, spark: Optional[SparkSession] = None):
        self.spark = spark or get_or_create_spark()
        self._read = None
        self._write = None

    @property
    def read(self):
        """SparkReader object."""
        if not self._read:
            self._read = SparkReader(self.spark)
        return self._read

    @property
    def write(self):
        """SparkWriter object."""
        if not self._write:
            self._write = SparkWriter()
        return self._write

    def display(self, df: DataFrame, limit: int = 100):
        """DataFrame display functionality."""
        limit_df = self.spark.createDataFrame(df.head(limit), df.schema)
        display(limit_df.toPandas())


class SparkReader:
    """Spark input class."""

    CSV_OPTIONS = {'header': True}

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def csv(self, path: Union[str, List[str]], **kw_options) -> DataFrame:
        """Read csv file into DataFrame obj."""
        kw_options = {**self.CSV_OPTIONS, **kw_options}
        if isinstance(path, list):
            return self._read_multi(self.csv, path, **kw_options)
        return self.spark.read.csv(path=path, **kw_options)

    def json(self, path: Union[str, List[str]], **kw_options) -> DataFrame:
        """Read json file into DataFrame obj."""
        if isinstance(path, list):
            return self._read_multi(self.json, path, **kw_options)
        return self.spark.read.json(path=path, **kw_options)

    def parquet(self, path: Union[str, List[str]], **kw_options) -> DataFrame:
        """Read parquet file into DataFrame obj."""
        if isinstance(path, list):
            return self.spark.read.parquet(*path, **kw_options)
        return self.spark.read.parquet(path, **kw_options)

    def _read_multi(self,
                    func: Callable,
                    paths: List[str],
                    origin_file: bool = True,
                    **kw_options):
        if origin_file:
            dfs = [func(p, **kw_options).withColumn('__origin', lit(p)) for p in paths]
        else:
            dfs = [func(p, **kw_options) for p in paths]
        return reduce(DataFrame.union, dfs)


class SparkWriter:
    """Spark output class."""

    @staticmethod
    def csv(df: DataFrame, path: str, **kw_options) -> None:
        """Write DataFrame obj to csv format."""
        df.write.csv(path=path, **kw_options)

    @staticmethod
    def json(df: DataFrame, path: str, **kw_options) -> None:
        """Write DataFrame obj to json format."""
        df.write.json(path=path, **kw_options)

    @staticmethod
    def parquet(df: DataFrame, path: str, **kw_options) -> None:
        """Write DataFrame obj to parquet format."""
        df.write.parquet(path=path, **kw_options)
