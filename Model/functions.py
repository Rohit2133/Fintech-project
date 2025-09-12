def financial_health_score(income, expenses, savings, debt=0):

    # Calculate a simple financial health score.
    if income <= 0:
        return "Income must be greater than zero."
    savings_rate = (savings / income) * 100
    expense_ratio = (expenses / income) * 100
    debt_ratio = (debt / income) * 100
    score = (savings_rate * 0.5) - (expense_ratio * 0.3) - (debt_ratio * 0.2)
    if score > 60:
        status = "Healthy"
    elif score >= 40:
        status = "Moderate"
    else:
        status = "Risky"
    return f"Your financial health score is {round(score,2)} → {status}"


def calculate_emi(principal, rate, years):

    # Calculate monthly EMI for a loan.
    r = rate / (12 * 100)  # monthly interest
    n = years * 12
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return round(emi, 2)


def savings_goal(target, months, monthly_saving):

    # Check if savings goal is achievable.
    total = monthly_saving * months
    if total >= target:
        return f"You will reach your goal! Saved {total} vs target {target}."
    else:
        shortfall = target - total
        return f"You will fall short by {shortfall}. Increase your monthly saving."
