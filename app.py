"""Main orchestration module serving the Interactive Flask Dashboard layer.

Loads persistent datasets safely at server startup and routes incoming
web client interactions efficiently across templates.
"""

from flask import Flask, render_template, request
from data_processing import load_and_clean_data, COUNTRIES
from visualization import plot_trend, plot_compare
from exceptions import DashboardError

app = Flask(__name__)

# System-wide global state pointer storage for the dataset
GLOBAL_DATAFRAME = None

try:
    # Initialize resource bindings cleanly at startup application checkpoint
    GLOBAL_DATAFRAME = load_and_clean_data('owid-covid-data.csv')
except DashboardError as startup_error:
    print(f"CRITICAL SYSTEM BOOT ALERT: {startup_error}")


@app.route('/', methods=['GET', 'POST'])
def index():
    """Manages system execution paths for primary route data and analytical trend selections."""
    rendered_chart = None
    target_country = None
    target_metric = None
    error_feedback = None

    # Safety protection check ensuring active persistence boundaries exist
    if GLOBAL_DATAFRAME is None or GLOBAL_DATAFRAME.empty:
        return "Internal Application Initialization Failure: Missing Dataset File Assets.", 500

    if request.method == 'POST':
        target_country = request.form.get('country')
        target_metric = request.form.get('metric')

        try:
            # Safely generate trend graphs wrapping inputs inside standard exception protections
            rendered_chart = plot_trend(GLOBAL_DATAFRAME, target_country, target_metric)
        except DashboardError as context_exception:
            error_feedback = str(context_exception)

    return render_template(
        'index.html',
        countries=COUNTRIES,
        chart_data=rendered_chart,
        selected_country=target_country,
        selected_metric=target_metric,
        error_message=error_feedback
    )


@app.route('/compare', methods=['GET'])
def compare():
    """Manages structural routing workflows displaying comparative death metrics."""
    if GLOBAL_DATAFRAME is None or GLOBAL_DATAFRAME.empty:
        return "Internal Application Initialization Failure: Missing Dataset File Assets.", 500

    try:
        comparison_chart = plot_compare(GLOBAL_DATAFRAME)
    except Exception as runtime_error:
        return f"An unhandled structural exception occurred: {str(runtime_error)}", 500

    return render_template('compare.html', chart_data=comparison_chart)


if __name__ == '__main__':
    # Execute application engine deployment server run sequence
    app.run(debug=True)