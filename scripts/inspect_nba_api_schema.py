"""
Helper: print an endpoint's declared `expected_data` schema (the "contract")
WITHOUT making any network call. It just reads the class attribute.

How to use it on any endpoint

from inspect_schema import print_schema, load
print_schema(load("nba_api.stats.endpoints.boxscoretraditionalv3", "BoxScoreTraditionalV3"))

Or add any ("module.path", "ClassName") pair to the demos list at the bottom. 


Usage:
    python inspect_schema.py                  # inspects the demo endpoints below
    print_schema(SomeEndpointClass)           # from your own code
"""
import importlib


def print_schema(endpoint_cls):
    """Print the datasets and columns an endpoint class declares it returns."""
    name = endpoint_cls.__name__
    schema = getattr(endpoint_cls, "expected_data", None)

    print(f"\n{'=' * 60}")
    print(f"  {name}   (endpoint: '{getattr(endpoint_cls, 'endpoint', getattr(endpoint_cls, 'endpoint_url', 'n/a'))}')")
    print(f"{'=' * 60}")

    if schema is None:
        print("  No `expected_data` declared on this class.")
        return

    if not isinstance(schema, dict):
        print(f"  expected_data is a {type(schema).__name__}, not the usual dict-of-columns.")
        return

    for dataset_name, columns in schema.items():
        # Newer stats endpoints: {dataset: [col, col, ...]}
        if isinstance(columns, list) and (not columns or isinstance(columns[0], str)):
            print(f"\n  Dataset: {dataset_name}  ({len(columns)} fields)")
            for col in columns:
                print(f"      - {col}")
        else:
            # Nested structure (e.g. live ScoreBoard) — show top-level keys only
            print(f"\n  Dataset: {dataset_name}  (nested structure)")
            if isinstance(columns, dict):
                for key in columns:
                    print(f"      - {key}")


def load(module_path, class_name):
    """Import an endpoint class by module path + class name."""
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


if __name__ == "__main__":
    demos = [
        ("nba_api.stats.endpoints.scoreboardv3", "ScoreboardV3"),
        ("nba_api.stats.endpoints.leaguedashplayerstats", "LeagueDashPlayerStats"),
    ]
    for module_path, class_name in demos:
        print_schema(load(module_path, class_name))
