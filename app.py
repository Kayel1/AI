import streamlit as st
from api import get_weather_data, get_weekly_forecast, generate_weather_description
from ui import display_current_weather, display_weekly_forecast, plot_temperature_chart
from utils import get_background_image_for_weather, set_local_background

def main():
    st.sidebar.title("⛅ Weather Forecast AI")
    city = st.sidebar.text_input("Enter City Name:")

    if st.sidebar.button("Get Weather"):
        st.title(f"Weather Updates for {city}")
        with st.spinner("Fetching weather data..."):
            weather = get_weather_data(city)

            if weather.get("cod") == 200:
                desc = weather["weather"][0]["description"]
                bg = get_background_image_for_weather(desc)
                st.markdown(set_local_background(bg), unsafe_allow_html=True)

                display_current_weather(weather)
                st.subheader("AI Weather Summary")
                st.write(generate_weather_description(weather))

                lat, lon = weather["coord"]["lat"], weather["coord"]["lon"]
                forecast = get_weekly_forecast(lat, lon)

                if forecast.get("cod") != "404":
                    display_weekly_forecast(forecast)
                    plot_temperature_chart(forecast)
                else:
                    st.error("Error fetching forecast!")
            else:
                st.error("‼ Error: City not found ‼")
    else:
        st.markdown("""
        <style>
        .typing {
            width: 22ch;
            white-space: nowrap;
            overflow: hidden;
            font-size: 2.5em;
            font-weight: bold;
            color: white;
            text-align: center;
            margin: 40px auto;
            animation: typing 2s steps(22);
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 22ch }
        }
        </style>
        <div class="typing">Weather Chatbot</div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
