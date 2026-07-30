import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from create_charts import generate_exploration_charts

df = pd.read_csv("hicsp.csv")
df.shape
df.info()
df.describe()
df.head()

generate_exploration_charts(df)