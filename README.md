TalkTrace 💬 | WhatsApp Chat Analyzer
TalkTrace is a full-stack web application that transforms your raw WhatsApp chat history into a beautiful, interactive analytics dashboard. Upload your exported .txt file and gain deep insights into communication patterns, user activity, content trends, and sentiment over time.

✨ Key Features
📊 Overall Statistics: Get a high-level overview including total messages, words, media, and links shared.

👤 User-Specific Analysis: Use the dropdown to filter the entire dashboard for a specific user's activity.

🏆 Activity Ranking:

Contribution Pie Chart: Visualize the percentage of messages sent by each user.

Most Active Time: Instantly find out the peak hour for conversations.

📈 Timeline Visualization:

Daily & Monthly Trends: Track the chat's activity over time with interactive line charts.

Weekly Activity Heatmap: Discover the most active day of the week and hour of the day.

📝 Content & Language Insights:

Most Common Words: See the top 10 most used words with their frequency and percentage.

Word Cloud: A visual representation of the most prominent words in the chat.

Emoji Analysis: Find out the most popular emojis and who uses them.

Average Message Length: Compare the verbosity of different users.

😊 Sentiment Analysis:

Sentiment Over Time: Track the trend of positive, negative, and neutral messages on a monthly basis.

🛠️ Tech Stack
Frontend:

React.js: For building the interactive user interface.

Recharts: For creating beautiful and responsive charts.

Axios: For making API requests to the backend.

Hosted on Netlify.

Backend:

Python: The core language for data processing and analysis.

Flask: A micro web framework to create the REST API.

Pandas: For efficient data manipulation and structuring.

NLTK (Vader): For performing sentiment analysis.

WordCloud: For generating word cloud images.

Gunicorn: As the production WSGI server.

Hosted on Render.

🚀 Local Setup and Installation
To run this project on your local machine, follow these steps:

1. Backend Setup

# Clone the backend repository

git clone https://github.com/your-username/talktrace-backend.git
cd talktrace-backend

# Create and activate a virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Download NLTK data (one-time setup)

python -c "import nltk; nltk.download('vader_lexicon')"

# Run the Flask server

python app.py

The backend will be running at http://127.0.0.1:5000.

2. Frontend Setup

# Clone the frontend repository in a new terminal

git clone https://github.com/your-username/talktrace-frontend.git
cd talktrace-frontend

# Install dependencies

npm install

# Run the React development server

npm start

The frontend will open in your browser at http://localhost:3000.

Screenshots
(Here you can add screenshots of your application dashboard)

Caption: The main dashboard showing overall chat analysis.

Author
Harsh Ramsurat Yadav
