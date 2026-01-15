"""
SMAHI GROUP - Professional Farm Management System
Productly Design Style
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF
import hashlib
import os

st.set_page_config(page_title="SMAHI GROUP", layout="wide", page_icon="🌾", initial_sidebar_state="expanded")

DB_NAME = "smahi_ultimate.db"
PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

COMPANY = {
    "name": "SMAHI GROUP",
    "ice": "002165492000071",
    "address": "Sidi Bennour, Maroc",
    "phone": "+212 XXX XXXXXX",
    "email": "contact@smahigroup.ma"
}

# PRODUCTLY PROFESSIONAL DESIGN
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Remove Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background: #F5F7FA;}
    .main .block-container {padding: 2rem 3rem; max-width: 100%;}
    
    /* Productly Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1C243C 0%, #2D3651 100%);
        padding: 0;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
        padding: 1.5rem 1rem;
    }
    
    /* Sidebar Logo */
    .sidebar-logo {
        background: linear-gradient(135deg, #FF7F50 0%, #FF6B45 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .sidebar-logo h2 {
        color: white;
        font-size: 1.2rem;
        font-weight: 800;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Menu Items */
    .sidebar-menu-item {
        color: #94A3B8;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .sidebar-menu-item:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
    }
    .sidebar-menu-item.active {
        background: linear-gradient(135deg, #FF7F50 0%, #FF6B45 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(255, 127, 80, 0.3);
    }
    
    /* Productly Metric Cards */
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 1.75rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    .metric-icon.orange {background: linear-gradient(135deg, #FF7F50 0%, #FF6B45 100%);}
    .metric-icon.blue {background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);}
    .metric-icon.green {background: linear-gradient(135deg, #5CC97B 0%, #4CAF50 100%);}
    .metric-icon.purple {background: linear-gradient(135deg, #7B68EE 0%, #6A5ACD 100%);}
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    .metric-change {
        font-size: 0.8rem;
        font-weight: 600;
    }
    .metric-change.up {color: #10B981;}
    .metric-change.down {color: #EF4444;}
    
    /* Active Balance Card (Orange Gradient) */
    .balance-card {
        background: linear-gradient(135deg, #FF7F50 0%, #FF6B45 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        box-shadow: 0 8px 24px rgba(255, 127, 80, 0.3);
    }
    .balance-title {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .balance-amount {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
    }
    .balance-item {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 0.9rem;
    }
    .balance-item:last-child {border-bottom: none;}
    
    /* Chart Container */
    .chart-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .chart-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #FF7F50 0%, #FF6B45 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        box-shadow: 0 4px 12px rgba(255, 127, 80, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FF6B45 0%, #FF5A3A 100%);
        box-shadow: 0 6px 16px rgba(255, 127, 80, 0.4);
    }
    
    /* Search Bar */
    .search-bar {
        background: white;
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 2rem;
    }
    
    /* Hide Streamlit elements */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Database Setup
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, type TEXT NOT NULL,
        category TEXT NOT NULL, partner_name TEXT, product TEXT NOT NULL,
        quantity REAL DEFAULT 0, unit TEXT DEFAULT 'kg', fuel_liters REAL DEFAULT 0,
        fuel_station TEXT, price_unit REAL NOT NULL, total_price REAL NOT NULL,
        amount_paid REAL DEFAULT 0, amount_remaining REAL DEFAULT 0, notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS plantations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date_planted TEXT NOT NULL,
        crop_name TEXT NOT NULL, hectares REAL NOT NULL, plot_name TEXT NOT NULL,
        status TEXT DEFAULT 'En cours', expected_harvest TEXT, notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL,
        category TEXT NOT NULL, description TEXT, amount REAL NOT NULL,
        payment_method TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

def format_currency(amount):
    return f"{amount:,.0f}"

def calculate_percentage_change(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# Database Manager
class DB:
    @staticmethod
    def get_transactions():
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM transactions ORDER BY date DESC", conn)
        conn.close()
        return df
    
    @staticmethod
    def add_transaction(data):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''INSERT INTO transactions (date, type, category, partner_name, product, quantity, unit, 
            fuel_liters, fuel_station, price_unit, total_price, amount_paid, amount_remaining, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (dt, data['type'], data['category'], data['partner'], data['product'], data['quantity'],
             data['unit'], data['fuel_liters'], data['fuel_station'], data['price'], data['total'],
             data['paid'], data['remaining'], data['notes']))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_plantations():
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM plantations ORDER BY date_planted DESC", conn)
        conn.close()
        return df
    
    @staticmethod
    def add_plantation(crop, hectares, plot, expected_harvest=None, notes=None):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        dt = datetime.now().strftime("%Y-%m-%d")
        c.execute('''INSERT INTO plantations (date_planted, crop_name, hectares, plot_name, expected_harvest, notes)
            VALUES (?, ?, ?, ?, ?, ?)''', (dt, crop, hectares, plot, expected_harvest, notes))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_expenses():
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
        conn.close()
        return df
    
    @staticmethod
    def add_expense(category, description, amount, payment_method=None, notes=None):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''INSERT INTO expenses (date, category, description, amount, payment_method, notes)
            VALUES (?, ?, ?, ?, ?, ?)''', (dt, category, description, amount, payment_method, notes))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_dashboard_stats(period_days=30):
        conn = sqlite3.connect(DB_NAME)
        date_threshold = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
        prev_date = (datetime.now() - timedelta(days=period_days*2)).strftime("%Y-%m-%d")
        
        stats = {}
        stats['total_sales'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(total_price), 0) as total FROM transactions WHERE type='Vente' AND date >= ?",
            conn, params=[date_threshold])['total'][0]
        stats['total_purchases'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(total_price), 0) as total FROM transactions WHERE type='Achat' AND date >= ?",
            conn, params=[date_threshold])['total'][0]
        stats['total_expenses'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date >= ?",
            conn, params=[date_threshold])['total'][0]
        stats['total_fuel'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(fuel_liters), 0) as total FROM transactions WHERE category LIKE '%Mazot%' AND date >= ?",
            conn, params=[date_threshold])['total'][0]
        stats['outstanding'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(amount_remaining), 0) as total FROM transactions WHERE amount_remaining > 0", conn)['total'][0]
        stats['prev_sales'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(total_price), 0) as total FROM transactions WHERE type='Vente' AND date >= ? AND date < ?",
            conn, params=[prev_date, date_threshold])['total'][0]
        stats['prev_purchases'] = pd.read_sql_query(
            "SELECT COALESCE(SUM(total_price), 0) as total FROM transactions WHERE type='Achat' AND date >= ? AND date < ?",
            conn, params=[prev_date, date_threshold])['total'][0]
        
        conn.close()
        return stats

db = DB()

# PDF Generator
class PDFGen:
    @staticmethod
    def create_document(data, doc_type="Bon de Livraison"):
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 20)
                self.cell(0, 10, COMPANY['name'], 0, 1, 'C')
                self.ln(10)
        
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, doc_type.upper(), 0, 1, 'C')
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"Document N: {data['id']}", 0, 1)
        pdf.cell(0, 10, f"Client: {data['partner_name']}", 0, 1)
        pdf.cell(0, 10, f"Produit: {data['product']}", 0, 1)
        pdf.cell(0, 10, f"Total: {data['total_price']:.2f} DH", 0, 1)
        return pdf.output(dest='S').encode('latin1')

pdf_gen = PDFGen()

# Authentication
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style='background: white; padding: 3rem; border-radius: 20px; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-top: 80px; text-align: center;'>
                <div style='font-size: 70px; margin-bottom: 1rem;'>🌾</div>
                <h1 style='color: #1E293B; font-size: 2rem; font-weight: 800; margin: 0;'>
                    SMAHI GROUP
                </h1>
                <p style='color: #64748B; margin-top: 0.5rem;'>
                    Professional Farm Management
                </p>
            </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("", type="password", placeholder="Password", label_visibility="collapsed")
        if st.button("Sign In", use_container_width=True):
            pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
            if pwd_hash == PASSWORD_HASH:
                st.session_state['logged_in'] = True
                st.success("Welcome!")
                st.rerun()
            else:
                st.error("Invalid password")

# Session
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'selected_menu' not in st.session_state:
    st.session_state['selected_menu'] = "Dashboard"

if not st.session_state['logged_in']:
    login_page()
    st.stop()

# Productly Sidebar
with st.sidebar:
    st.markdown("""
        <div class='sidebar-logo'>
            <h2>🌾 Productly</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #64748B; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 1.5rem 0 0.75rem 1rem;'>Menu</p>", unsafe_allow_html=True)
    
    menu_items = [
        ("Dashboard", "📊"),
        ("Analytics", "📈"),
        ("Sales", "💰"),
        ("Management", "⚙️")
    ]
    
    st.markdown("<p style='color: #64748B; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 1.5rem 0 0.75rem 1rem;'>Management</p>", unsafe_allow_html=True)
    
    management_items = [
        ("Products", "📦"),
        ("Customer", "👥"),
        ("Warehouse", "🏢"),
        ("Reports", "📋")
    ]
    
    st.markdown("<p style='color: #64748B; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin: 1.5rem 0 0.75rem 1rem;'>Notifications</p>", unsafe_allow_html=True)
    
    notif_items = [
        ("Transaction", "💳"),
        ("Message", "✉️")
    ]
    
    for item, icon in menu_items + management_items + notif_items:
        if st.button(f"{icon}  {item}", key=f"menu_{item}", use_container_width=True):
            st.session_state['selected_menu'] = item
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FF7F50 0%, #FF6B45 100%); 
                    border-radius: 12px; padding: 1rem; text-align: center; color: white;'>
            <div style='font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem;'>AR Jakir</div>
            <div style='font-size: 0.8rem; opacity: 0.9;'>Farm Manager</div>
        </div>
    """, unsafe_allow_html=True)

menu = st.session_state['selected_menu']

# PRODUCTLY DASHBOARD
if menu == "Dashboard":
    # Search Bar
    st.markdown("""
        <div class='search-bar'>
            <input type='text' placeholder='🔍 Search' style='border: none; outline: none; width: 100%; font-size: 0.9rem;'>
        </div>
    """, unsafe_allow_html=True)
    
    stats = db.get_dashboard_stats(30)
    net_profit = stats['total_sales'] - stats['total_purchases'] - stats['total_expenses']
    sales_change = calculate_percentage_change(stats['total_sales'], stats['prev_sales'])
    purchases_change = calculate_percentage_change(stats['total_purchases'], stats['prev_purchases'])
    
    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        change_icon = "↑" if sales_change >= 0 else "↓"
        change_class = "up" if sales_change >= 0 else "down"
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon orange'>📈</div>
                <div class='metric-label'>Total Sales</div>
                <div class='metric-value'>{format_currency(stats['total_sales'])}</div>
                <div class='metric-change {change_class}'>{change_icon}{abs(sales_change):.1f}% Incomes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon blue'>🎯</div>
                <div class='metric-label'>Daily Sales</div>
                <div class='metric-value'>{format_currency(stats['total_sales']/30)}</div>
                <div class='metric-change down'>↓13% Sales</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon green'>👥</div>
                <div class='metric-label'>Net Profit</div>
                <div class='metric-value'>{format_currency(net_profit)}</div>
                <div class='metric-change up'>↑48% New User</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon purple'>⛽</div>
                <div class='metric-label'>Mazot (Fuel)</div>
                <div class='metric-value'>{format_currency(stats['total_fuel'])}</div>
                <div class='metric-change up'>+25% Liters</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Chart + Balance Card Row
    col_chart, col_balance = st.columns([2, 1])
    
    with col_chart:
        st.markdown("<div class='chart-container'><div class='chart-title'>Summary Sales</div>", unsafe_allow_html=True)
        
        # Get daily sales data
        df = db.get_transactions()
        if not df.empty:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df[~df['date_dt'].isna()].copy()
            df['Date'] = df['date_dt'].dt.strftime("%Y-%m-%d")
            daily_sales = df[df['type'] == 'Vente'].groupby('Date')['total_price'].sum().reset_index()
            daily_sales = daily_sales.sort_values('Date').tail(12)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_sales['Date'],
                y=daily_sales['total_price'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(255, 127, 80, 0.2)',
                line=dict(color='#FF7F50', width=3, shape='spline'),
                hovertemplate='<b>%{x}</b><br>Sales: %{y:,.0f} DH<extra></extra>'
            ))
            
            fig.update_layout(
                height=350,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, showline=False),
                yaxis=dict(showgrid=True, gridcolor='#F5F7FA', showline=False),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_balance:
        st.markdown(f"""
            <div class='balance-card'>
                <div class='balance-title'>Active Balance</div>
                <div class='balance-amount'>$ {format_currency(net_profit)}</div>
                
                <div class='balance-item'>
                    <span>💰 Incomes</span>
                    <span>$ {format_currency(stats['total_sales'])}</span>
                </div>
                <div class='balance-item'>
                    <span>💸 Expenses</span>
                    <span>$ -{format_currency(stats['total_purchases'])}</span>
                </div>
                <div class='balance-item'>
                    <span>📊 Taxes</span>
                    <span>$ -{format_currency(stats['total_expenses'])}</span>
                </div>
                
                <div style='margin-top: 1.5rem;'>
                    <button style='background: white; color: #FF7F50; border: none; border-radius: 10px; 
                                   padding: 0.75rem 1.5rem; font-weight: 600; cursor: pointer; width: 100%;'>
                        Add Virtual Card  ▶
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)

elif menu == "Sales":
    st.markdown("<h1 style='color: #1E293B; margin-bottom: 2rem;'>Sales Management</h1>", unsafe_allow_html=True)
    
    with st.form("new_trans"):
        col1, col2, col3 = st.columns(3)
        with col1:
            type_op = st.selectbox("Type", ["Vente", "Achat"])
            cat = st.selectbox("Category", ["Cereales", "Legumineuses", "Engrais", "Mazot", "Semences"])
        with col2:
            partner = st.text_input("Partner")
            prod = st.text_input("Product")
        with col3:
            price = st.number_input("Unit Price (DH)", min_value=0.0, step=0.01)
            paid = st.number_input("Amount Paid (DH)", min_value=0.0, step=0.01)
        
        if "Mazot" in cat:
            l = st.number_input("Liters", min_value=0.0, step=1.0)
            qte, unit, stn = 0, "L", st.text_input("Station")
        else:
            qte = st.number_input("Quantity", min_value=0.0, step=1.0)
            unit = st.selectbox("Unit", ["kg", "T", "qx", "sac"])
            l, stn = 0, ""
        
        note = st.text_area("Notes")
        
        if st.form_submit_button("Save Transaction", use_container_width=True):
            if partner and prod and (qte > 0 or l > 0) and price > 0:
                total = (l * price) if l > 0 else (qte * price)
                data = {'type': type_op, 'category': cat, 'partner': partner, 'product': prod, 'quantity': qte, 'unit': unit, 'fuel_liters': l, 'fuel_station': stn, 'price': price, 'total': total, 'paid': paid, 'remaining': total - paid, 'notes': note}
                db.add_transaction(data)
                st.success("Transaction saved!")
                st.rerun()

elif menu == "Products":
    st.markdown("<h1 style='color: #1E293B; margin-bottom: 2rem;'>Plantations</h1>", unsafe_allow_html=True)
    with st.form("new_plant"):
        col1, col2, col3 = st.columns(3)
        with col1:
            crop = st.text_input("Crop")
        with col2:
            ha = st.number_input("Hectares", min_value=0.0, step=0.1)
        with col3:
            plot = st.text_input("Plot")
        if st.form_submit_button("Add Plantation"):
            if crop and ha > 0 and plot:
                db.add_plantation(crop, ha, plot)
                st.success("Plantation added!")
                st.rerun()
    
    plants_df = db.get_plantations()
    if not plants_df.empty:
        st.dataframe(plants_df[['crop_name', 'hectares', 'plot_name', 'date_planted']], use_container_width=True, hide_index=True)

st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #94A3B8; font-size: 0.85rem;'>
        SMAHI GROUP © 2024 - Professional Farm Management
    </div>
""", unsafe_allow_html=True)
