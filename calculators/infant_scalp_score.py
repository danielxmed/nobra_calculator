"""
Infant Scalp Score Calculator

Assesses risk of traumatic brain injury in infants with asymptomatic head injury 
and isolated scalp hematoma. The Infant Scalp Score (ISS) is a validated clinical 
tool for infants ≤12 months old to stratify risk for clinically important traumatic 
brain injury (ciTBI) or TBI on CT imaging.

References (Vancouver style):
1. Schutzman SA, Nigrovic LE, Mannix R, et al. The Infant Scalp Score: A Validated 
   Tool to Stratify Risk of Traumatic Brain Injury in Infants With Isolated Scalp 
   Hematoma. Acad Emerg Med. 2021;28(1):16-24. doi: 10.1111/acem.14087.
2. Kuppermann N, Holmes JF, Dayan PS, et al. Identification of children at very low 
   risk of clinically-important brain injuries after head trauma: a prospective 
   cohort study. Lancet. 2009;374(9696):1160-1170. doi: 10.1016/S0140-6736(09)61558-0.
3. Greenberg JK, Jeffe DB, Carpenter CR, et al. North American Survey of the Management 
   of Minor Head Injury in Children. J Trauma Acute Care Surg. 2018;84(4):613-619. 
   doi: 10.1097/TA.0000000000001808.
"""

from typing import Dict, Any


class InfantScalpScoreCalculator:
    """Calculator for Infant Scalp Score (ISS)"""
    
    def __init__(self):
        # ISS scoring weights
        self.scoring_weights = {
            "patient_age_months": {
                "over_12_months": 0,
                "6_to_11_months": 1,
                "3_to_5_months": 2,
                "0_to_2_months": 3
            },
            "hematoma_size": {
                "none": 0,
                "small_barely_palpable": 1,
                "medium_easily_palpable": 2,
                "large_boggy_consistency": 3
            },
            "hematoma_location": {
                "frontal": 0,
                "occipital": 1,
                "temporal_parietal": 2
            }
        }
    
    def calculate(self, patient_age_months: str, hematoma_size: str, 
                 hematoma_location: str) -> Dict[str, Any]:
        """
        Calculates the Infant Scalp Score
        
        Args:
            patient_age_months (str): Patient age in months
            hematoma_size (str): Size and consistency of scalp hematoma
            hematoma_location (str): Anatomical location of scalp hematoma
            
        Returns:
            Dict with the score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(patient_age_months, hematoma_size, hematoma_location)
        
        # Calculate total score
        score = self._calculate_total_score(patient_age_months, hematoma_size, hematoma_location)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, patient_age_months: str, hematoma_size: str, 
                        hematoma_location: str):
        """Validates input parameters"""
        
        # Define valid options for each parameter
        valid_options = {
            "patient_age_months": ["over_12_months", "6_to_11_months", "3_to_5_months", "0_to_2_months"],
            "hematoma_size": ["none", "small_barely_palpable", "medium_easily_palpable", "large_boggy_consistency"],
            "hematoma_location": ["frontal", "occipital", "temporal_parietal"]
        }
        
        # Validate each parameter
        parameters = {
            "patient_age_months": patient_age_months,
            "hematoma_size": hematoma_size,
            "hematoma_location": hematoma_location
        }
        
        for param_name, param_value in parameters.items():
            if param_value not in valid_options[param_name]:
                raise ValueError(f"{param_name} must be one of: {valid_options[param_name]}")
    
    def _calculate_total_score(self, patient_age_months: str, hematoma_size: str, 
                              hematoma_location: str) -> int:
        """
        Calculates the total Infant Scalp Score
        
        ISS Scoring System:
        Age: >12 months (0), 6-11 months (1), 3-5 months (2), 0-2 months (3)
        Size: None (0), Small/barely palpable (1), Medium/easily palpable (2), Large/boggy (3)
        Location: Frontal (0), Occipital (1), Temporal/Parietal (2)
        
        Total score range: 0-8 points
        """
        
        total_score = 0
        
        # Add points for each component
        total_score += self.scoring_weights["patient_age_months"][patient_age_months]
        total_score += self.scoring_weights["hematoma_size"][hematoma_size]
        total_score += self.scoring_weights["hematoma_location"][hematoma_location]
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on Infant Scalp Score
        
        Args:
            score (int): Infant Scalp Score (0-8)
            
        Returns:
            Dict with interpretation details
        """
        
        if score < 4:
            return {
                "stage": "Low Risk",
                "description": f"Score {score} points (0-3 points)",
                "interpretation": "Low risk of traumatic brain injury. Clinical observation may be appropriate. Consider shared decision-making with family regarding CT imaging based on clinical judgment and family concerns."
            }
        else:  # score >= 4
            return {
                "stage": "High Risk",
                "description": f"Score {score} points (4-8 points)",
                "interpretation": "High risk of traumatic brain injury. Strong consideration for cranial CT imaging to evaluate for clinically important traumatic brain injury or TBI."
            }


def calculate_infant_scalp_score(patient_age_months: str, hematoma_size: str, 
                               hematoma_location: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = InfantScalpScoreCalculator()
    return calculator.calculate(patient_age_months, hematoma_size, hematoma_location)