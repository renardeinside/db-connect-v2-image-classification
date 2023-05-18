import logging
from random import choice

from dash import Dash, dcc, html

from db_connect_v2_image_classification.configs import AppConfig
from db_connect_v2_image_classification.css_utils import external_scripts, external_stylesheets
from db_connect_v2_image_classification.frontend.callbacks import prepare_callbacks
from db_connect_v2_image_classification.frontend.components import data_container, guideline, header, nav_container
from db_connect_v2_image_classification.frontend.crud import DataOperator
from db_connect_v2_image_classification.main_wrapper import main_wrapper

logger = logging.getLogger("frontend_app")
logger.setLevel(logging.INFO)


def prepare_layout(op: DataOperator) -> html.Div:
    logger.info("Preparing the layout")
    layout = html.Div(
        children=[
            header,
            guideline,
            data_container(op.get_all_classes()),
            nav_container,
            dcc.Store(id="current_index", data=choice(op.get_all_indexes())),
        ],
        className="p-5",
        style={"height": "100vh"},
    )
    logger.info("layout prepared")
    return layout


@main_wrapper()
def entrypoint(cfg: AppConfig):
    app = Dash(
        __name__,
        title="Image Classification App",
        external_scripts=external_scripts,
        external_stylesheets=external_stylesheets,
    )
    logger.info("Preparing the data operator")
    op = DataOperator(cfg)
    logger.info("Data operator loaded successfully")
    app.layout = prepare_layout(op)
    prepare_callbacks(app, op)
    app.run(debug=cfg.debug, host="0.0.0.0")


if __name__ == "__main__":
    entrypoint()
