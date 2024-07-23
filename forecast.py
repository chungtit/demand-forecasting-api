import io
import pandas as pd

from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from statsmodels.tsa.arima.model import ARIMA


class DemandForecastingAPI:
    """
    A class to represent the demand forecasting API.
    """

    def __init__(self):
        self.model = None
        self.data = None

    async def load_model_and_data(self):
        """
        Load and preprocess the data, and train the ARIMA model.
        """
        data_path = "data/data_training.csv"
        self.data = pd.read_csv(data_path)
        self.data["slot_start_time"] = pd.to_datetime(self.data["slot_start_time"])
        self.data.set_index("slot_start_time", inplace=True)
        daily_data = self.data["demand"].resample("D").sum()

        train_size = int(len(daily_data) * 0.8)
        train = daily_data[:train_size]
        self.model = ARIMA(train, order=(5, 1, 0)).fit()

    def get_forecast(self, days_to_forecast: int = 30):
        """
        Get demand forecast for a specified number of days.

        Args:
            days_to_forecast    : Number of days to forecast
        Return: 
            Forecasted demand for the specified number of days
        """
        try:
            forecast = self.model.forecast(steps=days_to_forecast)
            return forecast.to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_data(self, file: UploadFile):
        """
        Update the data used for training the forecasting model and retrain the model.

        Args:
            file    : CSV file containing the updated data
        Return: 
            Success message
        """
        try:
            contents = file.file.read()
            self.data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
            self.data["slot_start_time"] = pd.to_datetime(self.data["slot_start_time"])
            self.data.set_index("slot_start_time", inplace=True)
            daily_data = self.data["demand"].resample("D").sum()

            train_size = int(len(daily_data) * 0.8)
            train = daily_data[:train_size]
            self.model = ARIMA(train, order=(5, 1, 0)).fit()
            return {"message": "Data updated and model retrained successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


app = FastAPI()
api = DemandForecastingAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await api.load_model_and_data()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/v1/inference")
def get_forecast(days_to_forecast: int = 30):
    """
    Endpoint to get demand forecast for a specified number of days

    Args:
        days_to_forecast    : Number of days to forecast, default is 30
    Return: 
        Forecasted demand for the specified number of days
    """
    return api.get_forecast(days_to_forecast)


@app.post("/v1/update-data")
def update_data(file: UploadFile = File(...)):
    """
    Endpoint to update the data used for training the forecasting model and retrain the model

    Args:
        file    : CSV file containing the updated data
    Return: 
        Success message
    """
    return api.update_data(file)
