import json

from agents import function_tool
import streamlit as st

@function_tool
def get_tenth_result(roll_number: str) -> None:
    """"Fetches and displays the matric result for a given roll number."""
    with open("data/tenth_class_results.json", "r") as file:
        results = json.load(file)
        for result in results:
            if result["roll_no"] == roll_number:
                st.success("✅ Result Found\n")
                print("Result Found")
                st.write(f"**Name:** {result['student_name']}")
                st.write(f"**Roll Number:** {result['roll_no']}")
                st.write(f"**Class:** {result['class']}")
                st.write(f"**Marks:** {result["obtained_marks"]}/{result["total_marks"]}")
                st.write(f"**Percentage:** {result["obtained_marks"]/result["total_marks"] * 100:.2f}%")
                return
    st.warning("⚠️ No result found for this roll number.")
                
    

@function_tool
def get_ninth_result(roll_number: str) -> None:
    """"Fetches and displays the matric result for a given roll number."""
    with open("data/ninth_class_results.json", "r") as file:
        results = json.load(file)
        for result in results:
            if result["roll_no"] == roll_number:
                st.success("✅ Result Found\n")
                print("Result Found")
                st.write(f"**Name:** {result['student_name']}")
                st.write(f"**Roll Number:** {result['roll_no']}")
                st.write(f"**Class:** {result['class']}")
                st.write(f"**Marks:** {result["obtained_marks"]}/{result["total_marks"]}")
                st.write(f"**Percentage:** {result["obtained_marks"]/result["total_marks"] * 100:.2f}%")
                return
    st.warning("⚠️ No result found for this roll number.")
                
    
