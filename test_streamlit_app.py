import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
import time
import random

class TestStreamlitApp:
    """Test suite for the Streamlit app using streamlit-app-action"""
    
    def test_app_loads_successfully(self):
        """Test that the app loads without errors"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Check that the app runs without exceptions
        assert not at.exception, f"App failed to load with error: {at.exception}"
        
        # Verify basic structure exists
        assert len(at.markdown) > 0, "No markdown elements found - app may not be rendering"
        
        print("✅ App loads successfully")
    
    def test_user_interaction_flow(self):
        """Test basic user interaction flow"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Test name input functionality
        name_input = None
        for text_input in at.sidebar.text_input:
            if "name" in text_input.label.lower():
                name_input = text_input
                break
        
        assert name_input is not None, "Name input field not found in sidebar"
        
        # Enter a test name
        name_input.input("Test User")
        at.run()
        
        # Verify session state is updated
        assert "user_data" in at.session_state, "User data not stored in session state"
        assert at.session_state.user_data.get("name") == "Test User", "Name not properly stored"
        
        # Test that visit counter increments
        initial_visits = at.session_state.visit_count
        at.run()  # Simulate page refresh
        assert at.session_state.visit_count >= initial_visits, "Visit counter not working"
        
        print(f"✅ User interaction flow works - Visit count: {at.session_state.visit_count}")

    def test_session_state_persistence(self):
        """Test that session state persists correctly"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Check initial session state
        required_keys = ['user_data', 'visit_count', 'messages', 'quiz_score', 'quiz_completed']
        
        for key in required_keys:
            assert key in at.session_state, f"Required session state key '{key}' not found"
        
        # Test data persistence
        at.sidebar.text_input[0].input("Persistence Test")
        at.run()
        
        original_visit_count = at.session_state.visit_count
        original_name = at.session_state.user_data.get("name")
        
        # Simulate multiple interactions
        for i in range(3):
            at.run()
            
            # Verify data persists
            assert at.session_state.user_data.get("name") == original_name, "Name data not persisting"
            assert at.session_state.visit_count >= original_visit_count, "Visit count not persisting"
        
        print(f"✅ Session state persistence works - Final visit count: {at.session_state.visit_count}")

    def test_error_handling_and_edge_cases(self):
        """Test error handling and edge cases"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Test with empty name initially
        assert not at.exception, "App should handle empty name gracefully"
        
        # Test with very long name
        long_name = "A" * 100
        at.sidebar.text_input[0].input(long_name)
        at.run()
        
        assert not at.exception, "App should handle long names gracefully"
        assert at.session_state.user_data.get("name") == long_name, "Long name not stored properly"
        
        # Test navigation without errors
        nav_radio = None
        for radio in at.sidebar.radio:
            if len(radio.options) > 1:  # Find navigation radio
                nav_radio = radio
                break
        
        if nav_radio:
            # Test rapid navigation changes
            for page in nav_radio.options[:3]:  # Test first 3 pages
                nav_radio.set_value(page)
                at.run()
                assert not at.exception, f"Error during rapid navigation to {page}"
        
        print("✅ Error handling and edge cases work correctly")

# Additional utility test for performance
def test_app_performance():
    """Test basic performance metrics"""
    import time
    
    start_time = time.time()
    
    at = AppTest.from_file("app.py")
    at.run()
    
    load_time = time.time() - start_time
    
    # App should load within reasonable time (adjust threshold as needed)
    assert load_time < 10, f"App took too long to load: {load_time:.2f} seconds"
    
    print(f"✅ App performance test passed - Load time: {load_time:.2f} seconds")

# Test for UI elements count (ensures UI complexity is maintained)
def test_ui_elements_present():
    """Test that expected UI elements are present"""
    at = AppTest.from_file("app.py")
    at.run()
    
    # Count different types of elements
    element_counts = {
        'markdown': len(at.markdown),
        'text_input': len(at.text_input) + len(at.sidebar.text_input),
        'selectbox': len(at.selectbox) + len(at.sidebar.selectbox),
        'button': len(at.button),
        'radio': len(at.radio) + len(at.sidebar.radio),
        'slider': len(at.slider) + len(at.sidebar.slider),
        'checkbox': len(at.checkbox) + len(at.sidebar.checkbox)
    }
    
    # Ensure minimum UI complexity
    total_elements = sum(element_counts.values())
    assert total_elements >= 10, f"Expected at least 10 UI elements, found {total_elements}"
    
    # Ensure key element types are present
    assert element_counts['text_input'] >= 1, "At least one text input should be present"
    assert element_counts['markdown'] >= 1, "At least one markdown element should be present"
    
    print(f"✅ UI elements test passed - Total elements: {total_elements}")
    for element_type, count in element_counts.items():
        if count > 0:
            print(f"   {element_type}: {count}")
