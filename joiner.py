import csv
import chardet
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--eduhub", "--eduhub-student-file", type=str, required=True, help="eduHub Student File (ST_XXXX.csv)")
parser.add_argument("--edupass", "--edupass-student-export", type=str, required=True, help="eduPass Student Export from the EduSTAR MC")
parser.add_argument("--out", "--out-file", type=str, required=True, help="Output file name or path")
args = parser.parse_args()


def get_encoding(file_name):
    with open(file_name, "rb") as rawdata:
        result = chardet.detect(rawdata.read())
    return result["encoding"]


eduhub_data = pd.read_csv(args.eduhub, encoding=get_encoding(args.eduhub))
edupass_data = pd.read_csv(args.edupass, encoding=get_encoding(args.edupass))

eduhub_data = eduhub_data.loc[eduhub_data["STATUS"].isin(["ACTV", "LVNG"])]

merged_data = edupass_data.merge(
    eduhub_data,
    how="left",
    left_on=["firstName", "lastName", "student_class"],
    right_on=["FIRST_NAME", "SURNAME", "HOME_GROUP"],
)

merged_data.to_csv(args.out, index=False)
