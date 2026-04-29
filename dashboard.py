import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')
# ==============================
# Helper Functions
# ==============================

def create_city_customer_df(df):
    city_df = df.groupby("customer_city")["customer_unique_id"] \
        .nunique().sort_values(ascending=False).reset_index()
    city_df.rename(columns={"customer_unique_id": "customer_count"}, inplace=True)
    return city_df


def create_product_sales_df(df):
    product_df = df.groupby("product_category_name_english") \
        .size().sort_values(ascending=False).reset_index()
    product_df.rename(columns={0: "total_sales"}, inplace=True)
    return product_df


def create_payment_df(df):
    payment_df = df.groupby("payment_type") \
        .size().sort_values(ascending=False).reset_index()
    payment_df.rename(columns={0: "total_usage"}, inplace=True)
    return payment_df


# ==============================
# Load Data
# ==============================

df1 = pd.read_csv("customers_dataset.csv")
df2 = pd.read_csv("geolocation_dataset.zip")
df3 = pd.read_csv("order_items_dataset.csv")
df4 = pd.read_csv("order_payments_dataset.csv")
df5 = pd.read_csv("order_reviews_dataset.csv")
df6 = pd.read_csv("orders_dataset.csv")
df7 = pd.read_csv("product_category_name_translation.csv")
df8 = pd.read_csv("products_dataset.csv")
df9 = pd.read_csv("sellers_dataset.csv")

all_df = pd.merge(df6, df1, on="customer_id", how="left")
all_df = pd.merge(all_df, df4, on="order_id", how="left")
all_df = pd.merge(all_df, df3, on="order_id", how="left")
all_df = pd.merge(all_df, df8, on="product_id", how="left")
all_df = pd.merge(all_df, df7, on="product_category_name", how="left")
# all_df = pd.read_csv("all_data.csv")

all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# ==============================
# Sidebar Filter
# ==============================

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.title("E-Commerce Dashboard")
    
    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
main_df = all_df[
    (all_df["order_purchase_timestamp"] >= str(start_date)) &
    (all_df["order_purchase_timestamp"] <= str(end_date))
]

# ==============================
# Data Preparation
# ==============================

city_df = create_city_customer_df(main_df)
product_df = create_product_sales_df(main_df)
payment_df = create_payment_df(main_df)

# ==============================
# Dashboard
# ==============================

st.header("📊 E-Commerce Data Dashboard")
st.caption("Analisis berdasarkan dataset Brazilian E-Commerce")

# ==============================
# 1. Kota dengan pelanggan terbanyak
# ==============================

st.subheader("Top Kota dengan Pelanggan Terbanyak")

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x="customer_count",
    y="customer_city",
    data=city_df.head(10),
    palette="Blues_r",
    ax=ax
)

ax.set_title("Top 10 Kota (Customer)")
ax.set_xlabel("Jumlah Customer")
ax.set_ylabel("Kota")

st.pyplot(fig)

# ==============================
# 2. Produk terlaris
# ==============================

st.subheader("Kategori Produk Terlaris")

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x="total_sales",
    y="product_category_name_english",
    data=product_df.head(5),
    palette="Greens_r",
    ax=ax
)

ax.set_title("Top 5 Produk Terlaris")
ax.set_xlabel("Total Penjualan")
ax.set_ylabel("Kategori")

st.pyplot(fig)

# ==============================
# 3. Metode pembayaran
# ==============================

st.subheader("Metode Pembayaran Paling Digunakan")

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(
    x="total_usage",
    y="payment_type",
    data=payment_df,
    palette="Oranges_r",
    ax=ax
)

ax.set_title("Distribusi Metode Pembayaran")
ax.set_xlabel("Jumlah Transaksi")
ax.set_ylabel("Metode")

st.pyplot(fig)

# ==============================
# Insight Ringkas
# ==============================

st.subheader("Insight")

top_city = city_df.iloc[0]["customer_city"]
top_product = product_df.iloc[0]["product_category_name_english"]
top_payment = payment_df.iloc[0]["payment_type"]

st.markdown(f"""
- Kota dengan customer terbanyak: **{top_city}**
- Produk paling laris: **{top_product}**
- Metode pembayaran favorit: **{top_payment}**
""")

st.caption("© 2026 Dashboard by You")
