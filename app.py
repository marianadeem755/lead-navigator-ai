import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib
import sqlite3
import secrets
import io
import json

# Custom CSS Styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Main background gradient */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
            border-right: 3px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        /* Main content area */
        .main .block-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin: 1rem;
        }
        
        /* Headers */
        h1 {
            color: #2d3748;
            font-weight: 800;
            font-size: 2.5rem !important;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        h2 {
            color: #4a5568;
            font-weight: 700;
            font-size: 1.8rem !important;
            margin-top: 1.5rem;
        }
        
        h3 {
            color: #718096;
            font-weight: 600;
            font-size: 1.3rem !important;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700;
            color: #667eea !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-weight: 600;
            color: #4a5568 !important;
            font-size: 0.9rem !important;
        }
        
        [data-testid="stMetricDelta"] {
            font-weight: 600;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Form buttons */
        .stForm button[type="submit"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stForm button[type="submit"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5);
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 0.6rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
        }
        
        .stTabs [aria-selected="true"] {
            background: white;
            color: #667eea;
        }
        
        /* Dataframes */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stInfoBox"] {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            border: none;
            color: white;
        }
        
        [data-testid="stSuccessBox"] {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            border: none;
            color: white;
        }
        
        [data-testid="stWarningBox"] {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border: none;
            color: white;
        }
        
        [data-testid="stErrorBox"] {
            background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
            border: none;
            color: white;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 10px;
            font-weight: 600;
            color: #2d3748;
        }
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 2rem;
            background: rgba(102, 126, 234, 0.05);
        }
        
        /* Download button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(17, 153, 142, 0.6);
        }
        
        # /* Sliders */
        # .stSlider > div > div > div {
        #     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        # }
        
        /* Radio buttons */
        [data-testid="stRadio"] > div {
            background: rgba(102, 126, 234, 0.05);
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Divider */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 2rem 0;
        }
        
        /* Custom badge */
        .custom-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Loading animation */
        .stSpinner > div {
            border-color: #667eea !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        </style>
    """, unsafe_allow_html=True)

# Color palettes for charts
COLOR_PALETTES = {
    'primary': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
    'purple': ['#667eea', '#764ba2', '#9f7aea', '#805ad5', '#6b46c1', '#553c9a'],
    'gradient': ['#11998e', '#38ef7d', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'],
    'sunset': ['#f093fb', '#f5576c', '#fa709a', '#fee140', '#ff9a56', '#ff6a00'],
    'ocean': ['#4facfe', '#00f2fe', '#667eea', '#764ba2', '#43e97b', '#38f9d7'],
    'fire': ['#ee0979', '#ff6a00', '#f5576c', '#fa709a', '#fee140', '#ffd89b']
}

# Page config
st.set_page_config(
    page_title="DAN HHS Buyer Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_custom_css()

# Database setup with improved connection handling
def get_db_connection():
    """Get a new database connection with timeout"""
    conn = sqlite3.connect('buyers_dashboard.db', check_same_thread=False, timeout=10.0)
    conn.execute('PRAGMA journal_mode=WAL')
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT DEFAULT 'Viewer',
                  created_at TEXT,
                  last_login TEXT)''')
    
    # Magic links table
    c.execute('''CREATE TABLE IF NOT EXISTS magic_links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT NOT NULL,
                  token TEXT UNIQUE NOT NULL,
                  created_at TEXT,
                  expires_at TEXT,
                  used INTEGER DEFAULT 0)''')
    
    # Audit log table
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_email TEXT,
                  action TEXT,
                  timestamp TEXT,
                  details TEXT)''')
    
    # Upload history table
    c.execute('''CREATE TABLE IF NOT EXISTS upload_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_email TEXT,
                  filename TEXT,
                  upload_date TEXT,
                  row_count INTEGER,
                  file_data TEXT)''')
    
    # Saved segments table
    c.execute('''CREATE TABLE IF NOT EXISTS saved_segments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_email TEXT,
                  segment_name TEXT,
                  filters TEXT,
                  created_at TEXT)''')
    
    conn.commit()
    conn.close()
    return True

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password
def verify_password(password, hashed):
    return hash_password(password) == hashed

# Create user with improved error handling
def create_user(email, password, role='Viewer'):
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        hashed_pw = hash_password(password)
        now = datetime.now().isoformat()
        c.execute('INSERT INTO users (email, password, role, created_at) VALUES (?, ?, ?, ?)',
                  (email, hashed_pw, role, now))
        conn.commit()
        log_audit(email, 'User Created', f'New user registered: {email}')
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        st.error(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Verify user
def verify_user(email, password):
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT password, role FROM users WHERE email = ?', (email,))
        result = c.fetchone()
        if result and verify_password(password, result[0]):
            now = datetime.now().isoformat()
            c.execute('UPDATE users SET last_login = ? WHERE email = ?', (now, email))
            conn.commit()
            log_audit(email, 'Login', 'User logged in')
            return True, result[1]
        return False, None
    finally:
        if conn:
            conn.close()

# Generate magic link
def generate_magic_link(email):
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT email FROM users WHERE email = ?', (email,))
        if not c.fetchone():
            return None
        
        token = secrets.token_urlsafe(32)
        created_at = datetime.now()
        expires_at = created_at + timedelta(hours=1)
        
        c.execute('INSERT INTO magic_links (email, token, created_at, expires_at) VALUES (?, ?, ?, ?)',
                  (email, token, created_at.isoformat(), expires_at.isoformat()))
        conn.commit()
        
        magic_url = f"?token={token}"
        return magic_url
    finally:
        if conn:
            conn.close()

# Verify magic link
def verify_magic_link(token):
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''SELECT email, expires_at, used FROM magic_links 
                     WHERE token = ? AND used = 0''', (token,))
        result = c.fetchone()
        
        if result:
            email, expires_at, used = result
            if datetime.now() < datetime.fromisoformat(expires_at):
                c.execute('UPDATE magic_links SET used = 1 WHERE token = ?', (token,))
                now = datetime.now().isoformat()
                c.execute('UPDATE users SET last_login = ? WHERE email = ?', (now, email))
                conn.commit()
                
                c.execute('SELECT role FROM users WHERE email = ?', (email,))
                role = c.fetchone()[0]
                log_audit(email, 'Magic Link Login', 'User logged in via magic link')
                return email, role
        return None, None
    finally:
        if conn:
            conn.close()

# Audit logging with separate connection
def log_audit(user_email, action, details=''):
    conn = None
    try:
        conn = get_db_connection()
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute('INSERT INTO audit_log (user_email, action, timestamp, details) VALUES (?, ?, ?, ?)',
                  (user_email, action, timestamp, details))
        conn.commit()
    except Exception as e:
        print(f"Audit log error: {e}")
    finally:
        if conn:
            conn.close()

# Initialize database
init_db()

# Create default admin if no users exist
conn = get_db_connection()
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM users')
if c.fetchone()[0] == 0:
    create_user('admin@danhhs.com', 'admin123', 'Owner')
conn.close()

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'data' not in st.session_state:
    st.session_state.data = None
if 'saved_segments' not in st.session_state:
    st.session_state.saved_segments = []
if 'current_file_hash' not in st.session_state:
    st.session_state.current_file_hash = None
if 'search_result' not in st.session_state:
    st.session_state.search_result = None

# Helper function to get file hash
def get_file_hash(file_content):
    """Generate hash of file content to check if it's the same file"""
    return hashlib.md5(file_content).hexdigest()

# Check for magic link token
query_params = st.query_params
if 'token' in query_params and not st.session_state.authenticated:
    token = query_params['token']
    email, role = verify_magic_link(token)
    if email:
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.session_state.user_role = role
        st.rerun()

# Authentication page
def show_auth_page():
    st.markdown("<h1 style='text-align: center;'>🎯 DAN HHS Buyer Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #718096;'>Analytics Dashboard</p>", unsafe_allow_html=True)
    
    st.info("**Default Login Credentials:**\n\nEmail: `admin@danhhs.com`\n\nPassword: `admin123`")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "✨ Create Account", "🔗 Magic Link"])
    
    with tab1:
        st.subheader("Login to Dashboard")
        with st.form("login_form"):
            email = st.text_input("📧 Email", value="admin@danhhs.com")
            password = st.text_input("🔒 Password", type="password", value="admin123")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if email and password:
                    success, role = verify_user(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_role = role
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.warning("Please enter both email and password")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("signup_form"):
            new_email = st.text_input("📧 Email", key="signup_email")
            new_password = st.text_input("🔒 Password", type="password", key="signup_password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            submit_signup = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit_signup:
                if new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        if create_user(new_email, new_password):
                            st.success("Account created! Please login.")
                        else:
                            st.error("Email already exists")
                else:
                    st.warning("Please fill in all fields")
    
    with tab3:
        st.subheader("Magic Link Login")
        st.write("Enter your email to receive a magic link")
        with st.form("magic_link_form"):
            magic_email = st.text_input("📧 Email", key="magic_email")
            submit_magic = st.form_submit_button("Send Magic Link", use_container_width=True)
            
            if submit_magic:
                if magic_email:
                    magic_url = generate_magic_link(magic_email)
                    if magic_url:
                        st.success("Magic link generated!")
                        st.info(f"Click this link to login: {st.query_params.to_dict().get('', 'http://localhost:8501')}{magic_url}")
                        st.caption("In production, this would be sent via email")
                        log_audit(magic_email, 'Magic Link Generated', 'Magic link requested')
                    else:
                        st.error("Email not found")
                else:
                    st.warning("Please enter your email")

# Load data function
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read()
            file_hash = get_file_hash(file_content)
            
            if st.session_state.current_file_hash == file_hash:
                return st.session_state.data
            
            uploaded_file.seek(0)
            
            first_lines = []
            for i, line in enumerate(uploaded_file):
                if i < 5:
                    first_lines.append(line.decode('utf-8') if isinstance(line, bytes) else line)
                else:
                    break
            
            uploaded_file.seek(0)
            skip_rows = 0
            
            if 'Combo Conversion' in first_lines[0] or 'visitors =' in first_lines[0]:
                skip_rows = 1
                if len(first_lines) > 1 and 'Min Visitors' in first_lines[1] and '40' in first_lines[1]:
                    skip_rows = 2
            
            if skip_rows > 0:
                df = pd.read_csv(uploaded_file, skiprows=skip_rows)
            else:
                df = pd.read_csv(uploaded_file)
            
            df.columns = df.columns.str.strip()
            
            if any('Unnamed' in str(col) for col in df.columns):
                uploaded_file.seek(0)
                lines = uploaded_file.readlines()
                
                header_line_idx = None
                for idx, line in enumerate(lines):
                    line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                    if 'Rank' in line_str and 'Combo Size' in line_str:
                        header_line_idx = idx
                        break
                
                if header_line_idx is not None:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, skiprows=header_line_idx)
                    df.columns = df.columns.str.strip()
            
            column_mapping = {
                'Purchaser': 'Purchasers',
                'Conversion%': 'Conversion %',
                'Conversion': 'Conversion %',
                'Combo_Size': 'Combo Size',
                'ComboSize': 'Combo Size',
                'Min_Visitors': 'Min Visitors',
                'MinVisitors': 'Min Visitors',
                'Combo Cc': 'Combo_Cc',
                'ComboConversion %': 'Conversion %'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df.rename(columns={old_col: new_col}, inplace=True)
            
            required_columns = ['Rank', 'Combo Size', 'Visitors', 'Purchasers', 'Conversion %']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.info(f"Available columns: {', '.join(df.columns.tolist())}")
                
                with st.expander("Raw File Preview (first 10 lines)"):
                    uploaded_file.seek(0)
                    for i, line in enumerate(uploaded_file):
                        if i < 10:
                            st.code(line.decode('utf-8') if isinstance(line, bytes) else line)
                        else:
                            break
                
                return None
            
            df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
            df['Combo Size'] = pd.to_numeric(df['Combo Size'], errors='coerce')
            df['Visitors'] = pd.to_numeric(df['Visitors'], errors='coerce')
            df['Purchasers'] = pd.to_numeric(df['Purchasers'], errors='coerce')
            
            if df['Conversion %'].dtype == 'object':
                df['Conversion %'] = df['Conversion %'].str.replace('%', '').astype(float)
            else:
                df['Conversion %'] = pd.to_numeric(df['Conversion %'], errors='coerce')
            
            df = df.dropna(subset=['Purchasers', 'Conversion %', 'Rank'])
            
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        df[col] = pd.to_numeric(df[col], errors='ignore')
                    except:
                        df[col] = df[col].astype(str)
            
            st.session_state.current_file_hash = file_hash
            
            log_audit(st.session_state.user_email, 'Data Upload', 
                     f'Uploaded file: {uploaded_file.name}, Rows: {len(df)}')
            
            file_data_json = df.to_json(orient='records')
            
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO upload_history (user_email, filename, upload_date, row_count, file_data) VALUES (?, ?, ?, ?, ?)',
                     (st.session_state.user_email, uploaded_file.name, datetime.now().isoformat(), len(df), file_data_json))
            conn.commit()
            conn.close()
            
            return df
            
        except Exception as e:
            st.error(f"Error loading file: {e}")
            import traceback
            st.code(traceback.format_exc())
            return None
    return None

# Apply filters function
def apply_filters(df, filters):
    filtered_df = df.copy()
    
    for column, values in filters.items():
        if values and column in filtered_df.columns:
            if isinstance(values, list):
                filtered_df = filtered_df[filtered_df[column].isin(values)]
            else:
                filtered_df = filtered_df[filtered_df[column] == values]
    
    return filtered_df

# Main dashboard
def show_dashboard():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🎯 DAN HHS</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; margin-bottom: 1rem;'><span class='custom-badge'>{st.session_state.user_role}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 0.9rem;'>{st.session_state.user_email}</p>", unsafe_allow_html=True)
        
        st.divider()
        
        page = st.radio("📍 Navigation", 
                       ["🏠 Home Dashboard", 
                        "🏆 Top Combos", 
                        "🎨 Segment Builder", 
                        "🔍 Buyer Deep Dive",
                        "📤 Uploads",
                        "⚙️ Admin"],
                       label_visibility="collapsed")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            log_audit(st.session_state.user_email, 'Logout', 'User logged out')
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_role = None
            st.session_state.data = None
            st.session_state.current_file_hash = None
            st.session_state.search_result = None
            st.rerun()
    
    if st.session_state.data is None:
        st.info("📁 Please upload your buyer data CSV to get started")
        uploaded_file = st.file_uploader("Upload Buyer Data CSV", type=['csv'], key='main_uploader')
        
        if uploaded_file:
            data = load_data(uploaded_file)
            if data is not None:
                st.session_state.data = data
                st.success(f"✅ Loaded {len(data)} rows successfully!")
                
                with st.expander("📊 Data Preview"):
                    st.write("**Column Names:**")
                    st.write(list(data.columns))
                    st.write("**First 5 Rows:**")
                    st.dataframe(data.head())
                    st.write("**Data Types:**")
                    st.write(data.dtypes)
                
                st.rerun()
    
    if st.session_state.data is not None:
        df = st.session_state.data
        
        if page == "🏠 Home Dashboard":
            show_home_dashboard(df)
        elif page == "🏆 Top Combos":
            show_top_combos(df)
        elif page == "🎨 Segment Builder":
            show_segment_builder(df)
        elif page == "🔍 Buyer Deep Dive":
            show_buyer_deep_dive(df)
        elif page == "📤 Uploads":
            show_uploads()
        elif page == "⚙️ Admin":
            show_admin()

# Home Dashboard with improved search
def show_home_dashboard(df):
    st.title("🏠 Home Dashboard - Buyer Intelligence")
    
    required_cols = ['Purchasers', 'Conversion %', 'Combo Size']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        return
    
    st.subheader("🎛️ Global Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_purchasers = st.slider("Min Purchasers", 0, 100, 10)
    with col2:
        min_conversion = st.slider("Min Conversion %", 0.0, 10.0, 4.0, 0.1)
    with col3:
        combo_size_range = st.slider("Combo Size", 1, 5, (2, 5))
    
    filtered_df = df[
        (df['Purchasers'] >= min_purchasers) &
        (df['Conversion %'] >= min_conversion) &
        (df['Combo Size'] >= combo_size_range[0]) &
        (df['Combo Size'] <= combo_size_range[1])
    ]
    
    st.subheader("📊 Key Metrics")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        total_buyers = int(filtered_df['Purchasers'].sum())
        st.metric("Total Buyers", f"{total_buyers:,}")
    
    with kpi2:
        top_50_buyers = int(filtered_df.nlargest(50, 'Conversion %')['Purchasers'].sum())
        pct_from_top = (top_50_buyers / total_buyers * 100) if total_buyers > 0 else 0
        st.metric("% from Top 50 Combos", f"{pct_from_top:.1f}%")
    
    with kpi3:
        if len(filtered_df) > 0:
            best_combo = filtered_df.nlargest(1, 'Conversion %').iloc[0]
            st.metric("Highest Converting Combo", 
                     f"{best_combo['Conversion %']:.1f}%",
                     delta=f"Rank #{int(best_combo['Rank'])}")
    
    with kpi4:
        if len(filtered_df) > 0:
            best_volume = filtered_df.nlargest(1, 'Purchasers').iloc[0]
            st.metric("Best Volume Combo", 
                     f"{int(best_volume['Purchasers'])} buyers",
                     delta=f"Rank #{int(best_volume['Rank'])}")
    
    st.divider()
    
    # Search section
    st.subheader("🔍 Search and Analyze Data")
    search = st.text_input("Search across all columns (e.g., age range, state, income, etc.)", "")
    
    display_df = filtered_df.copy()
    
    if search:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
        search_result_df = display_df[mask]
        st.session_state.search_result = search_result_df
        
        if len(search_result_df) > 0:
            st.success(f"✅ Found {len(search_result_df)} matching rows")
            
            with st.expander("📋 Search Results Preview", expanded=True):
                st.dataframe(search_result_df, use_container_width=True, height=300)
                
                csv_search = search_result_df.to_csv(index=False)
                st.download_button(
                    label="📥 Export Search Results",
                    data=csv_search,
                    file_name=f"search_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="export_search"
                )
            
            # === REPLACE THE OLD BUTTON WITH THIS NEW CODE ===
            if st.button("Create Detailed Insights from Search Results"):
                st.session_state.showing_insights = search_result_df
                st.session_state.insights_title = "Search Results Analysis"
                st.rerun()

            # === ADD THIS NEW BLOCK JUST BELOW THE BUTTON ===
            if 'showing_insights' in st.session_state:
                st.markdown("---")
                st.markdown(f"### Currently Viewing: **{st.session_state.insights_title}**")
                
                # Add a close button
                if st.button("Close Detailed Insights ×", type="secondary"):
                    del st.session_state.showing_insights
                    del st.session_state.insights_title
                    st.rerun()
                
                # Now safely show the insights without flickering!
                show_detailed_insights(st.session_state.showing_insights, st.session_state.insights_title)
            else:
                st.session_state.search_result = None
        else:
            st.session_state.search_result = None
    
    st.subheader("📈 All Top Converting Combos")
    st.dataframe(display_df, use_container_width=True, height=400)
    
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Export Full Data to CSV",
        data=csv,
        file_name=f"top_combos_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        key="export_full"
    )
    
    st.divider()
    
    # Demographic charts with custom colors
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("👥 Top Age Ranges by Buyers", expanded=True):
            if 'AGE_RANGE' in df.columns:
                age_data = df.groupby('AGE_RANGE')['Purchasers'].sum().nlargest(10).reset_index()
                fig = px.bar(age_data, x='AGE_RANGE', y='Purchasers', 
                           title='Top 10 Age Ranges',
                           color='Purchasers',
                           color_continuous_scale=COLOR_PALETTES['purple'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    title_font_size=16,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("💰 Top Income Ranges by Buyers", expanded=True):
            if 'INCOME_RANGE' in df.columns:
                income_data = df.groupby('INCOME_RANGE')['Purchasers'].sum().nlargest(10).reset_index()
                fig = px.bar(income_data, x='Purchasers', y='INCOME_RANGE', 
                           orientation='h', title='Top 10 Income Ranges',
                           color='Purchasers',
                           color_continuous_scale=COLOR_PALETTES['gradient'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    title_font_size=16,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        with st.expander("🗺️ Top States by Buyers", expanded=True):
            if 'STATE' in df.columns:
                state_data = df.groupby('STATE')['Purchasers'].sum().nlargest(10).reset_index()
                fig = px.bar(state_data, x='STATE', y='Purchasers', 
                           title='Top 10 States',
                           color='Purchasers',
                           color_continuous_scale=COLOR_PALETTES['sunset'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    title_font_size=16,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📊 Credit Rating Distribution", expanded=True):
            if 'SKIPTRACE_CREDIT_RATING' in df.columns:
                credit_data = df.groupby('SKIPTRACE_CREDIT_RATING')['Purchasers'].sum().reset_index()
                fig = px.pie(credit_data, values='Purchasers', names='SKIPTRACE_CREDIT_RATING',
                           title='Credit Rating Distribution',
                           color_discrete_sequence=COLOR_PALETTES['ocean'])
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    title_font_size=16
                )
                st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Buyer Concentration")
    top_n = [5, 10, 20, 50, 100]
    cumulative_buyers = []

    for n in top_n:
        buyers = int(filtered_df.nlargest(n, 'Conversion %')['Purchasers'].sum())
        cumulative_buyers.append(buyers / total_buyers * 100 if total_buyers > 0 else 0)

    # Updated chart with hover showing "Top X" label
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f'Top {n}' for n in top_n],
        y=cumulative_buyers,
        text=[f'{val:.1f}%' for val in cumulative_buyers],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>% of Total Buyers: <b>%{y:.1f}%</b><extra></extra>',  # ← This line is the fix
        marker=dict(
            color=cumulative_buyers,
            colorscale=[[0, '#667eea'], [0.5, '#764ba2'], [1, '#f093fb']],
            line=dict(color='rgba(255,255,255,0.5)', width=2)
        )
    ))
    fig.update_layout(
        title='Cumulative % of Total Buyers by Top Combos',
        yaxis_title='% of Total Buyers',
        xaxis_title='Top Combos',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12),
        title_font_size=16
    )
    st.plotly_chart(fig, use_container_width=True)
    
# Detailed insights from data
def show_detailed_insights(df, title="Data"):
    st.subheader(f"💡 Detailed Insights: {title}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Rows", f"{len(df):,}")
        st.metric("👥 Total Purchasers", f"{int(df['Purchasers'].sum()):,}")
    
    with col2:
        st.metric("👀 Total Visitors", f"{int(df['Visitors'].sum()):,}")
        st.metric("📈 Avg Conversion %", f"{df['Conversion %'].mean():.2f}%")
    
    with col3:
        st.metric("📊 Median Conversion %", f"{df['Conversion %'].median():.2f}%")
        st.metric("🎯 Max Conversion %", f"{df['Conversion %'].max():.2f}%")
    
    st.divider()
    
    st.subheader("👥 Demographic Breakdown")
    
    demographic_cols = []
    potential_demo_keywords = ['AGE', 'INCOME', 'GENDER', 'STATE', 'CREDIT', 'MARITAL', 'EDUCATION', 
                               'OCCUPATION', 'ETHNICITY', 'LANGUAGE', 'HOME', 'VEHICLE']
    
    for col in df.columns:
        col_upper = col.upper()
        if any(keyword in col_upper for keyword in potential_demo_keywords):
            if col not in ['Rank', 'Combo Size', 'Visitors', 'Purchasers', 'Conversion %', 'Min Visitors']:
                demographic_cols.append(col)
    
    if demographic_cols:
        color_idx = 0
        num_cols = 2
        for i in range(0, len(demographic_cols), num_cols):
            cols = st.columns(num_cols)
            for j in range(num_cols):
                if i + j < len(demographic_cols):
                    col_name = demographic_cols[i + j]
                    with cols[j]:
                        try:
                            demo_data = df.groupby(col_name)['Purchasers'].sum().nlargest(10).reset_index()
                            if len(demo_data) > 0:
                                palette_key = list(COLOR_PALETTES.keys())[color_idx % len(COLOR_PALETTES)]
                                fig = px.bar(demo_data, x=col_name, y='Purchasers',
                                           title=f'{col_name} Distribution',
                                           color='Purchasers',
                                           color_continuous_scale=COLOR_PALETTES[palette_key])
                                fig.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font=dict(family="Inter", size=11),
                                    title_font_size=14,
                                    showlegend=False
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                color_idx += 1
                        except:
                            pass
    else:
        st.info("No demographic columns found in the data")
    
    st.divider()
    
    st.subheader("📊 Visitor Behavior Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(df, x='Conversion %', nbins=30,
                          title='Conversion Rate Distribution',
                          color_discrete_sequence=COLOR_PALETTES['fire'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**🏆 Top 10 Converting Combos:**")
        
        @st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour, no spinner
        def get_top_10(df):
            return df.nlargest(10, 'Conversion %')[['Rank', 'Visitors', 'Purchasers', 'Conversion %']].reset_index(drop=True)
        
        top_10_cached = get_top_10(df)
        st.dataframe(
            top_10_cached,
            use_container_width=True,
            hide_index=True,
            height=380
        )
    
    with col2:
        fig = px.scatter(df, x='Visitors', y='Purchasers', 
                        color='Conversion %',
                        title='Visitors vs Purchasers',
                        hover_data=['Rank'],
                        color_continuous_scale=COLOR_PALETTES['ocean'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", size=12),
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**💡 What Visitors Like (High Conversion Insights):**")
        
        @st.cache_data(ttl=3600, show_spinner=False)
        def get_high_conversion_insights(df, demographic_cols):
            high = df[df['Conversion %'] >= df['Conversion %'].quantile(0.75)]
            insights = []
            for col in demographic_cols[:5]:
                try:
                    mode_val = high[col].mode()
                    if len(mode_val) > 0:
                        insights.append(f"**{col.replace('_', ' ').title()}:** {mode_val[0]}")
                except:
                    pass
            return insights if insights else ["No clear preference detected yet"]
        
        insights = get_high_conversion_insights(df, demographic_cols)
        for insight in insights:
            st.markdown(f"• {insight}")
# Top Combos Page
def show_top_combos(df):
    st.title("🏆 Top Combos - Full Ranking")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        sort_by = st.selectbox("📊 Sort by", ['Conversion %', 'Purchasers', 'Rank'])
    with col2:
        ascending = st.checkbox("⬆️ Ascending order", False)
    
    sorted_df = df.sort_values(by=sort_by, ascending=ascending)
    
    st.dataframe(sorted_df, use_container_width=True, height=600)

# Segment Builder
def show_segment_builder(df):
    st.title("🎨 Segment Builder")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Attribute Filters")
        
        filters = {}
        
        if 'AGE_RANGE' in df.columns:
            age_options = df['AGE_RANGE'].dropna().unique().tolist()
            filters['AGE_RANGE'] = st.multiselect("👥 Age Range", age_options)
        
        if 'INCOME_RANGE' in df.columns:
            income_options = df['INCOME_RANGE'].dropna().unique().tolist()
            filters['INCOME_RANGE'] = st.multiselect("💰 Income Range", income_options)
        
        if 'GENDER' in df.columns:
            gender_options = df['GENDER'].dropna().unique().tolist()
            filters['GENDER'] = st.multiselect("👤 Gender", gender_options)
        
        if 'STATE' in df.columns:
            state_options = df['STATE'].dropna().unique().tolist()
            filters['STATE'] = st.multiselect("🗺️ State", state_options)
    
    with col2:
        st.subheader("📊 Segment Results")
        
        filtered_data = apply_filters(df, filters)
        
        segment_name = st.text_input("💾 Segment Name")
        
        if len(filtered_data) > 0:
            total_purchasers = int(filtered_data['Purchasers'].sum())
            pct_total = (total_purchasers / df['Purchasers'].sum() * 100)
            avg_conversion = filtered_data['Conversion %'].mean()
            
            metric1, metric2, metric3 = st.columns(3)
            with metric1:
                st.metric("👥 Purchasers", f"{total_purchasers:,}")
            with metric2:
                st.metric("📊 % of Total", f"{pct_total:.1f}%")
            with metric3:
                st.metric("📈 Avg Conversion", f"{avg_conversion:.2f}%")
            
            with st.expander("📋 Preview Filtered Data", expanded=True):
                st.dataframe(filtered_data, use_container_width=True, height=400)
                
                csv_seg = filtered_data.to_csv(index=False)
                st.download_button(
                    label="📥 Export Segment Data",
                    data=csv_seg,
                    file_name=f"segment_{segment_name or 'custom'}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            if st.button("💾 Save Segment") and segment_name:
                segment_data = {
                    'name': segment_name,
                    'filters': filters,
                    'purchasers': total_purchasers,
                    'conversion': avg_conversion
                }
                st.session_state.saved_segments.append(segment_data)
                st.success(f"✅ Saved segment: {segment_name}")
                log_audit(st.session_state.user_email, 'Segment Saved', segment_name)
        else:
            st.info("No rows match the selected filters.")
        
        if st.session_state.saved_segments:
            st.subheader("💾 Saved Segments")
            for seg in st.session_state.saved_segments:
                with st.expander(seg['name']):
                    st.write(f"👥 Purchasers: {seg['purchasers']:,}")
                    st.write(f"📈 Avg Conversion: {seg['conversion']:.2f}%")
                    st.json(seg['filters'])
        if st.session_state.saved_segments:
            st.subheader("💾 Saved Segments")
            for seg in st.session_state.saved_segments:
                with st.expander(seg['name']):
                    st.write(f"👥 Purchasers: {seg['purchasers']:,}")
                    st.write(f"📈 Avg Conversion: {seg['conversion']:.2f}%")
                    st.json(seg['filters'])
            
            # ========== NEW COMPARISON FEATURE STARTS HERE ==========
            st.divider()
            st.subheader("📊 Compare Saved Segments Side-by-Side")
            
            if len(st.session_state.saved_segments) < 2:
                st.info("💡 Save at least 2 segments to enable comparison")
            else:
                # Let user choose how many to compare
                num_compare = st.radio(
                    "How many segments do you want to compare?",
                    [2, 3, 4],
                    horizontal=True,
                    help="Select up to 4 segments for side-by-side comparison"
                )
                
                # Create selection columns
                select_cols = st.columns(num_compare)
                selected_segments = []
                segment_names = [seg['name'] for seg in st.session_state.saved_segments]
                
                # Let user pick segments
                for i in range(num_compare):
                    with select_cols[i]:
                        default_idx = i if i < len(segment_names) else 0
                        selected = st.selectbox(
                            f"Segment {i+1}",
                            segment_names,
                            index=default_idx,
                            key=f"compare_seg_{i}"
                        )
                        # Find the full segment data
                        seg_data = next((s for s in st.session_state.saved_segments if s['name'] == selected), None)
                        if seg_data:
                            selected_segments.append(seg_data)
                
                # ← BUTTON MOVED OUTSIDE THE LOOP - THIS FIXES IT!
                if st.button("🔍 Compare Selected Segments", use_container_width=True, type="primary", key="compare_segments_btn"):
                    if len(selected_segments) >= 2:
                        st.markdown("---")
                        st.markdown("### 📊 Comparison Results")
                        
                        # ===== COMPARISON TABLE =====
                        comparison_data = []
                        
                        # Row 1: Segment Names
                        names_row = ["Segment Name"] + [seg['name'] for seg in selected_segments]
                        comparison_data.append(names_row)
                        
                        # Row 2: Total Purchasers
                        purchasers_row = ["Total Purchasers"] + [f"{seg['purchasers']:,}" for seg in selected_segments]
                        comparison_data.append(purchasers_row)
                        
                        # Row 3: Avg Conversion
                        conversion_row = ["Avg Conversion %"] + [f"{seg['conversion']:.2f}%" for seg in selected_segments]
                        comparison_data.append(conversion_row)
                        
                        # Row 4: % of Total Buyers
                        total_buyers = df['Purchasers'].sum()
                        pct_row = ["% of Total Buyers"] + [f"{(seg['purchasers']/total_buyers*100):.1f}%" for seg in selected_segments]
                        comparison_data.append(pct_row)
                        
                        # Create DataFrame
                        comparison_df = pd.DataFrame(comparison_data)
                        comparison_df.columns = ['Metric'] + [f'Segment {i+1}' for i in range(len(selected_segments))]
                        
                        # Display with custom styling
                        st.dataframe(
                            comparison_df,
                            use_container_width=True,
                            hide_index=True,
                            height=200
                        )
                        
                        # ===== VISUAL COMPARISON CHARTS =====
                        st.markdown("### 📈 Visual Comparison")
                        
                        chart_col1, chart_col2 = st.columns(2)
                        
                        with chart_col1:
                            # Purchasers comparison bar chart
                            purchasers_chart_data = pd.DataFrame({
                                'Segment': [seg['name'] for seg in selected_segments],
                                'Purchasers': [seg['purchasers'] for seg in selected_segments]
                            })
                            
                            fig1 = px.bar(
                                purchasers_chart_data,
                                x='Segment',
                                y='Purchasers',
                                title='👥 Total Purchasers Comparison',
                                color='Purchasers',
                                color_continuous_scale=COLOR_PALETTES['purple'],
                                text='Purchasers'
                            )
                            fig1.update_traces(texttemplate='<b>%{text:,}</b>', textposition='outside')
                            fig1.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="Inter", size=12),
                                title_font_size=16,
                                showlegend=False,
                                height=400
                            )
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        with chart_col2:
                            # Conversion rate comparison
                            conversion_chart_data = pd.DataFrame({
                                'Segment': [seg['name'] for seg in selected_segments],
                                'Conversion %': [seg['conversion'] for seg in selected_segments]
                            })
                            
                            fig2 = px.bar(
                                conversion_chart_data,
                                x='Segment',
                                y='Conversion %',
                                title='📈 Avg Conversion % Comparison',
                                color='Conversion %',
                                color_continuous_scale=COLOR_PALETTES['gradient'],
                                text='Conversion %'
                            )
                            fig2.update_traces(texttemplate='<b>%{text:.2f}%</b>', textposition='outside')
                            fig2.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(family="Inter", size=12),
                                title_font_size=16,
                                showlegend=False,
                                height=400
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # ===== DETAILED FILTERS COMPARISON =====
                        st.markdown("### 🎯 Filter Details Comparison")
                        
                        filter_cols = st.columns(num_compare)
                        
                        for i, seg in enumerate(selected_segments):
                            with filter_cols[i]:
                                st.markdown(f"**{seg['name']}**")
                                
                                if seg['filters']:
                                    for filter_key, filter_val in seg['filters'].items():
                                        if filter_val:  # Only show non-empty filters
                                            st.markdown(f"**{filter_key.replace('_', ' ').title()}:**")
                                            if isinstance(filter_val, list):
                                                for val in filter_val:
                                                    st.markdown(f"• {val}")
                                            else:
                                                st.markdown(f"• {filter_val}")
                                else:
                                    st.info("No filters applied")
                        
                        # ===== WINNER ANALYSIS =====
                        st.markdown("---")
                        st.markdown("### 🏆 Performance Winner")
                        
                        winner_col1, winner_col2 = st.columns(2)
                        
                        with winner_col1:
                            # Best by volume
                            best_volume = max(selected_segments, key=lambda x: x['purchasers'])
                            st.success(f"""
                            **🎯 Highest Volume Segment:**
                            
                            **{best_volume['name']}**
                            
                            - 👥 Purchasers: **{best_volume['purchasers']:,}**
                            - 📈 Conversion: **{best_volume['conversion']:.2f}%**
                            """)
                        
                        with winner_col2:
                            # Best by conversion
                            best_conversion = max(selected_segments, key=lambda x: x['conversion'])
                            st.info(f"""
                            **⚡ Highest Conversion Segment:**
                            
                            **{best_conversion['name']}**
                            
                            - 📈 Conversion: **{best_conversion['conversion']:.2f}%**
                            - 👥 Purchasers: **{best_conversion['purchasers']:,}**
                            """)
                        
                        # Export comparison
                        st.divider()
                        comparison_export = comparison_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Export Comparison Table",
                            data=comparison_export,
                            file_name=f"segment_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        log_audit(st.session_state.user_email, 'Segment Comparison', 
                                f"Compared {len(selected_segments)} segments")
                    else:
                        st.warning("Please select at least 2 different segments")
            # ========== NEW COMPARISON FEATURE ENDS HERE ==========

# Buyer Deep Dive
def show_buyer_deep_dive(df):
    st.title("🔍 Buyer Deep Dive")
    
    # Add rank selector with slider for easier navigation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        combo_rank = st.slider(
            "🎯 Select Combo Rank (slide to explore)", 
            min_value=1, 
            max_value=len(df), 
            value=1,
            help="Slide to see different combos and their performance"
        )
    
    with col2:
        # Quick jump to specific rank
        jump_rank = st.number_input(
            "Or jump to rank:", 
            min_value=1, 
            max_value=len(df), 
            value=combo_rank,
            key="jump_rank"
        )
        if jump_rank != combo_rank:
            combo_rank = jump_rank
    
    if combo_rank:
        combo_data = df[df['Rank'] == combo_rank]
        
        if len(combo_data) > 0:
            combo = combo_data.iloc[0]
            
            # Header with combo info
            st.markdown(f"### 🎯 Analyzing Combo Rank #{int(combo_rank)}")
            
            # Key Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👥 Purchasers", f"{int(combo['Purchasers'])}")
            with col2:
                st.metric("👀 Visitors", f"{int(combo['Visitors'])}")
            with col3:
                st.metric("📈 Conversion %", f"{combo['Conversion %']:.2f}%")
            with col4:
                st.metric("📦 Combo Size", f"{int(combo['Combo Size'])}")
            
            st.divider()
            
            # ==========================================
            # SECTION 1: Performance Comparison Charts
            # ==========================================
            st.subheader("📊 Performance Comparison with Other Combos")
            
            # Get surrounding ranks for comparison (±10 ranks)
            rank_range = 10
            min_rank = max(1, combo_rank - rank_range)
            max_rank = min(len(df), combo_rank + rank_range)
            comparison_df = df[(df['Rank'] >= min_rank) & (df['Rank'] <= max_rank)].copy()
            
            # Highlight current combo
            comparison_df['Highlight'] = comparison_df['Rank'].apply(
                lambda x: 'Current Combo' if x == combo_rank else 'Other Combos'
            )
            
            # Create two columns for charts
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Visitors comparison chart
                fig_visitors = px.bar(
                    comparison_df, 
                    x='Rank', 
                    y='Visitors',
                    color='Highlight',
                    color_discrete_map={
                        'Current Combo': '#f5576c',
                        'Other Combos': '#667eea'
                    },
                    title=f'👀 Visitors: Rank {min_rank}-{max_rank}',
                    hover_data=['Purchasers', 'Conversion %']
                )
                fig_visitors.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig_visitors, use_container_width=True)
            
            with chart_col2:
                # Purchasers comparison chart
                fig_purchasers = px.bar(
                    comparison_df, 
                    x='Rank', 
                    y='Purchasers',
                    color='Highlight',
                    color_discrete_map={
                        'Current Combo': '#f5576c',
                        'Other Combos': '#764ba2'
                    },
                    title=f'👥 Purchasers: Rank {min_rank}-{max_rank}',
                    hover_data=['Visitors', 'Conversion %']
                )
                fig_purchasers.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    showlegend=True,
                    height=400
                )
                st.plotly_chart(fig_purchasers, use_container_width=True)
            @st.cache_data(ttl=300)  
            def build_attributes_df(df, combo, combo_rank):
                """Builds the attributes dataframe - cached so no flicker"""
                attributes = []
                ignore_cols = ['Rank', 'Combo Size', 'Visitors', 'Purchasers', 'Conversion %', 'Min Visitors']

                for col in df.columns:
                    if col not in ignore_cols:
                        val = combo.get(col)
                        # Only include REAL values - no empty spam
                        if pd.notna(val) and str(val).strip() not in ['', 'nan', 'NaN', 'None', 'none']:
                            attributes.append({
                                "Attribute": col.replace("_", " ").title().replace("Skiptrace", "Credit"),
                                "Value": str(val).strip()
                            })

                # Sort alphabetically
                attributes.sort(key=lambda x: x["Attribute"])
                return pd.DataFrame(attributes)
            # ==========================================
            # SECTION 2: Conversion Rate Analysis
            # ==========================================
            st.subheader("📈 Conversion Rate Analysis")
            
            chart_col3, chart_col4 = st.columns(2)
            
            with chart_col3:
                # Conversion % trend
                fig_conversion = px.line(
                    comparison_df, 
                    x='Rank', 
                    y='Conversion %',
                    title=f'📈 Conversion Rate Trend',
                    markers=True
                )
                
                # Add a scatter point for current combo
                fig_conversion.add_scatter(
                    x=[combo_rank],
                    y=[combo['Conversion %']],
                    mode='markers',
                    marker=dict(size=15, color='#f5576c', line=dict(width=2, color='white')),
                    name='Current Combo',
                    showlegend=True
                )
                
                fig_conversion.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    height=400
                )
                st.plotly_chart(fig_conversion, use_container_width=True)
            
            with chart_col4:
                # Visitors vs Purchasers scatter
                fig_scatter = px.scatter(
                    comparison_df,
                    x='Visitors',
                    y='Purchasers',
                    color='Highlight',
                    size='Conversion %',
                    color_discrete_map={
                        'Current Combo': '#f5576c',
                        'Other Combos': '#667eea'
                    },
                    title='👥 Visitors vs Purchasers',
                    hover_data=['Rank', 'Conversion %']
                )
                fig_scatter.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter", size=12),
                    height=400
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.divider()
            
            # ==========================================
            # SECTION 3: Performance Metrics Card
            # ==========================================
            st.subheader("🎯 Performance Insights")
            
            # Calculate percentile rankings
            visitor_percentile = (df['Visitors'] < combo['Visitors']).sum() / len(df) * 100
            purchaser_percentile = (df['Purchasers'] < combo['Purchasers']).sum() / len(df) * 100
            conversion_percentile = (df['Conversion %'] < combo['Conversion %']).sum() / len(df) * 100
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                st.info(f"""
                **👀 Visitor Performance**
                
                This combo has **more visitors** than {visitor_percentile:.1f}% of all combos.
                
                **Visitors:** {int(combo['Visitors']):,}
                """)
            
            with insight_col2:
                st.success(f"""
                **👥 Purchaser Performance**
                
                This combo has **more purchasers** than {purchaser_percentile:.1f}% of all combos.
                
                **Purchasers:** {int(combo['Purchasers']):,}
                """)
            
            with insight_col3:
                st.warning(f"""
                **📈 Conversion Performance**
                
                This combo has a **higher conversion rate** than {conversion_percentile:.1f}% of all combos.
                
                **Conversion:** {combo['Conversion %']:.2f}%
                """)
            
            st.divider()
            # ==========================================
            # SECTION 4: Complete Combo Attributes → NO KEY, ZERO FLICKER, PERFECT
            # ==========================================
            st.subheader("📋 Complete Combo Attributes")

            # Use cached function - this is the magic that stops flickering
            attr_df = build_attributes_df(df, combo, combo_rank)

            if not attr_df.empty:
                # NO 'key' parameter - just pure stable display
                st.dataframe(
                    attr_df,
                    use_container_width=True,
                    hide_index=True,
                    height=min(600, (len(attr_df) + 1) * 35)  # Auto-size height
                )

                # Export button
                csv_attr = attr_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Targeted Attributes",
                    data=csv_attr,
                    file_name=f"Combo_Rank_{int(combo_rank)}_Targeted_Attributes.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.caption(f"📊 Showing {len(attr_df)} targeted attributes for Rank #{combo_rank}")
            else:
                st.info("🔓 No targeting attributes defined for this combo (targets all visitors)")
                st.caption("This means the combo includes buyers from all demographics")
            
            # ==========================================
            # SECTION 5: Demographic Profile of This Combo – 100% FIXED & BEAUTIFUL
            # ==========================================
            st.subheader("Demographic Profile of This Combo")

            demographic_cols = []
            potential_demo_keywords = ['AGE', 'INCOME', 'GENDER', 'STATE', 'CREDIT', 'MARITAL', 'EDUCATION', 'OCCUPATION', 'HOME', 'CHILD', 'ETHNIC', 'VEHICLE', 'LANGUAGE']

            # Collect only columns that exist in the dataframe and have a real value in the current combo
            for col in df.columns:
                if col not in ['Rank', 'Combo Size', 'Visitors', 'Purchasers', 'Conversion %', 'Min Visitors']:
                    if any(keyword in col.upper() for keyword in potential_demo_keywords):
                        val = combo.get(col)
                        if pd.notna(val) and str(val).strip() not in ['', 'nan', 'NaN', 'None']:
                            demographic_cols.append(col)

            if demographic_cols:
                cols_per_row = 2
                for i in range(0, len(demographic_cols), cols_per_row):
                    row_cols = st.columns(cols_per_row)
                    for j, col_name in enumerate(demographic_cols[i:i + cols_per_row]):
                        with row_cols[j]:
                            actual_value = str(combo[col_name]).strip()

                            # Nice title
                            title = col_name.replace("_", " ").title()
                            title = title.replace("Skiptrace", "Credit")

                            st.markdown(f"**{title}**")
                            st.markdown(
                                f"<h2 style='color:#f5576c; margin:8px 0 16px 0; font-size:2rem;'>{actual_value}</h2>",
                                unsafe_allow_html=True
                            )

                            # Distribution chart (horizontal for better readability)
                            value_counts = df[col_name].value_counts().head(10)   # ← Fixed: now defined!

                            fig = px.bar(
                                y=value_counts.index.astype(str),
                                x=value_counts.values,
                                orientation='h',
                                color=value_counts.values,
                                color_continuous_scale="purples",
                                height=340
                            )
                            fig.update_layout(
                                title="",
                                xaxis_title="Number of Combos",
                                yaxis_title="",
                                margin=dict(l=0, r=20, t=20, b=0),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                showlegend=False
                            )

                            # Highlight the current combo's value with a thick red border
                            fig.update_traces(
                                marker_line_width=[6 if str(idx) == actual_value else 1 
                                                 for idx in value_counts.index],
                                marker_line_color=["#f5576c" if str(idx) == actual_value else "#e2e8f0" 
                                                 for idx in value_counts.index]
                            )

                            st.plotly_chart(fig, use_container_width=True)
                            st.caption(f"This combo: **{actual_value}**")
            else:
                st.info("No demographic targeting applied — this combo includes buyers from all groups")
            
            st.divider()
            
            

# Uploads Page
def show_uploads():
    st.title("📤 Upload History")
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, user_email, filename, upload_date, row_count FROM upload_history ORDER BY upload_date DESC')
    uploads = c.fetchall()
    conn.close()
    
    if uploads:
        upload_df = pd.DataFrame(uploads, columns=['ID', 'User Email', 'Filename', 'Upload Date', 'Row Count'])
        
        st.subheader("📊 All Uploads")
        st.dataframe(upload_df, use_container_width=True)
        
        st.divider()
        
        st.subheader("🔍 Search Upload History")
        search_filename = st.text_input("Search by filename")
        
        if search_filename:
            filtered_uploads = upload_df[upload_df['Filename'].str.contains(search_filename, case=False, na=False)]
            st.dataframe(filtered_uploads, use_container_width=True)
        
        st.divider()
        
        st.subheader("👁️ View Stored Upload Data")
        
        upload_ids = upload_df['ID'].tolist()
        filenames = upload_df['Filename'].tolist()
        
        options = [f"ID {uid}: {fname}" for uid, fname in zip(upload_ids, filenames)]
        
        selected = st.selectbox("Select an upload to view", ["Select..."] + options)
        
        if selected != "Select...":
            selected_id = int(selected.split(":")[0].replace("ID ", ""))
            
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('SELECT file_data, filename, row_count FROM upload_history WHERE id = ?', (selected_id,))
            result = c.fetchone()
            conn.close()
            
            if result and result[0]:
                file_data_json, filename, row_count = result
                
                try:
                    stored_df = pd.read_json(file_data_json, orient='records')
                    
                    st.success(f"✅ Loaded stored data from: **{filename}** ({row_count} rows)")
                    
                    with st.expander("📋 Preview Stored Data", expanded=True):
                        st.dataframe(stored_df, use_container_width=True, height=400)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📂 Load This Data as Current Dataset"):
                            st.session_state.data = stored_df
                            st.session_state.current_file_hash = hashlib.md5(file_data_json.encode()).hexdigest()
                            st.success("✅ Data loaded! Navigate to Home Dashboard to analyze.")
                            st.rerun()
                    
                    with col2:
                        csv_data = stored_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Export This Data",
                            data=csv_data,
                            file_name=f"{filename.replace('.csv', '')}_stored.csv",
                            mime="text/csv"
                        )
                    
                    if st.button("📊 Create Insights from This Data"):
                        show_detailed_insights(stored_df, filename)
                        
                except Exception as e:
                    st.error(f"Error loading stored data: {e}")
            else:
                st.warning("No data stored for this upload")
    else:
        st.info("📁 No uploads yet")
    
    st.divider()
    
    st.subheader("📤 Upload New File")
    new_file = st.file_uploader("Upload a new CSV file", type=['csv'], key='uploads_page_uploader')
    
    if new_file:
        data = load_data(new_file)
        if data is not None:
            st.session_state.data = data
            st.success(f"✅ Uploaded and loaded {len(data)} rows successfully!")
            st.info("Navigate to Home Dashboard to analyze the data")
            st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Clear Current Data"):
        st.session_state.data = None
        st.session_state.current_file_hash = None
        st.session_state.search_result = None
        st.success("✅ Data cleared! You can upload a new file.")
        st.rerun()

# Admin Page
def show_admin():
    st.title("⚙️ Admin Panel")
    
    if st.session_state.user_role not in ['Owner', 'Admin']:
        st.error("❌ You don't have permission to access this page")
        return
    
    tab1, tab2, tab3 = st.tabs(["👥 Users", "📋 Audit Log", "ℹ️ System Info"])
    
    with tab1:
        st.subheader("👥 User Management")
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, email, role, created_at, last_login FROM users')
        users = c.fetchall()
        conn.close()
        
        if users:
            users_df = pd.DataFrame(users, columns=['ID', 'Email', 'Role', 'Created', 'Last Login'])
            st.dataframe(users_df, use_container_width=True)
        
        st.divider()
        
        st.subheader("✉️ Invite New User via Email")
        
        if not st.secrets.get("email", {}).get("enabled", False):
            st.warning("⚠️ Email sending is not configured. Add email secrets to enable real invites.")
            with st.expander("❓ How to enable email invites"):
                st.code("""
# .streamlit/secrets.toml
[email]
enabled = true
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "yourgmail@gmail.com"
sender_password = "your-16-digit-app-password"
                """)

        if 'invite_success' not in st.session_state:
            st.session_state.invite_success = False
            st.session_state.invite_credentials = None

        with st.form("invite_form", clear_on_submit=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                invite_email = st.text_input("📧 Email Address", placeholder="user@example.com")
            with col2:
                invite_role = st.selectbox("🎭 Role", ['Viewer', 'Analyst', 'Admin', 'Owner'])

            generate_password = st.checkbox("🔐 Auto-generate secure password (recommended)", value=True)
            manual_password = st.text_input("Or set custom password", type="password", disabled=generate_password)

            submit_button = st.form_submit_button("✨ Create User & Send Invite", use_container_width=True)

            if submit_button:
                if not invite_email or "@" not in invite_email or "." not in invite_email:
                    st.error("Please enter a valid email address")
                elif not generate_password and len(manual_password) < 8:
                    st.error("Password must be at least 8 characters")
                else:
                    temp_password = manual_password if not generate_password else secrets.token_urlsafe(12)

                    if create_user(invite_email, temp_password, invite_role):
                        credentials = f"Email: {invite_email}\nPassword: {temp_password}\nRole: {invite_role}"
                        st.session_state.invite_success = True
                        st.session_state.invite_credentials = credentials
                        st.session_state.invite_email = invite_email
                        st.session_state.invite_role = invite_role
                        st.session_state.temp_password = temp_password

                        st.success(f"✅ User {invite_email} created successfully!")
                        log_audit(st.session_state.user_email, 'User Created', f'{invite_email} as {invite_role}')
                    else:
                        st.error("❌ User already exists with this email")

        if st.session_state.invite_success:
            creds = st.session_state.invite_credentials
            email_to = st.session_state.invite_email

            st.code(creds, language="text")

            st.markdown(
                f"""
                <button onclick="navigator.clipboard.writeText(`{creds}`).then(()=>alert('Copied!'))" 
                style="padding:10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border:none; border-radius:10px; cursor:pointer; margin:10px 0; font-weight: 600; font-family: Inter; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                📋 Copy Credentials
                </button>
                """,
                unsafe_allow_html=True
            )

            if st.secrets.get("email", {}).get("enabled", False):
                if st.button("📧 Send Invite Email Now", type="primary", use_container_width=True):
                    with st.spinner("Sending email..."):
                        try:
                            sender = st.secrets["email"]["sender_email"]
                            app_pass = st.secrets["email"]["sender_password"]

                            msg = MIMEMultipart('alternative')
                            msg['From'] = sender
                            msg['To'] = email_to
                            msg['Subject'] = "Your DAN HHS Dashboard Access"

                            text_body = f"""
Welcome to DAN HHS Buyer Intelligence Dashboard!

You have been invited as {st.session_state.invite_role}.

Your Login Details:
Email: {email_to}
Password: {st.session_state.temp_password}

Please change your password after logging in.
                            """

                            html_body = f"""
<html>
<head>
    <style>
        body {{ font-family: 'Inter', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); }}
        h1 {{ color: #2d3748; margin-bottom: 10px; }}
        .gradient-text {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .credentials {{ background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #667eea; }}
        .btn {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; margin-top: 20px; font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }}
        .role-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: 600; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="gradient-text">🎯 Welcome to DAN HHS!</h1>
        <p>You have been invited to join the <strong>Buyer Intelligence Dashboard</strong></p>
        <p>Your role: <span class="role-badge">{st.session_state.invite_role}</span></p>
        
        <div class="credentials">
            <h3 style="margin-top: 0;">🔐 Your Login Credentials</h3>
            <p><strong>📧 Email:</strong> {email_to}</p>
            <p><strong>🔒 Password:</strong> <code style="background: #f0f2f6; padding: 4px 8px; border-radius: 4px;">{st.session_state.temp_password}</code></p>
        </div>
        
        <a href="https://{st.secrets.get('server', {}).get('url', 'your-app-url.streamlit.app')}" class="btn">
            🚀 Login to Dashboard
        </a>
        
        <p style="margin-top: 30px; color: #718096; font-size: 14px;">
            <em>💡 Pro tip: Change your password after your first login for enhanced security.</em>
        </p>
    </div>
</body>
</html>
                            """

                            part1 = MIMEText(text_body, 'plain')
                            part2 = MIMEText(html_body, 'html')
                            msg.attach(part1)
                            msg.attach(part2)

                            server = smtplib.SMTP(st.secrets["email"]["smtp_server"], st.secrets["email"]["smtp_port"])
                            server.set_debuglevel(0)
                            server.ehlo()
                            server.starttls()
                            server.ehlo()
                            server.login(sender, app_pass)
                            server.sendmail(sender, email_to, msg.as_string())
                            server.quit()

                            st.success(f"✅ Invite email sent successfully to {email_to}!")
                            log_audit(st.session_state.user_email, 'Invite Sent', f'Sent to {email_to}')

                        except smtplib.SMTPAuthenticationError as e:
                            st.error("❌ Gmail Authentication Failed!")
                            st.warning("""
**How to fix this:**
1. Go to your Google Account settings
2. Enable **2-Factor Authentication**
3. Generate an **App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Copy the 16-character password
4. Update your `.streamlit/secrets.toml`
                            """)
                            st.code("""
[email]
enabled = true
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your-16-char-app-password"
                            """)
                            
                        except Exception as e:
                            st.error(f"❌ Failed to send email: {e}")
            else:
                st.info("📧 Email sending is disabled. Copy credentials manually.")

            if st.button("➕ Invite Another User"):
                st.session_state.invite_success = False
                st.rerun()

    with tab2:
        st.subheader("📋 Audit Log")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 100')
        logs = c.fetchall()
        conn.close()
        
        if logs:
            logs_df = pd.DataFrame(logs, columns=['ID', 'User Email', 'Action', 'Timestamp', 'Details'])
            st.dataframe(logs_df, use_container_width=True, height=400)
        else:
            st.info("📝 No audit logs yet")

    with tab3:
        st.subheader("ℹ️ System Information")
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        total_users = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM upload_history')
        total_uploads = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM audit_log')
        total_logs = c.fetchone()[0]
        conn.close()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Total Users", total_users)
        with col2:
            st.metric("📤 Total Uploads", total_uploads)
        with col3:
            st.metric("📋 Total Audit Logs", total_logs)
        
        st.divider()
        
        st.info("💡 Email invites work when secrets are configured. Use Gmail + App Password.")
        
        st.markdown("""
        ### 📊 Dashboard Features
        - User Authentication & Role Management
        - Magic Link Login
        - Data Upload & Storage
        - Filtering & Search
        - Demographic Analysis
        - Segment Builder
        - Audit Logging
        - Email Invitations
        
        ### 🎨 Custom Styling
        - Modern gradient design
        - Interactive charts with unique color palettes
        - Responsive layout
        - Enhanced UX/UI elements
        """)

# Main app logic
if not st.session_state.authenticated:
    show_auth_page()
else:
    show_dashboard()