from db_connect_v2_image_classification.configs import AppConfig


import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf, SCMode


from typing import Callable


def main_wrapper():
    # prepares the config store for any entrypoints that will use this decorator
    # since we're using the same AppConfig both for table creation and for frontend app, we'll simply re-use this function.
    cs = ConfigStore.instance()
    cs.store(name="base_config", node=AppConfig)

    # a decorator that will wrap any function under @main_wrapper()
    def decorator(func: Callable[[AppConfig], None]):
        # hydra.main to enable flexible config provisioning
        @hydra.main(version_base=None, config_name="config")
        def _wrapped(cfg: DictConfig):
            # important - we're using dataclasses with additional functionality inside them (e.g. methods or __post_init__)
            # by default hydra returns an untyped DictConfig, with this we convert the config back into a Python dataclass with all methods.
            _cfg = OmegaConf.to_container(cfg, structured_config_mode=SCMode.INSTANTIATE)
            func(_cfg)

        return _wrapped

    return decorator
