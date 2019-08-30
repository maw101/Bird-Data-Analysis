import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.style.use("seaborn-darkgrid")

gull_data = pd.read_csv("gull_tracking_data.csv")

# gull_data.info()  # look at summary of the file

# plot lat and long of a flight trajectory for a single bird on a standard 2D plot
eric_indices = gull_data.bird_name == "Eric"
x, y = gull_data.longitude[eric_indices], gull_data.latitude[eric_indices]
plt.figure(figsize=(15, 15))
plt.plot(x, y, ".", alpha=0.7)
plt.title("Eric's Trajectory")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.savefig("outputs/eric_trajectory.pdf")  # save figure as a pdf
plt.show()