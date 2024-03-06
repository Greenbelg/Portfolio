from pathlib import Path
from flask import Flask, render_template, jsonify, request
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly import express as px
from datetime import date
import sys

app = Flask(__name__)
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

PATH_TO_TEMPLATES = Path(__file__).parent.joinpath("templates")

sys.path.append(Path(__file__).parent)

from src.visits import Visits


def initialize_dash():
    dash_app.layout = html.Div([
        html.H3("Уникальность посещений"),
        dcc.Dropdown(
            id="isUnique",
            options=[
                {'label': 'Только уникальные', 'value': "True"},
                {'label': 'Все', 'value': "False"}
            ],
            value="False"
        ),
        html.H3('Период'),
        dcc.Dropdown(
            id='period',
            options=[
                {'label': 'Для всех ip', 'value': 'all'},
                {'label': 'За день', 'value': 'day'},
                {'label': 'За неделю', 'value': 'week'},
                {'label': 'За месяц', 'value': 'month'},
                {'label': 'За год', 'value': 'year'}
            ],
            value='day'
        ),
        html.Br(),
        dcc.Graph(id='visits-graph')
    ])


def insert_data_in_page(name_page):
    page = PATH_TO_TEMPLATES.joinpath(name_page + '.html')\
        .open(encoding='utf-8').read()
    stats_day, unique_stats_day = Visits.get_stats_for('day')
    stats_month, unique_stats_month = Visits.get_stats_for('month')
    stats_all, unique_stats_all = Visits.get_stats_for('all')
    page = page.replace('DAY', str(stats_day.get(str(date.today().day))))
    page = page.replace('MONTH', str(stats_month.get(str(date.today().month))))
    page = page.replace('ALL', str(sum(stats_all.values())))
    return page


@app.route("/")
def root():
    client_host = request.remote_addr if request.remote_addr else "unknown"
    Visits.add_new_visit(client_host)
    page = insert_data_in_page('index')
    return page


@app.route("/stats/<period>")
def stats(period):
    if period in ["all", "day", "week", "month", "year"]:
        stats_data, unique_stats_data = Visits.get_stats_for(period)
        return jsonify(
            Visits.jsonize_data(stats_data, unique_stats_data, period))

    return "Page not found", 404


@app.route('/dashboard/')
def render_dashboard():
    return dash_app.index()


@dash_app.callback(Output('visits-graph', 'figure'),
                   Input('period', 'value'), Input('isUnique', 'value'))
def update_graph(selected_period, is_unique):
    stats_data, unique_stats_data = Visits.get_stats_for(selected_period)
    query = f"Unique visits for {selected_period}" if is_unique == "True" \
        else f"All visits for {selected_period}"
    data = unique_stats_data if is_unique == "True" else stats_data
    figure = px.pie(names=list(data.keys()), values=list(data.values()))
    return figure


if __name__ == "__main__":
    initialize_dash()
    app.run(debug=True)
