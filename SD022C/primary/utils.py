def return_scores(df,obj1,obj2,obj3,obj4,obj5):
    if ((obj1.get('totalScore_obj')) <= df.iloc[10]['RNO_Row_grade']):
        obj1["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj1["RNO_Modified_standard"] = df.iloc[10]['RNO_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['RNO_Row_grade'] <= (obj1.get('totalScore_obj'))):
                obj1["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj1["RNO_Modified_standard"] = df.iloc[r]['RNO_Modified_standard']
                if (df.iloc[r]['RNO_Row_grade'] == obj2.get('totalScore_obj')):
                    break #condition for 2 rows with same roe grade
    if((obj2.get('correctAnswers')) >= df.iloc[10]['PSD_Raw_grade'] ):
        obj2["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj2["PSD_Modified_standard"] = df.iloc[10]['PSD_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['PSD_Raw_grade'] >= (obj2.get('correctAnswers'))):
                obj2["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj2["PSD_Modified_standard"] = df.iloc[r]['PSD_Modified_standard']
                if (df.iloc[r]['PSD_Raw_grade'] == obj2.get('correctAnswers')):
                    break #condition for 2 rows with same roe grade
    if((obj3.get('totalScore_ltr')) <= df.iloc[10]['RNL_Raw_grade']):
        obj3["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj3["RNL_Modified_standard"] = df.iloc[10]['RNL_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['RNL_Raw_grade'] <= (obj3.get('totalScore_ltr'))):
                obj3["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj3["RNL_Modified_standard"] = df.iloc[r]['RNL_Modified_standard']
                if (df.iloc[r]['RNL_Raw_grade'] == obj3.get('totalScore_ltr')):
                    break #condition for 2 rows with same roe grade
    if((obj4.get('correctAnswers')) >= df.iloc[10]['NWR_Raw_grade'] ):
        obj4["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj4["NWR_Modified_standard"] = df.iloc[10]['NWR_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['NWR_Raw_grade'] >= (obj4.get('correctAnswers'))):
                obj4["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj4["NWR_Modified_standard"] = df.iloc[r]['NWR_Modified_standard']
                if (df.iloc[r]['NWR_Raw_grade'] == obj4.get('correctAnswers')):
                    break #condition for 2 rows with same roe grade
    if((obj5.get('correctAnswers')) >= df.iloc[10]['NWRA_Raw_grade']):
        obj5["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj5["NWRA_Modified_standard"] = df.iloc[10]['NWRA_Modified_standard']
    else:   
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['NWRA_Raw_grade'] >= (obj5.get('correctAnswers'))):
                obj5["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj5["NWRA_Modified_standard"] = df.iloc[r]['NWRA_Modified_standard']
                if (df.iloc[r]['NWRA_Raw_grade'] == obj5.get('correctAnswers')):
                    break #condition for 2 rows with same roe grade  
    return
    
def return_scores_Sec(df,obj1,obj2,obj3,obj4): 
    if ((obj1.get('correctAnswers')) >= df.iloc[10]['PSDS_Raw_grade']):
        obj1["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj1["PSDS_Modified_standard"] = df.iloc[10]['PSDS_Modified_standard']
    else:   
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['PSDS_Raw_grade'] >= (obj1.get('correctAnswers'))):
                obj1["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj1["PSDS_Modified_standard"] = df.iloc[r]['PSDS_Modified_standard']
                if (df.iloc[r]['PSDS_Raw_grade'] == obj1.get('correctAnswers')):
                    break #condition for 2 rows with same roe grade
    if ((obj2.get('totalScore_obj')) <= df.iloc[10]['RNOS_Row_grade']):
        obj2["Percentile_Number"] = df.iloc[10]['Percentile_Number']
        obj2["RNOS_Modified_standard"] = df.iloc[10]['RNOS_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['RNOS_Row_grade'] <= (obj2.get('totalScore_obj'))):
                obj2["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj2["RNOS_Modified_standard"] = df.iloc[r]['RNOS_Modified_standard']
                if (df.iloc[r]['RNOS_Row_grade'] == obj2.get('totalScore_obj')):
                    break #condition for 2 rows with same roe grade
    if((obj3.get('correctAnswers')) >= df.iloc[10]['NWRS_Raw_grade'] ):
            obj3["Percentile_Number"] = df.iloc[10]['Percentile_Number']
            obj3["NWRS_Modified_standard"] = df.iloc[10]['NWRS_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['NWRS_Raw_grade'] >= (obj3.get('correctAnswers'))):
                obj3["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj3["NWRS_Modified_standard"] = df.iloc[r]['NWRS_Modified_standard']
                if (df.iloc[r]['NWRS_Raw_grade'] == obj3.get('correctAnswers')):
                    break #condition for 2 rows with same roe grade
    if((obj4.get('correctAnswers')) >= df.iloc[10]['NWRAS_Raw_grade'] ):
            obj4["Percentile_Number"] = df.iloc[10]['Percentile_Number']
            obj4["NWRAS_Modified_standard"] = df.iloc[10]['NWRAS_Modified_standard']
    else:
        for index, row in df.iterrows():
            r = len(df.index) - index - 1
            if (df.iloc[r]['NWRAS_Raw_grade'] >= (obj4.get('correctAnswers'))):
                obj4["Percentile_Number"] = df.iloc[r]['Percentile_Number']
                obj4["NWRAS_Modified_standard"] = df.iloc[r]['NWRAS_Modified_standard']
                if (df.iloc[r]['NWRAS_Raw_grade'] == obj4.get('correctAnswers')):
                    break #condition for 2 rows with same roe grade
    return