import streamlit as st
import pandas as pd
import json
from db_manager import fetch_data

st.sidebar.title("Filtering Option")
filter_option = st.sidebar.selectbox(
    "Select Company", 
    ["microsoft", "apple", "google"],
    index=0)
start_date = st.sidebar.date_input(
    "Start Date", 
    value=pd.to_datetime("2024-05-01"))
end_date = st.sidebar.date_input(
    "End Date", 
    value=pd.to_datetime("2024-05-25"))

if filter_option:
    data = fetch_data(filter_option)

    # Check if data is a DataFrame and not empty
    if isinstance(data, pd.DataFrame) and not data.empty:
        data["seendate"] = pd.to_datetime(data["seendate"], errors="coerce")
        data["seendate"] = data["seendate"].dt.tz_localize(None)
        mask = (data["seendate"] >= pd.to_datetime(start_date)) & (data["seendate"] <= pd.to_datetime(end_date))
        data = data[mask]

        st.title(f"{filter_option} Data Visualization")
        st.write("### Main Table")
        main_table = data[["seendate", "category", "events"]].reset_index(drop=True)
        st.dataframe(main_table)

        show_summary = st.checkbox("Show Summary")

        if show_summary:
            st.write("### Summary")

            for _, row in data.iterrows():
                date_val = row["seendate"]
                title_val = row["title"]
                category_val = row["category"]
                event_val = row["events"]
                val = row["summary"]
                if pd.notnull(date_val):
                    date_str = date_val.strftime("%Y-%m-%d")
                else:
                    date_str = "N/A"

                if isinstance(val, str) and val.strip():
                    # Check if the value is already in JSON format
                    try:
                        parsed_json = json.loads(val)  # Attempt to parse as JSON
                        title = parsed_json.get("title", "N/A")
                        category = parsed_json.get("category", "N/A")
                        main_event = parsed_json.get("events", "N/A")
                        summary = parsed_json.get("summary", "N/A")
                    except json.JSONDecodeError:
                        # If not valid JSON, use raw summary text
                        title = title_val
                        category = category_val
                        main_event = event_val
                        summary = val
                else:
                    title = title_val
                    category = category_val
                    main_event = event_val
                    summary = "N/A"

                st.write(f"**Title**: {title}")
                st.write(f"**Date**: {date_str}")
                st.write(f"**Category**: {category}")
                st.write(f"**Main Event**: {main_event}")
                st.write(f"**Summary**: {summary}")
                st.write("---")
        else:
            st.warning("No summary.")
    else:
        st.warning("No data or invalid data.")
else:
    st.warning("No such company.")
