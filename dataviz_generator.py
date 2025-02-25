# Importing pandas and matplotlib
import pandas as pd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# plot user defined function
def get_plot(function):
    if function == 'b':
        ol = input('Include outliers [y/n]: ')
        if ol == 'n':
            boxplot_generator(measurements_df, outliers=False);
        elif ol == 'y':
            boxplot_generator(measurements_df);
        else:
            print('ERROR:incorrect input \'{}\' - please re-run script.'.format(ol))
    elif function == 'l':
        ol = input('Include outliers [y/n]: ')
        if ol == 'n':
            lineplot_generator(measurements_df, outliers=False);
        elif ol == 'y':
            lineplot_generator(measurements_df);
        else:
            print('ERROR:incorrect input \'{}\' - please re-run script.'.format(ol))
    else:
        print('ERROR:incorrect input \'{}\' - please re-run script.'.format(function))

    return None

# add dataframe column 'day' to represent the number of days since start of treatment
# return final day of treatment for filesaving
def add_days_column(dframe):
    start_date = datetime.strptime(dframe.loc[0,'date'], "%m/%d/%y") # datetime object for start of treatment
    final_date = datetime.strptime(dframe.iloc[-1,0], "%m/%d/%y").strftime('%d%b%Y') # datetime object for start of treatment
    for i in measurements_df.index:
        timedelta = int((datetime.strptime(dframe.loc[i,'date'], "%m/%d/%y") - start_date).days)
        dframe.loc[i, 'day'] = timedelta

    return final_date

# define a function that generates boxplot to compare `Test` vs `Control` group
def boxplot_generator(dframe, outliers=True): # input dframe(DataFrame), outlier(boolean)
    
    if outliers == False:
        i = int(input('Enter maximum value (area_mm^2): '))
        dframe = dframe[dframe['area_mm^2'] <= i]
    
    ax = sns.catplot(data=dframe, kind='box', x='day', y='area_mm^2', hue='type', native_scale=True)
       
    if outliers == True:
        plt.xlabel('Days from Start of Treatment')
        plt.ylabel('Area (mm^2)')
        plt.title('Test vs Control with Outliers')
        plt.savefig('{} boxplot with outliers.png'.format(last_day), dpi=300, bbox_inches='tight')
    else:
        plt.xlabel('Days from Start of Treatment')
        plt.ylabel('Area (mm^2)')
        plt.title('Test vs Control w/o Outliers greater than {}'.format(i))
        plt.savefig('{} boxplot without outliers greater than {}'.format(last_day, i), dpi=300, bbox_inches='tight')
    
    return None

# define a function that generates boxplot to compare `Test` vs `Control` group
def lineplot_generator(dframe, outliers=True): # input dframe(DataFrame), outlier(boolean)
    
    if outliers == False:
        i = int(input('Enter maximum value (area_mm^2): '))
        dframe = dframe[dframe['area_mm^2'] <= i]
    
    ax = sns.lineplot(data=dframe, x='day', y='area_mm^2', hue='type')
    
    if outliers == True:
        plt.xlabel('Days from Start of Treatment')
        plt.ylabel('Area (mm^2)')
        plt.title('Test vs Control with Outliers')
        plt.savefig('{} lineplot with outliers.png'.format(last_day), dpi=300, bbox_inches='tight')
    else:
        plt.xlabel('Days from Start of Treatment')
        plt.ylabel('Area (mm^2)')
        plt.title('Test vs Control w/o Outliers greater than {}'.format(i))
        plt.savefig('{} lineplot without outliers greater than {}'.format(last_day, i), dpi=300, bbox_inches='tight')
    
    return None
    
# Read in data collection CSV as a DataFrame and mutate
unfiltered_measurements_df = pd.read_csv(input('Enter filepath for .csv file: '))
measurements_df = unfiltered_measurements_df[pd.isna(unfiltered_measurements_df['date']) == False] # remove last NaN row
last_day = add_days_column(measurements_df);

# get user defined function call and test plot script
get_plot(input('Enter key-sensitive plot generation (boxplot or lineplot) [b/l]: '));
