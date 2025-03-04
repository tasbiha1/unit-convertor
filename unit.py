import streamlit as st
from forex_python.converter import CurrencyRates
from pint import UnitRegistry

# Initialize Unit Registry
ureg = UnitRegistry()

# Streamlit UI
st.title("Google-Style Unit Converter")

# Conversion categories
categories = ["Length", "Weight", "Temperature", "Currency"]
selected_category = st.selectbox("Select a category", categories)

# Define conversion logic
def convert_units(value, from_unit, to_unit, category):
    try:
        if category == "Currency":
            c = CurrencyRates()
            return c.convert(from_unit, to_unit, value)
        elif category == "Temperature":
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                return (value * 9/5) + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                return (value - 32) * 5/9
            elif from_unit == "Celsius" and to_unit == "Kelvin":
                return value + 273.15
            elif from_unit == "Kelvin" and to_unit == "Celsius":
                return value - 273.15
            elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
                return (value - 32) * 5/9 + 273.15
            elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
                return (value - 273.15) * 9/5 + 32
            else:
                return "Invalid Temperature Conversion"
        else:
            return (value * ureg(from_unit)).to(to_unit).magnitude
    except Exception as e:
        return f"Error: {e}"

# Define unit options based on category
unit_options = {
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch"],
    "Weight": ["gram", "kilogram", "pound", "ounce"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Currency": ["USD", "EUR", "GBP", "INR", "JPY"]
}

from_unit = st.selectbox("From", unit_options[selected_category])
to_unit = st.selectbox("To", unit_options[selected_category])
value = st.number_input("Enter value", min_value=0.0, format="%.2f")

if st.button("Convert"):
    result = convert_units(value, from_unit, to_unit, selected_category)
    st.success(f"{value} {from_unit} = {result} {to_unit}")