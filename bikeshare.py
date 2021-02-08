import time
import pandas as pd
from collections import Counter

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Use a while loop to handle invalid inputs and get user input for city (chicago, new york city, washington)
    while True:
        try:
            city = input(
                '\nWould you like to see data for Chicago, New York city, or Washington?\n').lower()
            if city in CITY_DATA:
                break
            raise ValueError
        except ValueError:
            print('{} This entry is not valid! Please try agin.'.format(city))

    #  Use a while loop to handle invalid inputs and get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input(
                '\nWhich month ? January, February, March, April, May, June, or "all" to apply no month filter?\n').lower()
            month_list = ['january', 'february',
                          'march', 'april', 'may', 'june', 'all']
            if month in month_list:
                break
            raise ValueError
        except ValueError:
            print('{} This entry is not valid! Please try agin.'.format(month))

    # Use a while loop to handle invalid inputs and get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input(
                '\nWhich day ? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all" to apply no day filter?\n').lower()
            day_list = ['monday', 'tuesday', 'wednesday',
                        'thursday', 'friday', 'saturday', 'sunday', 'all']
            if day in day_list:
                break
            raise ValueError
        except ValueError:
            print('{} This entry is not valid! Please try agin.'.format(day))

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
    # load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('What is the most Popular month for traveling?\n', popular_month)

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nWhat is the most Popular day for traveling?\n', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nWhat is the most Popular hour for traveling?\n', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    c = Counter(df['Start Station'])
    Station_name = c.most_common(1)[0][0]
    Station_count = c.most_common(1)[0][1]
    print('What is most commonly used start station?')
    print(Station_name, ', count:', Station_count)

    # Display most commonly used end station
    c = Counter(df['End Station'])
    Station_name = c.most_common(1)[0][0]
    Station_count = c.most_common(1)[0][1]
    print('\nWhat is most commonly used end station?')
    print(Station_name, ', count:', Station_count)

    # Display most frequent combination of start station and end station trip
    trip = (df['Start Station'] + '   ' + df['End Station'])
    c = Counter(trip)
    Stations_names = c.most_common(1)[0][0]
    Stations_count = c.most_common(1)[0][1]
    print('\nWhat is the most commonly trip from start to end?')
    print('|Start Station' + '              ' + '|End Station')
    print(Stations_names, ',  count:', Stations_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['Trip Duration'].sum()
    convrt_sec = time.strftime("%H:%M:%S", time.gmtime(total_duration))
    print('What is the total traveling duration?\n')
    print('The total is {} hour.'.format(convrt_sec))

    # Display mean travel time
    avg_duration = df['Trip Duration'].mean()
    convrt_sec2 = time.strftime("%H:%M:%S", time.gmtime(avg_duration))
    print('\nWhat is the average traveling duration?\n')
    print('The average is {} hour.'.format(convrt_sec2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("What is the breakdown of users?")
    print(user_types)

    # Check for NaN values and replace it if exist, Using the forward filling method
    if df.isnull().values.any():
        df.fillna(method='ffill', axis=0, inplace=True)

    # Display counts of gender if applicable
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('\nWhat is the breakdown of gender?')
        print(gender_count)
    else:
        print('\nWhat is the breakdown of gender?\n',
              'Ther is no gender data to calculat')

    # Display earliest, most recent, and most common year of birth if applicable
    if 'Birth Year' in df:
        early_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('\nWhat is the Earliest, Most recent, and Most Common year of birth?')
        print("Early year: {} \nRecent year: {} \nMost commonearly year: {} ".format(
            early_year, recent_year, most_common))
    else:
        print('\nWhat is the Earliest, Most recent, and Most Common year of birth?\n',
              'Ther is no birth year data to calculat')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data - print 5 rows each time- upon user answer."""
    # Displays 5 rows from raw data,it will continue prompting and printing until the user chooses 'no'
    strt = 0
    raw_data = input(
        '\nWould you like to see the raw data? Enter yes or no.\n').lower()
    while raw_data == 'yes':
        five_row = df.iloc[strt: strt+5]
        print(five_row)
        strt += 5
        raw_data = input(
            '\nWould you like to see moer of the raw data? Enter yes or no.\n').lower()
        if raw_data != 'yes':
            break


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
