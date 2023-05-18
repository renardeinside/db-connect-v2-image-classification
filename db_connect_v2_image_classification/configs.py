from dataclasses import dataclass, MISSING, field
from typing import Optional
from databricks.sdk import WorkspaceClient


@dataclass
class ImageTableConfig:
    catalog: str = "main"
    database: str = "default"
    table: str = "db_connect_v2_example_images_metadata"

    # note - repr is used both inside print statements and when table name is provided to Spark APIs
    def __repr__(self) -> str:
        return f"{self.catalog}.{self.database}.{self.table}"


@dataclass
class AppConfig:
    cluster_name: str
    cluster_id: str = field(init=False)
    image_table: ImageTableConfig = field(default_factory=ImageTableConfig)
    profile: Optional[str] = "DEFAULT"

    # defines is we want to overwite the table, fail when it exists or append data into it
    table_saving_mode: Optional[str] = "error"

    def __post_init__(self):
        _w = WorkspaceClient(profile=self.profile)
        found = list(filter(lambda c: c.cluster_name == self.cluster_name, _w.clusters.list()))
        assert found is not None, f"Not found any clusters with name {self.cluster_name}"
        assert len(found) == 1, f"There are more than one cluster with name {self.cluster_name}"
        self.cluster_id = found[0].cluster_id
