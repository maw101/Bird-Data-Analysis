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

# calculate daily mean speed
next_day = 1
current_day_indices = []
daily_mean_speed = []
for (index, day) in enumerate(elapsed_days_since_start):
    if day < next_day:
        current_day_indices.append(index)
    else:  # calculate the daily mean speed
        daily_mean_speed.append(np.mean(eric_data.speed_2d[current_day_indices]))
        next_day += 1
        current_day_indices = []

plt.figure(figsize=(15, 15))
plt.plot(daily_mean_speed)
plt.title("Eric's Mean Speed Per Day")
plt.xlabel("Day")
plt.ylabel("Mean Speed in m/s")
plt.savefig("outputs/eric_mean_speed.pdf")
plt.show()

# plot data for each of the gulls on a cartographic projection
mercator_projection = ccrs.Mercator()  # specify projection we will be using

plt.figure(figsize=(40, 40))
ax = plt.axes(projection=mercator_projection)
ax.set_extent((-25.0, 20.0, 52.0, 10.0))

## add features to map
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.STATES)

for bird_name in gull_names:
    indices = gull_data['bird_name'] == bird_name
    x, y = gull_data.longitude[indices], gull_data.latitude[indices]
    ax.plot(x, y, '.', transform=ccrs.Geodetic(), label=bird_name, alpha=0.4)

plt.title("Cartographic Projection of All Birds")
plt.legend(loc="upper right")
plt.savefig("outputs/cartographic_map.pdf")
plt.show()

# track all migration patterns

## add date column to dataframe
date_time_data = pd.to_datetime(gull_data.date_time)
gull_data['date'] = date_time_data.dt.date
grouped_gulls = gull_data.groupby('bird_name')
plot_colours = ['#FF0000', '#00FF00', '#0000FF']  # red, green, blue

plt.figure(figsize=(15, 15))
for bird_name, bird_plot_colour in zip(gull_names, plot_colours):
    current_bird = grouped_gulls.get_group(bird_name).groupby('date')
    mean_speed = current_bird.speed_2d.mean()
    mean_speed.plot(label=bird_name, color=bird_plot_colour, alpha=0.7)

plt.title("Migration Patterns of All Birds")
plt.xlabel("Date")
plt.ylabel("Mean Speed in m/s")
plt.legend(loc="upper right")
plt.savefig("outputs/migration_patterns_all_birds.pdf")
plt.show()
