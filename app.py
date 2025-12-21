import streamlit as st
import random
import time
from datetime import datetime, date, timedelta

# Page configuration
st.set_page_config(
    page_title="Advanced Streamlit App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# Increment visit count
st.session_state.visit_count += 1

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .success-box {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(90deg, #2196F3, #1976D2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(90deg, #FF9800, #F57C00);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🚀 Advanced Streamlit Experience</h1>', unsafe_allow_html=True)

# Sidebar with multiple sections
with st.sidebar:
    st.header("🎛️ Control Panel")
    
    # User Profile Section
    st.subheader("👤 User Profile")
    name = st.text_input("What's your name?", placeholder="Enter your name...")
    
    if name:
        age = st.slider("Your age", 1, 100, 25)
        occupation = st.selectbox("Occupation", 
            ["Student", "Engineer", "Teacher", "Doctor", "Artist", "Business", "Other"])
        
        # Store user data
        st.session_state.user_data = {
            'name': name,
            'age': age,
            'occupation': occupation
        }
    
    st.divider()
    
    # App Settings
    st.subheader("⚙️ App Settings")
    theme_color = st.color_picker("Choose theme color", "#FF6B6B")
    show_advanced = st.toggle("Show advanced features", value=True)
    auto_refresh = st.checkbox("Auto-refresh data")
    
    st.divider()
    
    # Navigation
    st.subheader("🧭 Navigation")
    page = st.radio("Select page:", 
        ["Home", "Data Generator", "Mini Games", "Chat System", "Quiz", "Settings"])

# Main content based on selected page
if name:
    # Welcome message
    st.markdown(f"""
    <div class="success-box">
        <h3>🎉 Welcome back, {st.session_state.user_data['name']}!</h3>
        <p>👤 Age: {st.session_state.user_data['age']} | 💼 Occupation: {st.session_state.user_data['occupation']}</p>
        <p>📊 Visit count: {st.session_state.visit_count}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if page == "Home":
        # Dashboard with metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Time", datetime.now().strftime("%H:%M:%S"))
        with col2:
            st.metric("Days this year", datetime.now().timetuple().tm_yday)
        with col3:
            st.metric("Your visits", st.session_state.visit_count, delta=1)
        with col4:
            random_number = random.randint(1, 100)
            st.metric("Lucky number", random_number)
        
        # Interactive elements
        st.subheader("🎯 Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎲 Generate Random Fact"):
                facts = [
                    "Honey never spoils! 🍯",
                    "Octopuses have three hearts! 🐙",
                    "Bananas are berries, but strawberries aren't! 🍌",
                    "A group of flamingos is called a 'flamboyance'! 🦩",
                    "Wombat poop is cube-shaped! 📦"
                ]
                st.info(f"💡 **Fun Fact:** {random.choice(facts)}")
        
        with col2:
            mood = st.selectbox("How are you feeling?", 
                ["😊 Happy", "😔 Sad", "😴 Tired", "🤔 Thoughtful", "🚀 Energetic"])
            if mood:
                responses = {
                    "😊 Happy": "That's wonderful! Keep spreading the joy! ✨",
                    "😔 Sad": "Hope your day gets better! Remember, this too shall pass 💙",
                    "😴 Tired": "Maybe time for a coffee break? ☕",
                    "🤔 Thoughtful": "Deep thinking leads to great insights! 🧠",
                    "🚀 Energetic": "Channel that energy into something amazing! ⚡"
                }
                st.success(responses[mood])
    
    elif page == "Data Generator":
        st.subheader("📊 Dynamic Data Generator")
        
        # Data generation controls
        col1, col2 = st.columns(2)
        
        with col1:
            data_points = st.number_input("Number of data points", 10, 1000, 100)
            data_type = st.selectbox("Data type", ["Sales", "Temperature", "Stock Price", "Website Visits"])
        
        with col2:
            chart_type = st.selectbox("Chart type", ["Line Chart", "Bar Chart", "Area Chart"])
            if st.button("🔄 Generate New Data"):
                st.rerun()
        
        # Generate and display data
        if auto_refresh:
            time.sleep(0.1)  # Small delay for auto-refresh effect
        
        # Create sample data
        data = {}
        for i in range(data_points):
            if data_type == "Sales":
                data[f"Day {i+1}"] = random.randint(100, 1000)
            elif data_type == "Temperature":
                data[f"Hour {i+1}"] = random.randint(-10, 40)
            elif data_type == "Stock Price":
                data[f"Time {i+1}"] = random.randint(50, 500)
            else:  # Website Visits
                data[f"Page {i+1}"] = random.randint(10, 200)
        
        # Display chart based on selection
        if chart_type == "Line Chart":
            st.line_chart(data)
        elif chart_type == "Bar Chart":
            st.bar_chart(data)
        else:  # Area Chart
            st.area_chart(data)
        
        # Data statistics
        values = list(data.values())
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average", f"{sum(values)/len(values):.1f}")
        with col2:
            st.metric("Maximum", max(values))
        with col3:
            st.metric("Minimum", min(values))
    
    elif page == "Mini Games":
        st.subheader("🎮 Mini Games")
        
        # Number guessing game
        st.markdown("### 🎯 Number Guessing Game")
        
        if 'target_number' not in st.session_state:
            st.session_state.target_number = random.randint(1, 100)
            st.session_state.guesses = 0
            st.session_state.game_won = False
        
        if not st.session_state.game_won:
            guess = st.number_input("Guess a number between 1 and 100:", 1, 100, 50)
            
            if st.button("Submit Guess"):
                st.session_state.guesses += 1
                
                if guess == st.session_state.target_number:
                    st.success(f"🎉 Congratulations! You got it in {st.session_state.guesses} guesses!")
                    st.session_state.game_won = True
                    st.balloons()
                elif guess < st.session_state.target_number:
                    st.warning("📈 Too low! Try higher.")
                else:
                    st.warning("📉 Too high! Try lower.")
                
                st.info(f"Guesses made: {st.session_state.guesses}")
        
        if st.button("🔄 New Game"):
            del st.session_state.target_number
            del st.session_state.guesses
            del st.session_state.game_won
            st.rerun()
        
        st.divider()
        
        # Simple calculator
        st.markdown("### 🧮 Simple Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num1 = st.number_input("First number", value=0.0)
        with col2:
            operation = st.selectbox("Operation", ["+", "-", "×", "÷"])
        with col3:
            num2 = st.number_input("Second number", value=0.0)
        
        if st.button("Calculate"):
            try:
                if operation == "+":
                    result = num1 + num2
                elif operation == "-":
                    result = num1 - num2
                elif operation == "×":
                    result = num1 * num2
                elif operation == "÷":
                    result = num1 / num2 if num2 != 0 else "Cannot divide by zero!"
                
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    elif page == "Chat System":
        st.subheader("💬 Simple Chat System")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate simple bot response
            bot_responses = [
                f"That's interesting, {name}! Tell me more.",
                f"I see what you mean, {name}. What do you think about that?",
                f"Thanks for sharing, {name}! How does that make you feel?",
                f"Fascinating perspective, {name}! Can you elaborate?",
                f"I appreciate you telling me that, {name}. What's next?"
            ]
            
            bot_response = random.choice(bot_responses)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            st.rerun()
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    elif page == "Quiz":
        st.subheader("🧠 Quick Quiz")
        
        questions = [
            {"q": "What is 15 + 27?", "options": ["40", "42", "45", "48"], "correct": 1},
            {"q": "Which planet is closest to the Sun?", "options": ["Venus", "Mercury", "Earth", "Mars"], "correct": 1},
            {"q": "What is the capital of France?", "options": ["London", "Berlin", "Paris", "Madrid"], "correct": 2},
            {"q": "How many sides does a hexagon have?", "options": ["5", "6", "7", "8"], "correct": 1}
        ]
        
        if not st.session_state.quiz_completed:
            for i, question in enumerate(questions):
                st.markdown(f"**Question {i+1}:** {question['q']}")
                answer = st.radio(f"Select answer for Q{i+1}:", 
                                question['options'], key=f"q{i}")
                
                if st.session_state.get(f"q{i}") == question['options'][question['correct']]:
                    st.session_state.quiz_score = st.session_state.get('quiz_score', 0)
            
            if st.button("Submit Quiz"):
                score = 0
                for i, question in enumerate(questions):
                    if st.session_state.get(f"q{i}") == question['options'][question['correct']]:
                        score += 1
                
                st.session_state.quiz_score = score
                st.session_state.quiz_completed = True
                st.rerun()
        else:
            st.success(f"🎉 Quiz completed! Your score: {st.session_state.quiz_score}/{len(questions)}")
            
            if st.session_state.quiz_score == len(questions):
                st.balloons()
                st.markdown("### 🏆 Perfect score! You're amazing!")
            elif st.session_state.quiz_score >= len(questions) // 2:
                st.markdown("### 👏 Good job! Well done!")
            else:
                st.markdown("### 📚 Keep learning! You'll do better next time!")
            
            if st.button("🔄 Retake Quiz"):
                st.session_state.quiz_completed = False
                st.session_state.quiz_score = 0
                for i in range(len(questions)):
                    if f"q{i}" in st.session_state:
                        del st.session_state[f"q{i}"]
                st.rerun()
    
    elif page == "Settings":
        st.subheader("⚙️ Advanced Settings")
        
        # User preferences
        st.markdown("### 👤 User Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            notifications = st.checkbox("Enable notifications", value=True)
            dark_mode = st.checkbox("Dark mode", value=False)
            sound_effects = st.checkbox("Sound effects", value=True)
        
        with col2:
            language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT"])
            date_format = st.selectbox("Date format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        
        st.divider()
        
        # Data management
        st.markdown("### 📊 Data Management")
        
        if st.button("📥 Export User Data"):
            user_data_export = {
                "name": st.session_state.user_data.get('name', ''),
                "visit_count": st.session_state.visit_count,
                "quiz_score": st.session_state.quiz_score,
                "messages_count": len(st.session_state.messages)
            }
            st.json(user_data_export)
        
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.button("⚠️ Confirm Clear All Data"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("All data cleared!")
                st.rerun()

else:
    # Landing page when no name is entered
    st.markdown("""
    <div class="info-box">
        <h2>🌟 Welcome to the Advanced Streamlit Experience!</h2>
        <p>Please enter your name in the sidebar to unlock all features and start your journey!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## 🚀 What awaits you:
    
    - **🏠 Home Dashboard** - Personal metrics and quick actions
    - **📊 Data Generator** - Create and visualize dynamic data
    - **🎮 Mini Games** - Number guessing and calculator
    - **💬 Chat System** - Interactive messaging experience  
    - **🧠 Quiz** - Test your knowledge
    - **⚙️ Settings** - Customize your experience
    
    ### ✨ Features:
    - Session state management
    - Interactive widgets and games
    - Dynamic data visualization
    - Personalized user experience
    - Multi-page navigation
    - Real-time updates
    """)
    
    # Demo chart for visitors
    st.subheader("📈 Sample Visualization")
    demo_data = {f"Item {i}": random.randint(10, 100) for i in range(1, 11)}
    st.bar_chart(demo_data)

# Footer
st.markdown("---")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<center>🕒 Last updated: {current_time} | Built with ❤️ using Streamlit</center>", 
        unsafe_allow_html=True)