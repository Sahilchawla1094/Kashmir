import streamlit as st
from datetime import datetime
import random

def main():
    st.title("Kashmir Itinerary Maker")
    st.header("Create a Customized Travel Itinerary")

    # Customer Information
    st.subheader("Customer Information")
    customer_name = st.text_input("Customer Name")
    phone_number = st.text_input("Phone Number")
    uploaded_files = st.file_uploader("Upload ID Documents", accept_multiple_files=True)

    # Trip Dates
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

    # Trip Details
    st.subheader("Trip Details")
    num_passengers = st.number_input("Number of Passengers", min_value=1, step=1)
    car_type = st.selectbox("Type of Car", ["Sedan", "SUV", "Minivan", "Luxury"])
    car_price_per_day = st.number_input("Price for Car Service per Day", min_value=0.0, step=100.0, format="%.2f")
    car_days = st.number_input("Number of Days Car is Needed", min_value=1, step=1)
    num_cars = st.number_input("Number of Cars Needed", min_value=1, step=1)
    total_car_price = car_price_per_day * car_days * num_cars

    # Places to Visit
    st.subheader("Places to Visit")
    categories = {
        "Kashmir": [
            "Srinagar", "Pahalgam", "Gulmarg", "Sonmarg", "Doodpathri",
            "Aharbal waterfall", "Gurez valley", "Keran valley", "Yusmarg",
            "Sinthan top", "Duksum valley", "Verinag", "Tosmaidan"
        ],
        "Jammu": ["Vaishno Devi"]
    }

    selected_categories = st.multiselect("Select Categories", list(categories.keys()))
    places_to_visit = []
    for category in selected_categories:
        places_to_visit += st.multiselect(f"Select Places to Visit in {category}", categories[category])

    # Stay Duration for Each Place
    stay_durations = {}
    total_stay_days = 0
    for place in places_to_visit:
        stay_durations[place] = st.number_input(f"Number of Days to Stay at {place}", min_value=1, step=1, key=f"stay_{place}")
        total_stay_days += stay_durations[place]

    if total_stay_days != num_days:
        st.error(f"The total number of stay days ({total_stay_days}) does not match the trip duration ({num_days}). Please adjust your inputs.")

    # Hotel Details
    st.subheader("Hotel Details")
    num_hotels = st.number_input("Number of Hotels Needed", min_value=1, step=1)
    hotel_details = []
    for i in range(1, num_hotels + 1):
        st.text(f"Hotel {i}")
        hotel_name = st.text_input(f"Name of Hotel {i}", key=f"hotel_name_{i}")
        hotel_price = st.number_input(f"Price for Hotel {i}", min_value=0.0, step=100.0, format="%.2f", key=f"hotel_price_{i}")
        hotel_location = st.selectbox(f"Location of Hotel {i}", options=places_to_visit, key=f"hotel_location_{i}")
        hotel_details.append({
            "name": hotel_name,
            "price": hotel_price,
            "location": hotel_location
        })

    # Addons Section
    st.subheader("Addons")

    # Union Cabs
    st.text("Union Cabs")
    num_union_cabs = st.number_input("Number of Union Cabs Needed", min_value=0, step=1, key="num_union_cabs")
    union_cab_price = st.number_input("Price per Union Cab", min_value=0.0, step=100.0, format="%.2f", key="union_cab_price")
    union_cab_locations = st.multiselect("Locations for Union Cabs", options=places_to_visit, key="union_cab_locations")

    # Gulmarg Gondola
    st.text("Gulmarg Gondola")
    gondola_phase_1_price = st.number_input("Price for Gulmarg Gondola Phase 1", min_value=0.0, step=100.0, format="%.2f", key="gondola_phase_1")
    gondola_phase_2_price = st.number_input("Price for Gulmarg Gondola Phase 2", min_value=0.0, step=100.0, format="%.2f", key="gondola_phase_2")

    # Horse Ride
    st.text("Horse Ride")
    horse_ride_price = st.number_input("Price for Horse Ride", min_value=0.0, step=100.0, format="%.2f", key="horse_ride")

    # Optional Flight Details
    st.subheader("Flight Details (Optional)")
    include_flight = st.checkbox("Include Flight in Package")
    if include_flight:
        flight_price = st.number_input("Enter Price of Plane Ticket (per passenger)", min_value=0.0, step=100.0, format="%.2f")
    else:
        flight_price = 0.0

    # Generate Itinerary Button
    if st.button("Generate Itinerary"):
        if not customer_name or not phone_number:
            st.error("Please enter both customer name and phone number.")
        elif not places_to_visit:
            st.error("Please select at least one place to visit.")
        elif num_days <= 0:
            st.error("Please ensure the start date is before the end date.")
        elif total_stay_days != num_days:
            st.error(f"The total number of stay days ({total_stay_days}) does not match the trip duration ({num_days}). Please adjust your inputs.")
        else:
            trip_id = str(random.randint(10000, 99999))
            total_amount, cost_breakup = calculate_total_amount(
                total_car_price, hotel_details, flight_price, include_flight, num_passengers, 
                num_union_cabs, union_cab_price, gondola_phase_1_price, gondola_phase_2_price, horse_ride_price
            )
            itinerary = generate_itinerary(
                customer_name, phone_number, uploaded_files,
                num_passengers, car_type, num_cars, places_to_visit, stay_durations, hotel_details,
                start_date, end_date, num_days, num_nights, trip_id, total_amount,
                num_union_cabs, union_cab_price, union_cab_locations,
                gondola_phase_1_price, gondola_phase_2_price, horse_ride_price, include_flight, flight_price
            )
            st.success(f"Itinerary Generated Successfully! (Trip ID: {trip_id})")
            st.markdown(itinerary, unsafe_allow_html=True)

            # Cost Breakdown
            st.subheader("Cost Breakdown (Internal Use)")
            for key, value in cost_breakup.items():
                st.write(f"{key}: ₹{value:.2f}")

def calculate_total_amount(total_car_price, hotel_details, flight_price, include_flight, num_passengers, 
                            num_union_cabs, union_cab_price, gondola_phase_1_price, gondola_phase_2_price, horse_ride_price):
    base_amount = total_car_price + sum(hotel["price"] for hotel in hotel_details)
    union_cabs_cost = num_union_cabs * union_cab_price
    gondola_cost = gondola_phase_1_price + gondola_phase_2_price
    horse_ride_cost = horse_ride_price

    if include_flight:
        flight_cost = flight_price * num_passengers
    else:
        flight_cost = 0.0

    margin = base_amount * 0.5  # 50% margin
    miscellaneous = base_amount * 0.1  # 10% miscellaneous expenses
    total_amount = base_amount + union_cabs_cost + gondola_cost + horse_ride_cost + flight_cost + margin + miscellaneous

    return total_amount, {
        "Car Service": total_car_price,
        "Hotels": sum(hotel["price"] for hotel in hotel_details),
        "Flight Cost": flight_cost,
        "Union Cabs": union_cabs_cost,
        "Gulmarg Gondola": gondola_cost,
        "Horse Ride": horse_ride_cost,
        "Base Amount": base_amount,
        "Margin (50%)": margin,
        "Miscellaneous (10%)": miscellaneous,
        "Total Amount": total_amount
    }

def generate_itinerary(customer_name, phone_number, uploaded_files, num_passengers, car_type, num_cars, places_to_visit, stay_durations, hotel_details,
                       start_date, end_date, num_days, num_nights, trip_id, total_amount,
                       num_union_cabs, union_cab_price, union_cab_locations,
                       gondola_phase_1_price, gondola_phase_2_price, horse_ride_price, include_flight, flight_price):
    itinerary = []

    # Customer Information
    itinerary.append(f"<h2 style='color: #2c3e50;'>Travel Itinerary</h2>")
    itinerary.append(f"<strong>Trip ID:</strong> {trip_id}<br>")
    itinerary.append(f"<strong>Customer Name:</strong> {customer_name}<br>")
    itinerary.append(f"<strong>Phone Number:</strong> {phone_number}<br>")

    # Trip Details
    itinerary.append("<h3 style='color: #2980b9;'>Trip Details</h3>")
    itinerary.append(f"<strong>Duration:</strong> {num_days} Days and {num_nights} Nights<br>")
    itinerary.append(f"<strong>Places to Visit:</strong><br>")
    for place, days in stay_durations.items():
        itinerary.append(f"- {place}: {days} day(s)<br>")

    # Addons
    itinerary.append("<h3 style='color: #e67e22;'>Addons</h3>")
    if num_union_cabs > 0:
        itinerary.append(f"<strong>Union Cabs:</strong> {num_union_cabs} cab(s) <br>")
        itinerary.append(f"Locations: {', '.join(union_cab_locations)}<br>")
    if gondola_phase_1_price > 0:
        itinerary.append(f"<strong>Gulmarg Gondola Phase 1:</strong> Yes <br>")
    if gondola_phase_2_price > 0:
        itinerary.append(f"<strong>Gulmarg Gondola Phase 2:</strong> Yes <br>")
    if horse_ride_price > 0:
        itinerary.append(f"<strong>Horse Ride:</strong> Yes <br>")
    if include_flight:
        itinerary.append(f"<strong>Flight Included:</strong> Yes <br>")

    # Total Amount
    itinerary.append("<h3 style='color: #27ae60;'>Total Trip Cost</h3>")
    itinerary.append(f"<strong>₹{total_amount:.2f}</strong><br>")

    return "\n".join(itinerary)

if __name__ == "__main__":
    main()
