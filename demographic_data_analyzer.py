import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
   #  df.info()
    # How many of each race are represented in this dataset? 
    # This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()
    #race_count = df.groupby('race').size().reset_index(name='count').sort_values(by='count', ascending=False).set_index('race')
  
    # What is the average age of men?
    mean_age = df.groupby('sex')['age'].mean()
    average_age_men = mean_age['Male'].round(1)

    # What is the percentage of people who have a Bachelor's degree?
    count_bachelor = df['education'].eq('Bachelors').sum() # boolean
    percent_ba = (count_bachelor / len(df)) * 100
    percentage_bachelors = round(percent_ba, 1)
    # or 
    # percentage_bachelors = (df["education"] == "Bachelors").mean() * 100


    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # 1. get the number of people with higher education
    higher = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    # 2. define rich
    rich = df['salary'].eq('>50K') # return true/false
    # 3. get the number of people with higher education and >50K
    count_higher_rich = df[higher & rich].shape[0]

    # 4. calculate the percentage 
    higher_education_rich = round((count_higher_rich/ df[higher].shape[0])*100, 1)



    # What percentage of people without advanced education make more than 50K?
    # 1. get the number of people with non-higher education
    non_higher = ~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    # 2. get the number of people with non-higher education and >50K and calculate the %
    lower_education_rich = round((df[non_higher & rich].shape[0]/ df[non_higher].shape[0])*100, 1)


    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    #1. get the number of people who work the minimum number of hours
    count_min = (df['hours-per-week'] == min_work_hours).sum() #use sum() because it's booleans
    #2. get the number of popele who work the minimum number of hours and rich
    count_min_rich = (df['hours-per-week']== min_work_hours & rich).sum()
    # or return the rows and use shape() to count the number of rows
    # count_min_rich = df[df['hours-per-week']== min_work_hours & rich].shape()
    #2. get the percentage 
    rich_percentage = round(count_min_rich / count_min * 100,1)

    # What country has the highest percentage of people that earn >50K?

    # 1. get the number of people with salary >50K by country
    rich_count = df[rich].groupby('native-country').size().reset_index(name = 'rich_count')
    total_count = df.groupby('native-country').size().reset_index(name = 'total_count')
    # 2. merge two tables using native-country as key
    merged_country = pd.merge(rich_count, total_count, on = 'native-country', how='inner')
    merged_country['rich_percent'] = merged_country['rich_count']/merged_country['total_count'] *100

    highest_earning_country = merged_country.sort_values(by='rich_percent', ascending=False).iloc[0,0]
    highest_earning_country_percentage = merged_country.sort_values(by='rich_percent', ascending=False).iloc[0,-1].round(1)


    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['native-country'] == 'India') & rich]['occupation'].value_counts().index[0]
    # alternative 
 # rich_india = df[(df['native-country'] == 'India') & rich]
  #pop_occupation =rich_india.groupby('occupation').size().reset_index(name ='count').sort_values(by = 'count', ascending=False)
 # top_IN_occupation = pop_occupation.iloc[0,0]
 

  # DO NOT MODIFY BELOW THIS LINE

    if print_data:
      print("Number of each race:\n", race_count)
      print("Average age of men:", average_age_men)
      print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
      print(
          f"Percentage with higher education that earn >50K: {higher_education_rich}%"
      )
      print(
          f"Percentage without higher education that earn >50K: {lower_education_rich}%"
      )
      print(f"Min work time: {min_work_hours} hours/week")
      print(
          f"Percentage of rich among those who work fewest hours: {rich_percentage}%"
      )
      print("Country with highest percentage of rich:", highest_earning_country)
      print(
          f"Highest percentage of rich people in country: {highest_earning_country_percentage}%"
      )
      print("Top occupations in India:", top_IN_occupation)

    return {
      'race_count': race_count,
      'average_age_men': average_age_men,
      'percentage_bachelors': percentage_bachelors,
      'higher_education_rich': higher_education_rich,
      'lower_education_rich': lower_education_rich,
      'min_work_hours': min_work_hours,
      'rich_percentage': rich_percentage,
      'highest_earning_country': highest_earning_country,
      'highest_earning_country_percentage': highest_earning_country_percentage,
      'top_IN_occupation': top_IN_occupation
    }
