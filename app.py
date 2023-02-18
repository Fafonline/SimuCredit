from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Fonction pour calculer l'échéancier complet


def compute_schedule(loan_amount, interest_rate, loan_duration):
    # Conversion du taux d'intérêt en taux mensuel
    monthly_interest_rate = interest_rate / 100 / 12

    # Calcul de la mensualité constante
    monthly_payment = (monthly_interest_rate * loan_amount) / \
        (1 - (1 + monthly_interest_rate)**(-loan_duration))

    # Initialisation des variables
    remaining_loan_balance = loan_amount
    monthly_interest = 0
    cumulated_interest = 0
    cumulated_capital = 0
    schedule = []

    # Calcul de l'échéancier mensuel
    for month in range(1, loan_duration + 1):
        # Calcul des intérêts mensuels
        monthly_interest = remaining_loan_balance * monthly_interest_rate
        cumulated_interest += monthly_interest

        # Calcul du capital amorti mensuel
        monthly_amortization = monthly_payment - monthly_interest
        cumulated_capital += monthly_amortization

        # Calcul du solde restant dû
        remaining_loan_balance -= monthly_amortization

        # Ajout des données mensuelles à l'échéancier
        schedule.append({
            "month": month,
            "monthly_payment": monthly_payment,
            "monthly_interest": monthly_interest,
            "monthly_amortization": monthly_amortization,
            "remaining_loan_balance": remaining_loan_balance,
            "cumulated_interest": cumulated_interest,
            "cumulated_capital": cumulated_capital
        })

    return schedule

# API pour l'échéancier complet


@app.route('/schedule', methods=['GET'])
def schedule():
    data = request.get_json()
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    loan_duration = data['loan_duration']
    schedule = compute_schedule(loan_amount, interest_rate, loan_duration)
    return jsonify(schedule)

# API pour le capital amorti cumulé pour le mois N


@app.route('/cumulated_capital/<int:month>', methods=['GET'])
def cumulated_capital(month):
    data = request.get_json()
    loan_amount = data['loan_amount']
    interest_rate = data['interest_rate']
    loan_duration = data['loan_duration']
    schedule = compute_schedule(loan_amount, interest_rate, loan_duration)
    cumulated_capital = schedule[month - 1]['cumulated_capital']
    return jsonify(cumulated_capital)


if __name__ == '__main__':
    app.run(debug=True)
