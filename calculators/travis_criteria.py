"""
Travis Criteria Calculator

Predicts risk of needing colectomy with severe ulcerative colitis.
Used on day 3 of treatment for acute severe ulcerative colitis.

References:
1. Travis SP, Farrant JM, Ricketts C, et al. Predicting outcome in severe 
   ulcerative colitis. Gut. 1996;38(6):905-910.
2. Lynch RW, Churchhouse AMD, Protheroe A, Arnott IDR, UK IBD Audit Steering Group. 
   Predicting outcome in acute severe ulcerative colitis: comparison of the Travis 
   and Ho scores using UK IBD audit data. Aliment Pharmacol Ther. 2016;43(11):1132-1141.
"""

from typing import Dict, Any


class TravisCriteriaCalculator:
    """
    Calculator for Travis Criteria
    
    Predicts risk of needing colectomy in patients with severe ulcerative colitis
    based on stool frequency and CRP levels on day 3 of treatment.
    """
    
    def __init__(self):
        # Risk categories
        self.LOW_RISK = "low"
        self.HIGH_RISK = "high"
    
    def calculate(self, stool_frequency: str, crp_elevated: str) -> Dict[str, Any]:
        """
        Calculates the Travis Criteria risk category
        
        Args:
            stool_frequency (str): Number of stools on day 3 ("less_than_3", "3_to_8", "more_than_8")
            crp_elevated (str): Whether CRP >45 mg/L ("yes" or "no")
            
        Returns:
            Dict with risk category and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(stool_frequency, crp_elevated)
        
        # Determine risk category
        risk_category = self._determine_risk(stool_frequency, crp_elevated)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_category)
        
        return {
            "result": risk_category,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, stool_frequency: str, crp_elevated: str):
        """Validates input parameters"""
        
        valid_stool_frequencies = ["less_than_3", "3_to_8", "more_than_8"]
        if stool_frequency not in valid_stool_frequencies:
            raise ValueError(f"Stool frequency must be one of: {', '.join(valid_stool_frequencies)}")
        
        valid_crp_values = ["yes", "no"]
        if crp_elevated not in valid_crp_values:
            raise ValueError(f"CRP elevated must be one of: {', '.join(valid_crp_values)}")
    
    def _determine_risk(self, stool_frequency: str, crp_elevated: str) -> str:
        """
        Determines risk category based on Travis Criteria
        
        High risk if:
        - >8 bowel movements OR
        - 3-8 bowel movements AND CRP >45 mg/L
        
        Args:
            stool_frequency (str): Number of stools
            crp_elevated (str): Whether CRP is elevated
            
        Returns:
            str: Risk category ("low" or "high")
        """
        
        # High risk if >8 bowel movements
        if stool_frequency == "more_than_8":
            return self.HIGH_RISK
        
        # High risk if 3-8 bowel movements AND CRP >45 mg/L
        if stool_frequency == "3_to_8" and crp_elevated == "yes":
            return self.HIGH_RISK
        
        # All other combinations are low risk
        return self.LOW_RISK
    
    def _get_interpretation(self, risk_category: str) -> Dict[str, str]:
        """
        Returns interpretation based on risk category
        
        Args:
            risk_category (str): "low" or "high"
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if risk_category == self.LOW_RISK:
            return {
                "stage": "Low Risk",
                "description": "Low risk of needing colectomy",
                "interpretation": "Patient has low risk of needing colectomy. Continue current medical therapy with close monitoring. Ensure appropriate follow-up and maintenance therapy on discharge."
            }
        else:  # HIGH_RISK
            return {
                "stage": "High Risk",
                "description": "High risk of needing colectomy",
                "interpretation": "Patient has high risk of needing colectomy. Consider early surgical consultation and other therapies including surgery. Intensify medical therapy or consider second-line treatments (cyclosporine, infliximab) if not already initiated."
            }


def calculate_travis_criteria(stool_frequency: str, crp_elevated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TravisCriteriaCalculator()
    return calculator.calculate(stool_frequency, crp_elevated)