import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # User input for city (chicago, new york city, washington).
    cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in cities:
            break
        else:
            print('Incorrect city name. Try again')

    # User input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        month = input('Would you to see data by month or for all the months? Type month name (month range from January to June) or type all:\n').lower()
        if month in months:
            break
        else:
            print('Incorrect input. Try again')

    # User input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        day = input('Would you to see data by day of the week or for all days of the week? Type day name or type all:\n').lower()
        if day in days:
            break
        else:
            print('Incorrect input. Try again')

    print('-'*40)
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

    # Loading data file into a df
    df = pd.read_csv(CITY_DATA[city])

    # Converting Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from Start Time into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # Month filter
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # Day filter
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displaying the most common month
    common_month = calendar.month_name[df['month'].mode()[0]]
    # Note: I used the following link to determine how to change month int into month name:
    # https://stackoverflow.com/questions/6557553/get-month-name-from-number
    print('Most common month: ', common_month)

    # Displaying the count of the most common month
    common_month_int = df['month'].mode()[0]
    common_month_count = df['month'].value_counts()[common_month_int]
    print(' (Count: ', common_month_count,')')

    # Displaying the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nMost common day of the week: ', common_day)

    # Displaying the count of the most common day of week
    common_day_count = df['day_of_week'].value_counts()[common_day]
    print(' (Count: ', common_day_count,')')

    # Displaying the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nMost common start hour: ', common_hour)

    # Displaying the count of the most common start hour
    common_hour_count = df['hour'].value_counts()[common_hour]
    print(' (Count: ', common_hour_count,')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displaying most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start station: ', common_start)

    # Displaying the count of the most commonly used start station
    common_start_count = df['Start Station'].value_counts()[common_start]
    print(' (Count: ', common_start_count,')')

    # Displaying most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nMost common end station: ', common_end)

    # Displaying the count of the most commonly end station
    common_end_count = df['End Station'].value_counts()[common_end]
    print(' (Count: ', common_end_count,')')

    # Displaying most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' to ' + df['End Station']
    # Note: I used the following link to determine how to concatenate dataframe columns of str type:
    # https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-pandas-dataframe
    common_route = df['route'].mode()[0]
    print('\nMost common route: ', common_route)

    # Displaying the count of the most frequent route taken
    common_route_count = df['route'].value_counts()[common_route]
    print(' (Count: ', common_route_count,')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displaying total travel time
    total_seconds = df['Trip Duration'].sum()
    total_days = total_seconds // 86400
    total_hours = (total_seconds - (total_days * 86400)) // 3600
    total_minutes = (total_seconds - (total_days * 86400) - (total_hours * 3600)) // 60
    print('Total travel time: ', int(total_days), 'Days ', int(total_hours), 'Hours ', int(total_minutes), 'Minutes\n')


    # Displaying mean travel time
    avg_seconds = df['Trip Duration'].mean()
    avg_days = avg_seconds // 86400
    avg_hours = (avg_seconds - (avg_days * 86400)) // 3600
    avg_minutes = (avg_seconds - (avg_days * 86400) - (avg_hours * 3600)) // 60
    print('Average travel time: ', int(avg_days), 'Days ', int(avg_hours), 'Hours ', int(avg_minutes), 'Minutes\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    user_type_count = df['User Type'].value_counts()
    print('User type counts:')
    print(user_type_count)

    # Displaying counts of gender
    if 'Gender' not in df.columns:
        # Note I used the following link to determine how to check if a column is in a dataframe:
        # https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas
        print("\nGender column/statistics not available in Washington dataset.")
    else:
        gender_count = df['Gender'].value_counts()
        print('\nGender counts:')
        print(gender_count)

    # Displaying earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("\nBirth Year column/statistics not available in Washington dataset.")
    else:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year: ', int(earliest_birth_year))

        recent_birth_year = df['Birth Year'].max()
        print('\nMost recent birth year: ', int(recent_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]
        print('\nMost common birth year: ', int(common_birth_year))

        # Displaying the count of the most common year of birth
        common_birth_year_count = df['Birth Year'].value_counts()[common_birth_year]
        print(' (Count: ', common_birth_year_count,')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_print(df):
    """
    Asks user if they want to see 5 lines of raw filtered data at a time.

    Displays:
    5 lines of df at a time.
    """
    # Enabliing pandas to display all the columns (Note this was a suggestion from one of the reviewers)
    pd.set_option('display.max_columns',200)

    row_index = 0
    while True:
        answer = input('Would you like to see 5 lines of the data?\n').lower()
        if answer == 'no':
            break
        elif answer == 'yes':
            print(df.iloc[row_index:row_index+5])
            # Note: I used the following link to determine how iterate through rows using row indexing:
            # https://stackoverflow.com/questions/46380075/pandas-select-n-middle-rows
            row_index += 5
        else:
            print('Incorrect input. Try again')
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_print(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
