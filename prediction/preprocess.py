import pandas as pd

def remove_unnecessary_cols(df, col=None):
    if col is None:
        col = []
    cols = ['name', 'state', 'city', 'risk_category', 'lpgPreference'] + col
    print('Columns to remove:', cols)
    df = df.drop(columns=cols, errors='ignore')
    return df

def binary_cols(df):
    yes_no_columns = ['internetUsed', 'hasLoan', 'cookingTogether', 'hasLand', 'ownsVehicle', 'awareOfGovtScheme', 'pastLoanDefault', 'facedEmergency']
    for col in yes_no_columns:
        df[col] = df[col].map({'yes':1, 'no': 0})
    return df

def oneHotEncoding_cols(df):
    cat_cols = list(df.describe(include='object').columns)
    from sklearn.preprocessing import OneHotEncoder
    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = encoder.fit_transform(df[cat_cols])
    one_hot_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out(cat_cols))
    df = pd.concat([df.drop(cat_cols, axis=1), one_hot_df], axis=1)
    return df

def ordinal_cols(df):
    # Define and apply mapping for lpgRefillFrequency
    lpg_refill_mapping = {
        '<1 month': 1,
        '1-2 months': 2,
        '3-4 months': 4,
        '4-5 months': 5,
        '5-6 months': 6,
        '>2 months': 3
    }

    df['lpgRefillFrequency'] = df['lpgRefillFrequency'].map(lpg_refill_mapping)
    return df

def fix_cylinderPreference(df):
    df['cylinderPreference'] = df['cylinderPreference'].apply(lambda x: float(x.replace('kg','')))
    return df

def monthlyExpense_col(df):
    df.loc[df['foodFuelExpensePercent']=='<25%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='<25%', 'monthlyIncome'].apply(lambda x: (x*0.25)/2)
    df.loc[df['foodFuelExpensePercent']=='0-25%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='0-25%', 'monthlyIncome'].apply(lambda x: (x*0.25)/2)

    df.loc[df['foodFuelExpensePercent']=='26-50%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='26-50%', 'monthlyIncome'].apply(lambda x: (x*0.25+x*0.50)/2)
    df.loc[df['foodFuelExpensePercent']=='25-50%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='25-50%', 'monthlyIncome'].apply(lambda x: (x*0.25+x*0.50)/2)

    df.loc[df['foodFuelExpensePercent']=='51-75%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='51-75%', 'monthlyIncome'].apply(lambda x: (x*0.51+x*0.75)/2)

    df.loc[df['foodFuelExpensePercent']=='76-100%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='76-100%', 'monthlyIncome'].apply(lambda x: (x*0.76+x*1)/2)
    df.loc[df['foodFuelExpensePercent']=='>75%', 'monthlyExpense'] = df.loc[df['foodFuelExpensePercent']=='>75%', 'monthlyIncome'].apply(lambda x: (x*0.76+x*1)/2)
    return df

def process_data(df):
    df = fix_cylinderPreference(df)
    df = remove_unnecessary_cols(df)
    df = binary_cols(df)
    df = ordinal_cols(df)
    df = oneHotEncoding_cols(df)
    return df

def Standardization(df, col=None):
    if col is None:
        col = []
    cols = ['monthlyIncome', 'dataPackExpense', 'savings', 'score']
    print('Columns to Normalize:', cols)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(df[cols])
    scaled_df = scaler.transform(df[cols])
    scaled_df = pd.DataFrame(scaled_df, columns=cols)
    for i in cols:
        df[i] = scaled_df[i]

    return df

