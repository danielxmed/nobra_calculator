"""
Ho Index Calculator

Predicts outcome of medical therapy in severe ulcerative colitis by assessing 
risk of failure of corticosteroid therapy.

References:
- Ho GT, et al. Aliment Pharmacol Ther. 2004;19(10):1079-87.
- Lynch RW, et al. Aliment Pharmacol Ther. 2016;43(11):1132-41.
"""

from typing import Dict, Any


class HoIndexCalculator:
    """Calculator for Ho Index for Ulcerative Colitis"""
    
    def __init__(self):
        # Stool frequency scoring
        self.stool_frequency_points = {
            "4_or_less": 0,        # ≤4 stools/24h
            "over_4_to_6": 1,      # >4 to ≤6 stools/24h  
            "over_6_to_9": 2,      # >6 to ≤9 stools/24h
            "over_9": 4            # >9 stools/24h
        }
        
        # Colonic dilatation scoring
        self.colonic_dilatation_points = {
            "absent": 0,
            "present": 4           # ≥5.5cm on abdominal X-ray
        }
        
        # Hypoalbuminemia scoring
        self.hypoalbuminemia_points = {
            "no": 0,
            "yes": 1               # Albumin ≤3 g/dL or ≤30 g/L
        }
    
    def calculate(self, mean_stool_frequency: str, colonic_dilatation: str,
                  hypoalbuminemia: str) -> Dict[str, Any]:
        """
        Calculates the Ho Index score for severe ulcerative colitis
        
        Args:
            mean_stool_frequency (str): Mean stools per 24h category
            colonic_dilatation (str): Presence of colonic dilatation
            hypoalbuminemia (str): Presence of hypoalbuminemia
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(mean_stool_frequency, colonic_dilatation, hypoalbuminemia)
        
        # Calculate score
        score = (self.stool_frequency_points[mean_stool_frequency] +
                self.colonic_dilatation_points[colonic_dilatation] +
                self.hypoalbuminemia_points[hypoalbuminemia])
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, mean_stool_frequency: str, colonic_dilatation: str,
                        hypoalbuminemia: str):
        """Validates input parameters"""
        
        if mean_stool_frequency not in self.stool_frequency_points:
            raise ValueError(f"Invalid mean_stool_frequency: {mean_stool_frequency}")
        
        if colonic_dilatation not in self.colonic_dilatation_points:
            raise ValueError(f"Invalid colonic_dilatation: {colonic_dilatation}")
        
        if hypoalbuminemia not in self.hypoalbuminemia_points:
            raise ValueError(f"Invalid hypoalbuminemia: {hypoalbuminemia}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the Ho Index score
        
        Args:
            score (int): Calculated Ho Index score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Score 0-1",
                "interpretation": "Low risk of medical therapy failure (11%). Continue current "
                                "corticosteroid therapy with close monitoring. Good response to "
                                "medical management expected."
            }
        elif score <= 3:
            return {
                "stage": "Intermediate Risk",
                "description": "Score 2-3",
                "interpretation": "Intermediate risk of medical therapy failure (45%). Consider "
                                "early assessment for second-line medical therapy (e.g., infliximab, "
                                "cyclosporine). Close monitoring required with low threshold for escalation."
            }
        else:  # score >= 4
            return {
                "stage": "High Risk",
                "description": "Score ≥4",
                "interpretation": "High risk of medical therapy failure (85%). Strong consideration "
                                "for immediate second-line medical therapy or surgical consultation. "
                                "Early multidisciplinary team involvement recommended."
            }


def calculate_ho_index(mean_stool_frequency: str, colonic_dilatation: str,
                      hypoalbuminemia: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HoIndexCalculator()
    return calculator.calculate(mean_stool_frequency, colonic_dilatation, hypoalbuminemia)