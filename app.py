#!/usr/bin/python3

import numpy as np
import pandas as pd
import streamlit as st

from algorithms import find_s, candidate_elimination

# Suppress warnings
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("Concept Learning Algorithms")

st.subheader("You can use anyone of the input methods!")
uploaded_file = st.file_uploader("Upload your dataset", type="csv")
text_input = st.text_area("Enter the data: columns separated by ',' and rows in newline\n(after writing data press ctrl+enter)")

if len(text_input) != 0 or uploaded_file is not None:
    header = st.checkbox("Does dataset contain header?")
    if uploaded_file is not None:
        if header is False:
            data = pd.read_csv(uploaded_file, header=None)
        else:
            data = pd.read_csv(uploaded_file)
    else:
        if len(text_input) != 0:
            data = pd.DataFrame(list(map(lambda x: x.split(','), text_input.split())))

            if header is True:
                data.columns = data.iloc[0]
                data.drop(0, inplace=True)

    show_data = st.checkbox("Show Data")
    if show_data:
        st.dataframe(data)

    label_col = st.selectbox("Select the Label columns", options=data.columns, index=len(data.columns)-1)
    pos_label = st.selectbox("What is the value of positive label?", options=data[label_col].unique())

    algo = st.sidebar.selectbox("Select the algorithm", ['Find S', 'Candidate Elimination'])

    if algo == 'Find S':
        find_s(data.loc[:, data.columns != label_col].values, data[label_col].values, pos=pos_label, print_funct=st.write)
    elif algo == 'Candidate Elimination':
        candidate_elimination(data.loc[:, data.columns != label_col].values, data[label_col].values, pos=pos_label, print_funct=st.write)