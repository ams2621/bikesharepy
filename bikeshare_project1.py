import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    invalid_input = "Please enter a valid input.Otherwise get lost"

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user raw_input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            "\nEnter the name of the city to examine city names are as follows\nchicago,\nnew york,\nwashington. \n").lower()
        if city in ['chicago', 'new york', 'washington']:
            break
        else:
            print(invalid_input)

    # TO DO: get user raw_input for month (all, january, february, ... , june)
    while True:
        month = input("\nEnter the name of the month\njanuary,\nfebruary,\nmarch,"
                      "\napril,\nmay,\njune\nto filter by, or \"all\" to apply no month filter\n").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print(invalid_input)

    # TO DO: get user raw_input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nEnter the name of the day\nmonday,\ntuesday,\nwednesday,\nthursday,"
                    "\nfriday,\nsaturday,\nsunday\nof week to filter by, or \"all\" to apply no day filter\n").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print(invalid_input)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]
    print("Accessing data from: " + file_name)
    df = pd.read_csv(file_name)

    # convert the Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(arg=df['Start Time'], format='%Y-%m-%d %H:%M:%S')

    # filter by month if relevant
    if month != 'all':
        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month

        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filtering by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filtering by day of week if appropriate
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n Calculating the Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert the Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(arg=df['Start Time'], format='%Y-%m-%d %H:%M:%S')

    # Creating new columns for month, weekday, hour
    month = df['Start Time'].dt.month
    weekday_name = df['Start Time'].dt.weekday_name
    hour = df['Start Time'].dt.hour

    # TO DO: display the most common month
    most_common_months = month.mode()[0]
    print('Most common month is : ', most_common_months)

    # TO DO: display the most common day of week
    most_common_day_of_weeks = weekday_name.mode()[0]
    print('Most common day of week is : ', most_common_day_of_weeks)

    # TO DO: display the most common start hour
    common_start_hours = hour.mode()[0]
    print('Most frequent start hour is: ', common_start_hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most commonly used start station is :', df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('Most commonly used end station is :', df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    combine_station1 = df['Start Station'] + "*" + df['End Station']
    common_stations = combine_station1.value_counts().idxmax()
    print('Most frequent used combinations are:\n{} \nto\n{}'.format(common_stations.split('*')[0],
                                                                     common_stations.split('*')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Converting seconds to readable time
    def secs_to_readable_time(seconds):
        m1, s1 = divmod(seconds, 60)
        h1, m1 = divmod(m1, 60)
        d1, h1 = divmod(h1, 24)
        y1, d1 = divmod(d1, 365)
        print('Years: {}, Days: {}, Hours: {}, Mins: {}, Secs: {}'.format(y1, d1, h1, m1, s1))

    # TO DO: display total travel time
    total_travel_times = df['Trip Duration'].sum()
    print('Total travel time:\n')
    secs_to_readable_time(total_travel_times)

    # TO DO: display mean travel time
    mean_travels_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(mean_travels_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_years = df['Birth Year'].min()
        most_recent_birth_years = df['Birth Year'].max()
        common_birth_years = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: " + str(earliest_birth_years))
        print("\nMost recent year of birth: " + str(most_recent_birth_years))
        print("\nMost common year of birth: " + str(common_birth_years))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raws_data1(df):
    user_inputs = input('Are you interested in raw data? Enter yes or no.\n')
    line_numbers = 0

    while 1 == 1:
        if user_inputs.lower() != 'no':
            print(df.iloc[line_numbers: line_numbers + 5])
            line_numbers += 5
            user_inputs = input('\nDo you want to see more raw data? Enter yes or no.\n')
        else:
            break

# origin : All the function will be called through this function
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raws_data1(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
