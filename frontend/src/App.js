// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';

// CSS is included directly in the component.
const GlobalStyles = () => (
  <style>{`
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      background-color: #f0f2f5;
      color: #1c1e21;
      margin: 0;
      padding: 0;
    }
    .App { text-align: center; }
    .App-header {
      background-color: #075E54; padding: 20px; color: white;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .App-header h1 { margin: 0; font-size: 2.5rem; }
    main { padding: 20px; max-width: 1200px; margin: 0 auto; }
    .upload-section {
      background-color: white; padding: 30px; border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px;
    }
    .upload-section input[type="file"] {
      margin-top: 15px; border: 1px solid #ddd; padding: 10px; border-radius: 6px;
    }
    .error { color: #d32f2f; margin-top: 10px; font-weight: bold; }
    .loader { font-size: 1.2rem; font-weight: bold; padding: 40px; }
    .results-section {
      background-color: white; padding: 30px; border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-selector { margin-bottom: 30px; }
    .user-selector select {
      padding: 10px; font-size: 1rem; border-radius: 6px; border: 1px solid #ccc;
    }
    .stats-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px; margin-bottom: 30px;
    }
    .stat-card {
      background-color: #e7f3ff; padding: 20px; border-radius: 8px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stat-card h4 { margin: 0 0 10px 0; color: #075E54; }
    .stat-card p { margin: 0; font-size: 2rem; font-weight: bold; }
    .chart-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
      margin-bottom: 40px;
    }
    .chart-container, .wordcloud-container {
      margin-bottom: 40px;
    }
    .wordcloud-container img {
      max-width: 100%; height: auto; border: 1px solid #eee; border-radius: 8px;
    }
    @media (max-width: 768px) {
      .chart-grid { grid-template-columns: 1fr; }
    }
  `}</style>
);

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A28DFF', '#FFD700'];

function App() {
  const [file, setFile] = useState(null);
  const [selectedUser, setSelectedUser] = useState('Overall');
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setAnalysisData(null); 
      setSelectedUser('Overall');
    }
  };

  const handleUserChange = (e) => setSelectedUser(e.target.value);

  const performAnalysis = async (currentUser) => {
    if (!file) return;
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('chatFile', file);
    formData.append('user', currentUser);

    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setAnalysisData(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'A network or server error occurred.';
      setError(errorMsg);
      setAnalysisData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (file) performAnalysis('Overall');
  }, [file]);

  useEffect(() => {
    if (file && analysisData) performAnalysis(selectedUser);
  }, [selectedUser]);

  return (
    <div className="App">
      <GlobalStyles />
      <header className="App-header">
        <h1>TalkTrace</h1>
        <p>Your WhatsApp Chat Analyzer</p>
      </header>
      
      <main>
        <div className="upload-section">
          <h2>Upload your WhatsApp Chat File (.txt)</h2>
          <input type="file" accept=".txt" onChange={handleFileChange} />
          {error && <p className="error">{error}</p>}
        </div>

        {loading && <div className="loader">Analyzing...</div>}

        {analysisData && !error && (
          <div className="results-section">
            <div className="user-selector">
              <h3>Select User to Analyze</h3>
              <select value={selectedUser} onChange={handleUserChange}>
                {analysisData.user_list.map(user => (
                  <option key={user} value={user}>{user}</option>
                ))}
              </select>
            </div>

            <h2>Analysis for: {selectedUser}</h2>

            <div className="stats-grid">
              <div className="stat-card"><h4>Total Messages</h4><p>{analysisData.stats.total_messages}</p></div>
              <div className="stat-card"><h4>Total Words</h4><p>{analysisData.stats.total_words}</p></div>
              <div className="stat-card"><h4>Media Shared</h4><p>{analysisData.stats.media_shared}</p></div>
              <div className="stat-card"><h4>Most Active Time</h4><p>{analysisData.most_active_time}</p></div>
            </div>

            <div className="chart-grid">
              {selectedUser === 'Overall' && (
                <div className="chart-container">
                  <h3>Message Contribution</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie data={analysisData.most_active_users_percent} dataKey="percent" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                        {analysisData.most_active_users_percent.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => `${value}%`} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              )}

              <div className="chart-container">
                <h3>Most Common Words</h3>
                <ResponsiveContainer width="100%" height={300}>
                   <BarChart data={analysisData.common_words} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis type="category" dataKey="word" width={60} />
                      <Tooltip formatter={(value, name) => (name === 'percent' ? `${value}%` : value)} />
                      <Legend />
                      <Bar dataKey="count" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="chart-container">
                <h3>Sentiment Over Time</h3>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={analysisData.sentiment_timeline}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month_year" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="Positive" stroke="#4CAF50" />
                        <Line type="monotone" dataKey="Negative" stroke="#F44336" />
                        <Line type="monotone" dataKey="Neutral" stroke="#FFC107" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            
            <div className="chart-grid">
                <div className="chart-container">
                    <h3>Average Message Length (Words)</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={analysisData.avg_message_length}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="user" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="avg_length" fill="#00C49F" name="Avg. Words"/>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                <div className="chart-container">
                    <h3>Most Used Emojis</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={analysisData.emoji_stats} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis type="number" />
                            <YAxis type="category" dataKey="emoji" width={60} />
                            <Tooltip formatter={(value, name) => (name === 'percent' ? `${value}%` : value)} />
                            <Legend />
                            <Bar dataKey="count" fill="#FFBB28" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {analysisData.wordcloud && (
              <div className="wordcloud-container">
                <h3>Word Cloud</h3>
                <img src={analysisData.wordcloud} alt="Word Cloud" />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
