# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Simulated database of projects and user groups
projects_database = [
    {"id": 1, "name": "Algiers Sunrise", "type": "VSP", "location": "Algiers", "housingType": "Apartment", "price": 8000000, "rooms": 3},
    {"id": 2, "name": "Oran Seaside", "type": "Finished", "location": "Oran", "housingType": "Villa", "price": 11000000, "rooms": 5},
    {"id": 3, "name": "Constantine Heights", "type": "VSP", "location": "Constantine", "housingType": "Duplex", "price": 9500000, "rooms": 4},
    {"id": 4, "name": "Annaba Community", "type": "Community", "location": "Annaba", "housingType": "Apartment", "price": 7500000, "rooms": 2},
    {"id": 5, "name": "Tlemcen Gardens", "type": "VSP", "location": "Tlemcen", "housingType": "Villa", "price": 10500000, "rooms": 4},
    {"id": 6, "name": "Sétif Plaza", "type": "Finished", "location": "Sétif", "housingType": "Apartment", "price": 8500000, "rooms": 3},
    {"id": 7, "name": "Batna Residences", "type": "Community", "location": "Batna", "housingType": "Duplex", "price": 9000000, "rooms": 3},
    {"id": 8, "name": "Blida Towers", "type": "VSP", "location": "Blida", "housingType": "Apartment", "price": 7800000, "rooms": 2},
]

user_groups = [
    {"id": 1, "location": "Algiers", "housingType": "Apartment", "averageBudget": 8500000, "members": 15},
    {"id": 2, "location": "Oran", "housingType": "Villa", "averageBudget": 12000000, "members": 8},
    {"id": 3, "location": "Constantine", "housingType": "Duplex", "averageBudget": 10000000, "members": 12},
    {"id": 4, "location": "Annaba", "housingType": "Apartment", "averageBudget": 7800000, "members": 10},
    {"id": 5, "location": "Tlemcen", "housingType": "Villa", "averageBudget": 11000000, "members": 6},
    {"id": 6, "location": "Sétif", "housingType": "Apartment", "averageBudget": 8800000, "members": 14},
    {"id": 7, "location": "Batna", "housingType": "Duplex", "averageBudget": 9200000, "members": 9},
    {"id": 8, "location": "Blida", "housingType": "Apartment", "averageBudget": 8000000, "members": 11},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_info = request.json
    print("Received user info:", user_info)  # Ajoutez cette ligne pour le débogage
    matching_projects = find_matching_projects(user_info)
    loan_simulation = simulate_loan(user_info)
    matching_groups = find_matching_groups(user_info)
    
    response = {
        'matchingProjects': matching_projects,
        'loanSimulation': loan_simulation,
        'matchingGroups': matching_groups
    }
    print("Sending response:", response)  # Ajoutez cette ligne pour le débogage
    return jsonify(response)

def find_matching_projects(user_info):
    return [
        project for project in projects_database
        if project['location'].lower() == user_info['location'].lower()
        and project['housingType'].lower() == user_info['housingType'].lower()
        and project['rooms'] == int(user_info['rooms'])
        and project['price'] <= float(user_info['maxBudget'])
    ]

def simulate_loan(user_info):
    income = float(user_info['income'])
    age = int(user_info['age'])
    max_loan_term = min(40, 70 - age)
    interest_rate = 0.01 if income <= 120000 else 0.03

    max_loan_amount = 12000000 if income <= 120000 else 15000000
    desired_loan_amount = float(user_info['maxBudget']) - float(user_info['currentSavings'])
    loan_amount = min(desired_loan_amount, max_loan_amount)

    monthly_rate = interest_rate / 12
    number_of_payments = max_loan_term * 12

    monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate) ** number_of_payments) / ((1 + monthly_rate) ** number_of_payments - 1)

    other_debts = float(user_info['otherDebts']) if user_info['otherDebts'] else 0
    total_monthly_debt = monthly_payment + other_debts
    debt_to_income_ratio = total_monthly_debt / income

    max_debt_to_income_ratio = 0.4
    max_monthly_payment = (income * max_debt_to_income_ratio) - other_debts
    max_debt_capacity = (max_monthly_payment / monthly_rate) * (1 - (1 + monthly_rate) ** -number_of_payments)

    is_eligible = age < 40 and debt_to_income_ratio <= max_debt_to_income_ratio

    return {
        'monthlyPayment': round(monthly_payment, 2),
        'interestRate': round(interest_rate * 100, 2),
        'loanAmount': round(loan_amount, 2),
        'loanTermYears': max_loan_term,
        'isEligible': is_eligible,
        'debtToIncomeRatio': round(debt_to_income_ratio * 100, 2),
        'maxDebtCapacity': round(max_debt_capacity, 2)
    }

def find_matching_groups(user_info):
    return [
        group for group in user_groups
        if group['location'].lower() == user_info['location'].lower()
        and group['housingType'].lower() == user_info['housingType'].lower()
        and abs(group['averageBudget'] - float(user_info['maxBudget'])) <= 1000000
    ]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)