"""
Abbreviated Injury Score (AIS) for Inhalation Injury Calculator

Classifies inhalation injury severity based on bronchoscopic findings in adult patients 
with suspected inhalation injury undergoing flexible bronchoscopy.

Reference: Endorf FW, Gamelli RL. Inhalation injury, pulmonary perturbations, 
and fluid resuscitation. J Burn Care Res. 2007;28(1):80-83.
"""

from typing import Dict, Any


class AisInhalationInjuryCalculator:
    """Calculator for Abbreviated Injury Score (AIS) for Inhalation Injury"""
    
    def __init__(self):
        self.GRADE_MAPPING = {
            "grade_0": 0,
            "grade_1": 1, 
            "grade_2": 2,
            "grade_3": 3,
            "grade_4": 4
        }
    
    def calculate(self, bronchoscopic_findings: str) -> Dict[str, Any]:
        """
        Calculates the AIS score based on bronchoscopic findings
        
        Args:
            bronchoscopic_findings (str): Grade of bronchoscopic findings (grade_0 to grade_4)
            
        Returns:
            Dict with the result and interpretation
        """
        
        self._validate_inputs(bronchoscopic_findings)
        
        score = self._calculate_score(bronchoscopic_findings)
        
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bronchoscopic_findings: str):
        """Validates input parameters"""
        
        if not isinstance(bronchoscopic_findings, str):
            raise ValueError("Bronchoscopic findings must be a string")
        
        if bronchoscopic_findings not in self.GRADE_MAPPING:
            raise ValueError(f"Bronchoscopic findings must be one of: {list(self.GRADE_MAPPING.keys())}")
    
    def _calculate_score(self, bronchoscopic_findings: str) -> int:
        """Calculates the AIS score based on bronchoscopic findings"""
        
        return self.GRADE_MAPPING[bronchoscopic_findings]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the AIS score
        
        Args:
            score (int): AIS score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "Grade 0",
                "description": "No inhalation injury",
                "interpretation": "No carbonaceous deposits, erythema, edema, bronchorrhea, or obstruction. Normal bronchoscopic findings."
            }
        elif score == 1:
            return {
                "stage": "Grade 1",
                "description": "Mild inhalation injury",
                "interpretation": "Minor or patchy areas of erythema, carbonaceous deposits, bronchorrhea, or bronchial obstruction present. Minimal inhalation injury with generally good prognosis."
            }
        elif score == 2:
            return {
                "stage": "Grade 2", 
                "description": "Moderate inhalation injury",
                "interpretation": "Moderate erythema, carbonaceous deposits, bronchorrhea, or bronchial obstruction present. Moderate inhalation injury requiring close monitoring and supportive care."
            }
        elif score == 3:
            return {
                "stage": "Grade 3",
                "description": "Severe inhalation injury", 
                "interpretation": "Severe inflammation with friability, copious carbonaceous deposits, bronchorrhea, or obstruction present. Severe inhalation injury with increased risk of ARDS, prolonged mechanical ventilation, and ICU stay."
            }
        elif score == 4:
            return {
                "stage": "Grade 4",
                "description": "Very severe inhalation injury",
                "interpretation": "Mucosal sloughing, necrosis, or endoluminal obstruction present. Very severe inhalation injury with high morbidity and mortality risk requiring intensive support and possible referral to burn center."
            }
        else:
            raise ValueError(f"Invalid score: {score}. Score must be between 0 and 4.")


def calculate_ais_inhalation_injury(bronchoscopic_findings: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AisInhalationInjuryCalculator()
    return calculator.calculate(bronchoscopic_findings)