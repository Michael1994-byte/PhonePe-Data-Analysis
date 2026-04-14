import pandas as pd
import json
import os

# Correct path
path = r"C:\PhonePe Final Project\Pulse\data\top\user\country\india\state"

state_list = os.listdir(path)

data_dict = {
    "State": [],
    "Year": [],
    "Quarter": [],
    "Pincode": [],
    "Registered_users": []
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

            if data.get("data") and data["data"].get("pincodes"):
                for item in data["data"]["pincodes"]:
                    pincode = item["name"]
                    registered_users = item["registeredUsers"]

                    data_dict["State"].append(state)
                    data_dict["Year"].append(int(year))
                    data_dict["Quarter"].append(int(file.replace(".json", "")))
                    data_dict["Pincode"].append(pincode)
                    data_dict["Registered_users"].append(registered_users)

df = pd.DataFrame(data_dict)

print(df.head())
print("Shape:", df.shape)

output_path = r"C:\PhonePe Final Project\Output\top_user.csv"
df.to_csv(output_path, index=False)

print("CSV saved successfully!")