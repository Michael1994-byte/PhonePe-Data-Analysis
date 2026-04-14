# 📊 PhonePe Data Analysis Project

## 📌 Overview
This project analyzes PhonePe Pulse data to extract meaningful insights on digital payment trends in India. The analysis focuses on transaction growth, device distribution, regional performance, user registration trends, and insurance activity.

The objective is to understand how digital payments are evolving and provide data-driven recommendations based on observed patterns.

---

## 🎯 Objectives
- Analyze transaction growth trends over time (year-wise and quarter-wise)
- Identify dominant mobile device brands among users
- Study state-wise transaction performance
- Understand user registration and app engagement trends
- Analyze insurance transaction growth and distribution

---

## 🛠️ Tools & Technologies
- Python (Pandas, NumPy, Plotly)
- MySQL
- Streamlit
- VS Code

---

## 📂 Project Structure

PhonePe-Data-Analysis/
│
├── Output/
│   ├── agg_insurance.csv
│   ├── agg_transaction.csv
│   ├── agg_user.csv
│   ├── map_insurance.csv
│   ├── map_transaction.csv
│   ├── map_user.csv
│   ├── top_insurance.csv
│   ├── top_transaction.csv
│   └── top_user.csv
│
├── Pulse/
│   └── data/  (Raw PhonePe Pulse dataset)
│
├── Scripts/
│   ├── 01_agg_transaction.py
│   ├── 02_agg_user.py
│   ├── 03_agg_insurance.py
│   ├── 04_map_transaction.py
│   ├── 05_map_user.py
│   ├── 06_map_insurance.py
│   ├── 07_top_transaction.py
│   ├── 08_top_user.py
│   ├── 09_top_insurance.py
│   ├── 10_load_all_to_mysql.py
│   └── clone_phonepe.py
│
├── SQL/
│   └── queries.sql
│
├── Streamlit_app/
│   └── app.py (Main Dashboard Application)
│
├── README.md
├── requirements.txt
└── .gitignore


---

## 🔄 Data Pipeline
1. Extracted JSON data from the PhonePe Pulse GitHub repository  
2. Transformed nested JSON data into structured tabular format  
3. Cleaned and processed data using Python (Pandas)  
4. Stored structured data into MySQL database  
5. Performed analysis using SQL queries  
6. Built interactive dashboards using Streamlit  

---

## 📊 Business Use Cases

### 1. Transaction Dynamics
Analysis of transaction trends over time to understand growth patterns.

### 2. Device Dominance
Analysis of user distribution across mobile device brands.

### 3. Transaction by State/District Analysis
Comparison of transaction activity across different regions.

### 4. User Registration Analysis
Analysis of user growth and engagement trends.

### 5. Insurance Transaction Analysis
Study of insurance transaction growth and regional distribution.

---

## 🔍 Key Insights
- Digital transactions have increased consistently from 2018 to 2024  
- Both transaction count and transaction amount show strong growth  
- User distribution is dominated by a few mobile device brands  
- Transaction activity is concentrated in top-performing states  
- Registered users and app opens are increasing over time  
- Insurance transactions show a steady upward trend from 2020 onwards    

---

## 💡 Recommendations
- Strengthen infrastructure to support increasing transaction volume  
- Focus on dominant device platforms for better reach  
- Expand digital services in regions with lower transaction levels  
- Improve user engagement and retention strategies  
- Increase awareness and adoption of insurance services  

---

## 🚀 How to Run the Project
1. Clone the repository  
2. Install required Python libraries  
3. Set up MySQL database and tables  
4. Run data extraction and loading scripts  
5. Launch the Streamlit dashboard using:
   ```bash
   streamlit run app.py

