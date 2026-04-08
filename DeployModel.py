import numpy as np
import pickle 
import streamlit as st
import time  
import pandas as pd;

#styling(importing style.css)
def load_css(file_path):
    with open(file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# loading the saved model
loaded_model = pickle.load(open("trained_model.sav", "rb"))

def heart_disease_prediction(input_data):
    #creating numpy array
    input_data_as_numpy_array= np.asarray(input_data)
    # reshape the numpy array as we are predicting for only on instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0]== 0):
        return 'The Person does not have a Heart Disease'
    else:
        return 'The Person has Heart Disease'


def main():
    # Load the CSS
    load_css("styles.css")
    #title
    st.markdown('<div class="title-container"><h1>Heart Disease Prediction</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Prediction", "About Heart Disease"])

    with tab1:

        st.subheader("Heart Disease Prediction")
        # Place your prediction form here
        form_container = st.container()

    # Create a placeholder for result
    result_placeholder = st.empty()

    with form_container:
    #input data from user
        age = st.number_input('Age of the Person', min_value=0, max_value=120, step=1)
        sex	= st.selectbox('Sex of the Person', options=[(1, 'Male(1)'), (0, 'Female(0)')], format_func=lambda x: x[1])[0]
        cp = st.selectbox('Chest Pain Type', 
                        options=[(0, 'Typical Angina(0)'), (1, 'Atypical Angina(1)'), (2, 'Non-anginal Pain(2)'), (3, 'Asymptomatic(3)')], 
                        format_func=lambda x: x[1])[0]
        trestbps = st.number_input('Resting Blood Pressure', step=1)
        chol  = st.number_input('Cholesterol Level', min_value=0, step=1)
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dL', options=[(1, 'True(1)'), (0, 'False(0)')], format_func=lambda x: x[1])[0]
        restecg = st.selectbox('Resting Electrocardiographic Results', 
                            options=[(0, 'Normal(0)'), (1, 'ST-T Wave Abnormality(1)'), (2, 'Left Ventricular Hypertrophy(2)')], 
                            format_func=lambda x: x[1])[0]
        thalach = st.number_input(' Maximum Heart Rate Achieved', min_value=0, step=1)
        exang = st.selectbox('Exercise Induced Angina', options=[(1, 'Yes(1)'), (0, 'No(0)')], format_func=lambda x: x[1])[0]
        oldpeak = st.number_input('ST Depression Induced by exercise')
        slope = st.selectbox('Slope of the Peak Exercise ST Segment', 
                            options=[(0, 'Upsloping(0)'), (1, 'Flat(1)'), (2, 'Downsloping(2)')], 
                            format_func=lambda x: x[1])[0]
        ca = st.number_input('Number of Major Vessels', min_value=0, max_value=5, step=1)
        thal = st.selectbox('Thalassemia', 
                            options=[(1, 'Normal(1)'), (2, 'Fixed Defect(2)'), (3, 'Reversible Defect(3)')], 
                            format_func=lambda x: x[1])[0]
        
        # Collect input data into a dictionary
        input_data_dict = {
            "Age": age,
            "Sex": sex,
            "Chest Pain Type": cp,
            "Resting Blood Pressure": trestbps,
            "Cholesterol Level": chol,
            "Fasting Blood Sugar": fbs,
            "Resting ECG": restecg,
            "Max Heart Rate": thalach,
            "Exercise Induced Angina": exang,
            "ST Depression": oldpeak,
            "Slope": slope,
            "Number of Major Vessels": ca,
            "Thalassemia": thal
        }
        # Display preview of input data in the sidebar
        st.sidebar.header("Enter Patient Details")
        st.sidebar.divider()
        with st.sidebar.expander("Preview Input Data"):
            st.write(pd.DataFrame([input_data_dict]))

        #code for prediction    
        diagnosis = ''
        if st.button('Heart Disease Test Result'):
            # Get prediction and display result
            with st.spinner("Processing... Please wait."):
                time.sleep(3) 
                diagnosis = heart_disease_prediction([age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal])
            st.divider()
            st.subheader("Result")
            with result_placeholder:
                if diagnosis == 'The Person has Heart Disease':
                    st.markdown(
                        f'<div class="result-box">{diagnosis}</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="result-box no-disease">{diagnosis}</div>', 
                        unsafe_allow_html=True
                    )
            #adding result to download file
            input_data_dict["Result"] = diagnosis
            #adding downlaod button
            input_data_df = pd.DataFrame([input_data_dict])
            st.sidebar.divider()
            st.sidebar.subheader("Download Report")
            st.sidebar.download_button(
            label="Download ",
            data=input_data_df.to_csv(index=False).encode('utf-8'),
            file_name='Report.csv',
            mime='text/csv', 
        )


    with tab2:
        st.subheader("About Heart Disease")
        st.write("""Heart disease refers to various conditions that affect the heart's structure and function. It is one of the leading causes of death globally. Early diagnosis and management can significantly reduce the risk of complications.""")
        st.subheader("Types of Heart Disease")
        st.write("""
            1. Coronary Artery Disease (CAD):
            Caused by narrowed or blocked coronary arteries, reducing blood flow to the heart.
            Often leads to chest pain (angina) or heart attacks.
                            
            2. Heart Arrhythmias:
            Irregular heartbeats, which can be too fast (tachycardia), too slow (bradycardia), or erratic.
                            
            3. Heart Valve Disease:
            Dysfunction of one or more heart valves, causing improper blood flow.

            4. Congenital Heart Defects:
            Structural heart issues present from birth.

            5. Heart Failure:
            The heart fails to pump blood effectively, leading to fluid buildup in the body.
                            
            6. Cardiomyopathy:
            Disease of the heart muscle, often leading to thickened or weakened walls.""")
        st.subheader("Common Symptoms")
        st.write("""
            1.Chest pain or discomfort \n
            2.Shortness of breath\n
            3.Fatigue\n
            4.Irregular heartbeat\n
            5.Swelling in the legs, ankles, or feet\n
            6.Lightheadedness or dizziness""")
        st.subheader("""
            Prevention
            Healthy Diet: Focus on fruits, vegetables, whole grains, and lean proteins. Avoid processed foods and excess salt.
            Regular Exercise: At least 30 minutes of moderate exercise most days of the week.
            No Smoking: Quit smoking and avoid exposure to second-hand smoke.
            Manage Stress: Practice relaxation techniques like meditation or yoga.
            Monitor Health: Regularly check blood pressure, cholesterol, and glucose levels.
            Medication Adherence: Take prescribed medications for conditions like hypertension and diabetes.
            Treatment Options
            Lifestyle Changes: Diet, exercise, and quitting smoking.""")
        st.subheader("Why Early Detection Matters")
        st.write("""Heart disease often develops silently over years. Early detection through tools like your application can help identify risks, encourage lifestyle changes, and initiate treatment before complications arise.""")    

    
if __name__ =="__main__":
    main()