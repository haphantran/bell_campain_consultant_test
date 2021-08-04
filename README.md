# bell_campain_consultant_test

## App usage
__You can use the app.exe if you don't want to install python and packages in requirements.txt__
```
usage: app.py [-h] [-p outputPath] [-fn FILENAME] inputPath

Read all csv inputs in path and output the quality of data

positional arguments:
  inputPath             the path to input files

optional arguments:
  -h, --help            show this help message and exit
  -p outputPath, --path outputPath
                        the path to output the data quality report, default to current folder
  -fn FILENAME, --filename FILENAME
                        Output File name, no need for .xlsx
```

## Assumptions

- For Text(n) in Data format, I assumed that is equivilent of Varchar(n), not Char(n): n is maximum length, the value can be shorter than that. That base on columns like Brand or NotificationLanguage
- This app will process all files in the InputPath that have the naming patern 'QA_INPUT{something}.csv'
- If one file doesn't have the same schema (different number of column names, more of less column,...), this app will skip that file and output to the log
- If users doesn't specify outputPath, will use current directory.
- If users doesn't specify output Filename, will use QA_Homework_Check.xlsx.

```shell
PS E:\Cloud Storage\haphantran drive\submission\app.exe -p ./testfolder ./testfolder
Start processing 4 files...
        Process file: QA_INPUT1.csv
                Row processed: 100
        Process file: QA_INPUT2.csv
                Row processed: 100
        Process file: QA_INPUT3.csv
                Row processed: 100
        Process file: QA_INPUT4.csv
                QA_INPUT4.csv does not have the correct schema
Finish processing 4 files
Output file saved to: E:\Cloud Storage\haphantran drive\testfolder\QA_Homework_Check.xlsx
```

