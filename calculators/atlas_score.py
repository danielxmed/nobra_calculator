"""
ATLAS Score for Clostridium Difficile Infection Calculator

Predicts response to therapy in C. diff patients.

Formula:
Sum of points from:
- Age ≥65 years: +1 point
- Treatment with Systemic Antibiotics: +2 points
- Leukocytosis >15,000/μL: +1 point
- Albumin <2.5 g/dL: +1 point
- Serum Creatinine >1.5× baseline: +1 point

Score Interpretation:
- 0-2 points: Low Risk (Good response to vancomycin therapy expected)
- 3-6 points: High Risk (Poor response to vancomycin therapy expected)

References:
1. Miller MA, Louie T, Mullane K, Weiss K, Lentnek A, Golan Y, et al. 
   Derivation and validation of a simple clinical bedside score (ATLAS) for 
   Clostridium difficile infection which predicts response to vancomycin therapy. 
   BMC Infect Dis. 2013;13:148.
2. Cohen SH, Gerding DN, Johnson S, Kelly CP, Loo VG, McDonald LC, et al. 
   Clinical practice guidelines for Clostridium difficile infection in adults: 
   2010 update by the society for healthcare epidemiology of America (SHEA) 
   and the infectious diseases society of America (IDSA). 
   Infect Control Hosp Epidemiol. 2010;31(5):431-55.
"""


def calculate_atlas_score(
    age_65_or_older: bool,
    systemic_antibiotics: bool,
    leukocytosis: bool,
    low_albumin: bool,
    elevated_creatinine: bool
) -> dict:
    """
    Calculate ATLAS Score for Clostridium Difficile Infection
    
    Args:
        age_65_or_older (bool): Patient is 65 years of age or older
        systemic_antibiotics (bool): Currently on systemic antibiotic therapy 
                                   (other than for C. diff treatment)
        leukocytosis (bool): White blood cell count >15,000/μL
        low_albumin (bool): Serum albumin <2.5 g/dL
        elevated_creatinine (bool): Serum creatinine >1.5× baseline
        
    Returns:
        dict: Dictionary containing score, risk level, and interpretation
    """
    
    # Calculate points
    points = 0
    
    # Age ≥65 years: +1 point
    if age_65_or_older:
        points += 1
        
    # Treatment with Systemic Antibiotics: +2 points
    if systemic_antibiotics:
        points += 2
        
    # Leukocytosis >15,000/μL: +1 point
    if leukocytosis:
        points += 1
        
    # Albumin <2.5 g/dL: +1 point
    if low_albumin:
        points += 1
        
    # Serum Creatinine >1.5× baseline: +1 point
    if elevated_creatinine:
        points += 1
    
    # Determine risk level and interpretation
    if points <= 2:
        risk_level = "Low Risk"
        interpretation = (
            "Good response to vancomycin therapy expected. Low risk of treatment failure. "
            "Standard vancomycin therapy should be effective. Monitor clinical response."
        )
        management = "Standard vancomycin therapy should be effective. Monitor clinical response."
    else:  # points >= 3
        risk_level = "High Risk" 
        interpretation = (
            "Poor response to vancomycin therapy expected. High risk of treatment failure. "
            "Consider alternative therapies such as fidaxomicin or fecal microbiota "
            "transplantation. Close monitoring required."
        )
        management = (
            "Consider alternative therapies such as fidaxomicin or fecal microbiota "
            "transplantation. Close monitoring required."
        )
    
    # Create breakdown of points
    breakdown = []
    if age_65_or_older:
        breakdown.append("Age ≥65 years: +1")
    if systemic_antibiotics:
        breakdown.append("Systemic antibiotics: +2")
    if leukocytosis:
        breakdown.append("Leukocytosis >15,000/μL: +1")
    if low_albumin:
        breakdown.append("Albumin <2.5 g/dL: +1")
    if elevated_creatinine:
        breakdown.append("Creatinine >1.5× baseline: +1")
    
    return {
        "score": points,
        "max_score": 6,
        "result": f"{points} points",
        "unit": "points",
        "risk_level": risk_level,
        "interpretation": interpretation,
        "management": management,
        "breakdown": breakdown,
        "ranges": {
            "low_risk": "0-2 points: Low Risk (Good response to vancomycin therapy expected)",
            "high_risk": "3-6 points: High Risk (Poor response to vancomycin therapy expected)"
        },
        "clinical_notes": [
            "Derived and validated specifically for vancomycin therapy",
            "May not apply to other C. diff treatments",
            "Consider clinical judgment alongside score",
            "Not validated for pediatric patients"
        ]
    }


# Example usage and test cases
if __name__ == "__main__":
    # Test case 1: Low risk patient
    print("Test Case 1: Low risk patient")
    result1 = calculate_atlas_score(
        age_65_or_older=False,
        systemic_antibiotics=False,
        leukocytosis=False,
        low_albumin=False,
        elevated_creatinine=False
    )
    print(f"Score: {result1['score']}")
    print(f"Risk Level: {result1['risk_level']}")
    print(f"Interpretation: {result1['interpretation']}")
    print()
    
    # Test case 2: High risk patient
    print("Test Case 2: High risk patient")
    result2 = calculate_atlas_score(
        age_65_or_older=True,
        systemic_antibiotics=True,
        leukocytosis=True,
        low_albumin=True,
        elevated_creatinine=False
    )
    print(f"Score: {result2['score']}")
    print(f"Risk Level: {result2['risk_level']}")
    print(f"Interpretation: {result2['interpretation']}")
    print()
    
    # Test case 3: Borderline case
    print("Test Case 3: Borderline case (exactly 3 points)")
    result3 = calculate_atlas_score(
        age_65_or_older=True,
        systemic_antibiotics=True,
        leukocytosis=False,
        low_albumin=False,
        elevated_creatinine=False
    )
    print(f"Score: {result3['score']}")
    print(f"Risk Level: {result3['risk_level']}")
    print(f"Breakdown: {', '.join(result3['breakdown'])}")
