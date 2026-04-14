import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import plotly.express as px
import requests

load_dotenv()

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

# -----------------------------------
# DB CONNECTION
# -----------------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# -----------------------------------
# HELPERS
# -----------------------------------
def style_df(df):
    return st.dataframe(df, use_container_width=True)

def plot_bar(df, x, y, title, categorical_x=False):
    fig = px.bar(df, x=x, y=y, title=title, text_auto=False)
    
    if categorical_x:
        fig.update_xaxes(type="category")
    
    st.plotly_chart(fig, use_container_width=True)

def plot_line(df, x, y, title, color=None):
    fig = px.line(df, x=x, y=y, color=color, markers=True, title=title)
    st.plotly_chart(fig, use_container_width=True)

def plot_pie(df, names, values, title, hole=0):
    fig = px.pie(df, names=names, values=values, title=title, hole=hole)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.title("PhonePe Analysis")
option = st.sidebar.selectbox(
    "Select Business Case",
    [
        "Home - India Map",
        "1. Transaction Dynamics",
        "2. Device Dominance",
        "3. Transaction by State/District",
        "4. User Registration Analysis",
        "5. Insurance Transactions Analysis"
    ]
)

st.title("📊 PhonePe Data Insights Dashboard")

# -----------------------------------
# HOME PAGE - INDIA MAP
# -----------------------------------
if option == "Home - India Map":
    st.subheader("India State-wise Transaction Overview")

    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    india_geojson = requests.get(geojson_url).json()

    map_query = """
    SELECT
        State,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM aggregated_transaction
    GROUP BY State;
    """
    map_df = run_query(map_query)

    detail_query = """
    SELECT
        State,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr,
        SUM(Transaction_count) AS Total_Transactions
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY State;
    """
    detail_df = run_query(detail_query)

    state_name_map = {
        "andaman-&-nicobar-islands": "Andaman & Nicobar",
        "andhra-pradesh": "Andhra Pradesh",
        "arunachal-pradesh": "Arunachal Pradesh",
        "assam": "Assam",
        "bihar": "Bihar",
        "chandigarh": "Chandigarh",
        "chhattisgarh": "Chhattisgarh",
        "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
        "delhi": "Delhi",
        "goa": "Goa",
        "gujarat": "Gujarat",
        "haryana": "Haryana",
        "himachal-pradesh": "Himachal Pradesh",
        "jammu-&-kashmir": "Jammu & Kashmir",
        "jharkhand": "Jharkhand",
        "karnataka": "Karnataka",
        "kerala": "Kerala",
        "ladakh": "Ladakh",
        "lakshadweep": "Lakshadweep",
        "madhya-pradesh": "Madhya Pradesh",
        "maharashtra": "Maharashtra",
        "manipur": "Manipur",
        "meghalaya": "Meghalaya",
        "mizoram": "Mizoram",
        "nagaland": "Nagaland",
        "odisha": "Odisha",
        "puducherry": "Puducherry",
        "punjab": "Punjab",
        "rajasthan": "Rajasthan",
        "sikkim": "Sikkim",
        "tamil-nadu": "Tamil Nadu",
        "telangana": "Telangana",
        "tripura": "Tripura",
        "uttar-pradesh": "Uttar Pradesh",
        "uttarakhand": "Uttarakhand",
        "west-bengal": "West Bengal"
    }

    map_df["State_Map"] = map_df["State"].map(state_name_map)
    detail_df["State_Map"] = detail_df["State"].map(state_name_map)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.choropleth(
            map_df,
            geojson=india_geojson,
            featureidkey="properties.ST_NM",
            locations="State_Map",
            color="Total_Amount_Cr",
            color_continuous_scale="Reds",
            title="Transaction Amount by State (in Crores)"
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        selected_state = st.selectbox(
            "Select State",
            sorted(detail_df["State"].dropna().unique())
        )

        state_row = detail_df[detail_df["State"] == selected_state]

        if not state_row.empty:
            total_amount = state_row["Total_Amount_Cr"].values[0]
            total_txns = state_row["Total_Transactions"].values[0]

            st.metric("Total Transaction Amount (Cr)", f"{total_amount:,.2f}")
            st.metric("Total Transactions", f"{int(total_txns):,}")

            type_query = f"""
            SELECT
                Transaction_type,
                ROUND(SUM(Transaction_amount) / 10000000, 2) AS Amount_Cr
            FROM aggregated_transaction
            WHERE State = '{selected_state}'
            GROUP BY Transaction_type
            ORDER BY Amount_Cr DESC
            LIMIT 1;
            """
            type_df = run_query(type_query)

            if not type_df.empty:
                st.metric("Top Transaction Type", type_df["Transaction_type"].values[0])
                st.metric("Top Type Amount (Cr)", f"{type_df['Amount_Cr'].values[0]:,.2f}")

            st.write("### State Summary")
            st.dataframe(
                state_row[["State", "Total_Amount_Cr", "Total_Transactions"]],
                use_container_width=True
            )

# -----------------------------------
# 1. TRANSACTION DYNAMICS
# -----------------------------------
elif option == "1. Transaction Dynamics":
    st.header("1. Decoding Transaction Dynamics on PhonePe")

    q1 = """
    SELECT 
        Year,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM aggregated_transaction
    GROUP BY Year
    ORDER BY Year;
    """
    q2 = """
    SELECT 
        Year,
        SUM(Transaction_count) AS Total_Transaction_Count
    FROM aggregated_transaction
    GROUP BY Year
    ORDER BY Year;
    """
    q3 = """
    SELECT 
        Year,
        Quarter,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM aggregated_transaction
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
    """
    q4 = """
    SELECT 
        Transaction_type,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM aggregated_transaction
    GROUP BY Transaction_type
    ORDER BY Total_Amount_Cr DESC;
    """
    q5 = """
    SELECT 
        Transaction_type,
        SUM(Transaction_count) AS Total_Transaction_Count
    FROM aggregated_transaction
    GROUP BY Transaction_type
    ORDER BY Total_Transaction_Count DESC;
    """

    df1 = run_query(q1)
    df2 = run_query(q2)
    df3 = run_query(q3)
    df4 = run_query(q4)
    df5 = run_query(q5)

    st.subheader("Total Transaction Amount by Year")
    style_df(df1)
    plot_line(df1, "Year", "Total_Amount_Cr", "Year-wise Transaction Amount (Cr)")

    st.subheader("Total Transaction Count by Year")
    style_df(df2)
    plot_line(df2, "Year", "Total_Transaction_Count", "Year-wise Transaction Count")

    st.subheader("Quarterly Transaction Amount Trend")
    style_df(df3)
    fig3 = px.bar(df3, x="Quarter", y="Total_Amount_Cr", color="Year",
                  barmode="group", title="Quarter-wise Transaction Amount Trend")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Transaction Amount by Transaction Type")
    style_df(df4)
    plot_pie(df4, "Transaction_type", "Total_Amount_Cr", "Transaction Amount Share by Type")

    st.subheader("Transaction Count by Transaction Type")
    style_df(df5)
    plot_pie(df5, "Transaction_type", "Total_Transaction_Count", "Transaction Count Share by Type", hole=0.45)

# -----------------------------------
# 2. DEVICE DOMINANCE
# -----------------------------------
elif option == "2. Device Dominance":
    st.header("2. Device Dominance and User Engagement Analysis")

    q6 = """
    SELECT 
        Brand,
        SUM(User_count) AS Total_Users
    FROM aggregated_user
    GROUP BY Brand
    ORDER BY Total_Users DESC;
    """
    q7 = """
    SELECT 
        Brand,
        ROUND(AVG(Percentage) * 100, 2) AS Avg_Percentage_Share
    FROM aggregated_user
    GROUP BY Brand
    ORDER BY Avg_Percentage_Share DESC;
    """
    q8 = """
    SELECT 
        Year,
        Brand,
        SUM(User_count) AS Total_Users
    FROM aggregated_user
    GROUP BY Year, Brand
    ORDER BY Year, Total_Users DESC;
    """
    q9 = """
    SELECT 
        State,
        SUM(User_count) AS Total_Users
    FROM aggregated_user
    GROUP BY State
    ORDER BY Total_Users DESC
    LIMIT 10;
    """
    q10 = """
    SELECT 
        Year,
        Quarter,
        Brand,
        SUM(User_count) AS Total_Users
    FROM aggregated_user
    GROUP BY Year, Quarter, Brand
    ORDER BY Year, Quarter, Total_Users DESC;
    """

    df6 = run_query(q6)
    df7 = run_query(q7)
    df8 = run_query(q8)
    df9 = run_query(q9)
    df10 = run_query(q10)

    st.subheader("Total Users by Device Brand")
    style_df(df6)
    top_brands = df6.head(10).copy()
    plot_bar(top_brands, "Brand", "Total_Users", "Top Device Brands by User Count")

    st.subheader("Average Percentage Share by Device Brand")
    style_df(df7)
    top_share = df7.head(10).copy()
    plot_pie(top_share, "Brand", "Avg_Percentage_Share", "Average Device Brand Share", hole=0.45)

    st.subheader("Brand-wise User Count by Year")
    style_df(df8)
    top_brand_names = top_brands["Brand"].head(5).tolist()
    df8_filtered = df8[df8["Brand"].isin(top_brand_names)]
    plot_line(df8_filtered, "Year", "Total_Users", "Brand-wise User Count by Year", color="Brand")

    st.subheader("Top 10 States by Device User Count")
    style_df(df9)
    plot_bar(df9, "State", "Total_Users", "Top 10 States by Device User Count")

    st.subheader("Quarter-wise User Trend by Brand")
    style_df(df10)
    df10["Year_Quarter"] = df10["Year"].astype(str) + "-Q" + df10["Quarter"].astype(str)
    df10_filtered = df10[df10["Brand"].isin(top_brand_names)]
    fig10 = px.line(
        df10_filtered,
        x="Year_Quarter",
        y="Total_Users",
        color="Brand",
        markers=True,
        title="Quarter-wise User Trend by Brand"
    )
    st.plotly_chart(fig10, use_container_width=True)

# -----------------------------------
# 3. TRANSACTION BY STATE / DISTRICT
# -----------------------------------
elif option == "3. Transaction by State/District":
    st.header("3. Transaction Analysis Across States and Districts")

    q11 = """
    SELECT 
        State,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM map_transaction
    GROUP BY State
    ORDER BY Total_Amount_Cr DESC
    LIMIT 10;
    """
    q12 = """
    SELECT 
        State,
        SUM(Transaction_count) AS Total_Transaction_Count
    FROM map_transaction
    GROUP BY State
    ORDER BY Total_Transaction_Count DESC
    LIMIT 10;
    """
    q13 = """
    SELECT 
        District,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM map_transaction
    GROUP BY District
    ORDER BY Total_Amount_Cr DESC
    LIMIT 10;
    """
    q14 = """
    SELECT 
        District,
        SUM(Transaction_count) AS Total_Transaction_Count
    FROM map_transaction
    GROUP BY District
    ORDER BY Total_Transaction_Count DESC
    LIMIT 10;
    """
    q15 = """
    SELECT 
        CAST(FLOOR(Pincode) AS CHAR) AS Pincode,
        ROUND(SUM(Transaction_amount) / 10000000, 2) AS Total_Amount_Cr
    FROM top_transaction
    GROUP BY Pincode
    ORDER BY Total_Amount_Cr DESC
    LIMIT 10;
    """

    df11 = run_query(q11)
    df12 = run_query(q12)
    df13 = run_query(q13)
    df14 = run_query(q14)
    df15 = run_query(q15)
    df15["Pincode"] = df15["Pincode"].astype(str)

    st.subheader("Top 10 States by Transaction Amount")
    style_df(df11)
    plot_bar(df11, "State", "Total_Amount_Cr", "Top 10 States by Transaction Amount (Cr)")

    st.subheader("Top 10 States by Transaction Count")
    style_df(df12)
    plot_bar(df12, "State", "Total_Transaction_Count", "Top 10 States by Transaction Count")

    st.subheader("Top 10 Districts by Transaction Amount")
    style_df(df13)
    plot_bar(df13, "District", "Total_Amount_Cr", "Top 10 Districts by Transaction Amount (Cr)")

    st.subheader("Top 10 Districts by Transaction Count")
    style_df(df14)
    plot_bar(df14, "District", "Total_Transaction_Count", "Top 10 Districts by Transaction Count")

    st.subheader("Top 10 Pincodes by Transaction Amount")
    style_df(df15)
    plot_bar(df15, "Pincode", "Total_Amount_Cr", "Top 10 Pincodes by Transaction Amount (Cr)", categorical_x=True)

# -----------------------------------
# 4. USER REGISTRATION ANALYSIS
# -----------------------------------
elif option == "4. User Registration Analysis":
    st.header("4. User Registration Analysis")

    q16 = """
    SELECT 
        State,
        SUM(Registered_users) AS Total_Registered_Users
    FROM map_user
    GROUP BY State
    ORDER BY Total_Registered_Users DESC
    LIMIT 10;
    """
    q17 = """
    SELECT 
        District,
        SUM(Registered_users) AS Total_Registered_Users
    FROM map_user
    GROUP BY District
    ORDER BY Total_Registered_Users DESC
    LIMIT 10;
    """
    q18 = """
    SELECT 
        CAST(FLOOR(Pincode) AS CHAR) AS Pincode,
        SUM(Registered_users) AS Total_Registered_Users
    FROM top_user
    GROUP BY Pincode
    ORDER BY Total_Registered_Users DESC
    LIMIT 10;
    """
    q19 = """
    SELECT 
        Year,
        SUM(Registered_users) AS Total_Registered_Users
    FROM map_user
    GROUP BY Year
    ORDER BY Year;
    """
    q20 = """
    SELECT 
        Year,
        Quarter,
        SUM(App_opens) AS Total_App_Opens
    FROM map_user
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
    """

    df16 = run_query(q16)
    df17 = run_query(q17)
    df18 = run_query(q18)
    df19 = run_query(q19)
    df20 = run_query(q20)
    df18["Pincode"] = df18["Pincode"].astype(str)

    st.subheader("Top 10 States by Registered Users")
    style_df(df16)
    plot_bar(df16, "State", "Total_Registered_Users", "Top 10 States by Registered Users")

    st.subheader("Top 10 Districts by Registered Users")
    style_df(df17)
    plot_bar(df17, "District", "Total_Registered_Users", "Top 10 Districts by Registered Users")

    st.subheader("Top 10 Pincodes by Registered Users")
    style_df(df18)
    plot_bar(df18, "Pincode", "Total_Registered_Users", "Top 10 Pincodes by Registered Users", categorical_x=True)

    st.subheader("Year-wise Registered Users Trend")
    style_df(df19)
    plot_line(df19, "Year", "Total_Registered_Users", "Year-wise Registered Users Trend")

    st.subheader("Year-Quarter Wise App Opens Trend")
    style_df(df20)
    df20["Year_Quarter"] = df20["Year"].astype(str) + "-Q" + df20["Quarter"].astype(str)
    fig20 = px.line(df20, x="Year_Quarter", y="Total_App_Opens", markers=True,
                    title="Year-Quarter Wise App Opens Trend")
    st.plotly_chart(fig20, use_container_width=True)

# -----------------------------------
# 5. INSURANCE TRANSACTIONS ANALYSIS
# -----------------------------------
elif option == "5. Insurance Transactions Analysis":
    st.header("5. Insurance Transactions Analysis")

    q21 = """
    SELECT 
        Year,
        ROUND(SUM(Insurance_amount) / 10000000, 2) AS Total_Insurance_Amount_Cr
    FROM aggregated_insurance
    GROUP BY Year
    ORDER BY Year;
    """
    q22 = """
    SELECT 
        Year,
        SUM(Insurance_count) AS Total_Insurance_Count
    FROM aggregated_insurance
    GROUP BY Year
    ORDER BY Year;
    """
    q23 = """
    SELECT 
        State,
        ROUND(SUM(Insurance_amount) / 10000000, 2) AS Total_Insurance_Amount_Cr
    FROM map_insurance
    GROUP BY State
    ORDER BY Total_Insurance_Amount_Cr DESC
    LIMIT 10;
    """
    q24 = """
    SELECT 
        District,
        SUM(Insurance_count) AS Total_Insurance_Count
    FROM map_insurance
    GROUP BY District
    ORDER BY Total_Insurance_Count DESC
    LIMIT 10;
    """
    q25 = """
    SELECT 
        CAST(FLOOR(Pincode) AS CHAR) AS Pincode,
        ROUND(SUM(Insurance_amount) / 10000000, 2) AS Total_Insurance_Amount_Cr
    FROM top_insurance
    GROUP BY Pincode
    ORDER BY Total_Insurance_Amount_Cr DESC
    LIMIT 10;
    """

    df21 = run_query(q21)
    df22 = run_query(q22)
    df23 = run_query(q23)
    df24 = run_query(q24)
    df25 = run_query(q25)
    df25["Pincode"] = df25["Pincode"].astype(str)

    st.subheader("Total Insurance Amount by Year")
    style_df(df21)
    plot_line(df21, "Year", "Total_Insurance_Amount_Cr", "Year-wise Insurance Amount (Cr)")

    st.subheader("Total Insurance Count by Year")
    style_df(df22)
    plot_line(df22, "Year", "Total_Insurance_Count", "Year-wise Insurance Transaction Count")

    st.subheader("Top 10 States by Insurance Amount")
    style_df(df23)
    plot_bar(df23, "State", "Total_Insurance_Amount_Cr", "Top 10 States by Insurance Amount (Cr)")

    st.subheader("Top 10 Districts by Insurance Count")
    style_df(df24)
    plot_bar(df24, "District", "Total_Insurance_Count", "Top 10 Districts by Insurance Count")

    st.subheader("Top 10 Pincodes by Insurance Amount")
    style_df(df25)
    plot_bar(df25, "Pincode", "Total_Insurance_Amount_Cr", "Top 10 Pincodes by Insurance Amount (Cr)", categorical_x=True)