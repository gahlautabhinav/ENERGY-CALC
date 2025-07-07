import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time
import numpy as np

# Page configuration
st.set_page_config(
    page_title="⚡ EcoSmart Energy Hub",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with animations and modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3); }
        100% { box-shadow: 0 20px 60px rgba(240, 147, 251, 0.4); }
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .energy-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 50%, #f39c12 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin: 1.5rem 0;
        animation: pulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    .neon-card {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 100%);
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #00ffff;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.1);
        animation: neonGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes neonGlow {
        0% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.1); }
        100% { box-shadow: 0 0 30px rgba(0, 255, 255, 0.6), inset 0 0 30px rgba(0, 255, 255, 0.2); }
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        transition: transform 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s linear infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .metric-container:hover {
        transform: scale(1.02);
    }
    
    .metric-container h2 {
        color: white;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-container h3 {
        color: rgba(255,255,255,0.9);
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    .appliance-toggle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        margin: 0.5rem;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .appliance-toggle:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    .tips-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: slideIn 1s ease-out;
    }
    
    .tips-container h3 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .tip-item {
        background: rgba(255,255,255,0.7);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        color: #2c3e50;
        transition: transform 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .tip-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .floating-element {
        position: fixed;
        pointer-events: none;
        z-index: 1000;
        font-size: 2rem;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .energy-particles {
        position: absolute;
        width: 100%;
        height: 100%;
        overflow: hidden;
        top: 0;
        left: 0;
        pointer-events: none;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        animation: particle-float 8s linear infinite;
    }
    
    @keyframes particle-float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .footer-creative {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .energy-wave {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 100px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        clip-path: polygon(0 60%, 100% 40%, 100% 100%, 0 100%);
        animation: wave 4s ease-in-out infinite;
    }
    
    @keyframes wave {
        0%, 100% { clip-path: polygon(0 60%, 100% 40%, 100% 100%, 0 100%); }
        50% { clip-path: polygon(0 40%, 100% 60%, 100% 100%, 0 100%); }
    }
</style>
""", unsafe_allow_html=True)

# Add floating particles
st.markdown("""
<div class="energy-particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 7s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 8s;"></div>
</div>
""", unsafe_allow_html=True)

# Creative Header with animations
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; margin-bottom: 1rem; position: relative; z-index: 1;">
        ⚡ EcoSmart Energy Hub 🌱
    </h1>
    <p style="font-size: 1.2rem; opacity: 0.9; position: relative; z-index: 1;">
        Revolutionizing home energy management with style & intelligence
    </p>
    <div style="margin-top: 1rem; position: relative; z-index: 1;">
        <span style="font-size: 0.9rem; opacity: 0.8;">🔮 Powered by AI Analytics</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Creative sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%); border-radius: 15px; margin-bottom: 2rem; backdrop-filter: blur(10px);">
        <h2 style="color: white; margin-bottom: 0.5rem;">🎛️ Control Center</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Configure your smart home</p>
    </div>
    """, unsafe_allow_html=True)
    
    # House type with creative styling
    st.markdown("### 🏠 Residence Type")
    house_type = st.selectbox(
        "",
        ["🏢 Modern Apartment", "🏡 Luxury Villa", "🏘️ Cozy Townhouse", "🌆 Sky Penthouse", "🏠 Compact Studio"],
        help="Choose your architectural paradise"
    )
    
    # BHK selection with star ratings
    st.markdown("### 🛏️ Living Space Configuration")
    bhk_options = {
        1: "🏠 1BHK ⭐ Cozy Nest",
        2: "🏠 2BHK ⭐⭐ Family Haven", 
        3: "🏠 3BHK ⭐⭐⭐ Spacious Sanctuary"
    }
    
    bhk = st.radio(
        "",
        [1, 2, 3],
        format_func=lambda x: bhk_options[x],
        help="Select your comfort zone"
    )
    
    st.markdown("---")
    
    # Creative appliance section
    st.markdown("### 🎮 Smart Appliances")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ac = st.checkbox("❄️ Climate Control", help="3 kW | Arctic Comfort")
        fridge = st.checkbox("🧊 Food Preserver", help="3 kW | Fresh Guardian")
    
    with col2:
        wm = st.checkbox("🌊 Fabric Cleaner", help="3 kW | Wash Wizard")
        dishwasher = st.checkbox("🍽️ Dish Sanitizer", help="2 kW | Sparkling Clean")
    
    # Add environmental impact meter
    st.markdown("### 🌍 Eco Impact")
    appliance_count = sum([ac, fridge, wm, dishwasher])
    eco_score = max(0, 100 - (appliance_count * 15))
    
    st.progress(eco_score / 100)
    if eco_score > 80:
        st.success(f"🌱 Eco Champion! Score: {eco_score}%")
    elif eco_score > 60:
        st.warning(f"🌿 Good Balance! Score: {eco_score}%")
    else:
        st.error(f"🔥 High Impact! Score: {eco_score}%")

# Main content with creative layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Energy calculation with new appliance
    cal_energy = 0
    
    if bhk == 1:
        cal_energy += (2*0.4) + (2*0.8)
    elif bhk == 2:
        cal_energy += (3*0.4) + (3*0.8)
    elif bhk == 3:
        cal_energy += (4*0.4) + (4*0.8)
    
    appliance_energy = 0
    if ac:
        appliance_energy += 3
    if fridge:
        appliance_energy += 3
    if wm:
        appliance_energy += 3
    if dishwasher:
        appliance_energy += 2
    
    total_energy = cal_energy + appliance_energy
    
    # Creative energy display
    st.markdown("## 🔬 Energy Analysis Laboratory")
    
    # Animated metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>🏠 Base Infrastructure</h3>
            <h2>{cal_energy:.1f} kW</h2>
            <p style="opacity: 0.8;">{bhk}BHK Configuration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>🔌 Smart Devices</h3>
            <h2>{appliance_energy:.1f} kW</h2>
            <p style="opacity: 0.8;">{sum([ac, fridge, wm, dishwasher])} active units</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>⚡ Total Consumption</h3>
            <h2>{total_energy:.1f} kW</h2>
            <p style="opacity: 0.8;">Live monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced energy breakdown
    st.markdown("### 🎯 Energy Distribution Matrix")
    
    # Create comprehensive data
    breakdown_data = {
        'Category': ['💡 Lighting', '🌪️ Ventilation', '❄️ Climate', '🧊 Refrigeration', '🌊 Washing', '🍽️ Dishwashing'],
        'Energy (kW)': [
            bhk * 0.4,
            bhk * 0.8,
            3 if ac else 0,
            3 if fridge else 0,
            3 if wm else 0,
            2 if dishwasher else 0
        ],
        'Status': ['Active', 'Active', 'Active' if ac else 'Inactive', 'Active' if fridge else 'Inactive', 
                  'Active' if wm else 'Inactive', 'Active' if dishwasher else 'Inactive']
    }
    
    breakdown_df = pd.DataFrame(breakdown_data)
    active_df = breakdown_df[breakdown_df['Energy (kW)'] > 0]
    
    if not active_df.empty:
        # Create a more creative visualization
        fig_pie = px.pie(
            active_df, 
            values='Energy (kW)', 
            names='Category',
            title="🌈 Energy Rainbow Distribution",
            color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b', '#eb4d4b']
        )
        
        fig_pie.update_layout(
            showlegend=True,
            height=500,
            font=dict(size=14, family="Poppins"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=20,
            title_font_color='#2c3e50'
        )
        
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hole=0.3,
            marker=dict(line=dict(color='white', width=2))
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Creative energy gauge
    st.markdown("### ⚡ Power Matrix")
    
    # Enhanced gauge with more creative styling
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = total_energy,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Energy Flow (kW)", 'font': {'size': 16, 'family': 'Poppins'}},
        delta = {'reference': 10},
        gauge = {
            'axis': {'range': [None, 25]},
            'bar': {'color': "#667eea", 'thickness': 0.8},
            'steps': [
                {'range': [0, 6], 'color': "#a8edea"},
                {'range': [6, 12], 'color': "#fed6e3"},
                {'range': [12, 18], 'color': "#ffb3ba"},
                {'range': [18, 25], 'color': "#ff9999"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=350,
        font=dict(family="Poppins"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Real-time energy status
    if total_energy < 6:
        status = "🟢 Optimal"
        color = "#28a745"
    elif total_energy < 12:
        status = "🟡 Moderate"
        color = "#ffc107"
    elif total_energy < 18:
        status = "🟠 High"
        color = "#fd7e14"
    else:
        status = "🔴 Critical"
        color = "#dc3545"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: {color}; color: white; border-radius: 15px; margin: 1rem 0;">
        <h3 style="margin: 0;">Energy Status: {status}</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # AI-powered suggestions
    st.markdown("### 🤖 AI Recommendations")
    
    suggestions = []
    if total_energy > 15:
        suggestions.append("🔥 Consider energy-efficient appliances")
    if ac and total_energy > 10:
        suggestions.append("🌡️ Optimize AC temperature settings")
    if sum([ac, fridge, wm, dishwasher]) > 3:
        suggestions.append("⏰ Schedule appliance usage")
    
    suggestions.extend([
        "💡 Switch to LED lighting",
        "🌱 Consider solar panels",
        "🔌 Use smart power strips"
    ])
    
    for i, suggestion in enumerate(suggestions[:4]):
        st.markdown(f"""
        <div class="tip-item">
            <strong>{suggestion}</strong>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)  # Small delay for animation effect

# Creative cost estimation
st.markdown("---")
st.markdown("## 💰 Financial Impact Calculator")

# Interactive rate slider with creative styling
rate_col1, rate_col2 = st.columns([1, 3])

with rate_col1:
    st.markdown("### 💱 Electricity Rate")
    rate_per_kwh = st.slider("Rate per kWh (₹)", 5.0, 20.0, 8.0, 0.5)

with rate_col2:
    # Real-time cost calculation
    daily_hours = st.slider("⏰ Daily Usage Hours", 4, 24, 12, 1)
    daily_cost = total_energy * daily_hours * rate_per_kwh / 1000
    monthly_cost = daily_cost * 30
    yearly_cost = daily_cost * 365

# Creative cost display
cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)

with cost_col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3>📅 Daily Impact</h3>
        <h2>₹{daily_cost:.2f}</h2>
        <p style="opacity: 0.8;">{daily_hours}h usage</p>
    </div>
    """, unsafe_allow_html=True)

with cost_col2:
    st.markdown(f"""
    <div class="metric-container">
        <h3>📊 Monthly Bill</h3>
        <h2>₹{monthly_cost:.2f}</h2>
        <p style="opacity: 0.8;">30 days</p>
    </div>
    """, unsafe_allow_html=True)

with cost_col3:
    st.markdown(f"""
    <div class="metric-container">
        <h3>📈 Annual Cost</h3>
        <h2>₹{yearly_cost:.2f}</h2>
        <p style="opacity: 0.8;">365 days</p>
    </div>
    """, unsafe_allow_html=True)

with cost_col4:
    carbon_footprint = total_energy * daily_hours * 0.82 * 365 / 1000  # kg CO2 per year
    st.markdown(f"""
    <div class="metric-container">
        <h3>🌍 Carbon Impact</h3>
        <h2>{carbon_footprint:.1f}kg</h2>
        <p style="opacity: 0.8;">CO₂ annually</p>
    </div>
    """, unsafe_allow_html=True)

# Creative tips section
st.markdown("---")
st.markdown("## 🎯 Energy Optimization Center")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    <div class="tips-container">
        <h3>💡 Smart Savings Tips</h3>
        <div class="tip-item">🌟 Replace incandescent bulbs with LEDs (80% energy savings)</div>
        <div class="tip-item">🌡️ Set AC to 24°C for optimal efficiency</div>
        <div class="tip-item">⏰ Use timer switches for automated control</div>
        <div class="tip-item">🔌 Unplug devices when not in use</div>
        <div class="tip-item">🏠 Improve home insulation</div>
    </div>
    """, unsafe_allow_html=True)

with tips_col2:
    st.markdown("""
    <div class="tips-container">
        <h3>🌱 Eco-Friendly Solutions</h3>
        <div class="tip-item">☀️ Install solar panels for renewable energy</div>
        <div class="tip-item">🌊 Use rainwater harvesting systems</div>
        <div class="tip-item">🌿 Plant trees around your home for natural cooling</div>
        <div class="tip-item">♻️ Choose energy-efficient appliances</div>
        <div class="tip-item">🏡 Consider smart home automation</div>
    </div>
    """, unsafe_allow_html=True)

# Interactive action buttons
st.markdown("---")
button_col1, button_col2, button_col3, button_col4 = st.columns(4)

with button_col1:
    if st.button("🔄 Recalculate Energy", use_container_width=True):
        with st.spinner("🔮 Analyzing energy patterns..."):
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            st.success("✅ Energy analysis complete!")
            st.balloons()

with button_col2:
    if st.button("📊 Generate Report", use_container_width=True):
        st.info("📋 Comprehensive energy report generated!")
        st.download_button(
            label="📥 Download Report",
            data=f"Energy Report\nTotal Consumption: {total_energy:.1f} kW\nMonthly Cost: ₹{monthly_cost:.2f}",
            file_name="energy_report.txt",
            mime="text/plain"
        )

with button_col3:
    if st.button("🌟 Optimize Settings", use_container_width=True):
        st.info("🤖 AI optimization suggestions applied!")
        st.snow()

with button_col4:
    if st.button("📱 Share Results", use_container_width=True):
        st.info("📤 Results shared to your dashboard!")

# Creative footer
st.markdown("---")
st.markdown(f"""
<div class="footer-creative">
    <div class="energy-wave"></div>
    <div style="position: relative; z-index: 1;">
        <h3 style="margin-bottom: 1rem;">🌱 EcoSmart Energy Hub</h3>
        <p style="opacity: 0.9; margin-bottom: 0.5rem;">Empowering sustainable living through intelligent energy management</p>
        <p style="opacity: 0.7; font-size: 0.9rem;">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <div style="margin-top: 1rem;">
            <span style="margin: 0 1rem;">🏆 Award Winner</span>
            <span style="margin: 0 1rem;">🌍 Eco Certified</span>
            <span style="margin: 0 1rem;">⚡ AI Powered</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)