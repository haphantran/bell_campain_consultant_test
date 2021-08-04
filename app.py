import argparse

import os
import sys

import pandas as pd
from helper import getDataQuality

# Create the parser
my_parser = argparse.ArgumentParser(
    description='Read all csv inputs in path and output the quality of data',
    allow_abbrev=False)

# Add required positional argument
my_parser.add_argument('inputPath',
                       metavar='inputPath',
                       type=str,
                       help='the path to input files')

# Add optional arguments
my_parser.add_argument('-p',
                       '--path',
                       metavar='outputPath',
                       type=str,
                       help='the path to output the data quality report, default to current folder',
                       default='./'
                       )
my_parser.add_argument('-fn',
                       '--filename',
                       type=str,
                       help='Output File name, no need for .xlsx',
                       default='QA_Homework_Check')

# parse arguments
args = my_parser.parse_args()

# getting data
input_path = args.inputPath
output_path = args.path
filename = args.filename if args.filename[-5:
                                          ] == ".xlsx" else args.filename + ".xlsx"

if not os.path.isdir(input_path):
    print('The path specified does not exist')
    sys.exit()

if not os.path.isdir(output_path):
    print('The output path specified does not exist')
    sys.exit()


if os.path.exists(os.path.join(output_path, filename)):

    print('The file {} already exists, please choose different output file path'.format(
        os.path.abspath(os.path.join(output_path, filename))))
    sys.exit()

input_files = []
for input_file in os.listdir(input_path):
    # looping through the file name in the folder then get only file with correct name
    if input_file.startswith("QA_INPUT") and input_file[-4:] == ".csv":
        input_files.append(input_file)

if not len(input_files):
    print(
        "There is no file in the input path following the naming pattern QA_INPUT[i].csv")
    sys.exit()

print('Start processing {} file{}...'.format(
    len(input_files), 's' if len(input_files) > 1 else ''))

# setting writer to output data
writer = pd.ExcelWriter(os.path.join(
    output_path, filename), engine='xlsxwriter')

# loop through the file
for input_file in input_files:
    # log process to user
    print('\tProcess file: {}'.format(input_file))
    out_df = getDataQuality(input_path, input_file)
    # check if the function return the dataframe, not None
    if out_df is not None:
        print('\t\tRow processed: {}'.format(
            out_df.iloc[0, 0][:out_df.iloc[0, 0].find(" ")]))
        # write each input quality report to excel sheet
        out_df.to_excel(writer, sheet_name=input_file[:-4],
                        index=False, header=False)
    else:
        print('\t\t{} does not have the correct schema'.format(input_file))


print('Finish processing {} file{}'.format(
    len(input_files), 's' if len(input_files) > 1 else ''))
writer.save()
print('Output file saved to: {}'.format(
    os.path.abspath(os.path.join(output_path, filename))))
