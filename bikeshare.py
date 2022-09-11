import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': './data_files/chicago.csv',
              'new york city': './data_files/new_york_city.csv',
              'washington': './data_files/washington.csv' }

# list out the input checking by lower
valid_city = ['chicago', 'new york city', 'washington']
valid_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
valid_days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data! \n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Enter a city need to be queried: ')).lower()
            # if((city != 'chicago') and (city != 'new york city') and (city != 'washington')):
            if(city not in valid_city):
                print('Input an invalid city, please re-input \n')
                continue
            else:
                break 
        except ValueError:
            print('That is not valid value for city name  \n')
        except UnboundLocalError:
            print('Something wrong during input data, please try again \n')
        except KeyboardInterrupt:
            print('No input taken \n')
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Enter a month need to be queried: ').lower()
            if(month not in valid_months):
                print('Input an invalid month, please re-input \n')
                continue
            else:
                break 
        except ValueError:
            print('That is not valid value for month \n')
        except UnboundLocalError:
            print('Something wrong during input data, please try again \n')
        except KeyboardInterrupt:
            print('No input taken \n')
            break
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
       try:
            day = input('Enter a day in week need to be queried: ').lower()
            if(day not in valid_days):
                print('Input an invalid day, please re-input \n')
                continue
            else:
                break 
       except ValueError:
           print('That is not valid value for day \n')
       except UnboundLocalError:
            print('Something wrong during input data, please try again \n')
       except KeyboardInterrupt:
           print('No input taken \n')
           break    

    print('>>> Loading........................')
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # print("to see column 'Start Time' after convert \n",df['Start Time'])
    # print()

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

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
    """Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    MostMonth = df['month'].mode().unique()
    MostMonthLet = valid_months[MostMonth[0]]
    print("The most common month is: {} - {}\n ".format(MostMonth, MostMonthLet))

    # display the most common day of week
    MostDayoWeek = df['month'].mode().unique()
    MostDoWLet = valid_days[MostDayoWeek[0]]
    print("The most common dayofweek in month {} is: {} - {} \n".format(MostMonthLet, MostDayoWeek, MostDoWLet))

    # display the most common start hour
    df['start_hours'] = df['Start Time'].dt.hour
    most_com_str_hour = df['start_hours'].mode().unique()
    print("The most common start hour in {} at {}: {} \n".format(MostMonthLet, MostDoWLet, most_com_str_hour))

    print("\n This took %s seconds." % (time.time() - start_time))
    print('==<+>=='*15)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    MostStrStation = df['Start Station'].mode()
    MostStrStation_c = df['Start Station'].value_counts()
    print("\nThe most Popular Start Station: {}, Count: {}".format(MostStrStation.iloc[0], MostStrStation_c.iloc[0]))

    # display most commonly used end station
    MostEndStation = df['End Station'].mode()
    MostEndStation_count = df['End Station'].value_counts()
    print("The most Popular End Station: {}, Count: {}".format(MostEndStation.iloc[0], MostEndStation_count.iloc[0]))

    # display the most commonly combined Start and End Station
    MostCombineStation = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)

    # print("to check type of MostCombineStation : \n", type(MostCombineStation))
    print("The most Popular Combined Station: \n {} \n Count {}".format(MostCombineStation.head(1), MostCombineStation[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('>'*120)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    TotalTimeTravel = df['Trip Duration'].sum()
    TotalTimeConvert = time.strftime("%H:%M:%S", time.gmtime(TotalTimeTravel))
    print("To see TotalTimeTravel in H:M:S is \n", TotalTimeConvert)

    # display mean travel time
    AverTimeTravel = df['Trip Duration'].mean()
    AverTimeConvert = time.strftime("%H:%M:%S", time.gmtime(AverTimeTravel))
    print("To see AverageTimeTravel in H:M:S is \n", AverTimeConvert)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('>>>'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    NumberUserType = df.groupby(['User Type']).size()
    print("Number of each User Type \n", NumberUserType)

    # Display counts of gender
    if ('Gender' in list(df)):
        NumberGender = df.groupby(['Gender']).size()
        print("Number of Gender \n", NumberGender)
    else:
        print("!!!!")
        print("Gender is not exist in this data \n")

    # Display earliest, most recent, and most common year of birth
    # Drop out all NaN Birth Year prior to filtering
    if (0 != df.isnull().sum().sum()):
        dfBYearDropNaN = df.dropna(axis=0)
        MostBirthYear = dfBYearDropNaN['Birth Year'].mode().unique()
        print("The most common Birth Year: ", MostBirthYear)

        Youngest = dfBYearDropNaN['Birth Year'].sort_values(axis=0, ascending=True)
        # print("The Youngest type \n", type(Youngest))
        print("The Oldest User Birth Year: ", Youngest.iloc[0])
        print("The Youngest User Birth Year: ", Youngest.iloc[-1])
    else:
        if ('Birth Year' in list(df)):
            MostBirthYear = df['Birth Year'].mode().unique()
            print("The most common Birth Year: ", MostBirthYear)

            Youngest = df['Birth Year'].sort_values(axis=0, ascending=True)
            print("The Oldest User Birth Year: ", Youngest.iloc[0])
            print("The Youngest User Birth Year: ", Youngest.iloc[-1])
        else:
            print("!!!!")
            print("Birth Year is not exist in this data \n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('==<+>=='*15)

def main():
    """ Main function to interfacing with User.
    """
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        print("==<+>=="*15)
        print('to see existing df:  \n', df.head())
        print('to see list of column in df \n', list(df))

        # to handling NaN
        print("to see NaN for each column \n", df.isnull().sum().sum())

        if (0 != df.isnull().sum().sum()):
            print(">>> to see NaN-cloumn status \n", df.isnull().sum())
            print()
            # df['Birth Year'].fillna(value=1900,axis=0, inplace=True)
            df['User Type'].fillna(value='Unknown',axis=0, inplace=True)
            df['Gender'].fillna(value='Unknown',axis=0, inplace=True)

            print(">>> NaN-cloumn status after handling User Type and Gender \n", df.isnull().sum())
            print()
        print("==<+>=="*15)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        count = 1
        while True:
            restart = input('\nWould you like to see more 5 lines raw table. Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
            else:
                print("to check df after load data \n", df.head(5*count))
                count += 1

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
