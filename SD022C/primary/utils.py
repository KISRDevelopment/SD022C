def return_scores(request):
    for index, row in request.iterrows():
        print (row['RNO_Row_grade'], row['RNO_Modified_standard'])
    return