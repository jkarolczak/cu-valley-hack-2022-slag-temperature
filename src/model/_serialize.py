import os
import pickle
from datetime import datetime


def serialize(regressor: object, name: str, directory: str = "../models") -> None:
    os.makedirs(directory, exist_ok=True)
    time = str(datetime.now()).replace(' ', '-')
    file_name = os.path.join(directory, f"{time}-{name}.pkl")
    with open(file_name, "wb") as fp:
        pickle.dump(regressor, fp)
