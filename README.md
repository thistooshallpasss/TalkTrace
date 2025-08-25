# TalkTrace 💬 | WhatsApp Chat Analyzer

**TalkTrace** is a full-stack web application that transforms your raw WhatsApp chat history into a beautiful, interactive analytics dashboard.  
Upload your exported `.txt` file and gain deep insights into communication patterns, user activity, content trends, and sentiment over time.

---

## ✨ Key Features

### 📊 Overall Statistics  
- High-level overview including total messages, words, media, and links shared.

### 👤 User-Specific Analysis  
- Use the dropdown to filter the entire dashboard for a specific user's activity.

### 🏆 Activity Ranking  
- **Contribution Pie Chart**: Visualize the percentage of messages sent by each user.  
- **Most Active Time**: Instantly find out the peak hour for conversations.

### 📈 Timeline Visualization  
- **Daily & Monthly Trends**: Track the chat's activity over time with interactive line charts.  
- **Weekly Activity Heatmap**: Discover the most active day of the week and hour of the day.

### 📝 Content & Language Insights  
- **Most Common Words**: See the top 10 most used words with their frequency and percentage.  
- **Word Cloud**: A visual representation of the most prominent words in the chat.  
- **Emoji Analysis**: Find out the most popular emojis and who uses them.  
- **Average Message Length**: Compare the verbosity of different users.

### 😊 Sentiment Analysis  
- **Sentiment Over Time**: Track the trend of positive, negative, and neutral messages on a monthly basis.

---

## 🛠️ Tech Stack

### Frontend  
- **React.js** → Interactive user interface  
- **Recharts** → Beautiful & responsive charts  
- **Axios** → API communication  
- **Netlify** → Deployment  

### Backend  
- **Python** → Data processing & analysis  
- **Flask** → REST API  
- **Pandas** → Data manipulation  
- **NLTK (VADER)** → Sentiment analysis  
- **WordCloud** → Generate word clouds  
- **Gunicorn** → Production WSGI server  
- **Render** → Deployment  

---

## 🚀 Local Setup & Installation

### 1️⃣ Backend Setup

```bash
# Clone the backend repository
git clone https://github.com/your-username/talktrace-backend.git
cd talktrace-backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (one-time setup)
python -c "import nltk; nltk.download('vader_lexicon')"

# Run the Flask server
python app.py
```


Backend will run at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### 2️⃣ Frontend Setup

```bash
# Clone the frontend repository in a new terminal
git clone https://github.com/your-username/talktrace-frontend.git
cd talktrace-frontend

# Install dependencies
npm install

# Run the React development server
npm start
```

Frontend will run at **[http://localhost:3000](http://localhost:3000)**

---

## 📸 Screenshots

*Add screenshots here of your dashboard UI and analytics.*

**Example:**
![Dashboard Screenshot](./screenshots/dashboard.png)
*Caption: The main dashboard showing overall chat analysis.*

---

## 👨‍💻 Author

**Harsh Ramsurat Yadav**

---

