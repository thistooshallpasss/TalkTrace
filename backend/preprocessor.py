# backend/preprocessor.py
import re
import pandas as pd

def preprocess(data):
    """
    Cleans and preprocesses raw WhatsApp chat text into a Pandas DataFrame.
    This version is more robust and handles multiple date/time formats,
    including the [DD/MM/YY, HH:MM:SS] format.

    Args:
        data (str): The raw text content of the WhatsApp chat file.

    Returns:
        pandas.DataFrame: A structured DataFrame with columns for date, user, and message.
    """
    # Pattern for [DD/MM/YY, HH:MM:SS] format
    pattern_new = r'\[(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}:\d{2})\]\s([^:]+):\s(.*)'
    messages = re.findall(pattern_new, data)
    
    # If the new pattern fails, try the original ones
    if not messages:
        # Original pattern for DD/MM/YY, HH:MM AM/PM - User: Message
        pattern_orig = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s?[apAPmM]{2})\s-\s([^:]+):\s(.*)'
        messages = re.findall(pattern_orig, data)

    if not messages:
        # Fallback for 24hr format without AM/PM
        pattern_24hr = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)'
        messages = re.findall(pattern_24hr, data)

    # If all patterns fail, return an empty DataFrame
    if not messages:
        return pd.DataFrame()

    df = pd.DataFrame(messages, columns=['date_str', 'time_str', 'user', 'message'])

    # Combine date and time and try parsing with multiple formats
    datetime_str = df['date_str'] + " " + df['time_str']
    
    # List of possible datetime formats to try
    formats_to_try = [
        '%d/%m/%y %H:%M:%S',    # For [11/07/25 15:23:54]
        '%d/%m/%Y %H:%M:%S',   # For [11/07/2025 15:23:54]
        '%d/%m/%y %I:%M %p',    # For 11/07/25 3:23 PM
        '%d/%m/%Y %I:%M %p',   # For 11/07/2025 3:23 PM
        '%m/%d/%y %I:%M %p',    # For 07/11/25 3:23 PM
        '%m/%d/%Y %I:%M %p',   # For 07/11/2025 3:23 PM
        '%d/%m/%y %H:%M',      # For 11/07/25 15:23
        '%d/%m/%Y %H:%M',     # For 11/07/2025 15:23
    ]
    
    parsed_dates = None
    for fmt in formats_to_try:
        try:
            parsed_dates = pd.to_datetime(datetime_str, format=fmt)
            # If parsing is successful, break the loop
            break 
        except ValueError:
            # If parsing fails, try the next format
            continue
            
    # If no format matched, we cannot proceed
    if parsed_dates is None:
         # This will now return an empty DF if no format matches after trying all of them
        return pd.DataFrame()

    df['date'] = parsed_dates
    df.drop(columns=['date_str', 'time_str'], inplace=True)

    # Extract additional time features
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create a period for hourly activity analysis
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df
