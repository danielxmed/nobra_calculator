"""
Emergency Department Assessment of Chest Pain Score (EDACS) Calculator

Risk stratifies chest pain patients for early discharge based on clinical factors.
EDACS is used to identify low-risk patients who can be safely discharged from
the emergency department when combined with no new ischemia on ECG and negative
troponins at 0 and 2 hours.

References:
1. Than M, Flaws D, Sanders S, Doust J, Glasziou P, Kline J, et al. Development 
   and validation of the Emergency Department Assessment of Chest pain Score and 
   2 h accelerated diagnostic protocol. Emerg Med Australas. 2014;26(1):34-44.
2. Than M, Cullen L, Aldous S, Parsonage WA, Reid CM, Greenslade J, et al. 
   2-Hour accelerated diagnostic protocol to assess patients with chest pain 
   symptoms using contemporary troponins as the only biomarker: the ADAPT-ADP. 
   J Am Coll Cardiol. 2012;59(23):2091-8.
"""

from typing import Dict, Any


class EmergencyDepartmentAssessmentChestPainEdacsCalculator:
    """Calculator for Emergency Department Assessment of Chest Pain Score (EDACS)"""
    
    def __init__(self):
        # Age-based point assignments
        self.AGE_POINTS = {
            range(18, 46): 2,   # 18-45 years
            range(46, 51): 4,   # 46-50 years
            range(51, 56): 6,   # 51-55 years
            range(56, 61): 8,   # 56-60 years
            range(61, 66): 10,  # 61-65 years
            range(66, 71): 12,  # 66-70 years
            range(71, 76): 14,  # 71-75 years
            range(76, 81): 16,  # 76-80 years
            range(81, 86): 18,  # 81-85 years
        }
        
        # Other scoring constants
        self.MALE_POINTS = 6
        self.RISK_FACTOR_POINTS = 4  # For ages 18-50 only
        self.DIAPHORESIS_POINTS = 3
        self.PAIN_RADIATES_POINTS = 5
        self.INSPIRATION_POINTS = -4  # Negative points
        self.PALPATION_POINTS = -6    # Negative points
        
        # Risk threshold
        self.LOW_RISK_THRESHOLD = 15  # <16 is low risk
    
    def calculate(self, age: int, sex: str, known_cad_or_risk_factors: str,
                  diaphoresis: str, pain_radiates: str, pain_with_inspiration: str,
                  pain_reproduced_by_palpation: str) -> Dict[str, Any]:
        """
        Calculates the EDACS score using the provided parameters
        
        Args:
            age (int): Patient age in years (18-120)
            sex (str): Patient sex ("Male" or "Female")
            known_cad_or_risk_factors (str): Known CAD or ≥3 risk factors for ages 18-50
            diaphoresis (str): Presence of diaphoresis ("Yes" or "No")
            pain_radiates (str): Pain radiates to arm/shoulder/neck/jaw ("Yes" or "No")
            pain_with_inspiration (str): Pain with inspiration ("Yes" or "No")
            pain_reproduced_by_palpation (str): Pain reproduced by palpation ("Yes" or "No")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, sex, known_cad_or_risk_factors, diaphoresis,
                            pain_radiates, pain_with_inspiration, pain_reproduced_by_palpation)
        
        # Calculate total score
        total_score = self._calculate_edacs_score(
            age, sex, known_cad_or_risk_factors, diaphoresis,
            pain_radiates, pain_with_inspiration, pain_reproduced_by_palpation
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, sex, known_cad_or_risk_factors, diaphoresis,
                        pain_radiates, pain_with_inspiration, pain_reproduced_by_palpation):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120 years")
        
        if sex not in ["Male", "Female"]:
            raise ValueError("Sex must be 'Male' or 'Female'")
        
        if known_cad_or_risk_factors not in ["Yes", "No", "Not applicable (age >50)"]:
            raise ValueError("Known CAD or risk factors must be 'Yes', 'No', or 'Not applicable (age >50)'")
        
        if diaphoresis not in ["Yes", "No"]:
            raise ValueError("Diaphoresis must be 'Yes' or 'No'")
        
        if pain_radiates not in ["Yes", "No"]:
            raise ValueError("Pain radiates must be 'Yes' or 'No'")
        
        if pain_with_inspiration not in ["Yes", "No"]:
            raise ValueError("Pain with inspiration must be 'Yes' or 'No'")
        
        if pain_reproduced_by_palpation not in ["Yes", "No"]:
            raise ValueError("Pain reproduced by palpation must be 'Yes' or 'No'")
        
        # Validate age-risk factor consistency
        if age <= 50 and known_cad_or_risk_factors == "Not applicable (age >50)":
            raise ValueError("For patients aged 18-50, known CAD or risk factors must be specified as 'Yes' or 'No'")
        
        if age > 50 and known_cad_or_risk_factors in ["Yes", "No"]:
            raise ValueError("For patients aged >50, known CAD or risk factors should be 'Not applicable (age >50)'")
    
    def _calculate_edacs_score(self, age, sex, known_cad_or_risk_factors, diaphoresis,
                              pain_radiates, pain_with_inspiration, pain_reproduced_by_palpation):
        """Calculates the EDACS score based on all parameters"""
        
        total_score = 0
        
        # Age points
        age_points = self._get_age_points(age)
        total_score += age_points
        
        # Sex points
        if sex == "Male":
            total_score += self.MALE_POINTS
        
        # Risk factors (only for ages 18-50)
        if age <= 50 and known_cad_or_risk_factors == "Yes":
            total_score += self.RISK_FACTOR_POINTS
        
        # Clinical symptoms and signs
        if diaphoresis == "Yes":
            total_score += self.DIAPHORESIS_POINTS
        
        if pain_radiates == "Yes":
            total_score += self.PAIN_RADIATES_POINTS
        
        if pain_with_inspiration == "Yes":
            total_score += self.INSPIRATION_POINTS  # Negative points
        
        if pain_reproduced_by_palpation == "Yes":
            total_score += self.PALPATION_POINTS    # Negative points
        
        return total_score
    
    def _get_age_points(self, age: int) -> int:
        """Determines age-based points"""
        
        # Handle ages ≥86
        if age >= 86:
            return 20
        
        # Check age ranges
        for age_range, points in self.AGE_POINTS.items():
            if age in age_range:
                return points
        
        # This should not happen with proper validation
        raise ValueError(f"Unable to determine age points for age {age}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the EDACS score
        
        Args:
            score (int): Calculated EDACS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "EDACS <16 indicates low risk",
                "interpretation": "Low risk for major adverse cardiac events (MACE). When combined with no new ischemia on ECG and negative troponins at 0 and 2 hours, patients may be considered for early discharge. The EDACS-Accelerated Diagnostic Protocol (EDACS-ADP) is >99% sensitive for 30-day MACE when all criteria are met. Patients should still receive appropriate follow-up and instruction for return if symptoms worsen."
            }
        else:
            return {
                "stage": "Higher Risk",
                "description": "EDACS ≥16 indicates higher risk",
                "interpretation": "Higher risk for major adverse cardiac events (MACE). Patients require further evaluation including serial troponins, stress testing, or coronary imaging as clinically indicated. Do not use accelerated discharge protocols. Consider admission or extended observation with cardiology consultation. Additional risk stratification and definitive cardiac evaluation recommended."
            }


def calculate_emergency_department_assessment_chest_pain_edacs(
    age: int, sex: str, known_cad_or_risk_factors: str, diaphoresis: str,
    pain_radiates: str, pain_with_inspiration: str, pain_reproduced_by_palpation: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_emergency_department_assessment_chest_pain_edacs pattern
    """
    calculator = EmergencyDepartmentAssessmentChestPainEdacsCalculator()
    return calculator.calculate(age, sex, known_cad_or_risk_factors, diaphoresis,
                               pain_radiates, pain_with_inspiration, pain_reproduced_by_palpation)