import streamlit as st
from urllib.parse import unquote
import pandas as pd

# ---- PAGE SETUP ----
st.set_page_config(
    page_title="Cogni Package Recommendation",
    page_icon="🧠",
    layout="wide"
)

# ---- HEADER SECTION ----
with st.container():
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image("https://via.placeholder.com/100x100?text=Cogni", width=60) 
    with col_title:
        st.markdown("## Cogni: Personalized Package Recommendation")
        st.markdown("Delivering smart, scalable mental health solutions tailored to your practice.")

# ---- PACKAGE DICTIONARY ----
PACKAGES = {
    'Fresh Start': {
        'ideal_client': 'Solo or small private practice',
        'seats': '2-4 seats',
        'pricing': '$199/month base + $40/seat/month',
        'features': [
            'Basic self-guided tools',
            'AI self-assessment',
            '1 group session/month',
            '1 report template'
        ]
    },
    'Practice Plus': {
        'ideal_client': 'Mental health clinics or private group practices (5–15 providers)',
        'seats': '5–15 seats',
        'pricing':'$299/month base (includes 5 seats) + $35/additional seat',
        'features': [
            'Full AI suite',
            'Group modules',
            '2 sessions/month',
            'Custom reports',
            'Provider dashboard'
        ]
    },
    'Community Access': {
        'ideal_client': 'Group homes, home care services',
        'seats': '10–30 staff, scalable by user volume',
        'pricing': '$299 base (includes 5 seats) + $7.99/ user/ month with volume discounts',
        'features': [
            'Multilingual AI tools',
            'Group support modules',
            'Onboarding support',
            'Usage dashboard',
            'Volume discounts for 500+ users'
        ]
    },
    'Enterprise Care (Public Health)': {
        'ideal_client': 'Public health institutions, rehabilitation centers, or clinics',
        'seats': '10+ staff, unlimited users',
        'pricing': 'Customized plan starting at $600+/month + fee-for-service contract',
        'features': [
            'Full AI triage',
            'Post-session care',
            'Real-time analytics',
            'API access',
            'Client monitoring & support',
            'Unlimited video, audio, and text-based monitoring tools'
        ]
    },
    'Enterprise Access (Insurance & EAS)': {
        'ideal_client': 'Insurance providers and Employee Assistance Services',
        'seats': 'Unlimited or tiered by number of covered members',
        'pricing': 'Customized plan starting at $600+/month + fee-for-service contract',
        'features': [
            'API integration',
            'Branded self-assessments',
            'Usage analytics',
            'Employer group modules',
            'Outcome dashboards',
            'Unlimited monitoring tools'
        ]
    }
}

# ---- PARSE QUERY PARAMETERS ----
query_params = st.experimental_get_query_params()
recommended_package = None
recommended_seats = None

if "tier" in query_params:
    recommended_package = unquote(str(query_params["tier"][0]))
if "seats" in query_params:
    recommended_seats = unquote(str(query_params["seats"][0]))

if not recommended_package or not recommended_seats:
    st.warning("No recommendation received. Please complete the chatbot conversation.")
    st.stop()

# ---- RECOMMENDATION SECTION ----
st.divider()
st.markdown("### 🌟 Recommended Package")

st.success(f"**Recommended Package:** {recommended_package}")
if recommended_seats:
    st.markdown(f"**Recommended Seats:** {recommended_seats}")

package = PACKAGES.get(recommended_package, {})

col1, col2 = st.columns([2, 1])

with col1:
    if package:
        st.markdown(f"**Ideal for:** {package.get('ideal_client', '')}")
        st.markdown(f"**Capacity:** {package.get('seats', '')}")
        st.markdown(f"**Pricing:** {package.get('pricing', '')}")

        with st.expander("🔍 View Key Features"):
            for feature in package.get('features', []):
                st.write(f"✅ {feature}")

with col2:
    with st.container():
        st.markdown("### 📞 Get in Touch")
        st.write("Have questions or need help picking the right package?")
        st.markdown("**📧 Email:** [support@cognicorplustherapy.com](mailto:support@cognicorplustherapy.com)  \n**📞 Phone:** (555) 123-4567")

# ---- EXPLORATION TABS ----
st.divider()
st.markdown("### 📦 Explore All Packages")

tab_list = list(PACKAGES.keys())
tabs = st.tabs(tab_list)

for tab, pkg_name in zip(tabs, tab_list):
    with tab:
        p = PACKAGES[pkg_name]

        if pkg_name == recommended_package:
            st.success("📝 **This is your recommended package**")

        st.markdown(f"**Ideal for:** {p['ideal_client']}")
        st.markdown(f"**Capacity:** {p['seats']}")
        st.markdown(f"**Pricing:** {p['pricing']}")

        with st.expander("🔍 View Key Features"):
            for f in p['features']:
                st.write(f"✅ {f}")

        if pkg_name != recommended_package:
            if st.button(f"Select {pkg_name}", key=f"select_{pkg_name}"):
                st.experimental_set_query_params(tier=pkg_name, seats=recommended_seats)
                st.experimental_rerun()

# ---- FOOTER ----
st.divider()
st.markdown("""
<div style='text-align: center; color: grey; font-size: small'>
    © 2025 Cogni Inc. | All rights reserved.
</div>
""", unsafe_allow_html=True)