#!/usr/bin/env python3
import argparse
import urllib.parse
from textwrap import dedent


def main():
    p = argparse.ArgumentParser(description="Draft a new-term issue URL and Markdown.")
    p.add_argument("--label", required=True, help="term_label")
    p.add_argument("--definition", required=True, help="term_definition")
    p.add_argument("--term-type", required=True, choices=["skos_concept", "owl_class", "owl_object_property"], help="term_type")
    p.add_argument("--parent-iri", required=True, help="suggested_parent_iri")
    p.add_argument("--definition-source-url", default="", help="definition_source_url")
    p.add_argument("--relationships", default="", help="suggested_relationships (comma-separated)")
    p.add_argument("--notes", default="", help="notes")
    args = p.parse_args()

    md = dedent(
        f"""
        ### Term request
        - term_label: {args.label}
        - term_definition: {args.definition}
        - term_type: {args.term_type}
        - suggested_parent_iri: {args.parent_iri}
        - definition_source_url: {args.definition_source_url}
        - suggested_relationships: {args.relationships}
        - notes: {args.notes}
        """
    ).strip()

    base = "https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new"
    params = {
        "template": "new-term-request.md",
        "title": f"New term: {args.label}",
        "body": md,
    }
    url = base + "?" + urllib.parse.urlencode(params)
    print(md)
    print("\nIssue URL:\n" + url)


if __name__ == "__main__":
    main()
