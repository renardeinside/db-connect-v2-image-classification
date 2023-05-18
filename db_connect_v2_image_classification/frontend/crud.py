from typing import List
from databricks.connect.session import DatabricksSession as SparkSession
from databricks.sdk.core import Config
from pyspark.sql import DataFrame

from db_connect_v2_image_classification.configs import AppConfig
import numpy as np
from functools import lru_cache


class DataOperator:
    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.spark = SparkSession.builder.sdkConfig(
            Config(profile=self.cfg.profile, cluster_id=self.cfg.cluster_id)
        ).getOrCreate()

    @property
    def _source_table(self) -> DataFrame:
        return self.spark.table(f"{self.cfg.image_table}")

    @lru_cache(maxsize=10_000)
    def get_all_indexes(self) -> List[str]:
        return self._source_table.select("image_id").distinct().toPandas()["image_id"].to_list()

    @lru_cache(maxsize=10_000)
    def get_all_classes(self) -> List[str]:
        return self._source_table.select("class").distinct().toPandas()["class"].to_list()

    def get_image_class(self, image_id: str) -> str:
        return self._source_table.select("class").where(f"image_id = '{image_id}'").toPandas().loc[0, "class"]

    def get_image_payload(self, image_id: str) -> np.ndarray:
        image_origin = self._source_table.select("origin").where(f"image_id = '{image_id}'").toPandas().loc[0, "origin"]
        image_info = self.spark.read.format("image").load(image_origin).toPandas().T.squeeze()

        img_payload = np.frombuffer(image_info["data"], dtype=np.uint8).reshape(
            image_info["height"], image_info["width"], image_info["nChannels"]
        )[:, :, ::-1]

        return img_payload

    def update_image_class(self, image_id: str, new_class: str):
        print("Updating the image class!")
        command = f"UPDATE {self.cfg.image_table} SET class='{new_class}' WHERE image_id='{image_id}'"
        df = self.spark.sql(command)
        df.show()
        print("Update finished")
