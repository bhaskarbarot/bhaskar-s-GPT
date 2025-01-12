import streamlit as st
from huggingface_hub import InferenceClient
import random

# Initialize Hugging Face client
client = InferenceClient(api_key="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")

# Funny responses templates
FUNNY_RESPONSES = [
    "Oh boy, let me put on my comedy hat for this one! 🎭\n{response}",
    "Here's what my funny circuit says: 🤪\n{response}",
    "Warning: Incoming dad joke! 🎯\n{response}",
    "My humor module is firing on all cylinders! 🎪\n{response}",
    "Before I get serious, here's a fun take: 🎨\n{response}"
]

# Function to generate funny responses
def generate_funny_response(question):
    funny_prompt = f"""You are a witty and humorous AI assistant. Give a short, funny, and slightly sarcastic response to this question. Keep it light and entertaining: {question}"""
    
    messages = [
        {"role": "user", "content": funny_prompt}
    ]
    
    response = ""
    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=messages,
        temperature=0.8,
        max_tokens=150,
        top_p=0.9,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    
    return random.choice(FUNNY_RESPONSES).format(response=response)

# Function to generate serious responses
def generate_serious_response(question):
    messages = [
        {"role": "user", "content": question}
    ]
    
    response = ""
    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=messages,
        temperature=0.5,
        max_tokens=2048,
        top_p=0.7,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    
    return response

# Streamlit UI
st.title("🤖 Funny Chat with Bhaskar's GPT 😄😄")
st.markdown("### Ask me anything🤔 - I'll give you a funny answer 😄 AND a serious one! 🎭")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_question = st.text_input("Your question:", key="user_input")

if user_question:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Generate and add funny response
    with st.spinner("Generating funny response... 🎪"):
        funny_response = generate_funny_response(user_question)
        st.session_state.messages.append({"role": "assistant", "content": funny_response, "type": "funny"})
    
    # Generate and add serious response
    with st.spinner("Now for the serious answer... 🎯"):
        serious_response = generate_serious_response(user_question)
        st.session_state.messages.append({"role": "assistant", "content": serious_response, "type": "serious"})

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write("You: " + message["content"])
    else:
        if message.get("type") == "funny":
            st.markdown("### 😄 Funny Answer")
            st.write(message["content"])
        else:
            st.markdown("### 🎓 Serious Answer")
            st.write(message["content"])
    st.markdown("---")

# Add some styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)