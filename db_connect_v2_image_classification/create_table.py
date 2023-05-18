from databricks.connect.session import DatabricksSession as SparkSession
from databricks.sdk.core import Config
from pyspark.sql.functions import element_at, split

from db_connect_v2_image_classification.configs import AppConfig
from db_connect_v2_image_classification.main_wrapper import main_wrapper


class CreateTableTask:
    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.spark = SparkSession.builder.sdkConfig(
            Config(profile=self.cfg.profile, cluster_id=self.cfg.cluster_id)
        ).getOrCreate()

    def launch(self):
        print(f"Loading image metadata into the table {self.cfg.image_table}")
        print(f"Using cluster {self.cfg.cluster_name} with id {self.cfg.cluster_id}")

        metadata_df = self._load_image_metadata()
        metadata_df.write.saveAsTable(f"{self.cfg.image_table}", format="delta", mode=self.cfg.table_saving_mode)
        print(f"Image metadata has been successfully saved into the table {self.cfg.image_table}")

    def _load_image_metadata(self):
        images = (
            self.spark.read.format("image")
            .load("/databricks-datasets/flower_photos/*/*.jpg")
            .select("image.origin")
            .withColumn("class", element_at(split("origin", "/"), 4))
            .withColumn(
                "image_id",
                element_at(split(element_at(split("origin", "/"), -1), ".jpg"), 1),
            )
            .select("image_id", "class", "origin")
        )
        return images


@main_wrapper()
def entrypoint(cfg: AppConfig):
    task = CreateTableTask(cfg)
    task.launch()
