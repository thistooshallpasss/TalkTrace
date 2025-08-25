# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import preprocessor
import analyzer
import traceback 

app = Flask(__name__)
# Add your Vercel URL to the list
CORS(app, resources={r"/analyze": {"origins": ["http://localhost:3000", "https://talk-trace.vercel.app/"]}})

@app.route('/analyze', methods=['POST'])
def analyze_chat():
    """
    API endpoint to analyze a WhatsApp chat file with expanded analytics.
    """
    try:
        if 'chatFile' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['chatFile']
        selected_user = request.form.get('user', 'Overall')

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            data = file.stream.read().decode("utf-8")
            
            df = preprocessor.preprocess(data)

            if df.empty:
                 return jsonify({"error": "Could not process the chat file. Please check if it's a valid WhatsApp export."}), 400

            user_list = df['user'].unique().tolist()
            if 'group_notification' in user_list:
                user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0, "Overall")

            df_filtered = df[df['user'] == selected_user] if selected_user != "Overall" else df

            # --- Calling all analysis functions ---
            stats = analyzer.fetch_stats(df_filtered)
            most_active_users_percent = analyzer.fetch_most_active_users(df) # Overall contribution
            wordcloud_base64 = analyzer.create_wordcloud_base64(df_filtered)
            common_words = analyzer.get_most_common_words(df_filtered)
            emoji_stats = analyzer.get_emoji_stats(df_filtered)
            monthly_timeline = analyzer.get_monthly_timeline(df_filtered)
            daily_timeline = analyzer.get_daily_timeline(df_filtered)
            weekly_activity = analyzer.get_weekly_activity(df_filtered)
            activity_heatmap = analyzer.get_activity_heatmap(df_filtered)
            
            # New analysis functions
            avg_message_length = analyzer.get_avg_message_length(df_filtered if selected_user != 'Overall' else df)
            sentiment_timeline = analyzer.get_sentiment_timeline(df_filtered)
            most_active_time = analyzer.get_most_active_time(df_filtered)


            return jsonify({
                "user_list": user_list,
                "stats": stats,
                "most_active_users_percent": most_active_users_percent,
                "wordcloud": wordcloud_base64,
                "common_words": common_words,
                "emoji_stats": emoji_stats,
                "monthly_timeline": monthly_timeline,
                "daily_timeline": daily_timeline,
                "weekly_activity": weekly_activity,
                "activity_heatmap": activity_heatmap,
                "avg_message_length": avg_message_length,
                "sentiment_timeline": sentiment_timeline,
                "most_active_time": most_active_time
            })

    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())
        return jsonify({"error": "An internal server error occurred. Check the backend console for details."}), 500

    return jsonify({"error": "Invalid file or request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
