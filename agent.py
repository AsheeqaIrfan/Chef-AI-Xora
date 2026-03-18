import streamlit as st
import google.generativeai as genai

# --- 1. API CONFIGURATION ---
# The error was caused by the model version. We are using the stable flash model now.
GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Use the stable model name to avoid the 404 error
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. SYSTEM INSTRUCTIONS (The Soul of Chef AI-Xora) ---
if "system_instructions" not in st.session_state:
    st.session_state.system_instructions = (
        "You are Chef AI-Xora, a strategic and bossy Kitchen Manager. "
        "Your core mission is to reduce food waste and manage the kitchen efficiently. "
        "Rule 1: If a user mentions an ingredient is expiring or old, prioritize it as VIP and build the recipe around it first. "
        "Rule 2: Always remember user preferences, allergies, and lifestyle from previous messages. "
        "Rule 3: Always present recipes in a Markdown table with columns: Ingredients | Time | Calories. "
        "Rule 4: Identify missing ingredients and suggest a shopping list within the user's budget in PKR. "
        "Rule 5: Be smart, confident, and not like a generic robot."
    )

# --- 3. UI/UX DESIGN ---
st.set_page_config(page_title="Chef AI-Xora | Strategic Kitchen Assistant", layout="wide", page_icon="🍳")

# Sidebar for Developer Credit and Tools 
with st.sidebar:
    st.title("👨‍🍳 Chef AI-Xora")
    
    # MANDATORY DEVELOPER CREDIT 
    st.markdown("### **Developed & Deployed by:**\n**[Asheeqa Irfan]**") 
    st.divider()
    
    # Budget Input for the Kitchen Management
    user_budget = st.number_input("Enter your Budget (PKR):", min_value=0, value=500, step=50)
    st.write(f"Available Budget: **Rs {user_budget}**")
    st.info("Status: Active & Waste-Aware ♻️")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 4. CHAT INTERFACE & MEMORY LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Strategic Kitchen Assistant 🍳")
st.caption("I help you cook smart, save money, and reduce food waste.")

# Display historical conversation for persistence 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Field
if prompt := st.chat_input("List your ingredients or mention what's expiring..."):
    # Store user message in history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Chef AI-Xora is analyzing your kitchen..."):
            # Provide full context: System Instructions + Budget + Chat History 
            full_context = (
                f"{st.session_state.system_instructions}\n"
                f"Current Budget: {user_budget} PKR\n"
                f"Conversation History: {st.session_state.messages}"
            )
            
            try:
                # Generate AI Response
                response = model.generate_content(full_context)
                ai_message = response.text
                
                # Display and store response
                st.markdown(ai_message)
                st.session_state.messages.append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error(f"An error occurred: Please check your API connection. {e}")
