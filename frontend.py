import streamlit as st
from chatbot import load_info, find_best_match, get_ans, add_new_ans
import time

# Page configuration
st.set_page_config(
    page_title="Grey the Machine Learning AI Bot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Custom CSS with simpler styling that should work more reliably
def load_css():
    st.markdown("""
    <style>
    /* Basic styling */
    .main {
        background-color: #181818;
        color: #E0E0E0;
    }

    /* Header styling */
    h1 {
        color: #7B68EE;
        font-weight: bold;
        text-align: center;
    }

    /* Subtitle styling */
    .subtitle {
        color: #B0B0B0;
        text-align: center;
        font-style: italic;
        margin-bottom: 20px;
    }

    /* Chat header */
    .chat-header {
        background-color: #2d2d2d;
        color: #E0E0E0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Bot icon styling */
    .bot-icon {
        font-size: 40px;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Teaching form styling */
    .teaching-container {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)


# Apply CSS
load_css()

# Title and subtitle
st.markdown("<h1>Grey the Machine Learning AI Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your intelligent learning companion</p>", unsafe_allow_html=True)

# Simple bot icon
st.markdown("<div class='bot-icon'>🤖</div>", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "waiting_for_teaching" not in st.session_state:
    st.session_state.waiting_for_teaching = False

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "show_typing" not in st.session_state:
    st.session_state.show_typing = False

# Load the knowledge base
info = load_info("memory.json")

# Create a header for the chat container
st.markdown("<div class='chat-header'><h3>💬 Conversation</h3></div>", unsafe_allow_html=True)

# Create a scrollable container with fixed height
chat_container = st.container(height=400)

# Display messages inside the scrollable container
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["text"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["text"])

    # Show typing indicator if needed
    if st.session_state.show_typing:
        with st.chat_message("assistant", avatar="🤖"):
            st.write("Thinking...")

# Teaching form - only show if we're waiting for a teaching input
if st.session_state.waiting_for_teaching:
    st.markdown("<div class='teaching-container'>", unsafe_allow_html=True)
    st.write(f"✨ I don't know about '{st.session_state.current_question}'. Please teach me!")

    with st.form(key="teach_form"):
        new_answer = st.text_input("Answer:", key="teaching_input")
        teach_submit = st.form_submit_button("Teach me!")

        if teach_submit and new_answer.strip():
            # Add the new knowledge
            add_new_ans(st.session_state.current_question, new_answer.strip(), info)

            # Show success message
            st.success("Knowledge added successfully!")

            # Add thank you message to chat
            thank_you = f"Thanks for teaching me about '{st.session_state.current_question}'! I'll remember that."
            st.session_state.messages.append({"role": "bot", "text": thank_you})

            # Reset teaching state
            st.session_state.waiting_for_teaching = False

            # Slight delay for better UX
            time.sleep(0.5)

            # Rerun to update the UI
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Main input form for questions - at the bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Message Grey:", placeholder="Ask me anything...", key="user_input")
    submitted = st.form_submit_button("Send 💬")

    if submitted and user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "text": user_input})

        # Show typing indicator
        st.session_state.show_typing = True
        st.rerun()

# Process the input (separated to show the typing animation)
if st.session_state.show_typing and not st.session_state.waiting_for_teaching:
    # Try to find a response
    best_match = find_best_match(user_input, [q["question"] for q in info["questions"]])

    # Small delay to show typing effect
    time.sleep(0.7)

    if best_match:
        # We found a match - provide the answer
        answer = get_ans(best_match, info)
        st.session_state.messages.append({"role": "bot", "text": answer})
    else:
        # No match found - enter teaching mode
        st.session_state.current_question = user_input
        st.session_state.waiting_for_teaching = True
        st.session_state.messages.append(
            {"role": "bot", "text": f"I don't know about '{user_input}'. Would you like to teach me?"})

    # Turn off typing indicator
    st.session_state.show_typing = False

    # Rerun to update the UI
    st.rerun()

# Footer with stats
st.markdown(f"""
<div style="text-align: center; margin-top: 20px; color: #888;">
    Grey's knowledge base: {len(info["questions"])} facts learned
</div>
""", unsafe_allow_html=True)