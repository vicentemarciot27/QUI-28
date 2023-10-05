from flask import Flask, request, jsonify
from flask_cors import CORS

from logica.Entregando_perifericos import *

app = Flask(__name__)
CORS(app)  # Handle CORS


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    # Extract the list of variables from the received data
    variables_data = data["variables"]

    # Create Parameter instances for each variable
    parameters = []
    for variable in variables_data:
        param = Parameter(
            name=variable["name"],
            unit=variable["unit"],
            is_integer=False,  # Assuming all are float for now. Modify as needed.
            center=float(variable["center"]),
            lower_limit=float(variable["minValue"]),
            upper_limit=float(variable["maxValue"]),
            delta=float(variable["delta"]),
        )
        parameters.append(param)

    # Create a FatorialPlan using the parameters and alpha value
    alpha = float(data["alpha"])
    fatorial_plan = FatorialPlan(
        parameters_list=parameters, alpha=alpha, has_integer=False
    )  # Assuming no integers for now. Modify as needed.

    # Retrieve the plan
    plan = fatorial_plan.return_plan()

    # Convert the plan (DataFrame) to JSON and send it back
    return plan.to_json(orient="split")


if __name__ == "__main__":
    app.run(debug=True)
