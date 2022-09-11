from src import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import activity dataset
df_activity = pd.read_csv('.\data\dailyActivity_merged.csv', parse_dates=['ActivityDate']).drop_duplicates() # No duplicates
# Import sleep dataset
df_sleep = pd.read_csv('.\data\sleepDay_merged.csv', parse_dates=['SleepDay']).drop_duplicates() # 3 duplicates


##########################
#### Data Exploration ####
##########################
#### Check data reliability
# Combine activity and sleep data
df_activity_sleep = pd.merge(df_activity[['Id','ActivityDate','TotalSteps','VeryActiveMinutes','FairlyActiveMinutes','LightlyActiveMinutes','SedentaryMinutes','Calories']],
							   df_sleep[['Id','SleepDay','TotalMinutesAsleep','TotalTimeInBed']],
							   left_on=['Id','ActivityDate'], right_on=['Id','SleepDay'], how='left')
# Take a peek as the data of activity time
df_activity_sleep['TotalActivityMinutes'] = df_activity_sleep['VeryActiveMinutes']+df_activity_sleep['FairlyActiveMinutes']+df_activity_sleep['LightlyActiveMinutes']+df_activity_sleep['SedentaryMinutes']+df_activity_sleep['TotalTimeInBed']
# Impute missing values in 'TotalTimeInBed' by 0
df_activity_sleep['TotalTimeInBed'].fillna(0, inplace=True)
df_activity_sleep['TotalSedentaryMinutes'] = df_activity_sleep['SedentaryMinutes']+df_activity_sleep['TotalTimeInBed']
df_activity_sleep['TotalActivityMinutes'] = df_activity_sleep['VeryActiveMinutes']+df_activity_sleep['FairlyActiveMinutes']+df_activity_sleep['LightlyActiveMinutes']+df_activity_sleep['TotalSedentaryMinutes']
# Count of total activity time that is above 1440
sum(df_activity_sleep['TotalActivityMinutes'] > 1440) # 155
# Drop unreasonable records
df_activity_sleep.drop(df_activity_sleep.index[df_activity_sleep['TotalActivityMinutes'] > 1440], inplace=True)
print('{} users contribute to the activity-sleep data.'.format(df_activity_sleep['Id'].nunique()))
print('The timespan ranges from {s_date} to {e_date}'.format(s_date=df_activity_sleep['ActivityDate'].min().date(), e_date=df_activity_sleep['ActivityDate'].max().date()))


##############################
#### Lifestyle Evaluation ####
##############################
#### User contribution
print('{} users contribute to the activity data.'.format(df_activity['Id'].nunique())) # 33
print('{} users contribute to the sleep data.'.format(df_sleep['Id'].nunique())) # 24

#### Evaluation on lifestyle: Daily step, daily sleep and weekly activity
# Daily step
df_daily_step = description.mean_value_by_id(df_activity, ['TotalSteps'])
df_daily_step['TotalSteps'] = df_daily_step['TotalSteps'].round().astype(int)
# Daily sleep
df_daily_sleep = description.mean_value_by_id(df_sleep, ['TotalMinutesAsleep'])
# Weekly activity
# Dataframe by Id and week
df_weekly_activity_full = description.sum_value_by_week(df_activity, date_col_name='ActivityDate', sum_col=['VeryActiveMinutes', 'FairlyActiveMinutes'])
# Id by avg of weeks
df_weekly_activity = description.mean_value_by_id(df_weekly_activity_full, ['VeryActiveMinutes', 'FairlyActiveMinutes'])

#### Distribution of users by recommended lifestyle
## Evaluate daily step: recommended value is 8000 steps/day
df_daily_step['HealthyStep'] = np.where(df_daily_step['TotalSteps'] >= 8000, 1, 0)
eval_step_data = [df_daily_step['HealthyStep'].sum(), len(df_daily_step)-df_daily_step['HealthyStep'].sum()]
eval_step_list = ['Daily step >= 8000', 'Daily step < 8000']
visualization.pct_pie_chart(eval_step_data, eval_step_list, title='User distribution by daily step', save='./results/pie_daily_step.png')

## Evaluate daily sleep time: recommended value is 7 hrs/day (420 mins/day) 
df_daily_sleep['HealthySleep'] = np.where(df_daily_sleep['TotalMinutesAsleep'] >= 420, 1, 0)
eval_sleep_data = [df_daily_sleep['HealthySleep'].sum(), len(df_daily_sleep)-df_daily_sleep['HealthySleep'].sum()]
eval_sleep_list = ['Daily sleep >= 420 mins', 'Daily sleep < 420 mins']
visualization.pct_pie_chart(eval_sleep_data, eval_sleep_list, title='User distribution by daily sleep', save='./results/pie_daily_sleep.png')

## Evaluate weekly activity time: recommended value is VeryActive >= 75 mins/wk or FairlyActive >= 150 mins/wk
df_weekly_activity['HealthyActivity'] = np.where((df_weekly_activity['VeryActiveMinutes'] >= 75) | (df_weekly_activity['FairlyActiveMinutes'] >= 150) , 1, 0)
eval_activity_data = [df_weekly_activity['HealthyActivity'].sum(), len(df_weekly_activity)-df_weekly_activity['HealthyActivity'].sum()]
eval_activity_list = ['Moderate >= 150 mins or\nVigorous >= 75 mins', 'Moderate < 150 mins or\nVigorous < 75 mins']
visualization.pct_pie_chart(eval_activity_data, eval_activity_list, title='User distribution by weekly activity', save='./results/pie_weekly_activity.png')

## For personalised feedback, call lifestyle_feedback() function in ./src/feedback.py
## Should use merged dataframe:
#merged_df = df_daily_step.merge(df_daily_sleep, on='Id', how='outer')
#merged_df = merged_df.merge(df_weekly_activity, on='Id', how='outer')
#merged_df.reset_index(inplace=True)
#feedback.lifestyle_feedback(merged_df, [1624580081, 1644430081])


####################
#### User Habit ####
####################
## Dataset used in this part is the filtered set: df_activity_sleep
# It is recommended to use UserDescription.pbix for an interactive visualisation
# Or you can call the usage_bar_chart() function in ./src/visualization.py
#visualization.usage_bar_chart(df_activity_sleep, 1503960366)
df_activity_sleep['FullyRecorded'] = np.where(df_activity_sleep['TotalActivityMinutes']>=1392, 1, 0)
# Summarise target metrics
df_habit = df_activity_sleep.groupby('Id').agg({'ActivityDate':'count', 'TotalSteps':'mean', 'Calories':'mean', 'FullyRecorded':'sum', 'TotalActivityMinutes':'mean'})
df_habit['PctFullyRecorded'] = df_habit['FullyRecorded'] / df_habit['ActivityDate']
# Take a peek at the correlations using scatter matrix
pd.plotting.scatter_matrix(df_habit, hist_kwds={'edgecolor':'black'}, figsize=(15,15))
plt.savefig('./results/userhabit_scatter_matrix.png')
plt.show()

# Correlation analysis
analysis.ana_correlation(df_habit[['ActivityDate', 'TotalSteps']].dropna())
analysis.ana_correlation(df_habit[['ActivityDate', 'Calories']].dropna())
analysis.ana_correlation(df_habit[['TotalActivityMinutes', 'TotalSteps']].dropna())
analysis.ana_correlation(df_habit[['TotalActivityMinutes', 'Calories']].dropna())
analysis.ana_correlation(df_habit[['PctFullyRecorded', 'TotalSteps']].dropna())
analysis.ana_correlation(df_habit[['PctFullyRecorded', 'Calories']].dropna())


#####################################
#### Activity and Sleep Analysis ####
#####################################
## Dataset used in this part is the filtered set: df_activity_sleep
# Take a peek at the correlations using scatter matrix
pd.plotting.scatter_matrix(
    df_activity_sleep[['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes', 'TotalSteps', 'TotalMinutesAsleep']], 
    hist_kwds={'edgecolor':'black'},
    figsize=(15,15))
plt.savefig('./results/association_scatter_matrix.png')
plt.show()

# Correlation analysis
analysis.ana_correlation(df_activity_sleep[['VeryActiveMinutes', 'TotalMinutesAsleep']].dropna())
analysis.ana_correlation(df_activity_sleep[['FairlyActiveMinutes', 'TotalMinutesAsleep']].dropna())
analysis.ana_correlation(df_activity_sleep[['LightlyActiveMinutes', 'TotalMinutesAsleep']].dropna())
analysis.ana_correlation(df_activity_sleep[['SedentaryMinutes', 'TotalMinutesAsleep']].dropna())
analysis.ana_correlation(df_activity_sleep[['TotalSteps', 'TotalMinutesAsleep']].dropna())