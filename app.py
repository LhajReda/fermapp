"""
MULTI-TENANT AGRICULTURAL ERP - SaaS Platform
Productly Design - Supabase Backend
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
from supabase import create_client, Client

# ========================================
# CONFIGURATION
# ========================================
st.set_page_config(
    page_title="Agricultural ERP", 
    layout="wide", 
    page_icon="🌾", 
    initial_sidebar_state="expanded"
)

# Supabase Configuration
SUPABASE_URL = "https://wpnfvewscggrkguaofno.supabase.co"
SUPABASE_KEY = "sb_publishable_cETUxgJW9dxXzNpt8lZJJA_g-AsmvxP"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========================================
# PRODUCTLY DESIGN SYSTEM
# ========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Remove Streamlit defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background: #F7F8FC;
        font-family: 'Inter', sans-serif;
    }
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 100%;
    }
    
    /* ========================================
       SIDEBAR DESIGN (Productly Style)
    ======================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #3F4C6B 0%, #515E7E 100%);
        padding: 0;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
        padding: 1.5rem 1rem;
    }
    
    /* Logo */
    .sidebar-logo {
        background: linear-gradient(135deg, #FF7558 0%, #FF6347 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(255, 117, 88, 0.3);
    }
    .sidebar-logo h2 {
        color: white;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }
    
    /* Menu Section Headers */
    .menu-section {
        color: #8896B0;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 2rem 0 0.5rem 1rem;
        font-weight: 600;
    }
    
    /* Menu Items */
    .stButton>button {
        background: transparent;
        color: #A8B3CF;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        width: 100%;
        text-align: left;
        transition: all 0.2s;
        margin: 0.15rem 0;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.08);
        color: white;
        transform: translateX(3px);
    }
    
    /* User Profile Card */
    .user-profile {
        background: linear-gradient(135deg, #FF7558 0%, #FF6347 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        color: white;
        margin-top: 2rem;
    }
    .user-profile .name {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .user-profile .role {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    /* ========================================
       DASHBOARD METRICS CARDS
    ======================================== */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .metric-icon {
        width: 56px;
        height: 56px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        margin-bottom: 1rem;
    }
    .metric-icon.orange {background: linear-gradient(135deg, #FF7558 0%, #FF6347 100%);}
    .metric-icon.blue {background: linear-gradient(135deg, #5B93FF 0%, #4A7FE7 100%);}
    .metric-icon.green {background: linear-gradient(135deg, #5CC97B 0%, #4CAF50 100%);}
    .metric-icon.purple {background: linear-gradient(135deg, #9D7CED 0%, #8B68E8 100%);}
    .metric-icon.yellow {background: linear-gradient(135deg, #FFC107 0%, #FFB300 100%);}
    
    .metric-label {
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }
    .metric-change {
        font-size: 0.75rem;
        font-weight: 600;
    }
    .metric-change.up {color: #10B981;}
    .metric-change.down {color: #EF4444;}
    
    /* ========================================
       ACTIVE BALANCE CARD (Orange Gradient)
    ======================================== */
    .balance-card {
        background: linear-gradient(135deg, #FF7558 0%, #FF6347 100%);
        border-radius: 16px;
        padding: 2rem;
        color: white;
        box-shadow: 0 8px 24px rgba(255, 117, 88, 0.3);
    }
    .balance-title {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
        font-weight: 500;
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
    .balance-btn {
        background: white;
        color: #FF6347;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .balance-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* ========================================
       CHART CONTAINER
    ======================================== */
    .chart-container {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .chart-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1F2937;
    }
    .chart-dropdown {
        background: #F3F4F6;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        color: #374151;
        cursor: pointer;
    }
    
    /* ========================================
       SEARCH BAR
    ======================================== */
    .search-container {
        background: white;
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .search-container input {
        border: none;
        outline: none;
        width: 100%;
        font-size: 0.9rem;
        color: #374151;
    }
    
    /* ========================================
       LOGIN PAGE
    ======================================== */
    .login-container {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-top: 80px;
        text-align: center;
    }
    .login-icon {
        font-size: 70px;
        margin-bottom: 1rem;
    }
    .login-title {
        color: #1F2937;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }
    .login-subtitle {
        color: #6B7280;
        margin-top: 0.5rem;
        font-size: 0.95rem;
    }
    
    /* ========================================
       UPCOMING PAYMENTS CARD
    ======================================== */
    .payments-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-top: 1.5rem;
    }
    .payments-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 1rem;
    }
    .payment-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #F3F4F6;
    }
    .payment-item:last-child {border-bottom: none;}
    .payment-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.75rem;
    }
    .payment-name {
        flex: 1;
        font-size: 0.85rem;
        color: #374151;
    }
    .payment-amount {
        font-size: 0.85rem;
        font-weight: 600;
        color: #FF6347;
    }
    
    /* Hide default Streamlit elements */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        padding: 0.75rem;
    }
    .stSelectbox>div>div>div {
        border-radius: 10px;
        border: 1px solid #E5E7EB;
    }
    
    /* Top bar styling */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    .logout-btn {
        background: white;
        color: #6B7280;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    .logout-btn:hover {
        background: #F9FAFB;
        border-color: #D1D5DB;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# UTILITY FUNCTIONS
# ========================================
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"{amount:,.0f}"

def calculate_percentage_change(current: float, previous: float) -> float:
    """Calculate percentage change"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# ========================================
# DATABASE MANAGER WITH MULTI-TENANCY
# ========================================
class DB:
    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        """Authenticate user and return user data with farm info"""
        try:
            password_hash = hash_password(password)
            response = supabase.table('users')\
                .select('*, farms!inner(id, name, plan_type)')\
                .eq('username', username)\
                .eq('password', password_hash)\
                .eq('is_active', True)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def get_transactions(farm_id: int):
        """Get all transactions for a specific farm"""
        try:
            response = supabase.table('transactions')\
                .select('*')\
                .eq('farm_id', farm_id)\
                .order('date', desc=True)\
                .execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching transactions: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def add_transaction(farm_id: int, data: dict):
        """Add transaction for a specific farm"""
        try:
            transaction_data = {
                'farm_id': farm_id,
                'date': datetime.now().isoformat(),
                'type': data['type'],
                'category': data['category'],
                'partner_name': data['partner'],
                'product': data['product'],
                'quantity': data['quantity'],
                'unit': data['unit'],
                'fuel_liters': data.get('fuel_liters', 0),
                'fuel_station': data.get('fuel_station', ''),
                'price_unit': data['price'],
                'total_price': data['total'],
                'amount_paid': data['paid'],
                'amount_remaining': data['remaining'],
                'notes': data.get('notes', ''),
                'created_by': st.session_state.get('user_id')
            }
            supabase.table('transactions').insert(transaction_data).execute()
            return True
        except Exception as e:
            st.error(f"Error adding transaction: {e}")
            return False
    
    @staticmethod
    def get_expenses(farm_id: int):
        """Get all expenses for a specific farm"""
        try:
            response = supabase.table('expenses')\
                .select('*')\
                .eq('farm_id', farm_id)\
                .order('date', desc=True)\
                .execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching expenses: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def add_expense(farm_id: int, category: str, description: str, amount: float, payment_method: str = None, notes: str = None):
        """Add expense for a specific farm"""
        try:
            expense_data = {
                'farm_id': farm_id,
                'date': datetime.now().isoformat(),
                'category': category,
                'description': description,
                'amount': amount,
                'payment_method': payment_method,
                'notes': notes,
                'created_by': st.session_state.get('user_id')
            }
            supabase.table('expenses').insert(expense_data).execute()
            return True
        except Exception as e:
            st.error(f"Error adding expense: {e}")
            return False
    
    @staticmethod
    def get_workers(farm_id: int):
        """Get all workers for a specific farm"""
        try:
            response = supabase.table('workers')\
                .select('*')\
                .eq('farm_id', farm_id)\
                .order('hire_date', desc=True)\
                .execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching workers: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_plantations(farm_id: int):
        """Get all plantations for a specific farm"""
        try:
            response = supabase.table('plantations')\
                .select('*')\
                .eq('farm_id', farm_id)\
                .order('date_planted', desc=True)\
                .execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching plantations: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def get_dashboard_stats(farm_id: int, period_days: int = 30):
        """Get dashboard statistics for a specific farm"""
        try:
            date_threshold = (datetime.now() - timedelta(days=period_days)).isoformat()
            prev_date = (datetime.now() - timedelta(days=period_days*2)).isoformat()
            
            stats = {}
            
            # Total sales (Revenue)
            sales_response = supabase.table('transactions')\
                .select('total_price')\
                .eq('farm_id', farm_id)\
                .eq('type', 'Vente')\
                .gte('date', date_threshold)\
                .execute()
            stats['total_sales'] = sum([item['total_price'] for item in sales_response.data]) if sales_response.data else 0
            
            # Total purchases
            purchases_response = supabase.table('transactions')\
                .select('total_price')\
                .eq('farm_id', farm_id)\
                .eq('type', 'Achat')\
                .gte('date', date_threshold)\
                .execute()
            stats['total_purchases'] = sum([item['total_price'] for item in purchases_response.data]) if purchases_response.data else 0
            
            # Total expenses
            expenses_response = supabase.table('expenses')\
                .select('amount')\
                .eq('farm_id', farm_id)\
                .gte('date', date_threshold)\
                .execute()
            stats['total_expenses'] = sum([item['amount'] for item in expenses_response.data]) if expenses_response.data else 0
            
            # Outstanding payments
            outstanding_response = supabase.table('transactions')\
                .select('amount_remaining')\
                .eq('farm_id', farm_id)\
                .gt('amount_remaining', 0)\
                .execute()
            stats['outstanding'] = sum([item['amount_remaining'] for item in outstanding_response.data]) if outstanding_response.data else 0
            
            # Previous period sales
            prev_sales_response = supabase.table('transactions')\
                .select('total_price')\
                .eq('farm_id', farm_id)\
                .eq('type', 'Vente')\
                .gte('date', prev_date)\
                .lt('date', date_threshold)\
                .execute()
            stats['prev_sales'] = sum([item['total_price'] for item in prev_sales_response.data]) if prev_sales_response.data else 0
            
            # Previous period purchases
            prev_purchases_response = supabase.table('transactions')\
                .select('total_price')\
                .eq('farm_id', farm_id)\
                .eq('type', 'Achat')\
                .gte('date', prev_date)\
                .lt('date', date_threshold)\
                .execute()
            stats['prev_purchases'] = sum([item['total_price'] for item in prev_purchases_response.data]) if prev_purchases_response.data else 0
            
            # Active workers count
            workers_response = supabase.table('workers')\
                .select('id', count='exact')\
                .eq('farm_id', farm_id)\
                .eq('status', 'active')\
                .execute()
            stats['active_workers'] = workers_response.count if workers_response.count else 0
            
            # Total stock items (unique products from plantations)
            plantations_response = supabase.table('plantations')\
                .select('crop_name')\
                .eq('farm_id', farm_id)\
                .eq('status', 'En cours')\
                .execute()
            stats['stock_items'] = len(plantations_response.data) if plantations_response.data else 0
            
            return stats
        except Exception as e:
            st.error(f"Error fetching dashboard stats: {e}")
            return {
                'total_sales': 0, 'total_purchases': 0, 'total_expenses': 0,
                'outstanding': 0, 'prev_sales': 0, 'prev_purchases': 0, 
                'active_workers': 0, 'stock_items': 0
            }

db = DB()

# ========================================
# SESSION STATE INITIALIZATION
# ========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'selected_menu' not in st.session_state:
    st.session_state['selected_menu'] = "Dashboard"

# ========================================
# LOGIN PAGE
# ========================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class='login-container'>
                <div class='login-icon'>🌾</div>
                <h1 class='login-title'>Agricultural ERP</h1>
                <p class='login-subtitle'>Multi-Tenant Farm Management System</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_btn = st.form_submit_button("🔐 Sign In", use_container_width=True)
            with col_btn2:
                demo_btn = st.form_submit_button("🎭 Demo Login", use_container_width=True)
            
            if login_btn:
                if username and password:
                    user_data = db.authenticate_user(username, password)
                    if user_data:
                        st.session_state['logged_in'] = True
                        st.session_state['user_id'] = user_data['id']
                        st.session_state['username'] = user_data['username']
                        st.session_state['full_name'] = user_data.get('full_name', username)
                        st.session_state['role'] = user_data['role']
                        st.session_state['farm_id'] = user_data['farm_id']
                        st.session_state['farm_name'] = user_data['farms']['name']
                        st.session_state['plan_type'] = user_data['farms']['plan_type']
                        st.success(f"Welcome back, {user_data.get('full_name', username)}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
            
            if demo_btn:
                # Auto-login with demo account
                user_data = db.authenticate_user('admin', 'admin123')
                if user_data:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user_data['id']
                    st.session_state['username'] = user_data['username']
                    st.session_state['full_name'] = user_data.get('full_name', 'Demo User')
                    st.session_state['role'] = user_data['role']
                    st.session_state['farm_id'] = user_data['farm_id']
                    st.session_state['farm_name'] = user_data['farms']['name']
                    st.session_state['plan_type'] = user_data['farms']['plan_type']
                    st.success("🎭 Logged in as Demo User (SMAHI GROUP)")
                    st.rerun()
        
        st.markdown("""
            <div style='text-align: center; margin-top: 2rem; color: #9CA3AF; font-size: 0.85rem;'>
                <p><strong>Demo Credentials:</strong></p>
                <p>Username: <code>admin</code> | Password: <code>admin123</code></p>
                <p style='margin-top: 1rem; font-size: 0.75rem;'>
                    🔒 Secure Multi-Tenant Architecture | 🌍 Built with Supabase
                </p>
            </div>
        """, unsafe_allow_html=True)

# ========================================
# CHECK AUTHENTICATION
# ========================================
if not st.session_state['logged_in']:
    login_page()
    st.stop()

# ========================================
# SIDEBAR NAVIGATION
# ========================================
with st.sidebar:
    st.markdown(f"""
        <div class='sidebar-logo'>
            <h2>🌾 Productly</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Display farm info
    st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 0.75rem; margin-bottom: 1.5rem; color: white;'>
            <div style='font-size: 0.7rem; opacity: 0.7; margin-bottom: 0.25rem;'>CURRENT FARM</div>
            <div style='font-weight: 600; font-size: 0.9rem;'>{st.session_state['farm_name']}</div>
            <div style='font-size: 0.75rem; opacity: 0.8; margin-top: 0.25rem;'>{st.session_state['plan_type'].upper()} PLAN</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='menu-section'>MENU</p>", unsafe_allow_html=True)
    
    menu_items = [
        ("Dashboard", "📊"),
        ("Analytics", "📈"),
        ("Sales", "💰"),
        ("Management", "⚙️")
    ]
    
    for item, icon in menu_items:
        if st.button(f"{icon}  {item}", key=f"menu_{item}"):
            st.session_state['selected_menu'] = item
            st.rerun()
    
    st.markdown("<p class='menu-section'>MANAGEMENT</p>", unsafe_allow_html=True)
    
    management_items = [
        ("Products", "📦"),
        ("Customer", "👥"),
        ("Warehouse", "🏢"),
        ("Reports", "📋")
    ]
    
    for item, icon in management_items:
        if st.button(f"{icon}  {item}", key=f"mgmt_{item}"):
            st.session_state['selected_menu'] = item
            st.rerun()
    
    st.markdown("<p class='menu-section'>NOTIFICATIONS</p>", unsafe_allow_html=True)
    
    notif_items = [
        ("Transaction", "💳"),
        ("Message", "✉️")
    ]
    
    for item, icon in notif_items:
        if st.button(f"{icon}  {item}", key=f"notif_{item}"):
            st.session_state['selected_menu'] = item
            st.rerun()
    
    # User Profile at bottom
    st.markdown(f"""
        <div class='user-profile'>
            <div class='name'>{st.session_state.get('full_name', 'User')}</div>
            <div class='role'>{st.session_state.get('role', 'user').title()}</div>
        </div>
    """, unsafe_allow_html=True)

# ========================================
# TOP BAR WITH SEARCH AND LOGOUT
# ========================================
col_search, col_actions = st.columns([3, 1])

with col_search:
    st.markdown("""
        <div class='search-container'>
            <span>🔍</span>
            <input type='text' placeholder='Search transactions, products, workers...'>
        </div>
    """, unsafe_allow_html=True)

with col_actions:
    if st.button("🔔", key="notifications"):
        st.info("No new notifications")
    if st.button("🌙", key="dark_mode"):
        st.info("Dark mode coming soon")
    if st.button("🚪 Log Out", key="logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ========================================
# PAGE ROUTING
# ========================================
menu = st.session_state['selected_menu']
farm_id = st.session_state['farm_id']

# ========================================
# DASHBOARD PAGE
# ========================================
if menu == "Dashboard":
    # Get statistics
    stats = db.get_dashboard_stats(farm_id, 30)
    net_profit = stats['total_sales'] - stats['total_purchases'] - stats['total_expenses']
    sales_change = calculate_percentage_change(stats['total_sales'], stats['prev_sales'])
    
    # Top Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        change_icon = "↑" if sales_change >= 0 else "↓"
        change_class = "up" if sales_change >= 0 else "down"
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon orange'>📈</div>
                <div class='metric-label'>Total Revenue</div>
                <div class='metric-value'>${format_currency(stats['total_sales'])}</div>
                <div class='metric-change {change_class}'>{change_icon} {abs(sales_change):.1f}% Incomes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        daily_sales = stats['total_sales'] / 30
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon blue'>🎯</div>
                <div class='metric-label'>Daily Revenue</div>
                <div class='metric-value'>${format_currency(daily_sales)}</div>
                <div class='metric-change down'>↓ 13% Sales</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon green'>👥</div>
                <div class='metric-label'>Workers Present</div>
                <div class='metric-value'>{stats['active_workers']}</div>
                <div class='metric-change up'>↑ 48% Ouvriers</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon purple'>📦</div>
                <div class='metric-label'>Stock Items</div>
                <div class='metric-value'>{stats['stock_items']}</div>
                <div class='metric-change up'>↑ 25% Active Crops</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon yellow'>💰</div>
                <div class='metric-label'>Expenses</div>
                <div class='metric-value'>${format_currency(stats['total_expenses'])}</div>
                <div class='metric-change down'>Target Expenses</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chart + Balance Card Row
    col_chart, col_balance = st.columns([2, 1])
    
    with col_chart:
        st.markdown("""
            <div class='chart-container'>
                <div class='chart-header'>
                    <div class='chart-title'>Summary Sales</div>
                    <select class='chart-dropdown'>
                        <option>Month</option>
                        <option>Week</option>
                        <option>Year</option>
                    </select>
                </div>
        """, unsafe_allow_html=True)
        
        # Get daily sales data
        df = db.get_transactions(farm_id)
        if not df.empty:
            df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
            df = df[~df['date_dt'].isna()].copy()
            df['Date'] = df['date_dt'].dt.strftime("%Y-%m-%d")
            daily_sales = df[df['type'] == 'Vente'].groupby('Date')['total_price'].sum().reset_index()
            daily_sales = daily_sales.sort_values('Date').tail(12)
            
            # Create smooth area chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_sales['Date'],
                y=daily_sales['total_price'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(255, 117, 88, 0.15)',
                line=dict(color='#FF7558', width=3, shape='spline'),
                hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(
                    showgrid=False,
                    showline=False,
                    tickfont=dict(size=10, color='#9CA3AF')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#F3F4F6',
                    showline=False,
                    tickfont=dict(size=10, color='#9CA3AF')
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data available yet")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_balance:
        # Create balance card using Streamlit components with custom styling
        balance_html = f"""
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
            
            <button class='balance-btn'>Add Virtual Card ▶</button>
        </div>
        """
        st.markdown(balance_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Row: Last Orders + Upcoming Payments
    col_orders, col_payments = st.columns([2, 1])
    
    with col_orders:
        st.markdown("""
            <div class='chart-container'>
                <div class='chart-header'>
                    <div class='chart-title'>Last Order</div>
                    <button class='chart-dropdown' style='cursor: pointer;'>Filter</button>
                </div>
        """, unsafe_allow_html=True)
        
        recent_transactions = df.head(5) if not df.empty else pd.DataFrame()
        if not recent_transactions.empty:
            st.dataframe(
                recent_transactions[['partner_name', 'product', 'total_price', 'date']].rename(columns={
                    'partner_name': 'Customer',
                    'product': 'Product',
                    'total_price': 'Price',
                    'date': 'Date'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions yet")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_payments:
        st.markdown("""
            <div class='payments-card'>
                <div class='payments-title'>Upcoming Payments</div>
                <div class='payment-item'>
                    <div style='display: flex; align-items: center;'>
                        <div class='payment-dot' style='background: #5CC97B;'></div>
                        <span class='payment-name'>Easy Pay Way.</span>
                    </div>
                    <span class='payment-amount'>$82258.23</span>
                </div>
                <div class='payment-item'>
                    <div style='display: flex; align-items: center;'>
                        <div class='payment-dot' style='background: #FFC107;'></div>
                        <span class='payment-name'>Payonner.</span>
                    </div>
                    <span class='payment-amount'>$64486.69</span>
                </div>
                <div class='payment-item'>
                    <div style='display: flex; align-items: center;'>
                        <div class='payment-dot' style='background: #FF7558;'></div>
                        <span class='payment-name'>FastSpring.</span>
                    </div>
                    <span class='payment-amount'>$4210.38</span>
                </div>
                <button class='balance-btn' style='margin-top: 1rem; background: #F9FAFB; color: #374151;'>More</button>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Expenses Status Widget
        st.markdown("""
            <div class='payments-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                    <div class='payments-title' style='margin: 0;'>Expenses Status</div>
                    <span style='font-size: 0.75rem; color: #10B981; font-weight: 600;'>On Track</span>
                </div>
        """, unsafe_allow_html=True)
        
        # Mini expense chart
        expenses_df = db.get_expenses(farm_id)
        if not expenses_df.empty:
            expenses_df['date_dt'] = pd.to_datetime(expenses_df['date'], errors='coerce')
            expenses_df = expenses_df[~expenses_df['date_dt'].isna()].copy()
            expenses_df['Date'] = expenses_df['date_dt'].dt.strftime("%Y-%m-%d")
            daily_expenses = expenses_df.groupby('Date')['amount'].sum().reset_index()
            daily_expenses = daily_expenses.sort_values('Date').tail(10)
            
            fig_expenses = go.Figure()
            fig_expenses.add_trace(go.Scatter(
                x=daily_expenses['Date'],
                y=daily_expenses['amount'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(255, 117, 88, 0.1)',
                line=dict(color='#FF7558', width=2, shape='spline'),
                showlegend=False
            ))
            
            fig_expenses.update_layout(
                height=120,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, showticklabels=False, showline=False),
                yaxis=dict(showgrid=False, showticklabels=False, showline=False),
                hovermode=False
            )
            
            st.plotly_chart(fig_expenses, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ========================================
# SALES PAGE
# ========================================
elif menu == "Sales":
    st.markdown("<h1 style='color: #1F2937; margin-bottom: 2rem;'>💰 Sales Management</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 New Transaction", "📊 Transaction History"])
    
    with tab1:
        with st.form("new_transaction", clear_on_submit=True):
            st.markdown("### Transaction Details")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                type_op = st.selectbox("Type *", ["Vente", "Achat"])
                category = st.selectbox("Category *", ["Cereales", "Legumineuses", "Engrais", "Mazot", "Semences", "Other"])
            with col2:
                partner = st.text_input("Partner Name *")
                product = st.text_input("Product *")
            with col3:
                price = st.number_input("Unit Price (DH) *", min_value=0.0, step=0.01)
                paid = st.number_input("Amount Paid (DH)", min_value=0.0, step=0.01)
            
            if "Mazot" in category:
                col_fuel1, col_fuel2 = st.columns(2)
                with col_fuel1:
                    liters = st.number_input("Liters *", min_value=0.0, step=1.0)
                with col_fuel2:
                    station = st.text_input("Fuel Station")
                quantity, unit = 0, "L"
            else:
                col_qty1, col_qty2 = st.columns(2)
                with col_qty1:
                    quantity = st.number_input("Quantity *", min_value=0.0, step=1.0)
                with col_qty2:
                    unit = st.selectbox("Unit", ["kg", "T", "qx", "sac", "L"])
                liters, station = 0, ""
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("💾 Save Transaction", use_container_width=True):
                if partner and product and (quantity > 0 or liters > 0) and price > 0:
                    total = (liters * price) if liters > 0 else (quantity * price)
                    data = {
                        'type': type_op,
                        'category': category,
                        'partner': partner,
                        'product': product,
                        'quantity': quantity,
                        'unit': unit,
                        'fuel_liters': liters,
                        'fuel_station': station,
                        'price': price,
                        'total': total,
                        'paid': paid,
                        'remaining': total - paid,
                        'notes': notes
                    }
                    if db.add_transaction(farm_id, data):
                        st.success("✅ Transaction saved successfully!")
                        st.rerun()
                else:
                    st.error("❌ Please fill all required fields (*)")
    
    with tab2:
        transactions_df = db.get_transactions(farm_id)
        if not transactions_df.empty:
            st.dataframe(
                transactions_df[['date', 'type', 'category', 'partner_name', 'product', 'total_price', 'amount_remaining']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions found for your farm")

# ========================================
# PRODUCTS PAGE (Plantations)
# ========================================
elif menu == "Products":
    st.markdown("<h1 style='color: #1F2937; margin-bottom: 2rem;'>📦 Plantations Management</h1>", unsafe_allow_html=True)
    
    plantations_df = db.get_plantations(farm_id)
    if not plantations_df.empty:
        st.dataframe(
            plantations_df[['crop_name', 'hectares', 'plot_name', 'date_planted', 'status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No plantations found for your farm")

# ========================================
# CUSTOMER PAGE (Workers)
# ========================================
elif menu == "Customer":
    st.markdown("<h1 style='color: #1F2937; margin-bottom: 2rem;'>👥 Workers Management</h1>", unsafe_allow_html=True)
    
    workers_df = db.get_workers(farm_id)
    if not workers_df.empty:
        st.dataframe(
            workers_df[['full_name', 'phone', 'role', 'daily_wage', 'hire_date', 'status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No workers found for your farm")

# ========================================
# ANALYTICS PAGE
# ========================================
elif menu == "Analytics":
    st.markdown("<h1 style='color: #1F2937; margin-bottom: 2rem;'>📈 Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.info("📊 Advanced analytics coming soon...")

# ========================================
# OTHER PAGES
# ========================================
else:
    st.markdown(f"<h1 style='color: #1F2937; margin-bottom: 2rem;'>{menu}</h1>", unsafe_allow_html=True)
    st.info(f"The {menu} page is under construction. Check back soon!")

# ========================================
# FOOTER
# ========================================
st.markdown("""
    <div style='text-align: center; padding: 3rem 0 1rem 0; color: #9CA3AF; font-size: 0.85rem;'>
        Agricultural ERP © 2024 | Multi-Tenant SaaS Platform | Powered by Supabase
    </div>
""", unsafe_allow_html=True)
