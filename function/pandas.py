import pandas as pd
import numpy as np


def create_dataframe(data: list[list], columns: list["str"]):
    df = pd.DataFrame(np.array(data), columns=columns)
    return df
