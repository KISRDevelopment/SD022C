def return_scores(df,obj1,obj2,obj3,obj4,obj5):
    for index, row in df.iterrows():
        if (row['RNO_Row_grade'] >= (obj1.get('totalScore_obj'))):
            obj1["Percentile_Number"] = row['Percentile_Number']
            obj1["RNO_Modified_standard"] = row['RNO_Modified_standard']
        if (row['PSD_Raw_grade'] <= (obj2.get('correctAnswers'))):
            obj2["Percentile_Number"] = row['Percentile_Number']
            obj2["PSD_Modified_standard"] = row['PSD_Modified_standard']    
        if (row['RNL_Raw_grade'] >= (obj3.get('totalScore_ltr'))):
            obj3["Percentile_Number"] = row['Percentile_Number']
            obj3["RNL_Modified_standard"] = row['RNL_Modified_standard'] 
        if (row['NWR_Raw_grade'] <= (obj4.get('correctAnswers'))):
            obj4["Percentile_Number"] = row['Percentile_Number']
            obj4["NWR_Modified_standard"] = row['NWR_Modified_standard']  
        if (row['NWRA_Raw_grade'] <= (obj5.get('correctAnswers'))):
            obj5["Percentile_Number"] = row['Percentile_Number']
            obj5["NWRA_Modified_standard"] = row['NWRA_Modified_standard'] 
    return