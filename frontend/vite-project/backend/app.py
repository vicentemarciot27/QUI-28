from flask import Flask, request, jsonify
from flask_cors import CORS

from logica.Entregando_perifericos import *
from logica.Processando_dados import *
import traceback

app = Flask(__name__)
CORS(app)  # Handle CORS


@app.route("/submit_param", methods=["POST"])
def submit():
    data = request.json
    variables_data = data["variables"]
    parameters = []

    for variable in variables_data:
        param = Parameter(
            name=variable["name"],
            unit=variable["unit"],
            is_integer=False,  # Assuming all are float for now. Modify as needed.
            center=float(variable["value"]),
            lower_limit=float(variable["minValue"]),
            upper_limit=float(variable["maxValue"]),
            delta=float(variable["delta"]),
        )
        parameters.append(param)

    # Extract has_integer value
    has_integer = data.get("has_integer", False)

    # Create a FatorialPlan using has_integer, parameters and alpha
    fatorial_plan = FatorialPlan(
        parameters_list=parameters,
        alpha=float(data["alpha"]),
        has_integer=has_integer
    )

    # Check for fatorial plan errors
    plan_errors = fatorial_plan_test(fatorial_plan)
    if plan_errors:
        return jsonify({"errors": plan_errors}), 400

    # Retrieve the plan
    plan = fatorial_plan.return_plan()

    # Convert the plan (DataFrame) to JSON and send it back
    return plan.to_json(orient="split")

@app.route("/submit_quadratic_model", methods=["POST"])
def submit_quadratic_model():
    try:
        # 1. Parse the data from the request
        request_data = request.get_json()
        columns = request_data['data_frame']['columns']
        data = request_data['data_frame']['data']

        # Convert the data_frame from a dictionary to a pandas DataFrame
        df = pd.DataFrame(data, columns=columns)
        df["Resposta"] = df['Resposta'].astype(float)
        
        # Reset the index of the DataFrame
        df.reset_index(drop=True, inplace=True)

        # 2. Create an instance of the QuadraticModel class
        model = QuadraticModel(df)

        # 3. Generate the quadratic plot
        plot_base64 = model.quadratic_plot()

        # 4. Return the plot as a base64 encoded string in a JSON response
        return jsonify({"plot": plot_base64})

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()})


if __name__ == "__main__":
    app.run(debug=True)
