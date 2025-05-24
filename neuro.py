import os
import pandas as pd
import h2o
from h2o.automl import H2OAutoML

# Ensure working directory contains 'dataset_train.json'
JSON_PATH = 'dataset_train.json'
CSV_PATH = 'dataset_train.csv'
LEADERBOARD_CSV = 'h2o_leaderboard.csv'
MODELS_DIR = 'h2o_models'


def main():
    # 1. Load JSON via pandas
    if not os.path.isfile(JSON_PATH):
        raise FileNotFoundError(f"JSON data file '{JSON_PATH}' not found.")
    print(f"Loading data from {JSON_PATH}...")
    df = pd.read_json(JSON_PATH)

    # 2. Convert to CSV for H2O import
    print(f"Saving data to CSV at {CSV_PATH} for H2O import...")
    df.to_csv(CSV_PATH, index=False)

    # 3. Initialize H2O
    print("Initializing H2O... (max 4 GB memory)")
    h2o.init(max_mem_size="4G")

    # 4. Import data into H2O Frame
    print(f"Importing data from {CSV_PATH} into H2O...")
    data = h2o.import_file(CSV_PATH)

    # Convert target to categorical for classification
    data['isCommercial'] = data['isCommercial'].asfactor()

    # 5. Run AutoML
    print("Starting H2O AutoML...")
    aml = H2OAutoML(
        max_runtime_secs=3600,
        seed=42,
        balance_classes=True
    )
    aml.train(y='isCommercial', training_frame=data)

    # 6. Leaderboard
    lb = aml.leaderboard
    print("Top 10 models in leaderboard:")
    print(lb.head(rows=10))

    # Save leaderboard to local CSV
    print(f"Saving leaderboard to {LEADERBOARD_CSV}...")
    lb_df = h2o.as_list(lb, use_pandas=True)
    lb_df.to_csv(LEADERBOARD_CSV, index=False)

    # 7. Save best model
    best_model = aml.leader
    print(f"Saving best model '{best_model.model_id}' to directory {MODELS_DIR}...")
    h2o.save_model(best_model, path=MODELS_DIR, force=True)

    print("H2O AutoML run complete.")


if __name__ == '__main__':
    main()