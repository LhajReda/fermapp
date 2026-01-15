"""
SMAHI GROUP - Professional Farm Management System
Productly Design Style - Supabase Version
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF
import hashlib
from supabase import create_client, Client

st.set_page_config(page_title="SMAHI GROUP", layout="wide", page_icon="🌾", initial_sidebar_state="expanded")

# Supabase Configuration
SUPABASE_URL = "https://wpnfvewscggrkguaofno.supabase.co"
SUPABASE_KEY = "sb_publishable_cETUxgJW9dxXzNpt8lZJJA_g-AsmvxP"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def format_currency(amount):
    return f"{amount:,.0f}"

def calculate_percentage_change(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# Database Manager with Supabase
class DB:
    @staticmethod
    def get_transactions():
        try:
            response = supabase.table('transactions').select('*').order('date', desc=True).execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching transactions: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def add_transaction(data):
        try:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction_data = {
                'date': dt,
                'type': data['type'],
                'category': data['category'],
                'partner_name': data['partner'],
                'product': data['product'],
                'quantity': data['quantity'],
                'unit': data['unit'],
                'fuel_liters': data['fuel_liters'],
                'fuel_station': data['fuel_station'],
                'price_unit': data['price'],
                'total_price': data['total'],
                'amount_paid': data['paid'],
                'amount_remaining': data['remaining'],
                'notes': data['notes']
            }
            supabase.table('transactions').insert(transaction_data).execute()
        except Exception as e:
            st.error(f"Error adding transaction: {e}")
    
    @staticmethod
    def get_plantations():
        try:
            response = supabase.table('plantations').select('*').order('date_planted', desc=True).execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching plantations: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def add_plantation(crop, hectares, plot, expected_harvest=None, notes=None):
        try:
            dt = datetime.now().strftime("%Y-%m-%d")
            plantation_data = {
                'date_planted': dt,
                'crop_name': crop,
                'hectares': hectares,
                'plot_name': plot,
                'expected_harvest': expected_harvest,
                'notes': notes,
                'status': 'En cours'
            }
            supabase.table('plantations').insert(plantation_data).execute()
        except Exception as e:
            st.error(f"Error adding plantation: {e}")
    
    @staticmethod
    def get_expenses():
        try:
            response = supabase.table('expenses').select('*').order('date', desc=True).execute()
            if response.data:
                return pd.DataFrame(response.data)
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error fetching expenses: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def add_expense(category, description, amount, payment_method=None, notes=None):
        try:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            expense_data = {
                'date': dt,
                'category': category,
                'description': description,
                'amount': amount,
                'payment_method': payment_method,
                'notes': notes
            }
            supabase.table('expenses').insert(expense_data).execute()
        except Exception as e:
            st.error(f"Error adding expense: {e}")
    
    @staticmethod
    def get_dashboard_stats(period_days=30):
        try:
            date_threshold = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
            prev_date = (datetime.now() - timedelta(days=period_days*2)).strftime("%Y-%m-%d")
            
            stats = {}
            
            # Total sales
            sales_response = supabase.table('transactions').select('total_price').eq('type', 'Vente').gte('date', date_threshold).execute()
            stats['total_sales'] = sum([item['total_price'] for item in sales_response.data]) if sales_response.data else 0
            
            # Total purchases
            purchases_response = supabase.table('transactions').select('total_price').eq('type', 'Achat').gte('date', date_threshold).execute()
            stats['total_purchases'] = sum([item['total_price'] for item in purchases_response.data]) if purchases_response.data else 0
            
            # Total expenses
            expenses_response = supabase.table('expenses').select('amount').gte('date', date_threshold).execute()
            stats['total_expenses'] = sum([item['amount'] for item in expenses_response.data]) if expenses_response.data else 0
            
            # Total fuel
            fuel_response = supabase.table('transactions').select('fuel_liters').like('category', '%Mazot%').gte('date', date_threshold).execute()
            stats['total_fuel'] = sum([item['fuel_liters'] for item in fuel_response.data]) if fuel_response.data else 0
            
            # Outstanding
            outstanding_response = supabase.table('transactions').select('amount_remaining').gt('amount_remaining', 0).execute()
            stats['outstanding'] = sum([item['amount_remaining'] for item in outstanding_response.data]) if outstanding_response.data else 0
            
            # Previous sales
            prev_sales_response = supabase.table('transactions').select('total_price').eq('type', 'Vente').gte('date', prev_date).lt('date', date_threshold).execute()
            stats['prev_sales'] = sum([item['total_price'] for item in prev_sales_response.data]) if prev_sales_response.data else 0
            
            # Previous purchases
            prev_purchases_response = supabase.table('transactions').select('total_price').eq('type', 'Achat').gte('date', prev_date).lt('date', date_threshold).execute()
            stats['prev_purchases'] = sum([item['total_price'] for item in prev_purchases_response.data]) if prev_purchases_response.data else 0
            
            return stats
        except Exception as e:
            st.error(f"Error fetching dashboard stats: {e}")
            return {
                'total_sales': 0, 'total_purchases': 0, 'total_expenses': 0,
                'total_fuel': 0, 'outstanding': 0, 'prev_sales': 0, 'prev_purchases': 0
            }

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
