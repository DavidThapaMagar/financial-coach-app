from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from core.financial_goal import FinancialGoal

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate financial goal based on user input"""
    try:
        data = request.json
        
        # Validate inputs
        required_fields = ['goal_name', 'target', 'deadline_months', 'hourly_wage', 
                          'hours_per_week', 'monthly_expenses']
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Create goal object
        goal = FinancialGoal(
            goal_name=data['goal_name'],
            target=float(data['target']),
            deadline_months=float(data['deadline_months']),
            hourly_wage=float(data['hourly_wage']),
            hours_per_week=float(data['hours_per_week']),
            monthly_expenses=float(data['monthly_expenses']),
            savings_percent=float(data.get('savings_percent', 0.20)) / 100,
            buffer_percent=float(data.get('buffer_percent', 0.10)) / 100
        )
        
        # Return summary as JSON
        summary = goal.get_summary()
        summary['on_track'] = bool(summary['on_track'])
        
        return jsonify(summary), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/purchase-impact', methods=['POST'])
def purchase_impact():
    """Calculate impact of a purchase on a goal"""
    try:
        data = request.json
        
        # Recreate goal object
        goal = FinancialGoal(
            goal_name=data['goal_name'],
            target=float(data['target']),
            deadline_months=float(data['deadline_months']),
            hourly_wage=float(data['hourly_wage']),
            hours_per_week=float(data['hours_per_week']),
            monthly_expenses=float(data['monthly_expenses']),
            savings_percent=float(data.get('savings_percent', 0.20)) / 100,
            buffer_percent=float(data.get('buffer_percent', 0.10)) / 100
        )
        
        purchase_amount = float(data['purchase_amount'])
        
        # Calculate delay
        delay = goal.calculate_purchase_delay(purchase_amount)
        percentage = goal.calculate_purchase_percentage(purchase_amount)
        
        return jsonify({
            "delay_days": delay['delay_days'],
            "delay_months": delay['delay_months'],
            "percentage_of_goal": percentage,
            "message": delay['message']
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
