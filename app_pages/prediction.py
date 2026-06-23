import streamlit as st
import pandas as pd
import numpy as np
import helper


def show_prediction(df):
    if not st.session_state["user_logged_in"]:
        st.warning("🚫 Please log in to access this page.")
        st.stop()

    prediction_menu = st.sidebar.radio(
        "Select an option",
        ("Medal Prediction", "Country Medal Prediction")
    )

    if prediction_menu == "Medal Prediction":
        st.title("🎯 Athlete Medal Prediction")
        st.write("Fill in or select an athlete to predict their chances of winning a medal.")

        use_existing = st.radio("Choose Input Method:", ["Select Athlete", "Manual Entry"])

        valid_athletes_df = df.dropna(subset=['Name', 'Age', 'Weight', 'Height', 'Sport', 'Event', 'Sex'])

        if use_existing == "Select Athlete":
            athlete_names = sorted(valid_athletes_df['Name'].unique().tolist())
            selected_athlete = st.selectbox("Select Athlete", athlete_names)
            athlete_data = valid_athletes_df[valid_athletes_df['Name'] == selected_athlete].iloc[0]

            age = int(athlete_data['Age'])
            height = int(athlete_data['Height'])
            weight = int(athlete_data['Weight'])
            sex = athlete_data['Sex']
            sport = athlete_data['Sport']
            event = athlete_data['Event']
            team = athlete_data.get('Team', 'Unknown')
            previous_medals = df[(df['Name'] == selected_athlete) & (df['Medal'].notna())].shape[0]

            st.markdown(f"**First olympics games of {selected_athlete}:**")
            st.write(f"**Age**: {age}, **Height**: {height} cm, **Weight**: {weight} kg, "
                     f"**Sex**: {sex}, **Sport**: {sport}, **Event**: {event}, "
                     f"**Team**: {team}, **Previous Medals**: {previous_medals}")
        else:
            age = st.number_input("Age", 10, 60)
            height = st.number_input("Height (cm)", 100, 250)
            weight = st.number_input("Weight (kg)", 30, 200)
            sex = st.selectbox("Sex", ['M', 'F'])
            sport = st.selectbox("Sport", sorted(df['Sport'].dropna().unique()))
            event = st.selectbox("Event", sorted(df[df['Sport'] == sport]['Event'].dropna().unique()))
            previous_medals = st.number_input("Number of Previous Medals", 0, 50)
            team = st.text_input("Team (Country)", "Unknown")

        bmi = round(weight / ((height / 100) ** 2), 2)
        st.metric("🧮 BMI", bmi)

        model_choice = st.selectbox("Select Model", ["Random Forest", "Logistic Regression", "XGBoost"])

        if st.button("Predict Medal"):
            from helper import train_medal_prediction_model_with_features

            try:
                model, encoders, feature_importance, acc = train_medal_prediction_model_with_features(df, model_choice)

                if team not in encoders["team"].classes_:
                    st.warning("⚠️ Selected team not found in training data. Please use an existing country/team name.")
                    st.stop()

                input_data = pd.DataFrame([[
                    age,
                    height,
                    weight,
                    bmi,
                    previous_medals,
                    encoders['sex'].transform([sex])[0],
                    encoders['sport'].transform([sport])[0],
                    encoders['event'].transform([event])[0],
                    encoders['team'].transform([team])[0]
                ]], columns=['Age', 'Height', 'Weight', 'BMI', 'Previous_Medals', 'Sex', 'Sport', 'Event', 'Team'])

                prediction = model.predict(input_data)[0]
                medal = encoders['medal'].inverse_transform([prediction])[0]
                probs = model.predict_proba(input_data)[0]

                st.success(f"🏅 Predicted Medal: **{medal}**")
                st.info(f"📊 Model Accuracy: **{acc:.2%}**")

                # Probability bar chart
                prob_df = pd.DataFrame({
                    'Medal': encoders['medal'].inverse_transform(np.arange(len(probs))),
                    'Probability': probs
                })
                st.bar_chart(prob_df.set_index('Medal'))

                # Feature importance chart
                st.subheader("📌 Feature Importance")
                fi_df = pd.DataFrame({
                    'Feature': input_data.columns,
                    'Importance': feature_importance
                }).sort_values(by="Importance", ascending=False)
                st.bar_chart(fi_df.set_index('Feature'))

            except Exception as e:
                st.error("❌ Prediction failed.")
                st.exception(e)

    if prediction_menu == "Country Medal Prediction":
        st.title("📈 Country & Sport Medal Prediction")
        st.write("Predict the number of medals a country might win in a selected **sport** for a future Olympics.")

        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.selectbox("Select Country", country_list)

        sport_list = df['Sport'].dropna().unique().tolist()
        sport_list.sort()
        selected_sport = st.selectbox("Select Sport", sport_list)

        future_year = st.number_input("Enter Future Olympic Year (e.g. 2028)", min_value=2024, max_value=2100, step=4)

        if st.button("Predict Medals"):
            from helper import train_country_sport_medal_model

            model, medal_df, r2 = train_country_sport_medal_model(df, selected_country, selected_sport)

            if model is None:
                st.warning(f"❌ Not enough data to predict medals for {selected_country} in {selected_sport}.")
            else:
                prediction = model.predict([[future_year]])[0]
                st.success(
                    f"🏅 Predicted Total Medals for **{selected_country}** in **{selected_sport}** ({future_year}): **{int(prediction)}**")
                st.info(f"📊 Model R² Score: {r2:.2f}")

                # Plot history + prediction
                import matplotlib.pyplot as plt

                fig, ax = plt.subplots()
                ax.plot(medal_df['Year'], medal_df['Total_Medals'], marker='o', label='Historical')
                ax.scatter(future_year, prediction, color='red', s=100, label='Prediction')
                ax.set_xlabel("Year")
                ax.set_ylabel("Medals Won")
                ax.set_title(f"{selected_country} - {selected_sport}")
                ax.legend()
                st.pyplot(fig)