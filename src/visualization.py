import matplotlib.pyplot as plt

def pct_pie_chart(data, list_names, title=None, save=None):
    """
    Pie chart (in percentage) given data and list name.
    Input:
        data [list]: A list of raw count
        list_names [list]: A list of labels in correspondent to data
        title [String]: Specify the title of the chart
        save [String]: Specify the path to save the chart
    Output:
        pie chart
    """

    # Plot pie chart, need to mention 'labels=' because the 2nd argument is explode
    plt.pie(data, labels=list_names, autopct='%.0f%%')
    if title:
        plt.title('{}'.format(title))
    if save:
        plt.savefig('{}'.format(save))
    plt.show()
	
def usage_bar_chart(df, Id, title=None, save=None):
	"""
	Bar chart of fitness device usage by Id.
	Input:
        df [DataFrame]: Input dataframe with columns of 'Id', 'ActivityDate' and 'TotalActivityMinutes'
        Id [Int]: Target Id
        title [String]: Specify the title of the chart
        save [String]: Specify the path to save the chart
	Output:
        bar chart
    """
	df_selected = df[df['Id']==Id][['ActivityDate', 'TotalActivityMinutes']]
	df_selected['ActivityDate'] = df_selected['ActivityDate'].dt.date
	fig, ax = plt.subplots(nrows=1, ncols=1)
	df_selected.plot.bar(x='ActivityDate', y='TotalActivityMinutes', ax=ax, legend=False)
	plt.xlabel('')

	if title:
		plt.title('{}'.format(title))
	if save:
		plt.savefig('{}'.format(save))
	plt.show()