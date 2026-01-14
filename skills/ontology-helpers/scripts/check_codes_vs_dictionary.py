#!/usr/bin/env python3
import argparse
import pandas as pd


def main():
    p = argparse.ArgumentParser(description="Check categorical columns against codes.csv.")
    p.add_argument("--dictionary", required=True, help="Path to column_dictionary.csv")
    p.add_argument("--codes", required=True, help="Path to codes.csv")
    args = p.parse_args()

    dict_df = pd.read_csv(args.dictionary)
    codes_df = pd.read_csv(args.codes)

    categorical = dict_df[dict_df["column_role"] == "categorical"][["table_id", "column_name"]]
    if categorical.empty:
        print("No categorical columns found.")
        return

    missing_codes = []
    for _, row in categorical.iterrows():
        subset = codes_df[
            (codes_df["table_id"] == row["table_id"]) & (codes_df["column_name"] == row["column_name"])
        ]
        if subset.empty:
            missing_codes.append((row["table_id"], row["column_name"]))

    if missing_codes:
        print("Categorical columns missing codes.csv entries:")
        for tbl, col in missing_codes:
            print(f"- table_id={tbl}, column_name={col}")
    else:
        print("All categorical columns have codes.csv entries.")


if __name__ == "__main__":
    main()
