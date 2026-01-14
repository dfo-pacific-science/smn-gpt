#!/usr/bin/env python3
import argparse
import pandas as pd


def main():
    p = argparse.ArgumentParser(description="Detect missing IRIs in column_dictionary.csv and draft gpt_proposed_terms skeleton.")
    p.add_argument("--dictionary", required=True, help="Path to column_dictionary.csv")
    p.add_argument("--output", default="gpt_proposed_terms.csv", help="Output CSV for proposed terms")
    args = p.parse_args()

    df = pd.read_csv(args.dictionary)
    missing_rows = df[
        (
            (df["column_role"] == "measurement") & (df["term_iri"].isna() | (df["term_iri"] == ""))
        )
        | (
            (df["column_role"] == "categorical") & (df.get("term_iri", pd.Series("")) == "")
        )
    ]

    if missing_rows.empty:
        print("No missing term_iri found for measurement or categorical columns.")
        return

    proposals = pd.DataFrame(
        {
            "term_label": missing_rows["column_label"],
            "term_definition": "",
            "term_type": "",
            "suggested_parent_iri": "",
            "definition_source_url": "",
            "suggested_relationships": "",
            "notes": "column_name=" + missing_rows["column_name"],
        }
    )
    proposals.to_csv(args.output, index=False)
    print(f"Wrote proposed terms skeleton to {args.output} (rows: {len(proposals)})")


if __name__ == "__main__":
    main()
