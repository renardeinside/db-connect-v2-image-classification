from random import choice

import plotly.express as px
from dash import Dash, Input, Output, State

from db_connect_v2_image_classification.frontend.crud import DataOperator


def prepare_callbacks(app: Dash, op: DataOperator):
    @app.callback(
        Output("current_index", "data"),
        Output("image_id", "children"),
        Output("class_selector", "value"),
        Output("img_display", "figure"),
        Input("random_btn", "n_clicks"),
    )
    def get_next_random(_):
        next_index = choice(op.get_all_indexes())
        img_class = op.get_image_class(next_index)
        img_payload = op.get_image_payload(next_index)
        figure = px.imshow(img_payload)
        figure.update_layout(coloraxis_showscale=False)
        figure.update_xaxes(showticklabels=False)
        figure.update_yaxes(showticklabels=False)
        return next_index, f"Image id: {next_index}", img_class, figure

    @app.callback(
        Output("output_mock", "children"),
        Input("confirm_btn", "n_clicks"),
        State("class_selector", "value"),
        State("current_index", "data"),
    )
    def save_selected_class(_, value, current_index):
        if value:
            op.update_image_class(current_index, value)
        return value
