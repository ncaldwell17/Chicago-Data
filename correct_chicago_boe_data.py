import re

def remove_middle_name(name):
    # define a regular expression to match middle names or nicknames
    pattern = r'\s+["(].*?[)"]|\s+[A-Z]\.'

    # replace all matches with a single space
    new_name = re.sub(pattern, '', name)

    return new_name.strip()

def create_candidate_map(series: pd.core.series.Series) -> dict:
    _dict = {}
    for c in range(len(series)):
        entity = series[c]
        if entity in ["Precinct", "Votes", "%"]:
            pass
        else:
            _dict[remove_middle_name(entity.title().rstrip())] = c
    return _dict

def reformat_chicago_boe_data(results: pd.DataFrame) -> pd.DataFrame:
    
    index = results.index[df.iloc[:,0]=="Ward 1"].tolist()[0]
    results = results.drop(range(index), axis=0)
    
    df2 = pd.DataFrame()
    ward_number = 0
    candidate_map = None
    for index, row in results.iterrows():

        if pd.isnull(row[0]):  # there's a blank row of NaNs between ward results
            pass


        elif type(row[0]) != int:
            if "Ward" in row[0]:
                ward_number = row[0][5:]  # the ward number is always the fifth element and above

            elif "Precinct" in row[0]:
                if candidate_map:
                    pass
                else:
                    candidate_map = create_candidate_map(row)

        else:
            new_row = pd.Series({
                'Ward': ward_number,
                'Precinct': row[0],
                'Votes': row[1],
                **{name: row[num] for name, num in candidate_map.items()}
            })
            df2 = df2.append(new_row, ignore_index=True)
            cols = ['Ward', 'Precinct'] + list(candidate_map.keys()) + ['Votes']
            df2 = df2.reindex(columns=cols)

            df2["Ward"] = df2["Ward"].astype(np.int64)
            df2[list(df2.columns[1:])] = df2[list(df2.columns[1:])].astype(int)

    return df2
