def calculate_airq(
    daytime_symptoms: str,
    nighttime_awakenings: str,
    activity_limitation: str,
    rescue_medication_daily: str,
    social_activity_limitation: str,
    exercise_limitation: str,
    difficult_control: str,
    oral_steroids: str,
    emergency_visits: str,
    hospitalization: str
) -> dict:
    """
    Calculate the Asthma Impairment and Risk Questionnaire (AIRQ) score.
    
    The AIRQ is a validated 10-item questionnaire that assesses both symptom impairment 
    and exacerbation risk in patients aged 12 years and older with asthma.
    
    Parameters (all yes/no questions):
    - daytime_symptoms: Symptoms bothering during day on >4 days in past 2 weeks
    - nighttime_awakenings: Woken from sleep >1 time in past 2 weeks  
    - activity_limitation: Limited daily activities every day in past 2 weeks
    - rescue_medication_daily: Used rescue inhaler/nebulizer every day in past 2 weeks
    - social_activity_limitation: Limited social activities in past 2 weeks
    - exercise_limitation: Limited ability to exercise in past 2 weeks
    - difficult_control: Felt difficult to control asthma in past 2 weeks
    - oral_steroids: Took steroid pills/shots in past 12 months
    - emergency_visits: ED or unplanned visits in past 12 months
    - hospitalization: Hospital stay overnight in past 12 months
    
    Returns:
    dict: Calculation result with score, interpretation, and category
    """
    
    # Define all parameters as yes/no questions
    questions = [
        daytime_symptoms,
        nighttime_awakenings,
        activity_limitation,
        rescue_medication_daily,
        social_activity_limitation,
        exercise_limitation,
        difficult_control,
        oral_steroids,
        emergency_visits,
        hospitalization
    ]
    
    # Validate all inputs are either 'yes' or 'no'
    for i, response in enumerate(questions):
        if response.lower() not in ['yes', 'no']:
            raise ValueError(f"Parameter {i+1} must be 'yes' or 'no', got '{response}'")
    
    # Calculate total score (count of 'yes' responses)
    airq_score = sum(1 for response in questions if response.lower() == 'yes')
    
    # Determine control category based on validated cut-points
    if airq_score <= 1:
        category = "Well-controlled"
        description = "Well-controlled asthma"
        interpretation = ("Asthma is well-controlled. Continue current management and monitor regularly. "
                         "Even well-controlled patients can have asthma attacks, but the risk is lower.")
        risk_level = "Low"
    elif airq_score <= 4:
        category = "Not well-controlled"
        description = "Not well-controlled asthma"
        interpretation = ("Asthma control is suboptimal. Consider step-up therapy, review inhaler technique "
                         "and adherence. Increased risk of exacerbations compared to well-controlled patients.")
        risk_level = "Moderate"
    else:  # score >= 5
        category = "Very poorly controlled"
        description = "Very poorly controlled asthma"
        interpretation = ("Asthma is very poorly controlled with significant impairment and high exacerbation risk. "
                         "Requires immediate therapeutic intervention and specialist referral consideration.")
        risk_level = "High"
    
    # Create breakdown of domains
    impairment_score = sum(1 for response in questions[:7] if response.lower() == 'yes')
    risk_score = sum(1 for response in questions[7:] if response.lower() == 'yes')
    
    return {
        'airq_score': airq_score,
        'category': category,
        'description': description,
        'interpretation': interpretation,
        'risk_level': risk_level,
        'impairment_score': impairment_score,
        'risk_score': risk_score,
        'details': {
            'total_questions': 10,
            'yes_responses': airq_score,
            'no_responses': 10 - airq_score,
            'impairment_domain': f"{impairment_score}/7 (past 2 weeks symptoms)",
            'risk_domain': f"{risk_score}/3 (past 12 months exacerbations)",
            'cut_points': {
                'well_controlled': '0-1 points',
                'not_well_controlled': '2-4 points', 
                'very_poorly_controlled': '5-10 points'
            }
        },
        'recommendations': _get_recommendations(airq_score, category),
        'validation_notes': [
            "Validated for patients aged 12 years and older with physician-diagnosed asthma",
            "ROC AUC 0.94 for identifying well-controlled vs not well-/very poorly controlled",
            "ROC AUC 0.93 for identifying well-/not well-controlled vs very poorly controlled",
            "Sensitivity 0.90 and specificity 0.79 for cut-point ≥2",
            "Specificity 0.95 for cut-point ≥5 (very poorly controlled)"
        ]
    }

def _get_recommendations(score: int, category: str) -> list:
    """Get clinical recommendations based on AIRQ score and category."""
    
    base_recommendations = [
        "Discuss individual question responses with healthcare provider",
        "Use AIRQ results as part of comprehensive clinical assessment",
        "Consider shared decision-making for treatment planning"
    ]
    
    if category == "Well-controlled":
        specific_recommendations = [
            "Continue current asthma management plan",
            "Monitor regularly with periodic assessments", 
            "Maintain good inhaler technique and adherence",
            "Review asthma action plan",
            "Annual AIRQ assessment recommended"
        ]
    elif category == "Not well-controlled":
        specific_recommendations = [
            "Consider step-up therapy according to guidelines",
            "Review and optimize inhaler technique",
            "Assess medication adherence",
            "Evaluate environmental triggers",
            "Consider more frequent monitoring (every 3-6 months)",
            "Update asthma action plan"
        ]
    else:  # Very poorly controlled
        specific_recommendations = [
            "Urgent review of asthma management required",
            "Consider specialist referral if not already under specialist care",
            "Evaluate for difficult-to-treat or severe asthma",
            "Comprehensive medication review and optimization",
            "Assess for comorbidities and triggers",
            "Consider biological therapy if appropriate",
            "Frequent monitoring required (monthly initially)",
            "Ensure emergency action plan is in place"
        ]
    
    return base_recommendations + specific_recommendations
