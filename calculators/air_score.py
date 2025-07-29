"""
Appendicitis Inflammatory Response (AIR) Score Calculator

Diagnoses appendicitis based on clinical and laboratory findings using objective
inflammatory variables and clinical signs of peritoneal irritation.

References (Vancouver style):
1. Andersson M, Andersson RE. The appendicitis inflammatory response score: 
   a tool for the diagnosis of acute appendicitis that outperforms the Alvarado score. 
   World J Surg. 2008;32(8):1843-9.
2. Sammalkorpi HE, Mentula P, Leppäniemi A. A new adult appendicitis score improves 
   diagnostic accuracy of acute appendicitis—a prospective study. BMC Gastroenterol. 
   2014;14:114.
3. Scott AJ, Mason SE, Arunakirinathan M, et al. Risk stratification by the 
   Appendicitis Inflammatory Response score to guide decision-making in patients 
   with suspected appendicitis. Br J Surg. 2015;102(5):563-72.

The AIR Score uses seven clinical and laboratory variables to assess appendicitis 
probability. It is designed with high sensitivity for advanced appendicitis, which 
is most clinically important to identify. The score performs well across age groups 
from 2-96 years and is particularly effective in children and women.
"""

from typing import Dict, Any


class AirScoreCalculator:
    """Calculator for Appendicitis Inflammatory Response (AIR) Score"""
    
    def __init__(self):
        # Score mapping for each parameter
        self.vomiting_scores = {"no": 0, "yes": 1}
        self.rif_pain_scores = {"no": 0, "yes": 1}
        self.rebound_tenderness_scores = {"none": 0, "light": 1, "medium": 2, "strong": 3}
        self.fever_scores = {"no": 0, "yes": 1}
        self.polymorphonuclear_scores = {"under_70": 0, "70_to_84": 1, "85_or_over": 2}
        self.wbc_scores = {"under_10": 0, "10_to_14_9": 1, "15_or_over": 2}
        self.crp_scores = {"under_10": 0, "10_to_49": 1, "50_or_over": 2}
    
    def calculate(self, vomiting: str, rif_pain: str, rebound_tenderness: str, 
                 fever: str, polymorphonuclear_percentage: str, wbc_count: str, 
                 crp_level: str) -> Dict[str, Any]:
        """
        Calculates the AIR Score using the provided clinical and laboratory parameters
        
        Args:
            vomiting (str): Presence of vomiting ("no" or "yes")
            rif_pain (str): Right iliac fossa pain ("no" or "yes")
            rebound_tenderness (str): Rebound tenderness intensity ("none", "light", "medium", "strong")
            fever (str): Temperature ≥38.5°C/101.3°F ("no" or "yes")
            polymorphonuclear_percentage (str): Neutrophil percentage ("under_70", "70_to_84", "85_or_over")
            wbc_count (str): WBC count ×10⁹/L ("under_10", "10_to_14_9", "15_or_over")
            crp_level (str): CRP level mg/L ("under_10", "10_to_49", "50_or_over")
            
        Returns:
            Dict with the AIR score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(vomiting, rif_pain, rebound_tenderness, fever, 
                            polymorphonuclear_percentage, wbc_count, crp_level)
        
        # Calculate total score
        score = self._calculate_total_score(vomiting, rif_pain, rebound_tenderness, 
                                          fever, polymorphonuclear_percentage, 
                                          wbc_count, crp_level)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, vomiting: str, rif_pain: str, rebound_tenderness: str, 
                        fever: str, polymorphonuclear_percentage: str, wbc_count: str, 
                        crp_level: str):
        """Validates all input parameters"""
        
        if vomiting not in self.vomiting_scores:
            raise ValueError(f"Vomiting must be 'no' or 'yes', got '{vomiting}'")
        
        if rif_pain not in self.rif_pain_scores:
            raise ValueError(f"RIF pain must be 'no' or 'yes', got '{rif_pain}'")
        
        if rebound_tenderness not in self.rebound_tenderness_scores:
            raise ValueError(f"Rebound tenderness must be 'none', 'light', 'medium', or 'strong', got '{rebound_tenderness}'")
        
        if fever not in self.fever_scores:
            raise ValueError(f"Fever must be 'no' or 'yes', got '{fever}'")
        
        if polymorphonuclear_percentage not in self.polymorphonuclear_scores:
            raise ValueError(f"Polymorphonuclear percentage must be 'under_70', '70_to_84', or '85_or_over', got '{polymorphonuclear_percentage}'")
        
        if wbc_count not in self.wbc_scores:
            raise ValueError(f"WBC count must be 'under_10', '10_to_14_9', or '15_or_over', got '{wbc_count}'")
        
        if crp_level not in self.crp_scores:
            raise ValueError(f"CRP level must be 'under_10', '10_to_49', or '50_or_over', got '{crp_level}'")
    
    def _calculate_total_score(self, vomiting: str, rif_pain: str, rebound_tenderness: str, 
                             fever: str, polymorphonuclear_percentage: str, wbc_count: str, 
                             crp_level: str) -> int:
        """Calculates the total AIR Score"""
        
        total_score = (
            self.vomiting_scores[vomiting] +
            self.rif_pain_scores[rif_pain] +
            self.rebound_tenderness_scores[rebound_tenderness] +
            self.fever_scores[fever] +
            self.polymorphonuclear_scores[polymorphonuclear_percentage] +
            self.wbc_scores[wbc_count] +
            self.crp_scores[crp_level]
        )
        
        return total_score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the AIR Score
        
        Args:
            score (int): Calculated AIR Score (0-12)
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 4:
            return {
                "stage": "Low Risk",
                "description": "Low probability of appendicitis",
                "interpretation": "Outpatient follow-up if unaltered general condition. Consider other diagnoses. Can be discharged with planned reexamination if clinically stable."
            }
        elif score <= 8:
            return {
                "stage": "Indeterminate Risk",
                "description": "Intermediate probability of appendicitis",
                "interpretation": "Admit patient for observation and serial reassessment. Consider rescoring after 4-8 hours of observation. May require imaging studies or surgical consultation."
            }
        else:  # score >= 9
            return {
                "stage": "High Risk",
                "description": "High probability of appendicitis",
                "interpretation": "High suspicion for appendicitis. Surgical consultation recommended. Consider immediate surgical intervention, especially in patients with advanced appendicitis."
            }


def calculate_air_score(vomiting: str, rif_pain: str, rebound_tenderness: str, 
                       fever: str, polymorphonuclear_percentage: str, wbc_count: str, 
                       crp_level: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AirScoreCalculator()
    return calculator.calculate(vomiting, rif_pain, rebound_tenderness, fever, 
                              polymorphonuclear_percentage, wbc_count, crp_level)
