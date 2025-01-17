import streamlit as st
from datetime import datetime, timedelta
import random

def main():
    st.title("Kashmir Itinerary Maker")
    st.header("Create a Customized Travel Itinerary")

    # Customer Information
    st.subheader("Customer Information")
    customer_name = st.text_input("Customer Name")
    phone_number = st.text_input("Phone Number")
    uploaded_files = st.file_uploader("Upload ID Documents", accept_multiple_files=True)

    # Trip Details
    st.subheader("Trip Details")
    num_passengers = st.number_input("Number of Passengers", min_value=1, step=1)
    car_type = st.selectbox("Type of Car", ["Sedan", "SUV", "Minivan", "Luxury"])
    car_price_per_day = st.number_input("Price for Car Service per Day", min_value=0.0, step=100.0, format="%.2f")
    car_days = st.number_input("Number of Days Car is Needed", min_value=1, step=1)
    num_cars = st.number_input("Number of Cars Needed", min_value=1, step=1)
    total_car_price = car_price_per_day * car_days * num_cars

    places_to_visit = st.multiselect("Places to Visit", ["Srinagar", "Pahalgam", "Gulmarg", "Sonmarg", "Doodpathri"])

    # Hotel Details for Each Location
    hotel_details = {}
    for place in places_to_visit:
        hotel_name = st.text_input(f"Hotel Name at {place}", key=f"hotel_name_{place}")
        hotel_price = st.number_input(f"Price for Hotel at {place}", min_value=0.0, step=100.0, format="%.2f", key=f"hotel_price_{place}")
        if hotel_name:
            hotel_details[place] = {
                "hotel_name": hotel_name,
                "hotel_price": hotel_price
            }

    # Start and End Dates
    st.subheader("Trip Dates")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if start_date and end_date and start_date < end_date:
        num_days = (end_date - start_date).days
        num_nights = num_days - 1
    else:
        num_days = 0
        num_nights = 0
        st.error("Please select valid start and end dates.")

    # Optional Flight Details
    st.subheader("Flight Details (Optional)")
    include_flight = st.checkbox("Include Flight in Package")
    if include_flight:
        flight_price = st.number_input("Enter Price of Plane Ticket (per passenger)", min_value=0.0, step=100.0, format="%.2f")
    else:
        flight_price = 0.0

    # Generate Itinerary Button
    if st.button("Generate Itinerary"):
        # Validate Inputs
        if not customer_name or not phone_number:
            st.error("Please enter both customer name and phone number.")
        elif not places_to_visit:
            st.error("Please select at least one place to visit.")
        elif num_days <= 0:
            st.error("Please ensure the start date is before the end date.")
        else:
            trip_id = generate_trip_id()
            total_amount = calculate_total_amount(
                total_car_price, hotel_details, flight_price, include_flight, num_passengers
            )
            itinerary = generate_itinerary(
                customer_name, phone_number, uploaded_files,
                num_passengers, car_type, num_cars, places_to_visit, hotel_details,
                start_date, end_date, num_days, num_nights, trip_id, total_amount
            )
            st.success("Itinerary Generated Successfully!")
            st.text(itinerary)

def generate_trip_id():
    return str(random.randint(10000, 99999))

def calculate_total_amount(total_car_price, hotel_details, flight_price, include_flight, num_passengers):
    base_amount = total_car_price + sum(hotel["hotel_price"] for hotel in hotel_details.values())
    if include_flight:
        base_amount += flight_price * num_passengers
    margin = base_amount * 0.5  # 50% margin
    miscellaneous = base_amount * 0.1  # 10% miscellaneous expenses
    total_amount = base_amount + margin + miscellaneous
    return total_amount

def generate_itinerary(customer_name, phone_number, uploaded_files,
                       num_passengers, car_type, num_cars, places_to_visit, hotel_details,
                       start_date, end_date, num_days, num_nights, trip_id, total_amount):
    itinerary = []

    # Customer Information
    itinerary.append("Kashmir Travel Itinerary")
    itinerary.append(f"Trip ID: {trip_id}")
    itinerary.append(f"Customer Name: {customer_name}")
    itinerary.append(f"Phone Number: {phone_number}")

    # Uploaded IDs
    if uploaded_files:
        itinerary.append("Uploaded ID Documents:")
        for file in uploaded_files:
            itinerary.append(f"- {file.name}")

    # Trip Details
    itinerary.append("\nTrip Details:")
    itinerary.append(f"Number of Passengers: {num_passengers}")
    itinerary.append(f"Type of Car: {car_type}")
    itinerary.append(f"Number of Cars: {num_cars}")
    itinerary.append(f"Places to Visit:")
    for place in places_to_visit:
        hotel_name = hotel_details.get(place, {}).get("hotel_name", "N/A")
        itinerary.append(f"- {place} (Hotel: {hotel_name})")
    itinerary.append(f"Duration: {num_days} Days and {num_nights} Nights")
    itinerary.append(f"Start Date: {start_date.strftime('%d-%m-%Y')}")
    itinerary.append(f"End Date: {end_date.strftime('%d-%m-%Y')}")

    # Total Amount
    itinerary.append("\nTotal Trip Cost:")
    itinerary.append(f"₹{total_amount:.2f}")

    return "\n".join(itinerary)

if __name__ == "__main__":
    main()
