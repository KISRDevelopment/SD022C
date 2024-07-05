def return_scores(df,obj1,obj2,obj3,obj4,obj5):
    for index, row in df.iterrows():
        r = len(df.index) - index - 1
        if (df.iloc[r]['RNO_Row_grade'] <= (obj1.get('totalScore_obj'))):
            obj1["Percentile_Number"] = df.iloc[r]['Percentile_Number']
            obj1["RNO_Modified_standard"] = df.iloc[r]['RNO_Modified_standard']
            if (df.iloc[r]['RNO_Row_grade'] == obj2.get('totalScore_obj')):
                break #condition for 2 rows with same roe grade
    for index, row in df.iterrows():
        r = len(df.index) - index - 1
        if (df.iloc[r]['PSD_Raw_grade'] >= (obj2.get('correctAnswers'))):
            obj2["Percentile_Number"] = df.iloc[r]['Percentile_Number']
            obj2["PSD_Modified_standard"] = df.iloc[r]['PSD_Modified_standard']
            if (df.iloc[r]['PSD_Raw_grade'] == obj2.get('correctAnswers')):
                break #condition for 2 rows with same roe grade
    for index, row in df.iterrows():
        r = len(df.index) - index - 1
        if (df.iloc[r]['RNL_Raw_grade'] <= (obj3.get('totalScore_ltr'))):
            obj3["Percentile_Number"] = df.iloc[r]['Percentile_Number']
            obj3["RNL_Modified_standard"] = df.iloc[r]['RNL_Modified_standard']
            if (df.iloc[r]['RNL_Raw_grade'] == obj3.get('totalScore_ltr')):
                break #condition for 2 rows with same roe grade
    for index, row in df.iterrows():
        r = len(df.index) - index - 1
        if (df.iloc[r]['NWR_Raw_grade'] >= (obj4.get('correctAnswers'))):
            obj4["Percentile_Number"] = df.iloc[r]['Percentile_Number']
            obj4["NWR_Modified_standard"] = df.iloc[r]['NWR_Modified_standard']
            if (df.iloc[r]['NWR_Raw_grade'] == obj4.get('correctAnswers')):
                break #condition for 2 rows with same roe grade
    for index, row in df.iterrows():
        r = len(df.index) - index - 1
        if (df.iloc[r]['NWRA_Raw_grade'] >= (obj5.get('correctAnswers'))):
            obj5["Percentile_Number"] = df.iloc[r]['Percentile_Number']
            obj5["NWRA_Modified_standard"] = df.iloc[r]['NWRA_Modified_standard']
            if (df.iloc[r]['NWRA_Raw_grade'] == obj5.get('correctAnswers')):
                break #condition for 2 rows with same roe grade
    return