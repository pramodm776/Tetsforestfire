# Forest Fire Prediction

A Flask web application that predicts the **Fire Weather Index (FWI)** from environmental and fire-weather measurements. The application loads a trained Ridge regression model and a fitted `StandardScaler`, accepts values through a browser form, and displays the predicted FWI.

## Features

- Flask web interface for entering fire-weather measurements.
- Ridge regression model for FWI prediction.
- Standardized input preprocessing using a saved scikit-learn scaler.
- Responsive prediction form for desktop and mobile screens.
- AWS Elastic Beanstalk WSGI configuration.
- Jupyter notebooks for exploratory data analysis, feature engineering, and model training.

## Project Structure

```text
Dployinng/
├── application.py                         # Flask application and prediction route
├── reuirement.txt                          # Python dependencies
├── README.md                               # Project documentation
├── models/
│   ├── ridge.pkl                           # Trained Ridge regression model
│   └── scaler.pkl                          # Fitted feature scaler
├── templates/
│   ├── index.html                          # Landing page
│   └── home.html                           # Prediction form and result page
├── nodebook/
│   ├── 2.0-EDA And FE Algerian Forest Fires.ipynb
│   ├── 3.0-Model Training.ipynb
│   └── Algerian_forest_fires_dataset_UPDATE.csv
└── .ebextensions/
    └── python.config                       # Elastic Beanstalk WSGI configuration
```

> Note: `reuirement.txt` is the dependency file currently used by this project. The conventional filename is `requirements.txt`; either rename the file or use the filename shown in the commands below.

## How the Application Works

1. Flask starts the application defined by `application` in `application.py`.
2. The Ridge model is loaded from `models/ridge.pkl`.
3. The fitted scaler is loaded from `models/scaler.pkl`.
4. A user submits nine numeric feature values through the form at `/predictdata`.
5. The values are scaled using the saved scaler.
6. The scaled values are passed to the Ridge model.
7. The predicted FWI value is rendered on the result page.

The model and scaler must be loaded from the same training workflow. Replacing one without the other can produce invalid predictions because the model expects the same feature order and preprocessing used during training.

## Requirements

- Python 3.8 or newer
- pip
- The files in the `models/` directory
- Flask, NumPy, pandas, and scikit-learn

## Installation

Open PowerShell in the project directory:

```powershell
cd "C:\Users\Pramod\Desktop\Machine Learning\regressionProject\Dployinng"
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r reuirement.txt
```

If the dependency file is renamed to `requirements.txt`, use:

```powershell
python -m pip install -r requirements.txt
```

## Run Locally

Start the Flask application:

```powershell
python application.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000/
```

The application runs with Flask debug mode enabled by the `app.run(debug=True)` statement. Debug mode is useful during development, but it should be disabled for production deployments.

## Prediction Inputs

Enter numeric values in this order. The order must match the order used to train the model.

| # | Field | Meaning |
|---:|---|---|
| 1 | `Temperature` | Temperature measurement |
| 2 | `RH` | Relative humidity |
| 3 | `Ws` | Wind speed |
| 4 | `Rain` | Rainfall measurement |
| 5 | `FFMC` | Fine Fuel Moisture Code |
| 6 | `DMC` | Duff Moisture Code |
| 7 | `ISI` | Initial Spread Index |
| 8 | `Classes` | Encoded fire-weather class feature |
| 9 | `Region` | Encoded region feature |

The current form submits all fields as text, and `application.py` converts each submitted value to a floating-point number. Use numeric values only.

## Routes

### `GET /`

Displays the landing page from `templates/index.html`.

### `GET /predictdata`

Displays the prediction form from `templates/home.html`.

### `POST /predictdata`

Reads the nine form fields, scales them, generates an FWI prediction, and displays the result in `templates/home.html`.

This project currently provides an HTML form workflow. It does not expose a JSON prediction API.

## Model Files

The application expects these files to exist before it starts:

```text
models/ridge.pkl
models/scaler.pkl
```

They are loaded with Python pickle. Only load model files that are trusted, because untrusted pickle files can execute arbitrary code when deserialized.

If the model is retrained, preserve all of the following:

- The same nine feature columns.
- The same feature order.
- The same preprocessing and scaling behavior.
- Compatible versions of Python, scikit-learn, and related libraries.
- Updated `ridge.pkl` and `scaler.pkl` files together.

## Notebook Workflow

The `nodebook/` directory contains the source data and training notebooks:

1. `2.0-EDA And FE Algerian Forest Fires.ipynb` is used for exploratory data analysis and feature engineering.
2. `3.0-Model Training.ipynb` is used to train the regression model and create the serialized model artifacts.
3. `Algerian_forest_fires_dataset_UPDATE.csv` contains the Algerian forest fire dataset used by the notebooks.

Run the notebooks in order when reproducing the training workflow. Confirm that the generated model and scaler use the same feature order consumed by the Flask application.

## AWS Elastic Beanstalk Deployment

The file `.ebextensions/python.config` configures Elastic Beanstalk to use:

```text
application:application
```

This means Elastic Beanstalk imports the `application` Flask object from `application.py`.

### Using the Elastic Beanstalk CLI

Install and configure the AWS Elastic Beanstalk CLI, then run these commands from the project directory:

```powershell
eb init
 eb create forest-fire-prediction-env
 eb deploy
 eb open
```

Remove the leading space before `eb create` if copying the command directly:

```powershell
eb create forest-fire-prediction-env
```

Before deploying, verify that the project includes:

- `application.py`
- `reuirement.txt` or a correctly named `requirements.txt`
- `models/ridge.pkl`
- `models/scaler.pkl`
- `templates/index.html`
- `templates/home.html`
- `.ebextensions/python.config`

For production, disable Flask debug mode and use a production WSGI server or the hosting platform's recommended Python configuration.

## Troubleshooting

### `FileNotFoundError` for a model file

Run the application from the project root and confirm that both files exist under `models/`:

```powershell
Get-ChildItem .\models
```

### `ModuleNotFoundError`

Activate the virtual environment and reinstall dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r reuirement.txt
```

### Prediction errors or unexpected values

Check that:

- All nine inputs are numeric.
- Inputs are entered in the documented order.
- `ridge.pkl` and `scaler.pkl` were produced from the same training run.
- The installed scikit-learn version is compatible with the serialized artifacts.

### PowerShell does not allow activation scripts

Run PowerShell with an appropriate execution policy for the current user, then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Development Notes

- The Flask application object is available as both `application` and `app`.
- The Elastic Beanstalk configuration uses `application:application`.
- Form conversion errors are currently not handled with custom validation, so invalid or missing numeric values can result in a server error.
- The current landing page is intentionally minimal; the prediction workflow is available at `/predictdata`.

## License

No license file is currently included in this repository. Add a license before distributing the project publicly.
