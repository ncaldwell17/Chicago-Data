df = pd.read_excel('chicago_mayor_runoff_2023_election_results.xlsx', header=None)
df = df.drop(0, axis=0)  # drop meaningless first row

# Create a new dataframe
df2 = pd.DataFrame()

# Iterate over the rows of the original dataframe
ward_number = 0
for index, row in df.iterrows():
    try:
        if type(row[0]) == int:
            new_row = pd.Series({'Ward': ward_number, 
                                 'Precinct': row[0], 
                                 'Votes': row[1], 
                                 'Brandon Johnson': row[2], 
                                 'Paul Vallas': row[4]})
            # Add the new row to the new dataframe
            df2 = df2.append(new_row, ignore_index=True)
            continue
        
        elif pd.isnull(row[0]) is False:  # blank row between ward results
            if "Ward" in row[0]:  # Check if the current row starts with the word "Ward"
                ward_number = row[0][5:] # Get the ward number

            elif "Precinct" in row[0]:
                pass
        
    except TypeError:
        raise TypeError(index-1)
    except IndexError:
        raise IndexError(index-1)
        
df2.to_excel('chicago_mayor_runoff_2023_election_results_corrected.xlsx')
