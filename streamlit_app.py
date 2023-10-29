import streamlit as st
import pandas as pd
import yfinance as yf


def calcem():

    # Define pre-election years (replace with your list of pre-election years)
    pre_election_years = [1931, 1935, 1939, 1943, 1947, 1951, 1955, 1959, 1963, 
                        1967, 1971, 1975, 1979, 1983, 1987, 1991, 1995, 1999, 
                        2003, 2007, 2011, 2015, 2019, 2023]

    # Get the spx data from yfinance
    sp500 = yf.Ticker('^GSPC')
    sp500df = sp500.history(period='max')

    # Remove the rows from sp500df that have a year of 1927
    sp500df = sp500df.drop(sp500df.loc[sp500df.index.year == 1927].index)

    # Split the sp500df DataFrame into two DataFrames based on the year
    df_before_election_years = sp500df.loc[sp500df.index.year.isin(pre_election_years)]
    df_other_years = sp500df.loc[~sp500df.index.year.isin(pre_election_years)]

    # Filter the data for December
    df_before_election_years_december = df_before_election_years[df_before_election_years.index.month == 12]
    df_other_years_december = df_other_years[df_other_years.index.month == 12]

    # Find the last record of each year in December for pre-election years
    pre_election_december_last = df_before_election_years_december.groupby(df_before_election_years_december.index.year).tail(1)

    # Find the last record of each year in December for other years
    other_years_december_last = df_other_years_december.groupby(df_other_years_december.index.year).tail(1)

    # Calculate the gain difference for the 10th to last trading day and the last trading day of December for pre-election years
    pre_election_december_10_last = df_before_election_years_december.groupby(df_before_election_years_december.index.year).tail(10)
    pre_election_10th_to_last = pre_election_december_10_last.groupby(pre_election_december_10_last.index.year).head(1)

    # Calculate the gain difference for the 10th to last trading day and the last trading day of December for other years
    other_years_december_10_last = df_other_years_december.groupby(df_other_years_december.index.year).tail(10)
    other_years_10th_to_last = other_years_december_10_last.groupby(other_years_december_10_last.index.year).head(1)

    # Resample both DataFrames to have the same frequency (i.e., annual) and calculate the difference for pre-election years
    pre_election_december_last_resampled = pre_election_december_last['Close'].resample('A').sum()
    pre_election_10th_to_last_resampled = pre_election_10th_to_last['Close'].resample('A').sum()

    # Calculate the percentage difference and get rid of the irrelevant years for pre-election years
    pre_election_difference_series = (pre_election_december_last_resampled - pre_election_10th_to_last_resampled) / pre_election_10th_to_last_resampled * 100
    pre_election_difference_series.dropna(inplace=True)

    # Create a new DataFrame with the 'Date' and 'Percentage Difference' for pre-election years
    pre_election_difference_df = pd.DataFrame({'Date': pre_election_difference_series.index, 'Percentage Difference': pre_election_difference_series.values})

    # Resample both DataFrames to have the same frequency (i.e., annual) and calculate the difference for other years
    other_years_december_last_resampled = other_years_december_last['Close'].resample('A').sum()
    other_years_10th_to_last_resampled = other_years_10th_to_last['Close'].resample('A').sum()

    # Calculate the percentage difference and get rid of the irrelevant years for other years
    other_years_difference_series = (other_years_december_last_resampled - other_years_10th_to_last_resampled) / other_years_10th_to_last_resampled * 100
    other_years_difference_series.dropna(inplace=True)

    # Create a new DataFrame with the 'Date' and 'Percentage Difference' for other years
    other_years_difference_df = pd.DataFrame({'Date': other_years_difference_series.index, 'Percentage Difference': other_years_difference_series.values})

    # Display the resulting DataFrames
    # print("Pre-election Years Difference:")
    # print(pre_election_difference_df)

    # print("\nOther Years Difference:")
    # print(other_years_difference_df)

    # Calculate the average of the "Percentage Difference" column for pre-election years
    pre_election_avg = pre_election_difference_df['Percentage Difference'].mean()

    # Calculate the average of the "Percentage Difference" column for other years
    other_years_avg = other_years_difference_df['Percentage Difference'].mean()

    return(pre_election_difference_df, other_years_difference_df, pre_election_avg, other_years_avg)


def main():
    pre_election_difference_df, other_years_difference_df, pre_election_avg, other_years_avg = calcem()
    st.title("Stock Analysis App")

    # Display the results using Streamlit widgets
    st.subheader("Pre-election Years Average Percentage Difference:")
    st.write("{:.2f}%".format(pre_election_avg))

    st.subheader("Other Years Average Percentage Difference:")
    st.write("{:.2f}%".format(other_years_avg))

    # Line chart for pre-election years
    st.subheader("Line Chart for Pre-election Years Difference")
    st.line_chart(pre_election_difference_df.set_index('Date'))

    # Line chart for other years
    st.subheader("Line Chart for Other Years Difference")
    st.line_chart(other_years_difference_df.set_index('Date'))

    # Dataframe data in table presentation
    st.subheader("Pre-election Years Difference:")
    st.write(pre_election_difference_df)

    st.subheader("Other Years Difference:")
    st.write(other_years_difference_df)

if __name__ == "__main__":
    main()
