"""
NAFLD (Non-Alcoholic Fatty Liver Disease) Activity Score Calculator

Diagnoses steatohepatitis based on histological findings in NAFLD patients.
The NAS evaluates disease activity by scoring three histological features:
steatosis, lobular inflammation, and hepatocellular ballooning.

References:
1. Kleiner DE, Brunt EM, Van Natta M, et al. Design and validation of a histological 
   scoring system for nonalcoholic fatty liver disease. Hepatology. 2005;41(6):1313-21.
2. Brunt EM, Kleiner DE, Wilson LA, et al. Nonalcoholic fatty liver disease (NAFLD) 
   activity score and the histopathologic diagnosis in NAFLD: distinct clinicopathologic 
   meanings. Hepatology. 2011;53(3):810-20.
"""

from typing import Dict, Any


class NafldActivityScoreCalculator:
    """Calculator for NAFLD Activity Score"""
    
    def __init__(self):
        # Scoring maps for each component
        self.steatosis_scores = {
            "<5%": 0,
            "5-33%": 1,
            "34-66%": 2,
            ">66%": 3
        }
        
        self.inflammation_scores = {
            "No foci": 0,
            "1 focus per 200× field": 1,
            "2-4 foci per 200× field": 2,
            ">4 foci per 200× field": 3
        }
        
        self.ballooning_scores = {
            "None": 0,
            "Few balloon cells": 1,
            "Many cells/prominent ballooning": 2
        }
    
    def calculate(self, steatosis: str, lobular_inflammation: str, ballooning: str) -> Dict[str, Any]:
        """
        Calculates the NAFLD Activity Score using histological parameters
        
        Args:
            steatosis (str): Percentage of hepatocytes with fat droplets
            lobular_inflammation (str): Number of inflammatory foci per 200× field
            ballooning (str): Degree of hepatocellular ballooning
            
        Returns:
            Dict with the NAS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(steatosis, lobular_inflammation, ballooning)
        
        # Calculate component scores
        steatosis_score = self.steatosis_scores[steatosis]
        inflammation_score = self.inflammation_scores[lobular_inflammation]
        ballooning_score = self.ballooning_scores[ballooning]
        
        # Calculate total NAS
        total_score = steatosis_score + inflammation_score + ballooning_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_scores": {
                "steatosis": steatosis_score,
                "lobular_inflammation": inflammation_score,
                "ballooning": ballooning_score
            }
        }
    
    def _validate_inputs(self, steatosis: str, lobular_inflammation: str, ballooning: str):
        """Validates input parameters"""
        
        if steatosis not in self.steatosis_scores:
            raise ValueError(f"Invalid steatosis value. Must be one of: {list(self.steatosis_scores.keys())}")
        
        if lobular_inflammation not in self.inflammation_scores:
            raise ValueError(f"Invalid lobular inflammation value. Must be one of: {list(self.inflammation_scores.keys())}")
        
        if ballooning not in self.ballooning_scores:
            raise ValueError(f"Invalid ballooning value. Must be one of: {list(self.ballooning_scores.keys())}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the NAS score
        
        Args:
            score (int): Total NAS score (0-8)
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "No activity",
                "description": "No NAFLD activity",
                "interpretation": "Score of 0 indicates no evidence of NAFLD activity. No steatosis, inflammation, or hepatocellular ballooning present."
            }
        elif score <= 2:
            return {
                "stage": "Mild activity",
                "description": "Mild NAFLD activity",
                "interpretation": "NAS of 1-2 indicates mild NAFLD activity. Generally correlated with 'not NASH' diagnosis. Close monitoring recommended."
            }
        elif score <= 5:
            return {
                "stage": "Moderate activity",
                "description": "Moderate NAFLD activity",
                "interpretation": "NAS of 3-5 indicates moderate NAFLD activity. Scores ≥4 have optimal sensitivity and specificity for predicting steatohepatitis. NAS ≥5 strongly correlates with 'definite NASH' diagnosis."
            }
        else:  # score 6-8
            return {
                "stage": "Marked activity",
                "description": "Marked NAFLD activity",
                "interpretation": "NAS of 6-8 indicates marked NAFLD activity. Strongly correlates with definite NASH diagnosis. Consider therapeutic intervention and close monitoring."
            }


def calculate_nafld_activity_score(steatosis: str, lobular_inflammation: str, ballooning: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NafldActivityScoreCalculator()
    return calculator.calculate(steatosis, lobular_inflammation, ballooning)