"""
The "after" version — YOUR file to complete.

Fill in the three functions marked with # TODO. Everything else (CLI wiring,
imports) is already done for you. Do not hardcode any path, format string, or
threshold value anywhere in this file — if you find yourself typing a literal
number or file path outside of a default/example, it belongs in the config
file instead.

Run with:
    python src/pipeline.py --config config/pipeline.yaml
"""
import argparse
import csv
import json

import yaml

REQUIRED_KEYS = ["input_path", "input_format", "high_value_threshold", "output_path"]


def load_config(path):
    """Load a YAML config file and validate required keys are present.

    Must raise ValueError naming the specific missing key if REQUIRED_KEYS
    are not all present. Do not let this fail with a bare KeyError later.
    """
    with open(path,"r") as f:
        config = yaml.safe_load(f)
    if not isinstance(config,dict):
        raise ValueError("config filw must contain a yaml mapping")
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing required config key:{key}")
            
    return config
    # raise NotImplementedError("load_config is not implemented yet")


def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    if fmt=="csv":
        with open(path,"r",newline="") as f:
            reader=csv.DictReader(f)
            return list(reader)
    elif fmt=="json":
        with open(path,"r",newline="") as f:
            data =json.load(f)
        return data
    else:
        raise ValueError(f"unsupported input {fmt}. Expected csv or json .")
   


def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    

    transactions=load_transactions(config["input_path"],config["input_format"])

    count=len(transactions)
    total_amount=sum(float(transaction["amount"]) for transaction in transactions)
    fraud_count=sum(str(t["is_fraud"]).strip().lower()=="true" for t in transactions)
    fraud_rate= fraud_count/count if count>0 else 0.0
    n_high_value=sum(float(transaction["amount"])>=float(config["high_value_threshold"]) for transaction in transactions)
    high_value_threshold=config["high_value_threshold"]

    summary = {
        "n_transactions": count,
        "total_amount": round(total_amount, 2),
        "fraud_rate": round(fraud_rate , 4) ,
        "n_high_value": n_high_value,
        "high_value_threshold": high_value_threshold,
    }
    with open(config["output_path"], "w") as f:
        json.dump(summary, f, indent=2)
    return summary    
    


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
