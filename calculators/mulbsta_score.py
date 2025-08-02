"""
MuLBSTA Score for Viral Pneumonia Mortality Calculator

Predicts 90-day mortality risk in patients with viral pneumonia using clinical 
and laboratory parameters to guide treatment decisions and resource allocation.

References:
1. Guo L, et al. Front Microbiol. 2019;10:2752.
2. Chen N, et al. Lancet. 2020;395(10223):507-513.
3. Fan G, et al. Eur Respir J. 2020;56(3):2002113.
"""

from typing import Dict, Any


class MulbstaScoreCalculator:
    """Calculator for MuLBSTA Score for Viral Pneumonia Mortality"""
    
    def __init__(self):
        # MuLBSTA scoring weights
        self.SCORING_WEIGHTS = {
            "multilobar_infiltrates": 5,
            "lymphopenia": 4,
            "bacterial_coinfection": 4,
            "smoking_history": 3,
            "hypertension": 2,
            "age_60_or_older": 2
        }
        
        # Maximum theoretical score is 20, but practical maximum observed is 12
        self.MAX_SCORE = 20
        self.PRACTICAL_MAX = 12
    
    def calculate(self, multilobar_infiltrates: str, lymphopenia: str, 
                  bacterial_coinfection: str, smoking_history: str, 
                  hypertension: str, age_60_or_older: str) -> Dict[str, Any]:
        """
        Calculates the MuLBSTA score for viral pneumonia mortality prediction
        
        Args:
            multilobar_infiltrates (str): Presence of multilobar infiltrates
            lymphopenia (str): Lymphocyte count ≤0.8 × 10⁹/L
            bacterial_coinfection (str): Presence of bacterial coinfection
            smoking_history (str): Current or former smoking history
            hypertension (str): History of hypertension
            age_60_or_older (str): Age 60 years or older
            
        Returns:
            Dict with MuLBSTA score and mortality risk interpretation
        """
        
        # Validate inputs
        self._validate_inputs(multilobar_infiltrates, lymphopenia, bacterial_coinfection,
                             smoking_history, hypertension, age_60_or_older)
        
        # Calculate score
        score = self._calculate_score(multilobar_infiltrates, lymphopenia, 
                                    bacterial_coinfection, smoking_history,
                                    hypertension, age_60_or_older)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, multilobar_infiltrates: str, lymphopenia: str,
                        bacterial_coinfection: str, smoking_history: str,
                        hypertension: str, age_60_or_older: str):
        """Validates input parameters"""
        
        parameters = {
            "multilobar_infiltrates": multilobar_infiltrates,
            "lymphopenia": lymphopenia,
            "bacterial_coinfection": bacterial_coinfection,
            "smoking_history": smoking_history,
            "hypertension": hypertension,
            "age_60_or_older": age_60_or_older
        }
        
        for param_name, param_value in parameters.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_score(self, multilobar_infiltrates: str, lymphopenia: str,
                        bacterial_coinfection: str, smoking_history: str,
                        hypertension: str, age_60_or_older: str) -> int:
        """Calculates the total MuLBSTA score"""
        
        score = 0
        
        # Add points for each positive criterion
        if multilobar_infiltrates == "yes":
            score += self.SCORING_WEIGHTS["multilobar_infiltrates"]
        
        if lymphopenia == "yes":
            score += self.SCORING_WEIGHTS["lymphopenia"]
        
        if bacterial_coinfection == "yes":
            score += self.SCORING_WEIGHTS["bacterial_coinfection"]
        
        if smoking_history == "yes":
            score += self.SCORING_WEIGHTS["smoking_history"]
        
        if hypertension == "yes":
            score += self.SCORING_WEIGHTS["hypertension"]
        
        if age_60_or_older == "yes":
            score += self.SCORING_WEIGHTS["age_60_or_older"]
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides mortality risk interpretation based on MuLBSTA score
        
        Args:
            score (int): MuLBSTA score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 5:
            return {
                "stage": "Low Risk",
                "description": "Low risk of 90-day mortality",
                "interpretation": (f"MuLBSTA Score {score}: Low risk of 90-day mortality (approximately 0-1.7%). "
                                f"This score indicates that the patient has a favorable prognosis with standard "
                                f"supportive care and monitoring. Patients in this category typically have minimal "
                                f"risk factors and can be managed with routine pneumonia care protocols. Standard "
                                f"antivirals if indicated, supportive oxygen therapy as needed, and regular monitoring "
                                f"for clinical deterioration are appropriate. Outpatient management may be considered "
                                f"for stable patients without other high-risk features. Continue to monitor for signs "
                                f"of respiratory deterioration, secondary bacterial infections, and response to treatment. "
                                f"Patient education on symptom monitoring and when to seek medical attention is important. "
                                f"Follow-up within 24-48 hours or sooner if symptoms worsen.")
            }
        elif score <= 11:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk of 90-day mortality",
                "interpretation": (f"MuLBSTA Score {score}: Moderate risk of 90-day mortality (approximately 7.3-26.7%). "
                                f"This score indicates intermediate risk requiring enhanced monitoring and potentially "
                                f"more aggressive supportive care. Consider hospitalization for closer observation, "
                                f"frequent vital sign monitoring, and serial laboratory assessments. Enhanced supportive "
                                f"care may include supplemental oxygen, careful fluid management, and consideration of "
                                f"antiviral therapy if appropriate. Monitor closely for signs of respiratory failure, "
                                f"secondary infections, and other complications. Consider ICU consultation if patient "
                                f"shows signs of deterioration. Implement protocols for early identification of sepsis, "
                                f"ARDS, or other severe complications. Family should be informed of the intermediate "
                                f"risk status and potential for clinical deterioration. Regular reassessment of the "
                                f"score and clinical status is recommended.")
            }
        else:  # score >= 12
            return {
                "stage": "High Risk",
                "description": "High risk of 90-day mortality",
                "interpretation": (f"MuLBSTA Score {score}: High risk of 90-day mortality (approximately 42.9%). "
                                f"This score indicates very high risk requiring intensive monitoring, aggressive "
                                f"treatment, and strongly consider ICU admission. Immediate ICU consultation and "
                                f"potential transfer for intensive care management is recommended. Aggressive supportive "
                                f"care should include mechanical ventilation if indicated, hemodynamic support, "
                                f"broad-spectrum antibiotics for bacterial coinfection, and antiviral therapy if "
                                f"appropriate. Continuous monitoring for multi-organ dysfunction, ARDS, septic shock, "
                                f"and other life-threatening complications. Early involvement of critical care team, "
                                f"infectious disease specialists, and pulmonologists as needed. Family should be "
                                f"informed of the high-risk status and poor prognosis. Consider goals of care "
                                f"discussions and advanced directive planning. Implement all available supportive "
                                f"measures and consider experimental therapies if available and appropriate.")
            }


def calculate_mulbsta_score(multilobar_infiltrates: str, lymphopenia: str,
                           bacterial_coinfection: str, smoking_history: str,
                           hypertension: str, age_60_or_older: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MulbstaScoreCalculator()
    return calculator.calculate(multilobar_infiltrates, lymphopenia, bacterial_coinfection,
                               smoking_history, hypertension, age_60_or_older)