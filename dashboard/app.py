import os                                         # to find the database
import sqlite3                                    # to open it
import pandas as pd                               # to hold query rows
import plotly.express as px                       # to draw the charts
import streamlit as st                            # to build the page

st.set_page_config(
    page_title='Airtel Revenue Intelligence',    # label name on browser tab
    page_icon='📶',                               # tab icon label
    layout='wide'                                 # full browser width
)

CSS = '''
<style>
    /* Force clean Light Theme across main page & sidebar */
    [data-testid="stAppViewContainer"] {
        background-color: #F4F5F7;
        color: #111827;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    [data-testid="stSidebar"] * {
        color: #111827 !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stHeader"] {
        background: transparent;
        height: 0rem;
    }

    /* Typography */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #111827;
    }

    /* ---- White KPI Cards ---- */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-left: 5px solid #E40000;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.08);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.78rem;
        color: #6B7280 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
        color: #111827 !important;
    }

    /* ---- White Chart & Table Containers ---- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }

    /* ---- Tabs Styling ---- */
    button[data-baseweb="tab"] {
        color: #4B5563 !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #E40000 !important;
        border-bottom-color: #E40000 !important;
    }

    /* ---- Tower Signal Sequential Wave Animation ---- */
    @keyframes signalPulse1 {
        0%, 100% { opacity: 0.15; }
        20%, 65% { opacity: 1; }
    }
    @keyframes signalPulse2 {
        0%, 20%, 100% { opacity: 0.12; }
        42%, 75% { opacity: 0.85; }
    }
    @keyframes signalPulse3 {
        0%, 42%, 100% { opacity: 0.08; }
        65%, 88% { opacity: 0.65; }
    }
    @keyframes dotGlow {
        0%, 100% { transform: scale(1); opacity: 0.85; }
        25% { transform: scale(1.25); opacity: 1; }
    }
    .wave-1 { animation: signalPulse1 1.8s infinite ease-in-out; }
    .wave-2 { animation: signalPulse2 1.8s infinite ease-in-out; }
    .wave-3 { animation: signalPulse3 1.8s infinite ease-in-out; }
    .tower-dot { transform-origin: 90px 26px; animation: dotGlow 1.8s infinite ease-in-out; }
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

HERE = os.path.dirname(os.path.abspath(__file__)) # the dashboard folder
DB = os.path.join(HERE, '..', 'data', 'raw',      # up one level,
                  'airtel.db')                    # into data/raw


@st.cache_data                                    # run each query once
def q(sql, params=()):                            # every query, here
    con = sqlite3.connect(DB)                     # open the database
    try:                                          # run the query...
        return pd.read_sql_query(sql, con,        # ...and hand back
                                 params=params)   # its rows
    finally:                                      # ...then always
        con.close()


# ---------- header labels ----------
st.markdown("<span style='color:#E40000; font-weight:700; font-size:0.85rem; letter-spacing:0.06em;'>REVENUE ANALYTICS DASHBOARD</span>", unsafe_allow_html=True)
st.title("Airtel Revenue Analysis")
st.caption("For the revenue analyst, understanding what money the base "
           "really brings in, and which plans and circles carry it.")

# ------------------------------------------------------------
# DOMAIN B : REVENUE   (filters: Connection Type and Region)
# ------------------------------------------------------------

RED = '#E40000'                                   # Airtel red
GREY = '#9CA3AF'                                  # clean neutral grey for stated bars


def tidy(fig, h=250):
    # clean white-card styling for every plotly chart with crisp dark axis titles
    fig.update_layout(
        template='plotly_white',
        height=h,
        margin=dict(l=10, r=10, t=28, b=10),
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#111827', size=12),
        legend_title_text='',
        legend=dict(orientation='h', y=1.18, font=dict(color='#111827'))
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor='#D1D5DB',
        tickfont=dict(color='#374151', size=11),
        title_font=dict(color='#111827', size=12)
    )
    fig.update_yaxes(
        gridcolor='#F3F4F6',
        linecolor='#D1D5DB',
        tickfont=dict(color='#374151', size=11),
        title_font=dict(color='#111827', size=12)
    )
    return fig


def show_table(df):
    # show a small table: no index, full width, height fits the rows
    st.dataframe(df, hide_index=True, use_container_width=True,
                 height=38 * (len(df) + 1))


# ---------- sidebar logo + filters + Animated Telecom Tower ----------
LOGO_PATH = r"C:\Users\muhsi\Downloads\Airtel-logo-on-white-background.avif"
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)

st.sidebar.header("Filter Labels")

all_types = ['Prepaid', 'Postpaid']
all_regions = q("SELECT DISTINCT region FROM customer_features ORDER BY region")['region'].tolist()

types = st.sidebar.multiselect("Connection Type", all_types, default=all_types)
regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)

st.sidebar.markdown(
    '''
    <div style="margin-top: 34px; text-align: center;">
        <svg width="175" height="265" viewBox="0 0 180 265" xmlns="http://www.w3.org/2000/svg">
            <!-- Animated Signal Waves (Bottom -> Middle -> Top) -->
            <path class="wave-1" d="M72 30 Q90 16 108 30" stroke="#E40000" stroke-width="2.8" fill="none" stroke-linecap="round"/>
            <path class="wave-2" d="M61 21 Q90 1 119 21" stroke="#E40000" stroke-width="2.3" fill="none" stroke-linecap="round"/>
            <path class="wave-3" d="M50 12 Q90 -14 130 12" stroke="#E40000" stroke-width="1.8" fill="none" stroke-linecap="round"/>
            <!-- Top Antenna Spire -->
            <line x1="90" y1="26" x2="90" y2="58" stroke="#8C4A4A" stroke-width="3" stroke-linecap="round"/>
            <circle class="tower-dot" cx="90" cy="26" r="3.8" fill="#E40000"/>
            <!-- Main Tower Lattice Legs -->
            <line x1="82" y1="58" x2="54" y2="255" stroke="#8C4A4A" stroke-width="3"/>
            <line x1="98" y1="58" x2="126" y2="255" stroke="#8C4A4A" stroke-width="3"/>
            <!-- Horizontal Platforms -->
            <line x1="65" y1="73" x2="115" y2="73" stroke="#8C4A4A" stroke-width="2.5"/>
            <line x1="60" y1="118" x2="120" y2="118" stroke="#8C4A4A" stroke-width="2.5"/>
            <line x1="68" y1="163" x2="112" y2="163" stroke="#8C4A4A" stroke-width="2"/>
            <line x1="61" y1="208" x2="119" y2="208" stroke="#8C4A4A" stroke-width="2"/>
            <line x1="42" y1="255" x2="138" y2="255" stroke="#8C4A4A" stroke-width="3.5" stroke-linecap="round"/>
            <!-- Cross Bracing -->
            <line x1="82" y1="58" x2="103" y2="118" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="98" y1="58" x2="77" y2="118" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="77" y1="118" x2="112" y2="163" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="103" y1="118" x2="68" y2="163" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="68" y1="163" x2="119" y2="208" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="112" y1="163" x2="61" y2="208" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="61" y1="208" x2="126" y2="255" stroke="#A66B6B" stroke-width="1.5"/>
            <line x1="119" y1="208" x2="54" y2="255" stroke="#A66B6B" stroke-width="1.5"/>
            <!-- 5G / Cellular Panel Antennas -->
            <rect x="63" y="57" width="6" height="22" rx="2" fill="#B57B7B" stroke="#7A3E3E" stroke-width="1"/>
            <rect x="87" y="57" width="6" height="22" rx="2" fill="#B57B7B" stroke="#7A3E3E" stroke-width="1"/>
            <rect x="111" y="57" width="6" height="22" rx="2" fill="#B57B7B" stroke="#7A3E3E" stroke-width="1"/>
            <!-- Microwave Dish Antennas -->
            <ellipse cx="58" cy="129" rx="6" ry="12" fill="#C48F8F" stroke="#7A3E3E" stroke-width="1.5"/>
            <ellipse cx="122" cy="148" rx="7" ry="14" fill="#C48F8F" stroke="#7A3E3E" stroke-width="1.5"/>
        </svg>
    </div>
    ''',
    unsafe_allow_html=True
)

# stop early if a filter is empty
if len(types) == 0 or len(regions) == 0:
    st.warning("Please select at least one Connection Type and one Region.")
    st.stop()

# build the WHERE part of every query from the two filters
type_marks = ','.join(['?'] * len(types))
region_marks = ','.join(['?'] * len(regions))
WHERE = ("WHERE connection_type IN (" + type_marks + ") "
         "AND region IN (" + region_marks + ")")
P = tuple(types) + tuple(regions)

# the same filters, written for queries that join recharges (r) to customers (c)
JOIN_WHERE = ("WHERE r.recharge_date BETWEEN '2025-01-01' AND '2025-06-30' "
              "AND c.connection_type IN (" + type_marks + ") "
              "AND c.region IN (" + region_marks + ")")

# ---------- the two pages ----------
tab1, tab2 = st.tabs(["Overview — Whole Base", "Plan — One Plan at a Time"])


# ============================================================
# PAGE 1 : OVERVIEW
# ============================================================
with tab1:
    st.subheader("Base Revenue Overview")

    # ---------- B2 + B3 + B9 : headline numbers ----------
    kpi = q("SELECT COUNT(*) AS subs, "
            "AVG(stated_arpu) AS stated, "
            "AVG(actual_arpu_6m) AS actual, "
            "SUM(stated_arpu) AS stated_total, "
            "SUM(actual_arpu_6m) AS actual_total, "
            "SUM(recharge_count = 0) AS paid_nothing "
            "FROM customer_features " + WHERE, P)

    subs = int(kpi['subs'][0] or 0)
    stated = kpi['stated'][0] or 0.0
    actual = kpi['actual'][0] or 0.0
    stated_total = kpi['stated_total'][0] or 0.0
    actual_total = kpi['actual_total'][0] or 0.0
    paid_nothing = int(kpi['paid_nothing'][0] or 0)

    # how much the plan-price figure overstates the money received
    overstate = (100 * (stated_total - actual_total) / actual_total) if actual_total else 0.0

    # ---------- B7 : money received Jan - Jun 2025 ----------
    money = q("SELECT SUM(r.amount_inr) AS total_inr "
              "FROM recharges r "
              "JOIN customer_features c ON c.customer_id = r.customer_id "
              + JOIN_WHERE, P)
    crore = (money['total_inr'][0] or 0) / 10000000

    # all six numbers sit in one row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Subscribers", f"{subs:,}")
    c2.metric("Actual ARPU (INR)", f"{actual:,.2f}")
    c3.metric("Stated ARPU (INR)", f"{stated:,.2f}")
    c4.metric("Stated overstates by", f"{overstate:.2f}%")
    c5.metric("Paid nothing (6 months)", f"{paid_nothing:,}")
    c6.metric("Received Jan-Jun (crore)", f"{crore:.2f}")

    st.write("")  # clean spacing

    # ---------- row of three charts inside white cards ----------
    g1, g2, g3 = st.columns(3)

    # B4 : stated vs actual ARPU by connection type
    with g1:
        with st.container(border=True):
            st.markdown("**Stated vs actual ARPU (INR)**")
            by_type = q("SELECT connection_type, "
                        "AVG(stated_arpu) AS Stated, "
                        "AVG(actual_arpu_6m) AS Actual "
                        "FROM customer_features " + WHERE +
                        " GROUP BY connection_type", P)
            by_type_long = by_type.melt(id_vars='connection_type',
                                        var_name='Measure', value_name='ARPU')
            fig1 = px.bar(by_type_long, x='connection_type', y='ARPU',
                          color='Measure', barmode='group', text_auto='.0f',
                          color_discrete_map={'Actual': RED, 'Stated': GREY},
                          labels={'connection_type': 'Connection Type',
                                  'ARPU': 'ARPU (INR)'})
            st.plotly_chart(tidy(fig1), use_container_width=True, theme=None, config={'displayModeBar': False})

    # B5 : top five plans by actual monthly revenue
    with g2:
        with st.container(border=True):
            st.markdown("**Top 5 plans by monthly revenue (INR)**")
            plans = q("SELECT plan_name, "
                      "SUM(actual_arpu_6m) AS revenue "
                      "FROM customer_features " + WHERE +
                      " GROUP BY plan_name ORDER BY revenue DESC LIMIT 5", P)
            fig2 = px.bar(plans, x='revenue', y='plan_name', orientation='h',
                          text_auto='.2s',
                          color_discrete_sequence=[RED],
                          labels={'revenue': 'Monthly Revenue (INR)',
                                  'plan_name': 'Plan'})
            fig2.update_yaxes(autorange='reversed')
            st.plotly_chart(tidy(fig2), use_container_width=True, theme=None, config={'displayModeBar': False})

    # B6 : top five circles by actual monthly revenue (Pie Chart)
    with g3:
        with st.container(border=True):
            st.markdown("**Top 5 circles by monthly revenue (INR)**")
            circles = q("SELECT circle_name, "
                        "SUM(actual_arpu_6m) AS revenue "
                        "FROM customer_features " + WHERE +
                        " GROUP BY circle_name ORDER BY revenue DESC LIMIT 5", P)
            fig3 = px.pie(circles, values='revenue', names='circle_name',
                          hole=0.45,
                          color_discrete_sequence=['#E40000', '#B91C1C', '#EF4444', '#F87171', '#9CA3AF'])
            fig3.update_traces(textposition='inside', textinfo='percent+label',
                               textfont=dict(color='white', size=11))
            fig3 = tidy(fig3)
            fig3.update_layout(showlegend=False)
            st.plotly_chart(fig3, use_container_width=True, theme=None, config={'displayModeBar': False})

    # ---------- row of two charts and the first table inside white cards ----------
    h1, h2, h3 = st.columns(3)

    # B8 : Top 10 recharge amounts by count
    with h1:
        with st.container(border=True):
            st.markdown("**Top 10 recharges by count**")
            top_rech = q("SELECT '₹' || CAST(ROUND(r.amount_inr, 0) AS INTEGER) AS pack, "
                         "COUNT(*) AS count "
                         "FROM recharges r "
                         "JOIN customer_features c ON c.customer_id = r.customer_id "
                         + JOIN_WHERE +
                         " GROUP BY r.amount_inr ORDER BY count DESC LIMIT 10", P)
            fig4 = px.bar(top_rech, x='count', y='pack', orientation='h',
                          text_auto=',',
                          color_discrete_sequence=[RED],
                          labels={'count': 'Number of Recharges',
                                  'pack': 'Recharge Pack'})
            fig4.update_yaxes(autorange='reversed')
            st.plotly_chart(tidy(fig4, h=280), use_container_width=True, theme=None, config={'displayModeBar': False})

    # B7 detail : money received each month
    with h2:
        with st.container(border=True):
            st.markdown("**Money received each month (INR)**")
            monthly = q("SELECT strftime('%Y-%m', r.recharge_date) AS month, "
                        "SUM(r.amount_inr) AS total_inr "
                        "FROM recharges r "
                        "JOIN customer_features c ON c.customer_id = r.customer_id "
                        + JOIN_WHERE +
                        " GROUP BY month ORDER BY month", P)
            fig5 = px.line(monthly, x='month', y='total_inr', markers=True,
                           text='total_inr',
                           color_discrete_sequence=[RED],
                           labels={'month': 'Month',
                                   'total_inr': 'Amount Received (INR)'})
            fig5.update_traces(texttemplate='%{text:.2s}', textposition='top center')
            st.plotly_chart(tidy(fig5), use_container_width=True, theme=None, config={'displayModeBar': False})

    # TABLE 1 : revenue by region
    with h3:
        with st.container(border=True):
            st.markdown("**Table 1 - Revenue by region**")
            t1 = q("SELECT region AS Region, "
                   "COUNT(*) AS Subscribers, "
                   "ROUND(AVG(actual_arpu_6m), 2) AS 'Actual ARPU', "
                   "ROUND(SUM(actual_arpu_6m), 0) AS 'Monthly revenue' "
                   "FROM customer_features " + WHERE +
                   " GROUP BY region", P)
            t1['Share %'] = (100 * t1['Monthly revenue'] / actual_total).round(1) if actual_total else 0.0
            show_table(t1.sort_values('Monthly revenue', ascending=False))

    # TABLE 2 : zero-payers by connection type inside white card
    with st.container(border=True):
        st.markdown("**Table 2 - Who paid nothing in six months, by connection type**")
        t2 = q("SELECT connection_type AS 'Connection Type', "
               "COUNT(*) AS Subscribers, "
               "SUM(recharge_count = 0) AS 'Paid nothing', "
               "ROUND(100.0 * AVG(recharge_count = 0), 1) AS '% paid nothing', "
               "ROUND(AVG(recharge_count), 2) AS 'Avg payments' "
               "FROM customer_features " + WHERE +
               " GROUP BY connection_type", P)
        show_table(t2)


# ============================================================
# PAGE 2 : ONE PLAN AT A TIME
# ============================================================
with tab2:
    st.subheader("Single Plan Deep Dive")

    # list the plans that exist in the filtered base, best earner first
    plan_list = q("SELECT plan_name, SUM(actual_arpu_6m) AS revenue "
                  "FROM customer_features " + WHERE +
                  " GROUP BY plan_name ORDER BY revenue DESC", P)

    plan = st.selectbox("Select Plan Label (biggest revenue first)",
                        plan_list['plan_name'].tolist())

    # same filters, plus the chosen plan
    PLAN_WHERE = WHERE + " AND plan_name = ?"
    PP = P + (plan,)

    info = q("SELECT MAX(plan_type) AS plan_type, "
             "MAX(price_inr) AS price, "
             "COUNT(*) AS subs, "
             "AVG(actual_arpu_6m) AS actual, "
             "SUM(actual_arpu_6m) AS revenue, "
             "SUM(recharge_count = 0) AS paid_nothing "
             "FROM customer_features " + PLAN_WHERE, PP)

    p_revenue = info['revenue'][0] or 0.0
    p_nothing = int(info['paid_nothing'][0] or 0)

    # share of all revenue in the current filters that this plan brings
    p_share = (100 * p_revenue / actual_total) if actual_total else 0.0

    # six numbers in one row
    a1, a2, a3, a4, a5, a6 = st.columns(6)
    a1.metric("Plan type", info['plan_type'][0])
    a2.metric("Plan price (INR)", f"{info['price'][0]:,.0f}")
    a3.metric("Subscribers", f"{int(info['subs'][0]):,}")
    a4.metric("Actual ARPU (INR)", f"{info['actual'][0]:,.2f}")
    a5.metric("Monthly revenue (INR)", f"{p_revenue:,.0f}")
    a6.metric("Share of revenue", f"{p_share:.1f}%")

    st.caption(f"{p_nothing:,} subscribers on this plan paid nothing in six months.")

    # ---------- row of three charts inside white cards ----------
    x1, x2, x3 = st.columns(3)

    # actual ARPU by tenure for this plan
    with x1:
        with st.container(border=True):
            st.markdown("**Actual ARPU by tenure (years)**")
            p_tenure = q("SELECT tenure_years, "
                         "AVG(actual_arpu_6m) AS arpu "
                         "FROM customer_features " + PLAN_WHERE +
                         " GROUP BY tenure_years ORDER BY tenure_years", PP)
            fig6 = px.bar(p_tenure, x='tenure_years', y='arpu', text_auto='.0f',
                          color_discrete_sequence=[RED],
                          labels={'tenure_years': 'Tenure (Years)',
                                  'arpu': 'Actual ARPU (INR)'})
            st.plotly_chart(tidy(fig6), use_container_width=True, theme=None, config={'displayModeBar': False})

    # top five circles for this plan
    with x2:
        with st.container(border=True):
            st.markdown("**Top 5 circles for this plan (INR)**")
            p_circles = q("SELECT circle_name, "
                          "SUM(actual_arpu_6m) AS revenue "
                          "FROM customer_features " + PLAN_WHERE +
                          " GROUP BY circle_name ORDER BY revenue DESC LIMIT 5", PP)
            fig7 = px.bar(p_circles, x='revenue', y='circle_name', orientation='h',
                          text_auto='.2s',
                          color_discrete_sequence=[RED],
                          labels={'revenue': 'Monthly Revenue (INR)',
                                  'circle_name': 'Circle'})
            fig7.update_yaxes(autorange='reversed')
            st.plotly_chart(tidy(fig7), use_container_width=True, theme=None, config={'displayModeBar': False})

    # money received each month for this plan
    with x3:
        with st.container(border=True):
            st.markdown("**Money received each month (INR)**")
            p_monthly = q("SELECT strftime('%Y-%m', r.recharge_date) AS month, "
                          "SUM(r.amount_inr) AS total_inr "
                          "FROM recharges r "
                          "JOIN customer_features c ON c.customer_id = r.customer_id "
                          + JOIN_WHERE + " AND c.plan_name = ? "
                          "GROUP BY month ORDER BY month", PP)
            fig8 = px.line(p_monthly, x='month', y='total_inr', markers=True,
                           text='total_inr',
                           color_discrete_sequence=[RED],
                           labels={'month': 'Month',
                                   'total_inr': 'Amount Received (INR)'})
            fig8.update_traces(texttemplate='%{text:.2s}', textposition='top center')
            st.plotly_chart(tidy(fig8), use_container_width=True, theme=None, config={'displayModeBar': False})

    # ---------- two tables side by side inside white cards ----------
    y1, y2 = st.columns(2)

    # TABLE 1 : this plan by region
    with y1:
        with st.container(border=True):
            st.markdown("**Table 1 - This plan by region**")
            pt1 = q("SELECT region AS Region, "
                    "COUNT(*) AS Subscribers, "
                    "ROUND(AVG(actual_arpu_6m), 2) AS 'Actual ARPU', "
                    "ROUND(SUM(actual_arpu_6m), 0) AS 'Monthly revenue' "
                    "FROM customer_features " + PLAN_WHERE +
                    " GROUP BY region", PP)
            show_table(pt1.sort_values('Monthly revenue', ascending=False))

    # TABLE 2 : this plan against all plans
    with y2:
        with st.container(border=True):
            st.markdown("**Table 2 - This plan vs all plans**")
            cols = ("AVG(stated_arpu) AS stated, "
                    "AVG(actual_arpu_6m) AS actual, "
                    "100.0 * AVG(recharge_count = 0) AS zero_pct, "
                    "100.0 * AVG(is_churned) AS churn ")
            this_row = q("SELECT " + cols + "FROM customer_features " + PLAN_WHERE, PP)
            all_row = q("SELECT " + cols + "FROM customer_features " + WHERE, P)

            compare = pd.DataFrame({
                'Measure': ['Stated ARPU (INR)', 'Actual ARPU (INR)',
                            'Gap (INR)', 'Paid nothing (%)', 'Churn (%)'],
                'This plan': [this_row['stated'][0], this_row['actual'][0],
                              this_row['stated'][0] - this_row['actual'][0],
                              this_row['zero_pct'][0], this_row['churn'][0]],
                'All plans': [all_row['stated'][0], all_row['actual'][0],
                              all_row['stated'][0] - all_row['actual'][0],
                              all_row['zero_pct'][0], all_row['churn'][0]],
            }).round(2)
            show_table(compare)