from flask import Flask, request, render_template
import requests
from flask import jsonify
import json

API_KEY = "WNOYbQ3_-Vz-1DZg4sfdB_I9RU2ki-1BDilaXGFq3_P0"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)  # initialising flask app



@app.route('/', methods=['GET'])

def home():
    return render_template('index1.html')
@app.route('/predict1.html')
def formpg():
    return render_template('predict1.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        GENDER = request.form['Gender']
        MARRIED=request.form['Married']
        DEPENDENTS=request.form['Dependents']
        EDUCATION = request.form['Education']
        SELF_EMPLOYES=request.form['Self_Employes']
        APPLICANTINCOME=request.form['ApplicantIncome']
        COAAPLICANTINCOME=request.form['CoaaplicantIncome']
        LOANAMOUNT= request.form['LoanAmount']
        LOAN_AMOUNT_TERM=request.form['Loan_Amount_Term']
        CREDIT_HISTORY=request.form['Credit_History']
        PROPERTY_AREA=request.form['Property_Area']
        if GENDER == 'Male':
            GENDER = 1
        else:
            GENDER = 0
        if MARRIED == 'yes':
            MARRIED = 1
        else:
            MARRIED = 0
        if DEPENDENTS == '3+':
            DEPENDENTS = 3
        elif DEPENDENTS==1:
            DEPENDENTS=1
        elif DEPENDENTS==2:
            DEPENDENTS=2
        else:
            DEPENDENTS=0
        if EDUCATION == 'Graduate':
            EDUCATION = 0
        else:
            EDUCATION = 1
        if SELF_EMPLOYES == 'yes':
            SELF_EMPLOYES = 1
        else:
            SELF_EMPLOYES = 0
        if CREDIT_HISTORY == 'yes':
            CREDIT_HISTORY = 1
        else:
            CREDIT_HISTORY = 0
        if  PROPERTY_AREA == 'Urban':
            PROPERTY_AREA = 2
        elif PROPERTY_AREA == 'Semiurban':
            PROPERTY_AREA = 1
        else:
            PROPERTY_AREA = 0
        prediction =[[GENDER, MARRIED, int(DEPENDENTS), EDUCATION, SELF_EMPLOYES, int(APPLICANTINCOME), int(COAAPLICANTINCOME), int(LOANAMOUNT), int(LOAN_AMOUNT_TERM), CREDIT_HISTORY, PROPERTY_AREA]]
        payload_scoring = {
        "input_data": [
                {
                        "field": [
                                "Gender",
                                "Married",
                                "Dependents",
                                "Education",
                                "Self_Employed",
                                "ApplicantIncome",
                                "CoapplicantIncome",
                                "LoanAmount",
                                "Loan_Amount_Term",
                                "Credit_History",
                                "Property_Area"
                        ],
                        "values": prediction
                }
        ]
}

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e3b81466-5919-4ba7-a4d9-13f2096d3f13/predictions?version=2022-11-13',
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        output=prediction[0]
        if(output==1):
            return render_template('submit.html', prediction_text="Congratulations Your are Eligible for LOAN")
        else:
            return render_template('submit.html', prediction_text="Sorry, Your are Not Eligible for LOAN")
    else:
        return render_template('predict1.html')

if __name__ == '__main__':
    app.run(debug=True)