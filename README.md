# 2026 World Cup Bracket Predictor

A web application for 2026 World Cup predictions with a dynamic scoring system. Users can create their brackets before each knockout stage and earn points based on how early they made their predictions.

## 🎯 Features

- **Dynamic scoring system**: Multipliers that vary based on prediction window (P1-P5)
- **Interactive bracket**: Visual interface to select winners of each match
- **Admin panel**: Control prediction windows and load match results
- **Real-time leaderboard**: Player rankings with point breakdown
- **Cloud database**: Supabase integration for data persistence
- **Modern design**: Dark UI with gold accents

## 📊 Scoring System

### Base Points per Round
- Round of 16: 10 pts
- Quarter-finals: 20 pts
- Semi-finals: 40 pts
- Finals: 80 pts
- Finalist: 150 pts
- Champion: 300 pts

### Anticipation Multipliers
- **P1 (Start)**: ×4 - Perfect initial bracket
- **P2 (Round of 16)**: ×3 - After group stage
- **P3 (Quarter-finals)**: ×2 - Clear picture
- **P4 (Semi-finals)**: ×1.5 - Final 4 teams
- **P5 (Final)**: ×1 - Direct single match prediction

### Critical Rule
Points are not cumulative between windows. Only the most recent prediction version counts. If you modify your prediction, you lose multipliers from previous windows.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- [Supabase](https://supabase.com) account

### 1. Clone the repository
```bash
git clone https://github.com/aleex-cs/2026wc-pred.git
cd 2026wc-pred
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Supabase

1. Create a project at [supabase.com](https://supabase.com)
2. Go to Settings → API and copy your `Project URL` and `anon public key`
3. Create the file `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "your_project_url"
SUPABASE_KEY = "your_anon_key"
ADMIN_PASSWORD = "your_admin_password"
```

### 4. Set up the database

Run the following SQL in Supabase SQL Editor:

```sql
-- Tournament results table
CREATE TABLE results (
    id SERIAL PRIMARY KEY,
    ronda VARCHAR(50) NOT NULL,
    equipo VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User predictions table
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    prediction_window VARCHAR(10) NOT NULL,
    ronda VARCHAR(50) NOT NULL,
    equipos JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(username, prediction_window)
);

-- Prediction locks table
CREATE TABLE prediction_locks (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    prediction_window VARCHAR(10) NOT NULL,
    locked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(username, prediction_window)
);

-- Window state table (admin control)
CREATE TABLE windows_state (
    prediction_window VARCHAR(10) PRIMARY KEY,
    enabled BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Insert initial window states
INSERT INTO windows_state (prediction_window, enabled) VALUES
    ('P1', true),
    ('P2', true),
    ('P3', true),
    ('P4', true),
    ('P5', true)
ON CONFLICT (prediction_window) DO NOTHING;

-- Performance indexes
CREATE INDEX idx_results_ronda ON results(ronda);
CREATE INDEX idx_predictions_username ON predictions(username);
CREATE INDEX idx_predictions_window ON predictions(prediction_window);
CREATE INDEX idx_prediction_locks_username ON prediction_locks(username);
```

### 5. Run the application
```bash
streamlit run app.py
```

## 👥 Usage

### For Players

1. **Create account**: Register with a username and password
2. **Make predictions**: Go to "My Prediction" and select winners for each match
3. **Lock prediction**: Once the bracket is complete, confirm to lock it
4. **View leaderboard**: Check rankings and your points in "Leaderboard"
5. **Review rules**: Check the scoring system in "Rules"

### For Administrators

1. **Login as admin**: Use username "admin" with the configured password
2. **Load results**: In the Admin panel, load qualified teams for each round
3. **Control windows**: Enable/disable prediction windows based on tournament stage
4. **Manage users**: View all registered users and their locked predictions

## 📁 Project Structure

```
worldcup_app/
├── app.py                 # Main page
├── auth.py                # Authentication system
├── config.py              # Tournament configuration
├── data_manager.py        # Data management (Supabase)
├── scoring.py             # Score calculation
├── styles.py              # Custom CSS styles
├── requirements.txt       # Python dependencies
├── pages/
│   ├── 1___Predicción.py  # Predictions page
│   ├── 2___Clasificación.py # Leaderboard page
│   ├── 3___Admin.py       # Admin panel
│   └── 4___Reglamento.py  # Scoring rules
└── .streamlit/
    └── secrets.toml        # Supabase credentials
```

## 🔧 Configuration

### Prediction Windows

Windows activate automatically based on loaded results:
- **P1**: Before round of 16 results
- **P2**: After loading round of 16 results
- **P3**: After loading quarter-final results
- **P4**: After loading semi-final results
- **P5**: After loading final results

Admin can manually enable/disable any window from the admin panel.

## 🏆 Participating Teams

The tournament includes 32 teams divided into round of 16 matchups:

**Left side**: Germany, Paraguay, France, Sweden, South Africa, Canada, Netherlands, Morocco, Portugal, Croatia, Spain, Austria, United States, Bosnia & H., Belgium, Senegal

**Right side**: Brazil, Japan, Ivory Coast, Norway, Mexico, Ecuador, England, DR Congo, Argentina, Cape Verde, Australia, Egypt, Switzerland, Algeria, Colombia, Ghana

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome. If you find a bug or have a suggestion, open an issue in the repository.

## 📧 Contact

For any questions, reach out through the GitHub repository.
