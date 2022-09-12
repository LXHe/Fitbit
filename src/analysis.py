from scipy import stats

def ana_correlation(df):
    """
    Correlation analysis on two columns in a dataframe.
    Input:
        df [Dataframe]: with two columns
    Output:
        correlation coefficient and p value
    """
    print('Correlation analysis between {col1} and {col2}:'.format(col1=df.columns[0], col2=df.columns[1]))
    # Shapiro-Wilk normality test
    print('  Normality checking...')
    shapiro_1 = stats.shapiro(df[df.columns[0]])
    shapiro_2 = stats.shapiro(df[df.columns[1]])
    if shapiro_1.pvalue <= 0.05:
        print('    {} data are not normally distributed.'.format(df.columns[0]))
        shapiro_eval_1 = False
    else:
        print('    {} data are normally distributed.'.format(df.columns[0]))
        shapiro_eval_1 = True        
    if shapiro_2.pvalue <= 0.05:
        print('    {} data are not normally distributed.'.format(df.columns[1]))
        shapiro_eval_2 = False
    else:
        print('    {} data are normally distributed.'.format(df.columns[1]))
        shapiro_eval_2 = True 
    # Perform correlation analysis
    if shapiro_1.pvalue > 0.05 and shapiro_2.pvalue > 0.05:
        # For both normally distributed data, Pearson correlation analysis is performed
        print('  Performing Pearson correlation analysis...')
        correlation = stats.pearsonr(df[df.columns[0]], df[df.columns[1]])
    else:
        # Otherwise, Spearman correlation analysis is performed
        print('  Performing Spearman correlation analysis...')
        correlation = stats.spearmanr(df[df.columns[0]], df[df.columns[1]])
    print('    The correlation between {col1} and {col2} is: {coef}'.format(col1=df.columns[0], col2=df.columns[1], coef=correlation[0]))
    print('    The p value of this correlation is: {}'.format(correlation[1]))
    print('='*50)
