import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.style.use("seaborn-darkgrid")

gull_data = pd.read_csv("gull_tracking_data.csv")

gull_data.info()  # look at summary of the file