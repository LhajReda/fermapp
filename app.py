"""
SMAHI GROUP - ULTIMATE AGRICULTURAL ERP (CLOUD VERSION)
Powered by Streamlit & Supabase
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF
import hashlib
from supabase import create_client

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SMAHI GROUP ERP", layout="wide", page_icon="🌾")

# معلومات الاتصال بـ Supabase (هادشي اللي كيخليك Professional)
SUPABASE_URL = "https://wpnfvewscggrkguaofno.supabase.co"
SUPABASE_KEY = "sb_publishable_cETUxgJW9dxXzNpt8lZJJA_g-AsmvxP"

# دير Cache للاتصال باش السيت يكون خفيف
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# معلومات الشركة
COMPANY = {
    "name": "SMAHI GROUP",
    "ice": "002165492000071",
    "address": "Sidi Bennour, Maroc",
    "phone": "+212 6XX XXXXXX",
    "email": "contact@smahigroup.ma"
}

# --- 2. CSS STYLING (Productly Design) ---
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

# Helper Functions
def format_currency(amount): return f"{amount:,.2f} DH"

# --- 3. DATABASE MANAGER (CLOUD) ---
class DB:
    @staticmethod
    def get_transactions():
        # كنجيبو الداتا من Supabase
        response = supabase.table('transactions').select("*").order('id', desc=True).execute()
        return pd.DataFrame(response.data)
    
    @staticmethod
    def add_transaction(data):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # كنوجدو الداتا باش نصيفطوها للسحاب
        payload = {
            "date": dt, "type": data['type'], "category": data['category'], 
            "partner_name": data['partner'], "product": data['product'], 
            "quantity": data['quantity'], "unit": data['unit'], 
            "fuel_liters": data['fuel_liters'], "fuel_station": data['fuel_station'], 
            "price_unit": data['price'], "total_price": data['total'], 
            "amount_paid": data['paid'], "amount_remaining": data['remaining'], 
            "notes": data['notes']
        }
        supabase.table('transactions').insert(payload).execute()
    
    @staticmethod
    def get_plantations():
        response = supabase.table('plantations').select("*").order('id', desc=True).execute()
        return pd.DataFrame(response.data)
    
    @staticmethod
    def add_plantation(crop, hectares, plot, expected_harvest=None, notes=None):
        dt = datetime.now().strftime("%Y-%m-%d")
        payload = {"date_planted": dt, "crop_name": crop, "hectares": hectares, "plot_name": plot, "status": "En cours"}
        supabase.table('plantations').insert(payload).execute()
    
    @staticmethod
    def get_expenses():
        response = supabase.table('expenses').select("*").order('id', desc=True).execute()
        return pd.DataFrame(response.data)
    
    @staticmethod
    def add_expense(category, description, amount, payment_method=None, notes=None):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {"date": dt, "category": category, "description": description, "amount": amount, "payment_method": payment_method}
        supabase.table('expenses').insert(payload).execute()
    
    @staticmethod
    def get_workers():
        response = supabase.table('workers').select("*").eq('status', 'active').execute()
        return pd.DataFrame(response.data)
    
    @staticmethod
    def add_worker(name, phone=None, job_title=None, daily_wage=None, notes=None):
        payload = {"name": name, "phone": phone, "job_title": job_title, "daily_wage": daily_wage, "notes": notes}
        supabase.table('workers').insert(payload).execute()

    # Dashboard Statistics (محسوبة من Cloud Data)
    @staticmethod
    def get_dashboard_stats(period_days=30):
        # كنجيبو كاع المعاملات ونحسبو ف Python (أسهل طريقة)
        trans_df = DB.get_transactions()
        exp_df = DB.get_expenses()
        
        # تحويل التواريخ
        if not trans_df.empty: trans_df['date'] = pd.to_datetime(trans_df['date'])
        if not exp_df.empty: exp_df['date'] = pd.to_datetime(exp_df['date'])
        
        cutoff = pd.Timestamp.now() - pd.Timedelta(days=period_days)
        
        # الحسابات
        stats = {'total_sales': 0, 'total_purchases': 0, 'total_expenses': 0, 'total_fuel': 0}
        
        if not trans_df.empty:
            recent_trans = trans_df[trans_df['date'] >= cutoff]
            stats['total_sales'] = recent_trans[recent_trans['type']=='Vente']['total_price'].sum()
            stats['total_purchases'] = recent_trans[recent_trans['type']=='Achat']['total_price'].sum()
            stats['total_fuel'] = recent_trans[recent_trans['category'].str.contains('Mazot', na=False)]['fuel_liters'].sum()
            
        if not exp_df.empty:
            stats['total_expenses'] = exp_df[exp_df['date'] >= cutoff]['amount'].sum()
            
        return stats

db = DB()

# --- 4. PDF GENERATOR ---
class PDFGen:
    @staticmethod
    def create_document(data, doc_type="Bon de Livraison"):
        class PDF(FPDF):
            def header(self):
                color = (59, 130, 246) if doc_type == "Bon de Livraison" else (16, 185, 129)
                self.set_fill_color(*color)
                self.rect(0, 0, 210, 40, 'F')
                self.set_text_color(255, 255, 255); self.set_font('Arial', 'B', 20)
                self.cell(0, 20, '', 0, 1); self.cell(0, 10, COMPANY['name'], 0, 1, 'C')
                self.set_text_color(0, 0, 0); self.ln(10)
            def footer(self):
                self.set_y(-20); self.set_font('Arial', 'I', 8); self.set_text_color(128, 128, 128)
                self.cell(0, 5, f"{COMPANY['address']} | ICE: {COMPANY['ice']}", 0, 1, 'C')
                self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'C')
        
        pdf = PDF(); pdf.add_page(); pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 12, doc_type.upper(), 0, 1, 'C'); pdf.ln(8)
        
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(95, 8, f"Document N: {data.get('id', '---')}", 0, 0)
        pdf.cell(0, 8, f"Date: {str(data.get('date', ''))[:10]}", 0, 1, 'R')
        pdf.ln(5)
        
        pdf.cell(0, 10, 'CLIENT', 0, 1); pdf.set_font('Arial', '', 10)
        pdf.cell(0, 7, f"Nom: {data.get('partner_name', '')}", 0, 1); pdf.ln(5)
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(70, 10, 'Produit', 1, 0, 'C'); pdf.cell(30, 10, 'Quantite', 1, 0, 'C')
        pdf.cell(30, 10, 'Prix Unit.', 1, 0, 'C'); pdf.cell(40, 10, 'Total', 1, 1, 'C')
        
        pdf.set_font('Arial', '', 10)
        prod = str(data.get('product', ''))
        qte = f"{data.get('fuel_liters',0):,.2f} L" if "Mazot" in str(data.get('category','')) else f"{data.get('quantity',0):,.2f} {data.get('unit','')}"
        
        pdf.cell(70, 10, prod, 1, 0, 'L'); pdf.cell(30, 10, qte, 1, 0, 'C')
        pdf.cell(30, 10, f"{data.get('price_unit',0):,.2f}", 1, 0, 'R')
        pdf.cell(40, 10, f"{data.get('total_price',0):,.2f}", 1, 1, 'R')
        
        pdf.ln(5); pdf.set_font('Arial', 'B', 12)
        pdf.cell(130, 12, 'TOTAL', 1, 0, 'R')
        pdf.cell(40, 12, f"{data.get('total_price',0):,.2f} DH", 1, 1, 'R')
        
        return pdf.output(dest='S').encode('latin1', 'replace')

pdf_gen = PDFGen()

# --- 5. AUTHENTICATION ---
# (هنا يمكن نزيدو التحقق عبر Supabase Users مستقبلاً)
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

def login_page():
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div style='background:white;padding:3rem;border-radius:20px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,0.1);margin-top:80px;'><h1>🌾 SMAHI ERP</h1><p>Cloud Edition</p></div>", unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if pwd == "admin123": # مؤقتا، من بعد نربطوها بـ Users
                st.session_state['logged_in'] = True; st.rerun()
            else: st.error("Error")

if not st.session_state['logged_in']:
    login_page(); st.stop()

# --- 6. MAIN APP (Sidebar & Pages) ---
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:2rem 0;'><h2 style='color:white;'>SMAHI GROUP</h2><p style='color:#94a3b8;'>Cloud System ☁️</p></div>", unsafe_allow_html=True)
    menu = st.radio("Menu", ["Dashboard", "Transactions", "Historique", "Plantations", "Expenses", "Workers"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Logout"): st.session_state['logged_in'] = False; st.rerun()

if menu == "Dashboard":
    st.markdown("<div class='page-header'><h1 class='page-title'>Tableau de Bord</h1></div>", unsafe_allow_html=True)
    stats = db.get_dashboard_stats(30)
    net = stats['total_sales'] - stats['total_purchases'] - stats['total_expenses']
    
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card border-green'><div class='kpi-label'>Ventes</div><div class='kpi-value'>{format_currency(stats['total_sales'])}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card border-red'><div class='kpi-label'>Achats</div><div class='kpi-value'>{format_currency(stats['total_purchases'])}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card border-blue'><div class='kpi-label'>Net Profit</div><div class='kpi-value'>{format_currency(net)}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card border-orange'><div class='kpi-label'>Mazot</div><div class='kpi-value'>{stats['total_fuel']:,.0f} L</div></div>", unsafe_allow_html=True)
    
    df = db.get_transactions()
    if not df.empty:
        df['Date'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m-%d")
        daily = df.groupby(['Date','type'])['total_price'].sum().reset_index().sort_values('Date')
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        fig = go.Figure()
        for t, c in [('Vente','#10b981'), ('Achat','#ef4444')]:
            d = daily[daily['type']==t]
            fig.add_trace(go.Scatter(x=d['Date'], y=d['total_price'], mode='lines+markers', name=t, line=dict(color=c, width=3)))
        fig.update_layout(height=400, plot_bgcolor='white', margin=dict(t=20,l=0,r=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Transactions":
    st.markdown("<div class='page-header'><h1 class='page-title'>Nouvelle Transaction</h1></div>", unsafe_allow_html=True)
    with st.form("new"):
        c1,c2,c3 = st.columns(3)
        typ = c1.selectbox("Type", ["Vente", "Achat"])
        cat = c1.selectbox("Cat", ["Cereales", "Mazot", "Engrais", "Autre"])
        part = c2.text_input("Client/Fournisseur")
        prod = c2.text_input("Produit")
        price = c3.number_input("Prix Unit", 0.0)
        
        if "Mazot" in cat: l=st.number_input("Litres",0.0); stn=st.text_input("Station"); q=0; u="L"
        else: q=st.number_input("Qte",0.0); u=st.selectbox("Unit", ["kg", "T", "Qx"]); l=0; stn=""
        
        note = st.text_area("Notes")
        if st.form_submit_button("Valider"):
            tot = (l*price) if l>0 else (q*price)
            data = {'type':typ, 'category':cat, 'partner':part, 'product':prod, 'quantity':q, 'unit':u, 'fuel_liters':l, 'fuel_station':stn, 'price':price, 'total':tot, 'paid':tot, 'remaining':0, 'notes':note}
            db.add_transaction(data)
            st.success("Enregistré sur Cloud! ☁️"); st.rerun()

elif menu == "Historique":
    st.markdown("<div class='page-header'><h1 class='page-title'>Historique</h1></div>", unsafe_allow_html=True)
    df = db.get_transactions()
    if not df.empty:
        st.dataframe(df[['id','date','type','partner_name','total_price']], use_container_width=True)
        tid = st.number_input("ID Transaction", 1)
        if st.button("Générer PDF"):
            row = df[df['id']==tid]
            if not row.empty:
                pdf = pdf_gen.create_document(row.iloc[0].to_dict())
                st.download_button("Télécharger PDF", pdf, f"Bon_{tid}.pdf", "application/pdf")

elif menu == "Plantations":
    st.markdown("<div class='page-header'><h1 class='page-title'>Plantations</h1></div>", unsafe_allow_html=True)
    with st.form("plant"):
        c1,c2 = st.columns(2)
        cr = c1.text_input("Culture"); ha = c2.number_input("Hectares", 0.0); pl = st.text_input("Parcelle")
        if st.form_submit_button("Ajouter"): db.add_plantation(cr, ha, pl); st.success("OK"); st.rerun()
    st.dataframe(db.get_plantations(), use_container_width=True)

elif menu == "Expenses":
    st.markdown("<div class='page-header'><h1 class='page-title'>Dépenses</h1></div>", unsafe_allow_html=True)
    with st.form("exp"):
        c1,c2 = st.columns(2)
        cat = c1.selectbox("Cat", ["Eau", "Electricité", "Maintenance", "Autre"]); am = c1.number_input("Montant", 0.0)
        desc = c2.text_input("Description"); pay = c2.selectbox("Méthode", ["Espèces", "Chèque"])
        if st.form_submit_button("Ajouter"): db.add_expense(cat, desc, am, pay); st.success("OK"); st.rerun()
    st.dataframe(db.get_expenses(), use_container_width=True)

elif menu == "Workers":
    st.markdown("<div class='page-header'><h1 class='page-title'>Ouvriers</h1></div>", unsafe_allow_html=True)
    with st.form("wrk"):
        c1,c2 = st.columns(2)
        nm = c1.text_input("Nom"); ph = c1.text_input("Tel"); jb = c2.text_input("Poste"); wg = c2.number_input("Salaire/J", 0.0)
        if st.form_submit_button("Ajouter"): db.add_worker(nm, ph, jb, wg); st.success("OK"); st.rerun()
    st.dataframe(db.get_workers(), use_container_width=True)
