import pandas as pd
import numpy as np
import os

from config import *

# number of check function = number of column
# each function will not check where if the value is blank, that will be done using isBlank column later


def checkCampaignCode(value: str) -> bool:
    return False if value is np.NaN else not(value.startswith("C") and len(value) <= 10)


def checkCellCode(value: str) -> bool:
    return False if value is np.NaN else not(value.startswith("A") and len(value) <= 10)


def checkTreatmentCode(value: str) -> bool:
    # in the docx file this is be 9, but most of the data is 8 OR 7 - Check again with Lucas
    return False if value is np.NaN else len(value) > 9


def checkTelephone_No(value: str) -> bool:
    return False if value is np.NaN else len(value) != 10


def checkNotificationLanguage(value: str) -> bool:
    return False if value is np.NaN else value not in LANGUAGUE_LIST


def checkCustomerProvince(value: str) -> bool:
    return False if value is np.NaN else value not in PROVINCE_LIST


def checkBrand(value: str) -> bool:
    return False if value is np.NaN else (value not in BRAND_LIST or len(value) > 5)

# function to explain the error with boolean flag True from which column


def explainErrorCode(columnName: str) -> str:
    if columnName.startswith('isBlank'):
        return '{} value is blank'.format(columnName[7:])
    elif columnName.startswith('check'):
        return '{} value is incorrect'.format(columnName[5:])
    else:
        return None


def getDataQuality(filepath: str, filename: str) -> pd.DataFrame:
    """
    getDataQuality function
    input: filepath, filename
    output: pd.DataFrame with correct format -> output to one excel sheet
    """

    # read file into DataFrame df
    df = pd.read_csv(os.path.join(filepath, filename), dtype=str)

    # check the schema

    if set(COLUMN_LIST) != set(df.columns):
        # if the schema is different -> get out of the function
        return None
    NUMBER_OF_COLUMN = len(COLUMN_LIST)

    """
    At this point, we can loop through rows and output the error in each row
    However, it will be slow if bigger data set
    -> I choose to embrace Pandas vectorization calculation (close to C's speed)
    After than, I can filter out rows with error then iterate through those smaller set of data
    """

    # for each column, return 2 boolean columns for blank and format check
    for col in COLUMN_LIST:
        df['isBlank' + col] = pd.isna(df[col])
        df['check' + col] = df[col].apply(globals()['check' + col])
    # Count number of error of each row
    df['countError'] = df.iloc[:,
                               NUMBER_OF_COLUMN: NUMBER_OF_COLUMN*3].sum(axis=1)
    # get the original index, we will need that to output
    df['original_index'] = df.index

    # filter rows with error only into error_df
    error_df = df[df['countError'] > 0]

    # add the first row of output depends on number of rows on error_df
    s = '{} row read'.format(df.shape[0])
    s += ' with the following errors:' if error_df.shape[0] else ', file contains no errors'
    output = []
    output.append(s)

    # loop through the error_df
    # use index instead of df.iterrows for better performance
    if error_df.shape[0]:
        new_columns = error_df.columns
        for idx in range(0, error_df.shape[0], 1):
            for i in range(NUMBER_OF_COLUMN, NUMBER_OF_COLUMN*3, 1):
                if error_df.iloc[idx, i]:
                    # 3*NUMBER_OF_COLUMN +1 will return the last column added to df, original_index. +1 to original_index because Python start at row 0
                    output.append('Row {}: {}'.format(error_df.iloc[idx, 3*NUMBER_OF_COLUMN + 1]+1,
                                                      explainErrorCode(new_columns[i])))

    return(pd.DataFrame(output))
