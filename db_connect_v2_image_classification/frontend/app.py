from random import choice

from dash import Dash, Input, Output, State, ctx, dcc, html
from db_connect_v2_image_classification.configs import AppConfig
from db_connect_v2_image_classification.css_utils import external_stylesheets
from db_connect_v2_image_classification.css_utils import external_scripts

from db_connect_v2_image_classification.main_wrapper import main_wrapper
from db_connect_v2_image_classification.frontend.components import header, guideline, nav_container, data_container
from db_connect_v2_image_classification.frontend.crud import DataOperator
from db_connect_v2_image_classification.frontend.callbacks import prepare_callbacks
from typing import List
import logging

logger = logging.getLogger("frontend_app")
logger.setLevel(logging.INFO)


def prepare_layout(op: DataOperator) -> html.Div:
    return html.Div(
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
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    entrypoint()
