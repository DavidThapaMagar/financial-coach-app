from flask import Flask, request, jsonify, send_from_directory
import time
from flask_cors import CORS
from backend.core.financial_goal import FinancialGoal

app = Flask(__name__, static_folder='../frontend')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_goal():
    try:
        data = request.json

        goal = FinancialGoal(
            goal_name=data['goal_name'],
            target=float(data['target']),
            deadline_months=float(data['deadline_months']),
            hourly_wage=float(data['hourly_wage']),
            hours_per_week=float(data['hours_per_week']),
            monthly_expenses=float(data['monthly_expenses']),
            savings_percent=float(data.get('savings_percent', 20)) / 100,
            buffer_percent=float(data.get('buffer_percent', 10)) / 100
        )

        return jsonify(goal.get_summary())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/purchase-impact', methods=['POST'])
def purchase_impact():
    try:
        data = request.json

        goal = FinancialGoal(
            goal_name=data['goal_name'],
            target=float(data['target']),
            deadline_months=float(data['deadline_months']),
            hourly_wage=float(data['hourly_wage']),
            hours_per_week=float(data['hours_per_week']),
            monthly_expenses=float(data['monthly_expenses']),
            savings_percent=float(data.get('savings_percent', 20)) / 100,
            buffer_percent=float(data.get('buffer_percent', 10)) / 100
        )

        purchase_amount = float(data['purchase_amount'])

        delay = goal.calculate_purchase_delay(purchase_amount)
        percent = goal.calculate_purchase_percentage(purchase_amount)

        return jsonify({
            "purchase_amount": purchase_amount,
            "delay_days": delay["delay_days"],
            "delay_months": delay["delay_months"],
            "message": delay["message"],
            "goal_percent": percent
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
