import os
import pandas as pd


if __name__=="__main__":

    column_names = ['name', 'start_time', 'end_time', 'cadence', '#']
    au = 149598000
    file_name = 'EUV_26082022'
    # file_name = 'LYA_26082022'
    
    input_file = os.path.join(os.getcwd(), 'data', file_name+'.txt')
    output_file = os.path.join(os.getcwd(), 'data', file_name+'.csv')

    to_sun_file = os.path.join(os.getcwd(), 'data', 'ToSun.csv')
    
    df = pd.read_csv(
        input_file, 
        sep=' ',
        header=None,
        names=column_names,
    )
    df_start_time = df['start_time'].str[:8].to_frame()
    
    dfToSun = pd.read_csv(to_sun_file, sep = ',')
    dfToSun['Date'] = dfToSun['Date'].replace("-", "", regex=True)

    df_start_time = pd.merge(
        df_start_time, 
        dfToSun, 
        left_on='start_time', 
        right_on='Date', 
        how='left',
    )

    df = pd.concat(
        [
            df.drop(
                column_names[-1], 
                axis=1, 
                inplace=False,
            ), 
            df_start_time['ToSun'], 
            df[column_names[-1]],
        ], 
        axis=1,
    )

    df['ToSun'] = (df['ToSun']/au).map(lambda x: '{0: .2f}'.format(x))
    df.to_csv(output_file, index=False)

    