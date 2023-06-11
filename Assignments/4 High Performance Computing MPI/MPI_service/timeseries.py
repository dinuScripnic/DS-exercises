import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression



def create_time_series(n: int, t: int) -> list[pd.Series]:
    """
    Creates n time series of length t

    Args:
        n (int): number of time series
        t (int): days of time series

    Returns:
        list[pd.Series]: list of time series
    """
    
    return [pd.Series(np.random.randn(t)) for _ in range(n)]


def linear_fit(ts: pd.Series) -> LinearRegression():
    """
    Fits a linear model to the time series

    Args:
        ts (pd.Series): the time series

    Returns:
        LinearRegression(): the fitted model
    """
    
    return LinearRegression().fit(ts.index.__array__().reshape(-1, 1), ts.values)


def predict_value(model:LinearRegression, x: int) -> float:
    """
    Predicts the value of the time series at time x

    Args:
        model (LinearRegression): model to predict
        x (int): time

    Returns:
        float: predicted value
    """
    
    return model.predict(np.array(x).reshape(-1,1))


if __name__ == '__main__':
    # for testing
    ts = create_time_series(100,300)
    models = [linear_fit(t) for t in ts]
    predicts = [predict_value(m, 301)[0] for m in models]