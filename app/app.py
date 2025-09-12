import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st # pyright: ignore[reportMissingImports]
from Model.model import build_QA_chain
from Model.functions import financial_health_score, calculate_emi, savings_goal

qa_chain = build_QA_chain()


st.set_page_config(page_title="Financial Assistant", page_icon="💰", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #111827;
        color: white;
    }
    .chat-container {
        padding: 10px;
        margin-bottom: 90px; /* space for fixed input */
    }
    .user-msg {
        background-color: #2563eb; /* Blue */
        color: white;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: right;
        display: inline-block;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.4;
    }
    .bot-msg {
        background-color: #374151; /* Dark grey */
        color: #f9fafb;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: left;
        display: inline-block;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.4;
    }
    /* Fix input bar at bottom */
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #111827;
        padding: 10px 20px;
        border-top: 1px solid #374151;
        z-index: 100;
    }
    .stTextInput > div > div > input {
        background-color: #1f2937;
        color: white;
        border-radius: 8px;
        border: 1px solid #4b5563;
        padding: 10px;
        font-size: 16px;
    }
    .stButton button {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #059669;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Title
# -------------------------------
st.markdown("<h1 style='text-align: center;'>💬 Financial Consultancy Web App</h1>", unsafe_allow_html=True)
st.write("Type your question below and get clear financial advice. Use the sidebar tools for calculations.")

# -------------------------------
# Session State for Chat History
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -------------------------------
# Display Chat Messages
# -------------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for role, msg in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"<div class='user-msg'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Chat Input at Bottom
# -------------------------------
st.markdown("<div class='fixed-input'>", unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Ask me anything about finance:", key="chat_input", label_visibility="collapsed")
with col2:
    send_clicked = st.button("Send")

if send_clicked and user_input:
    # Add user message
    st.session_state["messages"].append(("user", user_input))

    # Get bot response
    response = qa_chain.invoke(user_input)
    bot_answer = response["result"]

    # Add bot message
    st.session_state["messages"].append(("bot", bot_answer))

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Sidebar Financial Tools
# -------------------------------
st.sidebar.header("📊 Financial Tools")

tool_choice = st.sidebar.radio(
    "Choose a tool:",
    ["None", "Financial Health Score", "Loan EMI Calculator", "Savings Goal Planner"],
)

if tool_choice == "Financial Health Score":
    income = st.sidebar.number_input("Monthly Income", min_value=0.0)
    expenses = st.sidebar.number_input("Monthly Expenses", min_value=0.0)
    savings = st.sidebar.number_input("Monthly Savings", min_value=0.0)
    debt = st.sidebar.number_input("Outstanding Debt", min_value=0.0)
    if st.sidebar.button("Calculate Health"):
        st.sidebar.success(financial_health_score(income, expenses, savings, debt))

elif tool_choice == "Loan EMI Calculator":
    principal = st.sidebar.number_input("Loan Amount", min_value=1000.0)
    rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.1)
    years = st.sidebar.number_input("Tenure (years)", min_value=1)
    if st.sidebar.button("Calculate EMI"):
        st.sidebar.success(f"Monthly EMI: {calculate_emi(principal, rate, years)}")

elif tool_choice == "Savings Goal Planner":
    target = st.sidebar.number_input("Target Amount", min_value=1000.0)
    months = st.sidebar.number_input("Months", min_value=1)
    monthly = st.sidebar.number_input("Monthly Saving", min_value=100.0)
    if st.sidebar.button("Check Goal"):
        st.sidebar.success(savings_goal(target, months, monthly))