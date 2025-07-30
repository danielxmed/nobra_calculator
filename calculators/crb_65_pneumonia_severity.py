"""
CRB-65 Score for Pneumonia Severity Calculator

Stratifies severity of community-acquired pneumonia (CAP) to determine 
outpatient versus inpatient treatment using 4 clinical criteria.

References:
1. Lim WS, van der Eerden MM, Laing R, Boersma WG, Karalus N, Town GI, et al. 
   Defining community acquired pneumonia severity on presentation to hospital: 
   an international derivation and validation study. Thorax. 2003;58(5):377-382. 
   doi:10.1136/thorax.58.5.377
2. Capelastegui A, España PP, Quintana JM, Areitio I, Gorordo I, Egurrola M, et al. 
   Validation of a predictive rule for the management of community-acquired pneumonia. 
   Eur Respir J. 2006;27(1):151-157.
3. McNally M, Curtain J, O'Brien KK, Dimitrov BD, Fahey T. Validity of British 
   Thoracic Society guidance (the CRB-65 rule) for predicting the severity of 
   pneumonia in general practice: systematic review and meta-analysis. 
   Br J Gen Pract. 2010;60(579):e423-433.
"""

from typing import Dict, Any


class Crb65PneumoniaSeverityCalculator:
    """Calculator for CRB-65 Score for Pneumonia Severity"""
    
    def __init__(self):
        # Scoring criteria for each component
        self.CONFUSION_SCORES = {
            "yes": 1,
            "no": 0
        }
        
        self.RESPIRATORY_RATE_SCORES = {
            "<30": 0,
            ">=30": 1
        }
        
        self.BLOOD_PRESSURE_SCORES = {
            "normal": 0,  # Systolic ≥90 mmHg AND diastolic >60 mmHg
            "low": 1      # Systolic <90 mmHg OR diastolic ≤60 mmHg
        }
        
        self.AGE_SCORES = {
            "<65": 0,
            ">=65": 1
        }
    
    def calculate(
        self,
        confusion: str,
        respiratory_rate: str,
        blood_pressure: str,
        age: str
    ) -> Dict[str, Any]:
        """
        Calculates the CRB-65 score for pneumonia severity assessment
        
        Args:
            confusion: New onset confusion or altered mental status (yes/no)
            respiratory_rate: Respiratory rate category (<30 or >=30 breaths/min)
            blood_pressure: Blood pressure category (normal or low)
            age: Age category (<65 or >=65 years)
            
        Returns:
            Dict with total score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(confusion, respiratory_rate, blood_pressure, age)
        
        # Calculate individual scores
        confusion_score = self.CONFUSION_SCORES[confusion]
        respiratory_score = self.RESPIRATORY_RATE_SCORES[respiratory_rate]
        bp_score = self.BLOOD_PRESSURE_SCORES[blood_pressure]
        age_score = self.AGE_SCORES[age]
        
        # Calculate total score
        total_score = confusion_score + respiratory_score + bp_score + age_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "component_scores": {
                    "confusion": confusion_score,
                    "respiratory_rate": respiratory_score,
                    "blood_pressure": bp_score,
                    "age": age_score
                },
                "risk_assessment": interpretation["risk_assessment"],
                "treatment_recommendation": interpretation["treatment"],
                "mortality_risk": interpretation["mortality"],
                "clinical_setting": interpretation["setting"]
            }
        }
    
    def _validate_inputs(self, confusion, respiratory_rate, blood_pressure, age):
        """Validates input parameters"""
        
        # Check confusion
        if confusion not in self.CONFUSION_SCORES:
            raise ValueError(f"Invalid confusion value: {confusion}")
        
        # Check respiratory rate
        if respiratory_rate not in self.RESPIRATORY_RATE_SCORES:
            raise ValueError(f"Invalid respiratory_rate value: {respiratory_rate}")
        
        # Check blood pressure
        if blood_pressure not in self.BLOOD_PRESSURE_SCORES:
            raise ValueError(f"Invalid blood_pressure value: {blood_pressure}")
        
        # Check age
        if age not in self.AGE_SCORES:
            raise ValueError(f"Invalid age value: {age}")
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on CRB-65 total score
        
        Args:
            total_score: Total CRB-65 score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score == 0:
            stage = "Low Risk"
            description = "Very low risk of mortality"
            mortality = "30-day mortality risk <1%"
            treatment = "Home treatment appropriate"
            setting = "Outpatient management"
            risk_assessment = "Very low risk for adverse outcomes"
            
            interpretation = (
                f"CRB-65 score of {total_score} indicates very low risk pneumonia. "
                f"Home treatment is appropriate with standard outpatient management. "
                f"30-day mortality risk is less than 1%. Consider supportive care and "
                f"appropriate antibiotic therapy as per local guidelines."
            )
            
        elif total_score <= 2:
            stage = "Intermediate Risk"
            description = "Intermediate risk of mortality"
            mortality = "30-day mortality risk 1-10%"
            treatment = "Consider hospital evaluation or short inpatient observation"
            setting = "Hospital evaluation or observation unit"
            risk_assessment = "Intermediate risk requiring closer monitoring"
            
            interpretation = (
                f"CRB-65 score of {total_score} indicates intermediate risk pneumonia. "
                f"Consider hospital evaluation or short inpatient observation. "
                f"30-day mortality risk is 1-10%. Patient may benefit from "
                f"closer monitoring and assessment for complications."
            )
            
        else:  # score 3-4
            stage = "High Risk"
            description = "High risk of mortality"
            mortality = "30-day mortality risk >10%"
            treatment = "Hospital admission recommended, consider ICU assessment"
            setting = "Inpatient admission with potential ICU evaluation"
            risk_assessment = "High risk requiring intensive monitoring and treatment"
            
            interpretation = (
                f"CRB-65 score of {total_score} indicates high risk pneumonia. "
                f"Hospital admission is recommended with consideration for ICU assessment. "
                f"30-day mortality risk exceeds 10%. Patient requires intensive monitoring, "
                f"aggressive treatment, and prompt evaluation for complications."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "mortality": mortality,
            "treatment": treatment,
            "setting": setting,
            "risk_assessment": risk_assessment
        }


def calculate_crb_65_pneumonia_severity(
    confusion: str,
    respiratory_rate: str,
    blood_pressure: str,
    age: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Crb65PneumoniaSeverityCalculator()
    return calculator.calculate(
        confusion=confusion,
        respiratory_rate=respiratory_rate,
        blood_pressure=blood_pressure,
        age=age
    )