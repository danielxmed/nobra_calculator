"""
Surgical Apgar Score (SAS) Calculator

Predicts postoperative risk of major complications and death in patients 
undergoing major surgery based on intraoperative parameters. The SAS 
provides immediate postoperative risk stratification using three simple 
intraoperative measurements.

References (Vancouver style):
1. Gawande AA, Kwaan MR, Regenbogen SE, Lipsitz SA, Zinner MJ. An Apgar 
   score for surgery. J Am Coll Surg. 2007 Apr;204(2):201-8. 
   doi: 10.1016/j.jamcollsurg.2006.11.011.
2. Regenbogen SE, Lancaster RT, Lipsitz SR, Greenberg CC, Hutter MM, 
   Gawande AA. Does the Surgical Apgar Score measure intraoperative 
   performance? Ann Surg. 2008 Aug;248(2):320-8. 
   doi: 10.1097/SLA.0b013e318181c6d8.
"""

from typing import Dict, Any


class SurgicalApgarScoreCalculator:
    """Calculator for Surgical Apgar Score (SAS)"""
    
    def __init__(self):
        # Scoring tables for each parameter
        self.EBL_SCORES = {
            "≤100 mL": 3,
            "101-600 mL": 2,
            "601-1,000 mL": 1,
            ">1,000 mL": 0
        }
        
        self.MAP_SCORES = {
            "≥70 mmHg": 3,
            "55-69 mmHg": 2,
            "40-54 mmHg": 1,
            "<40 mmHg": 0
        }
        
        self.HEART_RATE_SCORES = {
            "≤55 bpm": 4,
            "56-65 bpm": 3,
            "66-75 bpm": 2,
            "76-85 bpm": 1,
            ">85 bpm": 0
        }
        
        # Risk thresholds
        self.VERY_HIGH_RISK_THRESHOLD = 4  # ≤4 = very high risk
        self.HIGH_RISK_THRESHOLD = 6       # 5-6 = high risk
        # ≥7 = low risk (usual care)
    
    def calculate(self, estimated_blood_loss: str, lowest_mean_arterial_pressure: str,
                  lowest_heart_rate: str) -> Dict[str, Any]:
        """
        Calculates the Surgical Apgar Score using intraoperative parameters
        
        The Surgical Apgar Score (SAS) is analogous to the Virginia Apgar score 
        for newborns, providing a simple numerical assessment of a patient's 
        condition at the end of surgery. It uses three intraoperative parameters 
        to predict postoperative risk of major complications and mortality.
        
        Args:
            estimated_blood_loss (str): Total estimated blood loss during surgery
            lowest_mean_arterial_pressure (str): Lowest MAP recorded during surgery
            lowest_heart_rate (str): Lowest heart rate recorded during surgery
            
        Returns:
            Dict with the calculated score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(estimated_blood_loss, lowest_mean_arterial_pressure, lowest_heart_rate)
        
        # Calculate individual component scores
        ebl_score = self._get_ebl_score(estimated_blood_loss)
        map_score = self._get_map_score(lowest_mean_arterial_pressure)
        hr_score = self._get_heart_rate_score(lowest_heart_rate)
        
        # Calculate total score
        total_score = ebl_score + map_score + hr_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, estimated_blood_loss: str, lowest_mean_arterial_pressure: str,
                        lowest_heart_rate: str):
        """Validates input parameters for the SAS calculation"""
        
        # EBL validation
        if not isinstance(estimated_blood_loss, str):
            raise ValueError("Estimated blood loss must be a string")
        
        if estimated_blood_loss not in self.EBL_SCORES:
            valid_options = list(self.EBL_SCORES.keys())
            raise ValueError(f"Estimated blood loss must be one of: {valid_options}")
        
        # MAP validation
        if not isinstance(lowest_mean_arterial_pressure, str):
            raise ValueError("Lowest mean arterial pressure must be a string")
        
        if lowest_mean_arterial_pressure not in self.MAP_SCORES:
            valid_options = list(self.MAP_SCORES.keys())
            raise ValueError(f"Lowest mean arterial pressure must be one of: {valid_options}")
        
        # Heart rate validation
        if not isinstance(lowest_heart_rate, str):
            raise ValueError("Lowest heart rate must be a string")
        
        if lowest_heart_rate not in self.HEART_RATE_SCORES:
            valid_options = list(self.HEART_RATE_SCORES.keys())
            raise ValueError(f"Lowest heart rate must be one of: {valid_options}")
    
    def _get_ebl_score(self, estimated_blood_loss: str) -> int:
        """Gets the score for estimated blood loss"""
        return self.EBL_SCORES[estimated_blood_loss]
    
    def _get_map_score(self, lowest_mean_arterial_pressure: str) -> int:
        """Gets the score for lowest mean arterial pressure"""
        return self.MAP_SCORES[lowest_mean_arterial_pressure]
    
    def _get_heart_rate_score(self, lowest_heart_rate: str) -> int:
        """Gets the score for lowest heart rate"""
        return self.HEART_RATE_SCORES[lowest_heart_rate]
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the SAS score
        
        Args:
            score (int): Total Surgical Apgar Score (0-10)
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        if score <= self.VERY_HIGH_RISK_THRESHOLD:
            return {
                "stage": "Very High Risk",
                "description": "Very high risk of major complications",
                "interpretation": (
                    f"Surgical Apgar Score of {score} indicates very high risk of major "
                    f"postoperative complications and mortality. Patients with scores ≤4 "
                    f"have a 30-day mortality or major morbidity rate of approximately 58.6%. "
                    f"Consider immediate intensive care unit admission, aggressive perioperative "
                    f"monitoring, and enhanced supportive care. Early recognition and prompt "
                    f"intervention for complications are essential. Close collaboration with "
                    f"critical care specialists and surgical teams is recommended for optimal "
                    f"patient outcomes."
                )
            }
        
        elif score <= self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "High Risk",
                "description": "High risk of major complications",
                "interpretation": (
                    f"Surgical Apgar Score of {score} indicates high risk of major "
                    f"postoperative complications. These patients require enhanced monitoring "
                    f"and close perioperative surveillance. Consider step-down unit or "
                    f"high-dependency care with frequent vital sign monitoring, early "
                    f"mobilization protocols, and proactive management of pain and nausea. "
                    f"Maintain low threshold for ICU transfer if clinical condition "
                    f"deteriorates. Regular assessment for complications and prompt "
                    f"intervention are crucial for preventing adverse outcomes."
                )
            }
        
        else:  # score >= 7
            return {
                "stage": "Low Risk",
                "description": "Low risk - usual care recommended",
                "interpretation": (
                    f"Surgical Apgar Score of {score} indicates low risk of major "
                    f"postoperative complications. Patients with scores of 9-10 have a "
                    f"mortality or major morbidity rate of only 3.6%. Standard postoperative "
                    f"care and monitoring are appropriate. Follow routine recovery protocols "
                    f"with standard vital sign monitoring, pain management, and early "
                    f"mobilization. While the risk is low, continue routine surveillance "
                    f"for potential complications and provide appropriate patient education "
                    f"for postoperative care and warning signs."
                )
            }


def calculate_surgical_apgar_score(estimated_blood_loss: str, lowest_mean_arterial_pressure: str,
                                  lowest_heart_rate: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the Surgical Apgar Score to predict postoperative risk.
    
    Args:
        estimated_blood_loss (str): Total estimated blood loss during surgery
        lowest_mean_arterial_pressure (str): Lowest MAP recorded during surgery
        lowest_heart_rate (str): Lowest heart rate recorded during surgery
        
    Returns:
        Dict with calculated score and clinical interpretation
    """
    calculator = SurgicalApgarScoreCalculator()
    return calculator.calculate(estimated_blood_loss, lowest_mean_arterial_pressure, lowest_heart_rate)