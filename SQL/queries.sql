CREATE DATABASE phonepe_final_project;
USE phonepe_final_project;

CREATE TABLE aggregated_transaction (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Transaction_type VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount DOUBLE
);

CREATE TABLE aggregated_user (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Brand VARCHAR(100),
    User_count BIGINT,
    Percentage DOUBLE
);

CREATE TABLE aggregated_insurance (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Insurance_type VARCHAR(100),
    Insurance_count BIGINT,
    Insurance_amount DOUBLE
);

CREATE TABLE map_transaction (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(150),
    Transaction_count BIGINT,
    Transaction_amount DOUBLE
);

CREATE TABLE map_user (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(150),
    Registered_users BIGINT,
    App_opens BIGINT
);

CREATE TABLE map_insurance (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(150),
    Insurance_count BIGINT,
    Insurance_amount DOUBLE
);

CREATE TABLE top_transaction (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Pincode VARCHAR(20),
    Transaction_count BIGINT,
    Transaction_amount DOUBLE
);

CREATE TABLE top_user (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Pincode VARCHAR(20),
    Registered_users BIGINT
);

CREATE TABLE top_insurance (
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Pincode VARCHAR(20),
    Insurance_count BIGINT,
    Insurance_amount DOUBLE
);

##Business Case 1: Decoding Transaction Dynamics on PhonePe
#Query 1: Total Transaction Amount by Year
SELECT 
    Year,
    ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
FROM aggregated_transaction
GROUP BY Year
ORDER BY Year;

##Query 2: Total Transaction Count by Year
SELECT 
    Year,
    SUM(Transaction_count) AS Total_Transaction_Count
FROM aggregated_transaction
GROUP BY Year
ORDER BY Year;

##Query 3: Quarterly Transaction Amount Trend
SELECT 
    Year,
    Quarter,
    ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
FROM aggregated_transaction
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

##Query 4: Transaction Amount by Transaction Type
SELECT 
    Transaction_type,
    ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
FROM aggregated_transaction
GROUP BY Transaction_type
ORDER BY Total_Amount_Cr DESC;

##Query 5: Transaction Count by Transaction Type
SELECT 
    Transaction_type,
    SUM(Transaction_count) AS Total_Transaction_Count
FROM aggregated_transaction
GROUP BY Transaction_type
ORDER BY Total_Transaction_Count DESC;

##Business Case 2: Device Dominance and User Engagement Analysis
##Query 6: Total Users by Device Brand
SELECT 
    Brand,
    SUM(User_count) AS Total_Users
FROM aggregated_user
GROUP BY Brand
ORDER BY Total_Users DESC;

##Query 7: Average Percentage Share by Device Brand
SELECT 
    Brand,
    ROUND(AVG(Percentage) * 100, 2) AS Avg_Percentage_Share
FROM aggregated_user
GROUP BY Brand
ORDER BY Avg_Percentage_Share DESC;

##Query 8: Brand-wise User Count by Year
SELECT 
    Year,
    Brand,
    SUM(User_count) AS Total_Users
FROM aggregated_user
GROUP BY Year, Brand
ORDER BY Year, Total_Users DESC;

##Query 9: Top 10 States by Device User Count
SELECT 
    State,
    SUM(User_count) AS Total_Users
FROM aggregated_user
GROUP BY State
ORDER BY Total_Users DESC
LIMIT 10;

##Query 10: Quarter-wise User Trend by Brand
SELECT 
    Year,
    Quarter,
    Brand,
    SUM(User_count) AS Total_Users
FROM aggregated_user
GROUP BY Year, Quarter, Brand
ORDER BY Year, Quarter, Total_Users DESC;

##Business Case 3: Transaction Analysis Across States and Districts
##Query 11: Top 10 States by Transaction Amount
SELECT 
    State,
    ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
FROM map_transaction
GROUP BY State
ORDER BY Total_Amount_Cr DESC
LIMIT 10;

##Query 12: Top 10 States by Transaction Count
SELECT 
    State,
    SUM(Transaction_count) AS Total_Transaction_Count
FROM map_transaction
GROUP BY State
ORDER BY Total_Transaction_Count DESC
LIMIT 10;

##Query 13: Top 10 Districts by Transaction Amount
SELECT 
    District,
    ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
FROM map_transaction
GROUP BY District
ORDER BY Total_Amount_Cr DESC
LIMIT 10;

##Query 14: Top 10 Districts by Transaction Count
SELECT 
    District,
    SUM(Transaction_count) AS Total_Transaction_Count
FROM map_transaction
GROUP BY District
ORDER BY Total_Transaction_Count DESC
LIMIT 10;

##Query 15: Top 10 Pincodes by Transaction Amount
SELECT 
    CAST(FLOOR(Pincode) AS CHAR) AS Pincode,
    ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
FROM top_transaction
GROUP BY Pincode
ORDER BY Total_Amount_Cr DESC
LIMIT 10;

##Business Case 4: User Registration Analysis
#Query 16: Top 10 States by Registered Users
SELECT 
    State,
    SUM(Registered_users) AS Total_Registered_Users
FROM map_user
GROUP BY State
ORDER BY Total_Registered_Users DESC
LIMIT 10;

##Query 17: Top 10 Districts by Registered Users
SELECT 
    District,
    SUM(Registered_users) AS Total_Registered_Users
FROM map_user
GROUP BY District
ORDER BY Total_Registered_Users DESC
LIMIT 10;

##Query 18: Top 10 Pincodes by Registered Users
SELECT 
    CAST(FLOOR(Pincode) AS CHAR) AS Pincode,
    SUM(Registered_users) AS Total_Registered_Users
FROM top_user
GROUP BY Pincode
ORDER BY Total_Registered_Users DESC
LIMIT 10;

##Query 19: Year-wise Registered Users Trend
SELECT 
    Year,
    SUM(Registered_users) AS Total_Registered_Users
FROM map_user
GROUP BY Year
ORDER BY Year;

##Query 20: Year-Quarter Wise App Opens Trend
SELECT 
    Year,
    Quarter,
    SUM(App_opens) AS Total_App_Opens
FROM map_user
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

##Business Case 5: Insurance Transactions Analysis
##Query 21: Total Insurance Amount by Year
SELECT 
    Year,
    ROUND(SUM(Insurance_amount) / 10000000, 2) AS Total_Insurance_Amount_Cr
FROM aggregated_insurance
GROUP BY Year
ORDER BY Year;

##Query 22: Total Insurance Count by Year
SELECT 
    Year,
    SUM(Insurance_count) AS Total_Insurance_Count
FROM aggregated_insurance
GROUP BY Year
ORDER BY Year;

##Query 23: Top 10 States by Insurance Amount
SELECT 
    State,
    ROUND(SUM(Insurance_amount) / 10000000, 2) AS Total_Insurance_Amount_Cr
FROM map_insurance
GROUP BY State
ORDER BY Total_Insurance_Amount_Cr DESC
LIMIT 10;

##Query 24: Top 10 Districts by Insurance Count
SELECT 
    District,
    SUM(Insurance_count) AS Total_Insurance_Count
FROM map_insurance
GROUP BY District
ORDER BY Total_Insurance_Count DESC
LIMIT 10;

##Query 25: Top 10 Pincodes by Insurance Amount
SELECT 
    CAST(FLOOR(Pincode) AS CHAR) AS Pincode,
    ROUND(SUM(Insurance_amount) / 10000000, 2) AS Total_Insurance_Amount_Cr
FROM top_insurance
GROUP BY Pincode
ORDER BY Total_Insurance_Amount_Cr DESC
LIMIT 10;