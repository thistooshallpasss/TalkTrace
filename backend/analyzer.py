# backend/analyzer.py
from collections import Counter
import pandas as pd
from wordcloud import WordCloud
import emoji
import io
import base64
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Load stop words
try:
    with open("stop_hinglish.txt", 'r') as f:
        stop_words = f.read().split()
except FileNotFoundError:
    stop_words = [] # Fallback to an empty list if file not found


def fetch_stats(df):
    """Calculates and returns key statistics of the chat."""
    num_messages = df.shape[0]
    words = [word for message in df['message'] for word in message.split()]
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = [word for message in df['message'] for word in message.split() if 'http' in word]
    
    return {
        "total_messages": num_messages,
        "total_words": len(words),
        "media_shared": num_media_messages,
        "links_shared": len(links)
    }

def fetch_most_active_users(df):
    """Returns the most active users and their message contribution percentage."""
    # We only care about actual users, not group notifications
    user_counts = df['user'].value_counts().head()
    
    total_messages = df.shape[0]
    user_percentages = round((df['user'].value_counts() / total_messages) * 100, 2).reset_index()
    user_percentages.columns = ['name', 'percent']
    
    return user_percentages.to_dict('records')

def create_wordcloud_base64(df):
    """Generates a word cloud and returns it as a base64 encoded string."""
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    
    def remove_stop_words(message):
        return " ".join([word for word in message.lower().split() if word not in stop_words])

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    
    # Handle cases where there are no words left after filtering
    if temp['message'].str.cat(sep=" ").strip() == "":
        return None

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    
    img_bytes = io.BytesIO()
    df_wc.to_image().save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    base64_string = base64.b64encode(img_bytes.read()).decode('utf-8')
    return "data:image/png;base64," + base64_string


def get_most_common_words(df):
    """Finds the most common words and their percentage contribution."""
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    total_words = len(words)
    if total_words == 0:
        return []

    word_counts = Counter(words).most_common(10)
    most_common_list = []
    for word, count in word_counts:
        most_common_list.append({
            "word": word,
            "count": count,
            "percent": round((count / total_words) * 100, 2)
        })
        
    return most_common_list

def get_emoji_stats(df):
    """Analyzes emoji usage and calculates percentage contribution."""
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        
    total_emojis = len(emojis)
    if total_emojis == 0:
        return []

    emoji_counts = Counter(emojis).most_common(10)
    emoji_list = []
    for item, count in emoji_counts:
        emoji_list.append({
            "emoji": item,
            "count": count,
            "percent": round((count / total_emojis) * 100, 2)
        })
        
    return emoji_list

def get_monthly_timeline(df):
    """Returns the message count timeline on a monthly basis."""
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline[['time', 'message']].to_dict('records')

def get_daily_timeline(df):
    """Returns the message count timeline on a daily basis."""
    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    daily_timeline['only_date'] = daily_timeline['only_date'].astype(str)
    return daily_timeline.to_dict('records')

def get_weekly_activity(df):
    """Returns the activity map for days of the week."""
    activity_map = df['day_name'].value_counts().reset_index()
    activity_map.columns = ['day', 'count']
    return activity_map.to_dict('records')

def get_activity_heatmap(df):
    """Generates a pivot table for an activity heatmap."""
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap.to_dict()

def get_avg_message_length(df):
    """Calculates the average message length (in words) per user."""
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    temp['word_count'] = temp['message'].apply(lambda s: len(s.split()))
    avg_length_df = temp.groupby('user')['word_count'].mean().round(2).reset_index()
    avg_length_df.columns = ['user', 'avg_length']
    return avg_length_df.sort_values('avg_length', ascending=False).to_dict('records')

def get_sentiment_timeline(df):
    """Performs sentiment analysis on messages over time."""
    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')].copy()
    
    # Filter out non-string messages just in case
    temp = temp[temp['message'].apply(lambda x: isinstance(x, str))]

    temp['sentiment'] = temp['message'].apply(lambda msg: sentiment_analyzer.polarity_scores(msg)['compound'])
    
    # Classify sentiment
    temp['sentiment_label'] = temp['sentiment'].apply(lambda score: 'Positive' if score > 0.05 else ('Negative' if score < -0.05 else 'Neutral'))
    
    # Create a timeline
    temp['month_year'] = temp['date'].dt.strftime('%Y-%m')
    sentiment_timeline = temp.groupby(['month_year', 'sentiment_label']).size().unstack(fill_value=0).reset_index()
    
    return sentiment_timeline.to_dict('records')

def get_most_active_time(df):
    """Finds the most active hour of the day."""
    # The 'period' column is already in the format 'HH-HH+1'
    most_active = df['period'].value_counts().head(1)
    if most_active.empty:
        return "N/A"
    return most_active.index[0]

