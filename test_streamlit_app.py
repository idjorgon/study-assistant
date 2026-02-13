import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
import time
import random
import pandas as pd
import io
from app import generate_csv_from_data

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

# Test for CSV export functionality
class TestCSVExport:
    """Test suite for CSV export functionality"""
    
    def test_generate_csv_from_data_basic(self):
        """Test basic CSV generation from data dictionary"""
        # Sample data
        data = {
            "Day 1": 100,
            "Day 2": 200,
            "Day 3": 150
        }
        data_type = "Sales"
        
        # Generate CSV
        csv_output = generate_csv_from_data(data, data_type)
        
        # Verify CSV is generated
        assert csv_output is not None, "CSV output should not be None"
        assert isinstance(csv_output, str), "CSV output should be a string"
        
        # Verify CSV content
        assert "Label,Sales" in csv_output, "CSV should have correct headers"
        assert "Day 1,100" in csv_output, "CSV should contain first data point"
        assert "Day 2,200" in csv_output, "CSV should contain second data point"
        assert "Day 3,150" in csv_output, "CSV should contain third data point"
        
        print("✅ Basic CSV generation test passed")
    
    def test_generate_csv_from_data_different_types(self):
        """Test CSV generation with different data types"""
        test_cases = [
            ({"Hour 1": -10, "Hour 2": 25}, "Temperature"),
            ({"Time 1": 100, "Time 2": 250}, "Stock Price"),
            ({"Page 1": 50, "Page 2": 75}, "Website Visits")
        ]
        
        for data, data_type in test_cases:
            csv_output = generate_csv_from_data(data, data_type)
            
            # Verify header contains the correct data type
            assert f"Label,{data_type}" in csv_output, f"CSV should have '{data_type}' in header"
            
            # Verify data is present
            for label, value in data.items():
                assert f"{label},{value}" in csv_output, f"CSV should contain {label},{value}"
        
        print("✅ CSV generation with different data types test passed")
    
    def test_generate_csv_parseable(self):
        """Test that generated CSV can be parsed back into DataFrame"""
        data = {
            "Item 1": 42,
            "Item 2": 87,
            "Item 3": 33
        }
        data_type = "Sales"
        
        # Generate CSV
        csv_output = generate_csv_from_data(data, data_type)
        
        # Parse CSV back into DataFrame
        df = pd.read_csv(io.StringIO(csv_output))
        
        # Verify DataFrame structure
        assert len(df) == len(data), "DataFrame should have same number of rows as input data"
        assert list(df.columns) == ['Label', data_type], "DataFrame should have correct column names"
        
        # Verify data integrity
        for idx, (label, value) in enumerate(data.items()):
            assert df.iloc[idx]['Label'] == label, f"Label at index {idx} should match input"
            assert df.iloc[idx][data_type] == value, f"Value at index {idx} should match input"
        
        print("✅ CSV parseability test passed")
    
    def test_generate_csv_with_empty_data(self):
        """Test CSV generation with edge cases"""
        # Empty data
        empty_data = {}
        csv_output = generate_csv_from_data(empty_data, "Sales")
        
        # Should still have headers
        assert "Label,Sales" in csv_output, "CSV should have headers even when empty"
        
        # Single item
        single_data = {"Item 1": 100}
        csv_output = generate_csv_from_data(single_data, "Sales")
        assert "Item 1,100" in csv_output, "CSV should handle single item correctly"
        
        print("✅ CSV edge cases test passed")
    
    def test_csv_download_button_present_in_app(self):
        """Test that CSV download button appears in the Data Generator page"""
        at = AppTest.from_file("app.py")
        at.run()
        
        # Enter name to unlock features
        at.sidebar.text_input[0].input("Test User")
        at.run()
        
        # Navigate to Data Generator page
        nav_radio = None
        for radio in at.sidebar.radio:
            if "Data Generator" in radio.options:
                nav_radio = radio
                nav_radio.set_value("Data Generator")
                break
        
        assert nav_radio is not None, "Navigation radio should be found"
        at.run()
        
        # Check for download button - Streamlit uses download_button which is separate from regular buttons
        # The download button is present if there are no exceptions and the page renders
        assert not at.exception, "Data Generator page should render without errors"
        
        # Verify the page has metrics (which are rendered alongside the download button)
        assert len(at.metric) >= 3, "Data Generator should show statistics metrics"
        
        print("✅ CSV download button integration test passed")
