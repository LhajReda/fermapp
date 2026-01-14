"""
SMAHI GROUP - ULTIMATE AGRICULTURAL ERP
Complete Farm Management System
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF
import hashlib
import os

st.set_page_config(page_title="SMAHI GROUP ERP", layout="wide", page_icon="🌾")

DB_NAME = "smahi_ultimate.db"
PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

COMPANY = {
    "name": "SMAHI GROUP",
    "ice": "002165492000071",
    "address": "Sidi Bennour, Maroc",
    "phone": "+212 XXX XXXXXX",
    "email": "contact@smahigroup.ma"
}

# CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * {font-family: 'Inter', sans-serif;}
    #MainMenu, footer, header {visibility: hidden;}
    .main {background: #f8fafc; padding: 2rem 3rem;}
    [data-testid="stSidebar"] {background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);}
    .page-header {background: white; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border-left: 5px solid #3b82f6;}
    .page-title {font-size: 1.875rem; font-weight: 700; color: #0f172a; margin: 0 0 0.5rem 0;}
    .page-subtitle {font-size: 0.95rem; color: #64748b; margin: 0;}
    .kpi-card {background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border-left: 4px solid; transition: all 0.3s ease; height: 100%;}
    .kpi-card:hover {box-shadow: 0 8px 16px rgba(0,0,0,0.1); transform: translateY(-4px);}
    .kpi-label {font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: #64748b; margin-bottom: 0.75rem;}
    .kpi-value {font-size: 2.25rem; font-weight: 800; color: #0f172a; margin: 0.75rem 0;}
    .border-blue {border-left-color: #3b82f6;} .border-green {border-left-color: #10b981;}
    .border-purple {border-left-color: #8b5cf6;} .border-orange {border-left-color: #f59e0b;}
    .border-red {border-left-color: #ef4444;} .border-pink {border-left-color: #ec4899;}
    .content-card {background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 2rem;}
    .card-title {font-size: 1.125rem; font-weight: 700; color: #0f172a; margin-bottom: 1.5rem;}
    .stButton>button {background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border: none; border-radius: 10px; padding: 0.625rem 1.5rem; font-weight: 600;}
    .stButton>button:hover {background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); transform: translateY(-2px);}
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
    c.execute('''CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
        phone TEXT, job_title TEXT, daily_wage REAL, status TEXT DEFAULT 'active',
        notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS work_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, worker_id INTEGER, date TEXT NOT NULL,
        hours_worked REAL, wage_paid REAL, task TEXT, notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (worker_id) REFERENCES workers(id)
    )''')
    conn.commit()
    conn.close()

init_db()

def format_currency(amount):
    return f"{amount:,.2f} DH"

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
    def get_workers():
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query("SELECT * FROM workers WHERE status='active' ORDER BY name", conn)
        conn.close()
        return df
    
    @staticmethod
    def add_worker(name, phone=None, job_title=None, daily_wage=None, notes=None):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO workers (name, phone, job_title, daily_wage, notes)
            VALUES (?, ?, ?, ?, ?)''', (name, phone, job_title, daily_wage, notes))
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
        
        conn.close()
        return stats

db = DB()

# PDF Generator
class PDFGen:
    @staticmethod
    def create_document(data, doc_type="Bon de Livraison"):
        class PDF(FPDF):
            def header(self):
                color = (59, 130, 246) if doc_type == "Bon de Livraison" else (16, 185, 129)
                self.set_fill_color(*color)
                self.rect(0, 0, 210, 40, 'F')
                self.set_text_color(255, 255, 255)
                self.set_font('Arial', 'B', 20)
                self.cell(0, 20, '', 0, 1)
                self.cell(0, 10, COMPANY['name'], 0, 1, 'C')
                self.set_text_color(0, 0, 0)
                self.ln(10)
            def footer(self):
                self.set_y(-20)
                self.set_font('Arial', 'I', 8)
                self.set_text_color(128, 128, 128)
                self.cell(0, 5, f"{COMPANY['address']} | ICE: {COMPANY['ice']}", 0, 1, 'C')
                self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'C')
        
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 12, doc_type.upper(), 0, 1, 'C')
        pdf.ln(8)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(95, 8, f"Document N: {data['id']}", 0, 0)
        pdf.cell(0, 8, f"Date: {str(data['date'])[:10]}", 0, 1, 'R')
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'CLIENT', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 7, f"Nom: {data['partner_name']}", 0, 1)
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(70, 10, 'Produit', 1, 0, 'C')
        pdf.cell(30, 10, 'Quantite', 1, 0, 'C')
        pdf.cell(30, 10, 'Prix Unit.', 1, 0, 'C')
        pdf.cell(40, 10, 'Total', 1, 1, 'C')
        pdf.set_font('Arial', '', 10)
        produit = str(data['product'])
        if "Mazot" in str(data.get('category', '')):
            qte = f"{data['fuel_liters']:,.2f} L"
        else:
            qte = f"{data['quantity']:,.2f} {data['unit']}"
        prix = data['price_unit']
        total = data['total_price']
        pdf.cell(70, 10, produit, 1, 0, 'L')
        pdf.cell(30, 10, qte, 1, 0, 'C')
        pdf.cell(30, 10, f"{prix:,.2f} DH", 1, 0, 'R')
        pdf.cell(40, 10, f"{total:,.2f} DH", 1, 1, 'R')
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(130, 12, 'TOTAL', 1, 0, 'R')
        pdf.cell(40, 12, f"{total:,.2f} DH", 1, 1, 'R')
        if data.get('amount_paid', 0) > 0:
            pdf.set_font('Arial', '', 10)
            pdf.cell(130, 8, 'Montant Paye', 1, 0, 'R')
            pdf.cell(40, 8, f"{data['amount_paid']:,.2f} DH", 1, 1, 'R')
            remaining = total - data['amount_paid']
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(130, 8, 'Reste a Payer', 1, 0, 'R')
            pdf.cell(40, 8, f"{remaining:,.2f} DH", 1, 1, 'R')
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
                <h1 style='color: #0f172a; font-size: 2rem; font-weight: 800; margin: 0;'>
                    SMAHI GROUP ERP
                </h1>
                <p style='color: #64748b; margin-top: 0.5rem;'>
                    Complete Farm Management System
                </p>
            </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("", type="password", placeholder="Enter password", label_visibility="collapsed")
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

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);'>
            <div style='width: 70px; height: 70px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); 
                        border-radius: 16px; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;'>
                <span style='font-size: 2.5rem;'>🌾</span>
            </div>
            <h2 style='color: white; font-size: 1.5rem; font-weight: 800; margin: 0;'>SMAHI GROUP</h2>
            <p style='color: rgba(255,255,255,0.6); font-size: 0.75rem; margin-top: 0.5rem;'>Ultimate Farm ERP</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu_items = [
        ("Dashboard", "📊"), ("Transactions", "💰"), ("Historique", "📋"),
        ("Plantations", "🌱"), ("Expenses", "💸"), ("Workers", "👷"), ("Settings", "⚙️")
    ]
    
    for item, icon in menu_items:
        if st.button(f"{icon}  {item}", key=f"menu_{item}", use_container_width=True):
            st.session_state['selected_menu'] = item
            st.rerun()
    
    st.markdown("<br><hr style='border: none; border-top: 1px solid rgba(255,255,255,0.1);'><br>", unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state['logged_in'] = False
        st.rerun()

menu = st.session_state['selected_menu']

# DASHBOARD
if menu == "Dashboard":
    st.markdown("""
        <div class='page-header'>
            <h1 class='page-title'>Dashboard Complet</h1>
            <p class='page-subtitle'>Vue d'ensemble de votre exploitation agricole</p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = db.get_dashboard_stats(30)
    net_profit = stats['total_sales'] - stats['total_purchases'] - stats['total_expenses']
    sales_change = calculate_percentage_change(stats['total_sales'], stats['prev_sales'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='kpi-card border-green'>
                <div class='kpi-label'>Total Ventes</div>
                <div class='kpi-value'>{format_currency(stats['total_sales'])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='kpi-card border-red'>
                <div class='kpi-label'>Total Achats</div>
                <div class='kpi-value'>{format_currency(stats['total_purchases'])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='kpi-card border-blue'>
                <div class='kpi-label'>Benefice Net</div>
                <div class='kpi-value'>{format_currency(net_profit)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='kpi-card border-orange'>
                <div class='kpi-label'>Carburant</div>
                <div class='kpi-value'>{stats['total_fuel']:,.0f} L</div>
            </div>
        """, unsafe_allow_html=True)
    
    df = db.get_transactions()
    if not df.empty:
        st.markdown("<div class='content-card'><div class='card-title'>Activite Financiere</div>", unsafe_allow_html=True)
        df['date_dt'] = pd.to_datetime(df['date'], errors='coerce')
        df = df[~df['date_dt'].isna()].copy()
        df['Date'] = df['date_dt'].dt.strftime("%Y-%m-%d")
        daily = df.groupby(['Date', 'type'])['total_price'].sum().reset_index().sort_values('Date')
        fig = go.Figure()
        ventes = daily[daily['type'] == 'Vente']
        achats = daily[daily['type'] == 'Achat']
        fig.add_trace(go.Scatter(x=ventes['Date'], y=ventes['total_price'], mode='lines+markers', name='Ventes', line=dict(color='#10b981', width=3)))
        fig.add_trace(go.Scatter(x=achats['Date'], y=achats['total_price'], mode='lines+markers', name='Achats', line=dict(color='#ef4444', width=3)))
        fig.update_layout(height=400, plot_bgcolor='white', margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Transactions":
    st.markdown("<div class='page-header'><h1 class='page-title'>Nouvelle Transaction</h1></div>", unsafe_allow_html=True)
    
    with st.form("new_trans"):
        col1, col2, col3 = st.columns(3)
        with col1:
            type_op = st.selectbox("Type", ["Vente", "Achat"])
            cat = st.selectbox("Categorie", ["Cereales", "Legumineuses", "Engrais", "Mazot", "Semences", "Autre"])
        with col2:
            partner = st.text_input("Partenaire")
            prod = st.text_input("Produit")
        with col3:
            price = st.number_input("Prix Unitaire (DH)", min_value=0.0, step=0.01)
            paid = st.number_input("Montant Paye (DH)", min_value=0.0, step=0.01)
        
        if "Mazot" in cat:
            l = st.number_input("Litres", min_value=0.0, step=1.0)
            stn = st.text_input("Station")
            qte, unit = 0, "L"
        else:
            qte = st.number_input("Quantite", min_value=0.0, step=1.0)
            unit = st.selectbox("Unite", ["kg", "T", "qx", "sac"])
            l, stn = 0, ""
        
        note = st.text_area("Notes")
        
        if st.form_submit_button("Enregistrer", use_container_width=True):
            if partner and prod and (qte > 0 or l > 0) and price > 0:
                total = (l * price) if l > 0 else (qte * price)
                data = {'type': type_op, 'category': cat, 'partner': partner, 'product': prod, 'quantity': qte, 'unit': unit, 'fuel_liters': l, 'fuel_station': stn, 'price': price, 'total': total, 'paid': paid, 'remaining': total - paid, 'notes': note}
                db.add_transaction(data)
                st.success("Transaction enregistree!")
                st.rerun()

elif menu == "Historique":
    st.markdown("<div class='page-header'><h1 class='page-title'>Historique</h1></div>", unsafe_allow_html=True)
    df = db.get_transactions()
    if not df.empty:
        st.dataframe(df[['id', 'date', 'type', 'partner_name', 'product', 'total_price']], use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            trans_id = st.number_input("ID Transaction", min_value=1, value=1)
        with col2:
            doc_type = st.selectbox("Type", ["Bon de Livraison", "Facture"])
        with col3:
            st.write("")
            st.write("")
            if st.button("Generer", use_container_width=True):
                row = df[df['id'] == trans_id]
                if not row.empty:
                    pdf_bytes = pdf_gen.create_document(row.iloc[0].to_dict(), doc_type)
                    st.download_button("Telecharger", pdf_bytes, f"{doc_type}_{trans_id}.pdf", "application/pdf")

elif menu == "Plantations":
    st.markdown("<div class='page-header'><h1 class='page-title'>Plantations</h1></div>", unsafe_allow_html=True)
    with st.form("new_plant"):
        col1, col2, col3 = st.columns(3)
        with col1:
            crop = st.text_input("Culture")
        with col2:
            ha = st.number_input("Hectares", min_value=0.0, step=0.1)
        with col3:
            plot = st.text_input("Parcelle")
        if st.form_submit_button("Ajouter"):
            if crop and ha > 0 and plot:
                db.add_plantation(crop, ha, plot)
                st.success("Plantation ajoutee!")
                st.rerun()
    plants_df = db.get_plantations()
    if not plants_df.empty:
        st.dataframe(plants_df[['crop_name', 'hectares', 'plot_name', 'date_planted']], use_container_width=True, hide_index=True)

elif menu == "Expenses":
    st.markdown("<div class='page-header'><h1 class='page-title'>Depenses</h1></div>", unsafe_allow_html=True)
    with st.form("new_expense"):
        col1, col2 = st.columns(2)
        with col1:
            cat = st.selectbox("Categorie", ["Electricite", "Eau", "Entretien", "Transport", "Autre"])
            amount = st.number_input("Montant (DH)", min_value=0.0, step=0.01)
        with col2:
            desc = st.text_input("Description")
            payment = st.selectbox("Paiement", ["Especes", "Cheque", "Virement"])
        if st.form_submit_button("Enregistrer"):
            if cat and desc and amount > 0:
                db.add_expense(cat, desc, amount, payment)
                st.success("Depense enregistree!")
                st.rerun()
    exp_df = db.get_expenses()
    if not exp_df.empty:
        st.dataframe(exp_df[['date', 'category', 'description', 'amount']], use_container_width=True, hide_index=True)

elif menu == "Workers":
    st.markdown("<div class='page-header'><h1 class='page-title'>Ouvriers</h1></div>", unsafe_allow_html=True)
    with st.form("new_worker"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nom")
            phone = st.text_input("Telephone")
        with col2:
            job = st.text_input("Fonction")
            wage = st.number_input("Salaire/Jour (DH)", min_value=0.0, step=10.0)
        if st.form_submit_button("Ajouter"):
            if name:
                db.add_worker(name, phone, job, wage)
                st.success("Ouvrier ajoute!")
                st.rerun()
    workers_df = db.get_workers()
    if not workers_df.empty:
        st.dataframe(workers_df[['name', 'phone', 'job_title', 'daily_wage']], use_container_width=True, hide_index=True)

elif menu == "Settings":
    st.markdown("<div class='page-header'><h1 class='page-title'>Parametres</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Entreprise", "Base de Donnees"])
    
    with tab1:
        st.markdown("<div class='content-card'><div class='card-title'>Informations Entreprise</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nom", value=COMPANY['name'])
            st.text_input("ICE", value=COMPANY['ice'])
        with col2:
            st.text_input("Adresse", value=COMPANY['address'])
            st.text_input("Telephone", value=COMPANY['phone'])
        if st.button("Sauvegarder"):
            st.success("Informations mises a jour")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='content-card'><div class='card-title'>Gestion Base de Donnees</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Exporter CSV"):
                df = db.get_transactions()
                if not df.empty:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Telecharger", csv, f"transactions_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        with col2:
            if st.button("Creer Backup"):
                with open(DB_NAME, "rb") as f:
                    st.download_button("Telecharger", f, f"backup_{datetime.now().strftime('%Y%m%d')}.db", mime="application/octet-stream")
        
        st.write("")
        df = db.get_transactions()
        plants = db.get_plantations()
        workers = db.get_workers()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Transactions", len(df))
        with col2:
            st.metric("Plantations", len(plants))
        with col3:
            st.metric("Ouvriers", len(workers))
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><hr style='border: none; border-top: 1px solid #e2e8f0; margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 1rem 0; color: #94a3b8; font-size: 0.85rem;'>
        SMAHI GROUP ERP v3.0 - Complete Farm Management System<br>
        © 2024 Smahi Group. Tous droits reserves.
    </div>
""", unsafe_allow_html=True)