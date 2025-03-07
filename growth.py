import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper", layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp{
       background-color: black;
       color:white;
       }   
    </style>
    """,
    unsafe_allow_html=True

)
   # Set up our App
st.title("Data Sweeper Sterling Integrator by Komal")
st.write("Transform your files between CVS and Excel formats with build-in data cleaning and visualization!")

   # files uploader
uploaded_files = st.file_uploader("upload your files(accepts CVS or Excel):", type=["cvs","xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
        continue

    # Display info about the file
    st.write(f"**File Name:** {file.name}")
    st.write(f"**File Size:** {file.size/1024}")

    # Show 5 rows of our df
    st.write("Preview the Head of the Dataframe")
    st.dataframe(df.head())

    # Data cleaning option
    st.subheader("Data cleaning option")
    if st.checkbox(f"Clean data for {file.name}"):
       col1, col2 = st.columns(2)

       with col1:
           if st.button(f"Remove duplicates from  : {file.name}"):
               df.drop_duplicates(inplace=True)
               st.write("Duplicates Removed!")

       with col2:
           if st.button(f"Fill missing value for : {file.name}"):
               numeric_cols = df.select_dtypes(include=["numbers"]).columns
               df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
               st.write("Missng values have been Filled")

    # Choose Specific Colums to Keep or Convert           
    st.subheader("Select Columns to Keep")
    columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
    df = df[columns]

    # Creat Some Visualization
    st.subheader("Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

    # Convert the File => CVS to Excel
    st.subheader("Conversion Option")
    conversion_type =st.radio(f"Convert {file.name} to:", ["CVS" , "Excel"], key=file.name)
    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CVS":
            df.to_cvs(buffer, index=False)
            file_name = file.name.replace(file_ext, ".cvs")
            mime_type = "text/cvs"

        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)  

    # Download Button
        st.download_button( 
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

st.success("All files processed successfully!")
