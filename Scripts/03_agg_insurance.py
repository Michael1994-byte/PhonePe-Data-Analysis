import pandas as pd
import json
import os

# Correct path
path = r"C:\PhonePe Final Project\Pulse\data\aggregated\insurance\country\india\state"

state_list = os.listdir(path)

data_dict = {
    "State": [],
    "Year": [],
    "Quarter": [],
    "Insurance_type": [],
    "Insurance_count": [],
    "Insurance_amount": []
}

for state in state_list:
    state_path = os.path.join(path, state)
    year_list = os.listdir(state_path)

    for year in year_list:
        year_path = os.path.join(state_path, year)
        quarter_files = os.listdir(year_path)

        for file in quarter_files:
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                data = json.load(f)

            # Safety check
            if data.get("data") and data["data"].get("transactionData"):
                for item in data["data"]["transactionData"]:
                    ins_type = item["name"]
                    count = item["paymentInstruments"][0]["count"]
                    amount = item["paymentInstruments"][0]["amount"]

                    data_dict["State"].append(state)
                    data_dict["Year"].append(int(year))
                    data_dict["Quarter"].append(int(file.replace(".json", "")))
                    data_dict["Insurance_type"].append(ins_type)
                    data_dict["Insurance_count"].append(count)
                    data_dict["Insurance_amount"].append(amount)

# Create DataFrame
df = pd.DataFrame(data_dict)

print(df.head())
print("Shape:", df.shape)

# Save CSV
output_path = r"C:\PhonePe Final Project\Output\agg_insurance.csv"
df.to_csv(output_path, index=False)

print("CSV saved successfully!")