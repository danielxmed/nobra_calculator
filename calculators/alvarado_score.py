"""
Alvarado Score for Acute Appendicitis Calculator

Predicts likelihood of acute appendicitis based on clinical symptoms, signs, and laboratory findings.
Uses the MANTRELS mnemonic (Migration, Anorexia, Nausea/vomiting, Tenderness, Rebound, 
Elevated temperature, Leukocytosis, Left Shift) to assess 8 clinical factors.

References:
- Alvarado A. A practical score for the early diagnosis of acute appendicitis. Ann Emerg Med. 1986;15(5):557-64.
- Alvarado A. How to improve the clinical diagnosis of acute appendicitis in resource limited settings. World J Emerg Surg. 2016;11:16.
"""

from typing import Dict, Any


class AlvaradoScoreCalculator:
    """Calculator for Alvarado Score for Acute Appendicitis"""
    
    def __init__(self):
        # MANTRELS scoring weights
        self.MIGRATION_POINTS = 1
        self.ANOREXIA_POINTS = 1
        self.NAUSEA_VOMITING_POINTS = 1
        self.TENDERNESS_RLQ_POINTS = 2  # Most important factor
        self.REBOUND_TENDERNESS_POINTS = 1
        self.ELEVATED_TEMPERATURE_POINTS = 1
        self.LEUKOCYTOSIS_POINTS = 2  # Most important factor
        self.NEUTROPHIL_LEFT_SHIFT_POINTS = 1
    
    def calculate(self, migration_to_rlq: str, anorexia: str, nausea_vomiting: str,
                 tenderness_rlq: str, rebound_tenderness: str, elevated_temperature: str,
                 leukocytosis: str, neutrophil_left_shift: str) -> Dict[str, Any]:
        """
        Calculates the Alvarado Score using the MANTRELS criteria
        
        Args:
            migration_to_rlq (str): Migration of pain to right lower quadrant ("yes"/"no")
            anorexia (str): Anorexia/loss of appetite ("yes"/"no")
            nausea_vomiting (str): Nausea or vomiting ("yes"/"no")
            tenderness_rlq (str): Tenderness in right lower quadrant ("yes"/"no")
            rebound_tenderness (str): Rebound tenderness or indirect signs ("yes"/"no")
            elevated_temperature (str): Fever >37.3°C/99.1°F ("yes"/"no")
            leukocytosis (str): WBC count >10,000/μL ("yes"/"no")
            neutrophil_left_shift (str): >75% neutrophils ("yes"/"no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(migration_to_rlq, anorexia, nausea_vomiting, tenderness_rlq,
                            rebound_tenderness, elevated_temperature, leukocytosis, neutrophil_left_shift)
        
        # Calculate score
        score = self._calculate_alvarado_score(
            migration_to_rlq, anorexia, nausea_vomiting, tenderness_rlq,
            rebound_tenderness, elevated_temperature, leukocytosis, neutrophil_left_shift
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, migration_to_rlq, anorexia, nausea_vomiting, tenderness_rlq,
                        rebound_tenderness, elevated_temperature, leukocytosis, neutrophil_left_shift):
        """Validates input parameters"""
        
        parameters = [
            ("migration_to_rlq", migration_to_rlq),
            ("anorexia", anorexia),
            ("nausea_vomiting", nausea_vomiting),
            ("tenderness_rlq", tenderness_rlq),
            ("rebound_tenderness", rebound_tenderness),
            ("elevated_temperature", elevated_temperature),
            ("leukocytosis", leukocytosis),
            ("neutrophil_left_shift", neutrophil_left_shift)
        ]
        
        for param_name, param_value in parameters:
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_alvarado_score(self, migration_to_rlq, anorexia, nausea_vomiting, tenderness_rlq,
                                 rebound_tenderness, elevated_temperature, leukocytosis, neutrophil_left_shift) -> int:
        """Calculates the Alvarado score using MANTRELS criteria"""
        
        score = 0
        
        # M - Migration of pain to RLQ (1 point)
        if migration_to_rlq == "yes":
            score += self.MIGRATION_POINTS
        
        # A - Anorexia (1 point)
        if anorexia == "yes":
            score += self.ANOREXIA_POINTS
        
        # N - Nausea/vomiting (1 point)
        if nausea_vomiting == "yes":
            score += self.NAUSEA_VOMITING_POINTS
        
        # T - Tenderness in RLQ (2 points - most important)
        if tenderness_rlq == "yes":
            score += self.TENDERNESS_RLQ_POINTS
        
        # R - Rebound tenderness (1 point)
        if rebound_tenderness == "yes":
            score += self.REBOUND_TENDERNESS_POINTS
        
        # E - Elevated temperature/fever (1 point)
        if elevated_temperature == "yes":
            score += self.ELEVATED_TEMPERATURE_POINTS
        
        # L - Leukocytosis (2 points - most important)
        if leukocytosis == "yes":
            score += self.LEUKOCYTOSIS_POINTS
        
        # S - Left shift of neutrophils (1 point)
        if neutrophil_left_shift == "yes":
            score += self.NEUTROPHIL_LEFT_SHIFT_POINTS
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the Alvarado score
        
        Args:
            score (int): Calculated Alvarado score (0-10)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low Risk",
                "description": "Low probability of appendicitis",
                "interpretation": "Low probability of appendicitis (1-6% risk). Consider discharge with close follow-up. No further imaging typically needed."
            }
        elif score <= 6:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate probability of appendicitis",
                "interpretation": "Intermediate probability of appendicitis (15-25% risk). Consider observation, serial exams, or imaging (CT scan). Surgical consultation may be warranted."
            }
        elif score <= 8:
            return {
                "stage": "High Risk",
                "description": "High probability of appendicitis",
                "interpretation": "High probability of appendicitis (75-85% risk). Strong indication for surgical consultation and likely appendectomy. Consider expedited surgical evaluation."
            }
        else:  # score 9-10
            return {
                "stage": "Very High Risk",
                "description": "Very high probability of appendicitis",
                "interpretation": "Very high probability of appendicitis (>90% risk). Very strong indication for immediate surgical consultation and appendectomy. Imaging may delay necessary surgery."
            }


def calculate_alvarado_score(migration_to_rlq, anorexia, nausea_vomiting, tenderness_rlq,
                           rebound_tenderness, elevated_temperature, leukocytosis, neutrophil_left_shift) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_alvarado_score pattern
    """
    calculator = AlvaradoScoreCalculator()
    return calculator.calculate(migration_to_rlq, anorexia, nausea_vomiting, tenderness_rlq,
                              rebound_tenderness, elevated_temperature, leukocytosis, neutrophil_left_shift)