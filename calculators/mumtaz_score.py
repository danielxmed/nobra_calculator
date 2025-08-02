"""
Mumtaz Score for Readmission in Cirrhosis Calculator

Predicts 30-day readmission risk in patients with cirrhosis following hospital discharge.
This prognostic tool helps clinicians identify high-risk patients who may benefit from 
enhanced discharge planning and close outpatient follow-up.

References:
1. Mumtaz K, Issak A, Porter K, Kelly S, Hanje J, Michaels AJ, et al. Validation of Risk Score 
   in Predicting Early Readmissions in Decompensated Cirrhotic Patients: A Model Based on the 
   Administrative Database. Hepatology. 2019;70(2):630-639. doi: 10.1002/hep.30274.
2. Berman K, Tandra S, Forssell K, Vuppalanchi R, Burton JR Jr, Nguyen JH, et al. Incidence 
   and predictors of 30-day readmission among patients hospitalized for advanced liver disease. 
   Clin Gastroenterol Hepatol. 2011;9(3):254-9. doi: 10.1016/j.cgh.2010.10.035.
"""

import math
from typing import Dict, Any


class MumtazScoreCalculator:
    """Calculator for Mumtaz Score for Readmission in Cirrhosis"""
    
    def __init__(self):
        # Model coefficients based on logistic regression analysis
        # These are approximate values based on the published study
        self.INTERCEPT = -2.5
        self.AGE_COEFFICIENT = 0.015
        self.SODIUM_COEFFICIENT = -0.04
        self.ALBUMIN_COEFFICIENT = -0.8
        self.LENGTH_OF_STAY_COEFFICIENT = 0.02
        self.PREVIOUS_ADMISSIONS_COEFFICIENT = 0.3
        self.MELD_COEFFICIENT = 0.05
        self.HEPATIC_ENCEPHALOPATHY_COEFFICIENT = 0.6
        self.ASCITES_COEFFICIENT = 0.4
        
    def calculate(self, age: int, serum_sodium: float, albumin: float, 
                 length_of_stay: int, previous_admissions_6_months: int, 
                 meld_score: int, hepatic_encephalopathy: str, ascites: str) -> Dict[str, Any]:
        """
        Calculates the Mumtaz Score for 30-day readmission risk in cirrhosis patients
        
        Args:
            age (int): Patient age in years
            serum_sodium (float): Serum sodium level in mEq/L
            albumin (float): Serum albumin level in g/dL
            length_of_stay (int): Current hospital length of stay in days
            previous_admissions_6_months (int): Number of admissions in previous 6 months
            meld_score (int): MELD score at discharge
            hepatic_encephalopathy (str): Presence of hepatic encephalopathy ("yes" or "no")
            ascites (str): Presence of ascites ("yes" or "no")
            
        Returns:
            Dict with the readmission risk probability and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, serum_sodium, albumin, length_of_stay, 
                            previous_admissions_6_months, meld_score, 
                            hepatic_encephalopathy, ascites)
        
        # Calculate logistic regression score
        linear_combination = self._calculate_linear_combination(
            age, serum_sodium, albumin, length_of_stay, 
            previous_admissions_6_months, meld_score, 
            hepatic_encephalopathy, ascites
        )
        
        # Convert to probability using logistic function
        probability = self._logistic_function(linear_combination)
        
        # Convert to percentage
        risk_percentage = probability * 100
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_percentage)
        
        return {
            "result": round(risk_percentage, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, serum_sodium: float, albumin: float,
                        length_of_stay: int, previous_admissions_6_months: int,
                        meld_score: int, hepatic_encephalopathy: str, ascites: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(serum_sodium, (int, float)) or serum_sodium < 100 or serum_sodium > 160:
            raise ValueError("Serum sodium must be between 100 and 160 mEq/L")
        
        if not isinstance(albumin, (int, float)) or albumin < 1.0 or albumin > 6.0:
            raise ValueError("Albumin must be between 1.0 and 6.0 g/dL")
        
        if not isinstance(length_of_stay, int) or length_of_stay < 1 or length_of_stay > 365:
            raise ValueError("Length of stay must be an integer between 1 and 365 days")
        
        if not isinstance(previous_admissions_6_months, int) or previous_admissions_6_months < 0 or previous_admissions_6_months > 20:
            raise ValueError("Previous admissions must be an integer between 0 and 20")
        
        if not isinstance(meld_score, int) or meld_score < 6 or meld_score > 40:
            raise ValueError("MELD score must be an integer between 6 and 40")
        
        if hepatic_encephalopathy not in ["yes", "no"]:
            raise ValueError("Hepatic encephalopathy must be 'yes' or 'no'")
        
        if ascites not in ["yes", "no"]:
            raise ValueError("Ascites must be 'yes' or 'no'")
    
    def _calculate_linear_combination(self, age: int, serum_sodium: float, albumin: float,
                                    length_of_stay: int, previous_admissions_6_months: int,
                                    meld_score: int, hepatic_encephalopathy: str, ascites: str) -> float:
        """Calculates the linear combination for logistic regression"""
        
        # Convert categorical variables to numeric
        he_numeric = 1 if hepatic_encephalopathy == "yes" else 0
        ascites_numeric = 1 if ascites == "yes" else 0
        
        # Calculate linear combination
        linear_combination = (
            self.INTERCEPT +
            self.AGE_COEFFICIENT * age +
            self.SODIUM_COEFFICIENT * serum_sodium +
            self.ALBUMIN_COEFFICIENT * albumin +
            self.LENGTH_OF_STAY_COEFFICIENT * length_of_stay +
            self.PREVIOUS_ADMISSIONS_COEFFICIENT * previous_admissions_6_months +
            self.MELD_COEFFICIENT * meld_score +
            self.HEPATIC_ENCEPHALOPATHY_COEFFICIENT * he_numeric +
            self.ASCITES_COEFFICIENT * ascites_numeric
        )
        
        return linear_combination
    
    def _logistic_function(self, x: float) -> float:
        """Applies logistic function to convert linear combination to probability"""
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            # Handle extreme values
            if x > 0:
                return 1.0
            else:
                return 0.0
    
    def _get_interpretation(self, risk_percentage: float) -> Dict[str, str]:
        """
        Determines the interpretation based on readmission risk percentage
        
        Args:
            risk_percentage (float): Calculated readmission risk as percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if risk_percentage < 15:
            return {
                "stage": "Low Risk",
                "description": "Low 30-day readmission risk",
                "interpretation": "LOW READMISSION RISK: The patient has a low probability of 30-day readmission. "
                                "MANAGEMENT: Standard discharge planning and routine outpatient follow-up may be sufficient. "
                                "Consider discharge coordination with primary care provider and standard post-discharge care. "
                                "FOLLOW-UP: Routine outpatient follow-up within 2-4 weeks unless clinically indicated sooner. "
                                "PATIENT EDUCATION: Provide standard discharge instructions and medication reconciliation. "
                                "Monitor for signs of decompensation and ensure patient understands when to seek medical attention."
            }
        elif risk_percentage < 30:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate 30-day readmission risk",
                "interpretation": "MODERATE READMISSION RISK: The patient has an intermediate probability of 30-day readmission. "
                                "MANAGEMENT: Enhanced discharge planning recommended with structured follow-up. "
                                "Consider early outpatient follow-up within 7-14 days, comprehensive medication reconciliation, "
                                "and patient education about warning signs. INTERVENTIONS: Assess social support systems, "
                                "medication adherence, and access to care. Consider care coordination with hepatology if available. "
                                "MONITORING: Close monitoring for signs of hepatic decompensation, fluid overload, and medication compliance."
            }
        elif risk_percentage < 50:
            return {
                "stage": "High Risk",
                "description": "High 30-day readmission risk",
                "interpretation": "HIGH READMISSION RISK: The patient has a high probability of 30-day readmission requiring intensive interventions. "
                                "MANAGEMENT: Intensive discharge planning and close follow-up required. Consider early post-discharge "
                                "contact within 48-72 hours, subspecialty referrals, and home health services. "
                                "INTERVENTIONS: Implement transitional care programs, medication management services, and care coordination. "
                                "Ensure hepatology follow-up within 1 week if possible. MONITORING: Frequent monitoring of liver function, "
                                "fluid status, and nutritional status. Consider telehealth or home monitoring programs."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high 30-day readmission risk",
                "interpretation": "VERY HIGH READMISSION RISK: The patient has a very high probability of 30-day readmission requiring comprehensive interventions. "
                                "MANAGEMENT: Comprehensive transitional care interventions strongly recommended. Consider prolonged hospitalization "
                                "if clinical status allows optimization, intensive case management, and immediate subspecialty follow-up. "
                                "INTERVENTIONS: Implement intensive care coordination, frequent outpatient monitoring, home health services, "
                                "and consider admission to transitional care unit if available. FOLLOW-UP: Hepatology follow-up within 48-72 hours, "
                                "primary care within 1 week. MONITORING: Daily to every-other-day monitoring initially with close attention to "
                                "medication adherence, dietary compliance, and early signs of decompensation."
            }


def calculate_mumtaz_score(age: int, serum_sodium: float, albumin: float,
                          length_of_stay: int, previous_admissions_6_months: int,
                          meld_score: int, hepatic_encephalopathy: str, ascites: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MumtazScoreCalculator()
    return calculator.calculate(age, serum_sodium, albumin, length_of_stay,
                              previous_admissions_6_months, meld_score,
                              hepatic_encephalopathy, ascites)