import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

########################################################################################################################
def plot_trajectory(df, subject_name):
    current_subject_indices = df.subject_name == subject_name
    x, y = df.longitude[current_subject_indices], df.latitude[current_subject_indices]

    plt.figure(figsize=(15, 15))

    plt.plot(x, y, ".", alpha=0.7)

    plt.title("{}'s Trajectory".format(subject_name))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.savefig("outputs/{}_trajectory.pdf".format(subject_name.lower())) # save figure as a pdf
    plt.show()

########################################################################################################################
def plot_all_trajectories(df, species_name):
    subject_names = pd.unique(df.subject_name)

    plt.figure(figsize=(15, 15))

    # Add each subjects trajectory to the plot in turn
    for subject_name in subject_names:
        current_subject_indices = df.subject_name == subject_name
        x, y = df.longitude[current_subject_indices], df.latitude[current_subject_indices]
        plt.plot(x, y, ".", label=subject_name, alpha=0.5)

    plt.title("Trajectories of All {}".format(species_name))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend(loc="upper left")

    plt.savefig("outputs/all_{}_trajectories.pdf".format(species_name.lower())) # save figure as a pdf
    plt.show()

########################################################################################################################
def plot_2d_speed_frequency(df, subject_name):
    current_subject_indices = df.subject_name == subject_name

    speed = df.speed_2d[current_subject_indices]
    nan_indices = np.isnan(speed) # ensures we do not process NaN values

    plt.figure(figsize=(15, 15))
    
    plt.hist(speed[~nan_indices], normed=True) # plot normalised histogram of the subjects speed
    
    plt.title("{}'s 2D Speed Frequency".format(subject_name))
    plt.xlabel("2D Speed in m/s")
    plt.ylabel("Speed Frequency")
    
    plt.savefig("outputs/{}_speed_hist.pdf".format(subject_name.lower())) # save figure as a pdf
    plt.show()

########################################################################################################################
def plot_daily_mean_speed(df, subject_name):
    current_subject_indices = df.subject_name == subject_name

    # get amount of time elapsed since data collection began for the given subject
    current_subject_data = df[current_subject_indices]
    current_subject_times = current_subject_data.timestamp

    elapsed_time_since_start = [current_time - current_subject_times[0] for current_time in current_subject_times]
    elapsed_days_since_start = np.array(elapsed_time_since_start) / datetime.timedelta(days=1)

    # calculate daily mean speed
    next_day = 1
    current_day_indices = []
    daily_mean_speed = []
    for index, day in enumerate(elapsed_days_since_start):
        if day < next_day:
            current_day_indices.append(index)
        else:  # calculate the daily mean speed
            daily_mean_speed.append(np.mean(current_subject_data.speed_2d[current_day_indices]))
            next_day += 1
            current_day_indices = []

    plt.figure(figsize=(15, 15))

    plt.plot(daily_mean_speed)
    
    plt.title("{}'s Mean Speed Per Day".format(subject_name))
    plt.xlabel("Day")
    plt.ylabel("Mean Speed in m/s")
    
    plt.savefig("outputs/{}_mean_speed.pdf".format(subject_name.lower()))
    plt.show()

########################################################################################################################
def plot_all_cartographic_projections(df, species_name):
    mercator_projection = ccrs.Mercator()  # specify projection we will be using

    plt.figure(figsize=(40, 40))
    ax = plt.axes(projection=mercator_projection)
    ax.set_extent((-25.0, 20.0, 52.0, 10.0)) # NOTE: Adjust based on data

    # add features to map
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.STATES)

    subject_names = pd.unique(df.subject_name)

    for subject_name in subject_names:
        indices = df['subject_name'] == subject_name
        x, y = df.longitude[indices], df.latitude[indices]
        ax.plot(x, y, '.', transform=ccrs.Geodetic(), label=subject_name, alpha=0.4)

    plt.title("Cartographic Projection of All {}".format(species_name))
    plt.legend(loc="upper right")

    plt.savefig("outputs/cartographic_map.pdf")
    plt.show()

########################################################################################################################
def plot_all_migration_patterns(df, species_name):
    # add date column to dataframe
    date_time_data = pd.to_datetime(df.date_time)
    df['date'] = date_time_data.dt.date
    grouped_subjects = df.groupby('subject_name')
    plot_colours = ['#FF0000', '#00FF00', '#0000FF'] # red, green, blue

    subject_names = pd.unique(df.subject_name)

    plt.figure(figsize=(15, 15))

    for subject_name, subject_plot_colour in zip(subject_names, plot_colours):
        current_subject = grouped_subjects.get_group(subject_name).groupby('date')
        mean_speed = current_subject.speed_2d.mean()
        mean_speed.plot(label=subject_name, color=subject_plot_colour, alpha=0.7)

    plt.title("Migration Patterns of All {}".format(species_name))
    plt.xlabel("Date")
    plt.ylabel("Mean Speed in m/s")
    plt.legend(loc="upper right")

    plt.savefig("outputs/migration_patterns_all_{}.pdf".format(species_name.lower()))
    plt.show()

########################################################################################################################
if __name__ == "__main__":
    plt.style.use("seaborn-darkgrid")

    # Load in and preprocess dataframe
    gull_data = pd.read_csv("gull_tracking_data.csv")

    # get timestamps in a format we can process
    gull_data_timestamps = []
    for row in range(len(gull_data)):
        formatted_date = datetime.datetime.strptime(gull_data.date_time.iloc[row][:-3], "%Y-%m-%d %H:%M:%S") # -3 to exclude the +hours from time diff
        gull_data_timestamps.append(formatted_date)
    
    # create pandas series object from timestamps
    gull_data['timestamp'] = pd.Series(gull_data_timestamps, index=gull_data.index)

    gull_data.rename(columns={'bird_name': 'subject_name'}, inplace=True)

    # gull_data.info()  # look at summary of the file


    # Produce plots
    plot_trajectory(gull_data, "Eric")
    plot_all_trajectories(gull_data, "Birds")

    plot_2d_speed_frequency(gull_data, "Eric")

    plot_daily_mean_speed(gull_data, "Eric")

    plot_all_cartographic_projections(gull_data, "Birds")

    plot_all_migration_patterns(gull_data, "Birds")
