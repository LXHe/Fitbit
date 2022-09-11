def lifestyle_feedback(df, id_list):
    """
    Give personalised lifestyle feedback.
    Input:
        df [Dataframe]: input dataframe, need to contain any of these columns: ['HealthyStep', 'HealthySleep', 'HealthyActivity']
        id_list [list]: Target users
    Output:
        Lifestyle feedback on available parameters.
    """
    for i in id_list:
        print('='*40)
        print('Now providing lifestyle feedback for {}:'.format(i))

        # Feedback for daily steps
        # This will return a series of boolean values, need to use .any() or .all() for evaluation
        if (df[df['Id']==i]['HealthyStep']==1).all():
            print('  For daily steps:')
            print('    Daily step target has been reached.')
        elif (df[df['Id']==i]['HealthyStep']==0).all():
            print('  For daily steps:')
            print('    Daily step target is not reached.')
        else:
            print('  For daily steps:')
            print('    No available data')
        
        # Feedback for daily sleep
        if (df[df['Id']==i]['HealthySleep']==1).all():
            print('  For daily sleep:')
            print('    Daily sleep time has been reached.')
        elif (df[df['Id']==i]['HealthySleep']==0).all():
            print('  For daily sleep:')
            print('    Daily sleep time is not reached.')
        else:
            print('  For daily sleep:')
            print('    No available data')

        # Feedback for weekly activity
        if (df[df['Id']==i]['HealthyActivity']==1).all():
            print('  For weekly activity:')
            print('    Weekly activity time has been reached.')
        elif (df[df['Id']==i]['HealthyActivity']==0).all():
            print('  For weekly activity:')
            print('    Weekly activity time is not reached.')
        else:
            print('  For weekly activity:')
            print('    No available data')

        print('='*40)

