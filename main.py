import streamlit as st
import pandas as pd

# Streamlit UI - Title
st.title("POTATO: Panel-based Open Term-level Aggregate Twitter Observatory")

# Upload File Section
uploaded_file = st.file_uploader("Upload the Twitter TSV file", type="tsv")

if uploaded_file:
    # Load the TSV file into a DataFrame
    df = pd.read_csv(uploaded_file, sep='\t', parse_dates=['created_at'])

    # Clean up columns and ensure proper datetime formatting
    df.columns = df.columns.str.strip()

    df['ts1'] = pd.to_datetime(df['ts1'], errors='coerce')
    df['ts2'] = pd.to_datetime(df['ts2'], errors='coerce')
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)

    st.write("Dataset successfully loaded. Here's a preview of the data:")
    st.dataframe(df.head())  # Display first few rows

    # User Input: Search Term
    term = st.text_input("Enter a term to query (e.g., 'Britney')", "Britney")

    # Functions for querying the data
    def tweets_per_day(df, term):
        filtered_df = df[df['text'].str.contains(term, case=False, na=False)]
        daily_counts = filtered_df.groupby(filtered_df['created_at'].dt.date).size()
        return daily_counts

    def unique_users(df, term):
        filtered_df = df[df['text'].str.contains(term, case=False, na=False)]
        unique_user_count = filtered_df['author_id'].nunique()
        return unique_user_count

    def average_likes(df, term):
        filtered_df = df[df['text'].str.contains(term, case=False, na=False)]
        avg_likes = filtered_df['like_count'].mean()
        return avg_likes

    def place_ids(df, term):
        filtered_df = df[df['text'].str.contains(term, case=False, na=False)]
        places = filtered_df['place_id'].dropna().unique()
        return places

    def tweets_by_time(df, term):
        filtered_df = df[df['text'].str.contains(term, case=False, na=False)]
        tweet_times = filtered_df['created_at'].dt.hour.value_counts().sort_index()
        return tweet_times

    def top_user(df, term):
        filtered_df = df[df['text'].str.contains(term, case=False, na=False)]
        top_user = filtered_df['author_handle'].value_counts().idxmax()
        return top_user

    # Streamlit UI - Display Results

    if st.button("Query Data"):
        st.subheader(f"Results for the term: {term}")
        
        # Display Tweets Per Day
        st.write("### Tweets per day:")
        tweets_day = tweets_per_day(df, term)
        st.bar_chart(tweets_day)

        # Display Unique Users
        st.write(f"### Unique users who tweeted about {term}:")
        st.write(unique_users(df, term))

        # Display Average Likes
        st.write(f"### Average number of likes for tweets containing '{term}':")
        st.write(average_likes(df, term))

        # Display Place IDs
        st.write(f"### Places (IDs) from which tweets about '{term}' originated:")
        st.write(place_ids(df, term))

        # Display Tweet Times (Distribution over hours)
        st.write(f"### Time of day when tweets about '{term}' were posted:")
        tweet_time = tweets_by_time(df, term)
        st.line_chart(tweet_time)

        # Display Top User
        st.write(f"### User who posted the most tweets containing '{term}':")
        st.write(top_user(df, term))

else:
    st.write("Please upload a TSV file to begin querying.")
