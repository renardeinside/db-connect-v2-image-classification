from dash import dcc, html

header = dcc.Markdown(
    "## Image labeling app, built with [Dash](https://plotly.com/dash/) "
    "and [DB Connect V2](https://www.databricks.com/blog/2022/07/07/introducing-spark-connect-the-power-of-apache-spark-everywhere.html) 🔥",
    className="text-4xl mb-2",
)


guideline = dcc.Markdown(
    "Please click below to navigate between images and correct their class labels when required.",
)

random_btn = html.Button(
    "🔀 Next image",
    id="random_btn",
    n_clicks=0,
    className="btn btn-primary btn-lg mt-5",
)

nav_container = html.Div(children=[random_btn], style={"display": "flex", "justify-content": "center"})

confirm_button = dcc.Loading(
    id="submit-loading",
    children=[
        html.Button(
            "Confirm",
            id="confirm_btn",
            n_clicks=0,
            className="btn btn-success btn-block my-4",
        ),
        html.Div(id="output_mock", style={"display": "none"}),
    ],
)


def class_selector(class_choices):
    return html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Loading(
                        children=[
                            html.P("Please choose the class below:"),
                            dcc.Dropdown(
                                class_choices,
                                id="class_selector",
                                className="dropdown-content text-black",
                                placeholder="Select the class",
                                multi=False,
                                clearable=False,
                            ),
                        ]
                    )
                ],
            ),
            confirm_button,
        ],
    )


def data_container(class_choices):
    return html.Div(
        children=[
            html.Div(
                className="flex justify-center pt-2",
                children=[
                    html.Div(
                        className="card w-96 bg-base-100 shadow-xl p-4",
                        children=[
                            dcc.Loading(
                                [
                                    dcc.Graph(id="img_display"),
                                    dcc.Markdown(id="image_id", className="text-sm text-sky-500"),
                                ]
                            ),
                            class_selector(class_choices),
                        ],
                    )
                ],
            ),
        ]
    )
