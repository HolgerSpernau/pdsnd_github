import time
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
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input('Please enter a city to analyze (Chicago, New Yor City, Washington): ')).lower()
        # checking, if the correct selection is entered
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print('Wrong entry. Please enter the name of the cities.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('Enter a month to filter for (all, january, february, ... , june): ')).lower()
        # checking, if the correct selection is entered
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            break
        else:
            print('Wrong entry. Please enter the name of a month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('Enter a day to filter for (all, monday, tuesday, ... sunday): ')).lower()
        # checking, if the correct selection is entered
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            break
        else:
            print('Wrong entry. Please enter the name of a day.')
            
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name
    df['day'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: ', df['month'].mode()[0])

    # display the most common day of week
    print('The most common day of the week is: ', df['day'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Start to End Station'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most frequent combination of start station and end station trip: ', df['Start to End Station'].mode()[0])

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # display total travel time
    print('Total travel time: ', df['Travel Time'].sum())

    # display mean travel time
    print('Mean travel time: ', df['Travel Time'].mean())

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('Counts of user types:')
        print(df['User Type'].value_counts())
    else:
        print('\nNo user tpye data collected.\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of gender:')
        print(df['Gender'].value_counts())
    else:
        print('\nNo gender data collected.\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth: ', int(df['Birth Year'].min()))
        print('\nMost recent year of birth: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth: ', int(df['Birth Year'].mode()[0]))
    else:
        print('\nNo birth year collected.\n')

    print("\nThis took %s seconds." % round((time.time() - start_time), 2))
    print('-'*40)


def raw_data(df):
    """Displays the raw data, if user enters 'y' or doesn't display, if user enters 'n'"""

    counter = 0

    while True:
        show_data = str(input('\nWould you like to see the raw data (yes/no)?\n')).lower()
        if show_data in ('yes'):
            print(df[:][counter:counter+5])
            counter += 5
        elif show_data in ('no'):
            break
        else:
            print('Wrong entry.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()