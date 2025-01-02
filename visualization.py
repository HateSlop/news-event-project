import streamlit as st
import pandas as pd
import json
from db_manager import fetch_data

st.sidebar.title("Filtering Option")
filter_option = st.sidebar.selectbox(
    "Select Company", 
    ['Nvidia', 'Google', "Microsoft"], 
    index=0)
start_date = st.sidebar.date_input(
    "Start Date", 
    value=pd.to_datetime("2024-07-01"))
end_date = st.sidebar.date_input(
    "End Date", 
    value=pd.to_datetime("2024-11-30"))


if filter_option:
    data = fetch_data(company=filter_option)

    if data:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
        mask = (data["date"] >= pd.to_datetime(start_date)) & (data["date"] <= pd.to_datetime(end_date))
        data = data[mask]

        st.title(f"{filter_option} Data Visualization")
        st.write("### Main Table")
        main_table = data[["date", "Category", "Main Event"]].reset_index(drop=True)
        st.dataframe(main_table)

        show_summary = st.checkbox("Show Summary")

        if show_summary:
            st.write("### Summary")

            for _, row in data.iterrows():
                date_val = row["date"]
                category_val = row["Category"]
                val = row["Summary"]                    
                if pd.notnull(date_val):
                    date_str = date_val.strftime("%Y-%m-%d")
                else:
                    date_str = "N/A"
                

                if isinstance(val, str) and val.strip():
                    parsed_json = json.loads(val)
                    category = parsed_json["Category"]
                    main_event = parsed_json["Main event"]
                    summary = parsed_json["Summary"]

                    st.write(f"**Date**: {date_str}")
                    st.write(f"**Category**: {category}")
                    st.write(f"**Main Event**: {main_event}")
                    st.write(f"**Summary**: {summary}")
                    st.write("---")
                else:
                    st.write(f"**Date**: {date_str}")
                    st.write(f"**Category**: {category_val}")
                    st.write(f"**Main Event**: N/A")
                    st.write(f"**Summary**: N/A")
                    st.write("---")
        else:
            st.warning("No summary.")
    else:
        st.warning("No data.")
else:
    st.warning("No such company.")