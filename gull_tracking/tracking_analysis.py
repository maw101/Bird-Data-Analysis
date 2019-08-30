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

# plot multiple birds
gull_names = pd.unique(gull_data.bird_name)  # extract names of the gulls
plt.figure(figsize=(15, 15))
for bird_name in gull_names:
    bird_indices = gull_data.bird_name == bird_name
    x, y = gull_data.longitude[bird_indices], gull_data.latitude[bird_indices]
    plt.plot(x, y, ".", label=bird_name, alpha=0.5)
plt.title("Trajectories of All Birds")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(loc="upper left")
plt.savefig("outputs/three_trajectories.pdf")  # save figure as a pdf
plt.show()

# speed of eric
eric_indices = gull_data.bird_name == "Eric"
speed = gull_data.speed_2d[eric_indices]
nan_indices = np.isnan(speed)  # ensures we do not process NaN values
plt.figure(figsize=(15, 15))
plt.hist(speed[~nan_indices], bins=np.linspace(0, 30, 20), normed=True)  # plot normalised histogram of Eric's Speed
plt.title("Eric's 2D Speed Frequency")
plt.xlabel("2D Speed in m/s")
plt.ylabel("Speed Frequency")
plt.savefig("outputs/eric_speed_hist.pdf")  # save figure as a pdf
plt.show()

# get timestamps in a format we can process
gull_data_timestamps = []
for row in range(len(gull_data)):
    formatted_date = datetime.datetime.strptime(gull_data.date_time.iloc[row][:-3], "%Y-%m-%d %H:%M:%S")  # -3 to exclude the +hours from time diff
    gull_data_timestamps.append(formatted_date)

# create pandas series object from timestamps
gull_data['timestamp'] = pd.Series(gull_data_timestamps, index=gull_data.index)

# get amount of time elapsed since data collection began for Eric
eric_data = gull_data[eric_indices]
eric_times = eric_data.timestamp

elapsed_time_since_start = [current_time - eric_times[0] for current_time in eric_times]
elapsed_days_since_start = np.array(elapsed_time_since_start) / datetime.timedelta(days=1)
