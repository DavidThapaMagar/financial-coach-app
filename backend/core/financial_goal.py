class FinancialGoal:
    """AI Financial Coach - Goal Tracker"""
    
    def __init__(self, goal_name, target, deadline_months, hourly_wage, hours_per_week, 
                 monthly_expenses, savings_percent=0.20, buffer_percent=0.10):
        """
        Initialize a financial goal.
        
        Args:
            goal_name: Name of the goal (e.g., "Mom's Dior Wallet")
            target: Target amount in dollars
            deadline_months: Desired deadline in months
            hourly_wage: Hourly wage in dollars
            hours_per_week: Hours worked per week
            monthly_expenses: Fixed monthly expenses
            savings_percent: Percent of income to save (default 20%)
            buffer_percent: Comfort buffer percent of FREE CASHFLOW (default 10%)
        """
        self.goal_name = goal_name
        self.target = target
        self.deadline_months = deadline_months
        self.hourly_wage = hourly_wage
        self.hours_per_week = hours_per_week
        self.monthly_expenses = monthly_expenses
        self.savings_percent = savings_percent
        self.buffer_percent = buffer_percent
        
        # Calculate derived values
        self.monthly_income = self._calculate_monthly_income()
        self.free_cashflow = self._calculate_free_cashflow()
        self.buffer_amount = self._calculate_buffer()
        self.discretionary_available = self._calculate_discretionary_available()
        self.recommended_monthly_savings = self._calculate_recommended_savings()
        self.eta_months = self._calculate_eta()
        self.required_monthly_savings = self._calculate_required_savings()
        self.shortfall = self._calculate_shortfall()
    
    def _calculate_monthly_income(self):
        """Calculate monthly income from hourly wage and weekly hours."""
        weekly_income = self.hourly_wage * self.hours_per_week
        monthly_income = weekly_income * (52 / 12)
        return round(monthly_income, 2)
    
    def _calculate_free_cashflow(self):
        """Calculate money left after fixed expenses."""
        return round(self.monthly_income - self.monthly_expenses, 2)
    
    def _calculate_buffer(self):
        """Calculate comfort buffer from FREE CASHFLOW (for emergencies)."""
        return round(self.free_cashflow * self.buffer_percent, 2)
    
    def _calculate_discretionary_available(self):
        """Calculate money available after buffer (for savings + fun)."""
        return round(self.free_cashflow - self.buffer_amount, 2)
    
    def _calculate_recommended_savings(self):
        """
        Recommend savings as percentage of income, but capped at discretionary available.
        
        Logic:
        1. Try to save 20% of income
        2. But don't exceed what's available after buffer
        3. Never negative
        """
        target_savings = self.monthly_income * self.savings_percent
        recommended = min(target_savings, self.discretionary_available)
        return round(max(0, recommended), 2)
    
    def _calculate_required_savings(self):
        """Calculate required monthly savings to hit deadline."""
        required = self.target / self.deadline_months
        return round(required, 2)
    
    def _calculate_eta(self):
        """Calculate estimated time to reach goal at recommended savings rate."""
        if self.recommended_monthly_savings <= 0:
            return float('inf')
        eta = self.target / self.recommended_monthly_savings
        return round(eta, 2)
    
    def _calculate_shortfall(self):
        """Calculate shortfall by deadline if using recommended savings."""
        saved_by_deadline = self.recommended_monthly_savings * self.deadline_months
        shortfall = max(0, self.target - saved_by_deadline)
        return round(shortfall, 2)
    
    def calculate_purchase_delay(self, purchase_amount):
        """
        Calculate how many days a purchase delays the goal.
        
        Args:
            purchase_amount: Purchase amount in dollars
            
        Returns:
            Dictionary with delay in days and months
        """
        if self.recommended_monthly_savings <= 0:
            return {
                "delay_days": float('inf'),
                "delay_months": float('inf'),
                "message": "You're currently saving $0/month. Set a savings amount to see impact."
            }
        
        daily_savings = self.recommended_monthly_savings / 30.44
        delay_days = purchase_amount / daily_savings
        delay_months = purchase_amount / self.recommended_monthly_savings
        
        return {
            "delay_days": round(delay_days, 1),
            "delay_months": round(delay_months, 2),
            "purchase_amount": purchase_amount,
            "message": f"This ${purchase_amount} purchase delays '{self.goal_name}' by {round(delay_days, 0)} days."
        }
    
    def calculate_purchase_percentage(self, purchase_amount):
        """
        Calculate what percent of the goal a purchase represents.
        
        Args:
            purchase_amount: Purchase amount in dollars
            
        Returns:
            Percentage of goal
        """
        percent = (purchase_amount / self.target) * 100
        return round(percent, 1)
    
    def get_summary(self):
        """Return a summary of the goal and financial situation."""
        summary = {
            "goal_name": self.goal_name,
            "target": self.target,
            "original_deadline": self.deadline_months,
            "monthly_income": self.monthly_income,
            "monthly_expenses": self.monthly_expenses,
            "free_cashflow": self.free_cashflow,
            "buffer_amount": self.buffer_amount,
            "discretionary_available": self.discretionary_available,
            "recommended_monthly_savings": self.recommended_monthly_savings,
            "required_monthly_savings_for_deadline": self.required_monthly_savings,
            "estimated_completion_months": self.eta_months if self.eta_months != float('inf') else "Not achievable with current savings",
            "shortfall_by_original_deadline": self.shortfall,
            "on_track": self.shortfall == 0,
            "savings_rate_percent": round(self.savings_percent * 100, 1)
        }
        return summary
    
    def print_report(self):
        """Print a readable report of the goal."""
        print("\n" + "="*60)
        print(f"💰 FINANCIAL GOAL: {self.goal_name}")
        print("="*60)
        print(f"\n📊 INCOME & EXPENSES:")
        print(f"  Monthly Income:        ${self.monthly_income:,.2f}")
        print(f"  Fixed Expenses:        ${self.monthly_expenses:,.2f}")
        print(f"  Free Cashflow:         ${self.free_cashflow:,.2f}")
        print(f"  Emergency Buffer:      ${self.buffer_amount:,.2f}")
        print(f"  Available for Goals:   ${self.discretionary_available:,.2f}")
        
        print(f"\n🎯 GOAL ANALYSIS:")
        print(f"  Target Amount:         ${self.target:,.2f}")
        print(f"  Original Deadline:     {self.deadline_months} months")
        print(f"  Required/Month:        ${self.required_monthly_savings:,.2f}")
        
        print(f"\n✅ RECOMMENDED PLAN:")
        print(f"  Monthly Set-Aside:     ${self.recommended_monthly_savings:,.2f}")
        print(f"  Savings Rate:          {self.savings_percent*100:.0f}% of income")
        
        if self.eta_months != float('inf'):
            print(f"  Estimated Completion:  {self.eta_months} months")
            months_diff = self.deadline_months - self.eta_months
            if months_diff > 0:
                print(f"  ⚡ Beats deadline by:   {months_diff} months")
            else:
                print(f"  ⚠️  Misses deadline by:  {abs(months_diff)} months")
        else:
            print(f"  Estimated Completion:  Not achievable")
        
        print(f"  Shortfall by deadline: ${self.shortfall:,.2f}")
        print("\n" + "="*60 + "\n")
