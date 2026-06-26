import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

#page configuration
st.set_page_config(page_title="Student Result Analysis",layout="wide")
st.title("🎓Student Result Analysis System")

with st.sidebar:

    st.header("🗂️Upload Datase")
    uploaded_files=st.file_uploader("Upload CSV File",type=["csv"])

    st.markdown("---")

    selected=option_menu(
        menu_title="Menu",
        options=[
           "Raw Data",
           "Student Result",
           "Topper",
           "Search Student",
           "Subject Analysis",
           "Pass/Fail",
           "Pivot Table",
        ],
        icons=[
            "table",
            "bar-chart",
            "trophy",
            "search",
            "book",
            "check-circle",
            "grid"
        ],
        menu_icon="menu-button-wide",
        default_index=0
    )

if uploaded_files is None:
    st.warning("Please Upload a CSV file to continue...")
    st.stop()

df=pd.read_csv(uploaded_files)

if selected=="Raw Data":
    st.subheader("Raw Data")
    st.dataframe(df)

elif selected=="Student Result":
    total=df.groupby("Name")["Marks"].sum()
    avg=df.groupby("Name")["Marks"].mean()

    result=pd.DataFrame({
        "Total":total,
        "Average":avg
    }).reset_index()

    st.dataframe(result)

elif selected=="Topper":
    total=df.groupby("Name")["Marks"].sum().sort_values(ascending=False)

    n=st.number_input("How many toppers do you want?",min_value=1,max_value=len(total),value=1)

    st.subheader(f"Top {n} students")
    st.dataframe(total.head(n))

elif selected=="Search Student":
    st.subheader("Search Student")

    search_name=st.text_input("Enter Student Name")

    if search_name:
        filtered_df=df[df["Name"].str.lower()==search_name.lower()]

        if not filtered_df.empty:
            st.success(f"Showing result for{search_name}")
            st.dataframe(filtered_df) 

            total=filtered_df["Marks"].sum()
            avg=filtered_df["Marks"].mean()

            st.write(f"Total Marks :{total}")
            st.write(f"Percentage : {avg}")
        else:
            st.error("Student not found")

elif selected=="Subject Analysis":
     subject_avg=df.groupby("Subject")["Marks"].mean()
     st.subheader("Subject Wise Average")
     st.dataframe(subject_avg)

elif selected=="Pass/Fail":
    pass_marks=st.slider("Select passing marks",0,100,40)

    df["Result"]=df["Marks"].apply(
        lambda x:"Pass" if x>=pass_marks else "Fail"
    )

    st.subheader("Result") 
    st.dataframe(df)

elif selected=="Pivot Table":
    pivot=df.pivot_table(
        values="Marks",
        index="Name",
        columns="Subject"
    )

    st.subheader("student vs Subject")
    st.dataframe(pivot)








            

    

    