# Demand Forecasting API

This project provides a demand forecasting API using FastAPI and ARIMA model. It allows users to get demand forecasts for a specified number of days and update the data used for training the forecasting model.

## Table of Contents

- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Running the Tests](#running-the-tests)
- [API Documentation](#api-documentation)
  - [GET /v1/inference](#get-v1inference)
  - [POST /v1/update-data](#post-v1update-data)
- [Code Linting and Formatting](#code-linting-and-formatting)
- [License](#license)

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)

### Installation

1. **Clone the repository**:
   ```sh
   https://github.com/chungtit/demand-forecasting-api.git
   cd demand-forecasting
   ```
2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
### Running the Application
1.  **Start the FastAPI server**:
    ```sh
    poetry run hypercorn main:app --reload
    ```
### Running the Tests
1. **Run the tests using pytest**:
    ```sh
    poetry run pytest
    ```
## API Documentation
### GET /v1/inference
- Request Parameters: `days_to_forecast` (query parameter): Number of days to forecast (default is 30).
- Response: 
    - 200 OK: A JSON object containing the forecasted demand for the specified number of days.
    - 500 Internal Server Error: If there is an error in generating the forecast.
- Example:
    ```sh 
    curl -X GET "http://127.0.0.1:8000/v1/inference?days_to_forecast=30"
    ```
### POST /v1/update-data
- Request Body:
    - file (form data): CSV file containing the updated data. The CSV should have columns `slot_start_time` and demand.
- Response:
    - 200 OK: A JSON object with a message indicating that the data was updated and the model was retrained successfully.
    - 500 Internal Server Error: If there is an error in updating the data or retraining the model.
- Example:
    ```sh
    curl -X POST "http://127.0.0.1:8000/v1/update-data" -F "file=@data_training.csv"
    ```
## Code Linting and Formatting
A `.flake8` configuration file is included in the project to maintain code style and quality. The configuration can be found in the root directory.

- To run Flake8, use the following command:
     ```sh
    poetry run flake8
    ```
- The project uses black for code formatting. To format the code, use the following command:
    ```sh
    poetry run black .
    ```
## License
Please do not use it for any commercial purposes, educational purposes are permitted.