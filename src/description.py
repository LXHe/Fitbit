import pandas as pd

def mean_value_by_id(df, col):
	"""
    Calculate mean values of specified columns over time by Id.
    Input:
        df [Dataframe]: Input dataframe, should have column 'Id' 
        col [list]: Target columns
    Output:
        df_mean [Dataframe]: Dataframe with mean value of target columns group by Id.
	"""

	print('Processing mean value by id...')
	df_mean = df.groupby('Id')[col].mean()
	print('Completed: info of {count} users have been processed.'.format(count=df['Id'].nunique()))	
	
	return df_mean

def sum_value_by_week(df, date_col_name, sum_col):
	"""
    Sum values of specified columns by week (7d) and Id.
    Input:
        df [Dataframe]: Input dataframe, should have column 'Id'
        date_col_name [String]: Datetime column based on which we want to sum over, the column should be in format datetime64[ns]
        sum_col [list]: Target columns
    Output:
        final_df [Dataframe]: Dataframe with summed values of target columns over week by Id.
    """

	print('Processing summed value by id and week...')
	
	# Extract Id
	id_list = df['Id'].unique()
	# Create a dataframe container
	final_df = pd.DataFrame()
	for i in id_list:
		select_df = df[df['Id']==i]
		# Skip user if the records are less than a week
		if len(select_df) < 7:
			print('Skip user:{} for lacking records of a full week'.format(i))
			pass
		else:
			# Extract only complete records in a week
			k = len(select_df) // 7
			sum_val_df = select_df.iloc[:k*7,:].resample('7d', on=date_col_name)[sum_col].sum().reset_index()
			sum_val_df['Id'] = i
			final_df = final_df.append(sum_val_df)
	print('Completed:')
	print('    info of {drop_num} users have been dropped.'.format(drop_num=len(id_list)-final_df['Id'].nunique()))
	print('    info of {complete_num} users have been processed.'.format(complete_num=final_df['Id'].nunique()))
	
	return final_df