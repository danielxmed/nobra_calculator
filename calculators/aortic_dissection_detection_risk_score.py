"""
Aortic Dissection Detection Risk Score (ADD-RS) Calculator

A guideline-based tool for identification of acute aortic dissection at initial presentation.
Developed from analysis of the International Registry of Acute Aortic Dissection (IRAD).

References:
- Rogers AM, et al. Circulation. 2011;123(20):2213-2218. doi: 10.1161/CIRCULATIONAHA.110.988568
- 2010 ACCF/AHA/AATS thoracic aortic disease guidelines
"""

from typing import Dict, Any


class AorticDissectionDetectionRiskScoreCalculator:
    """Calculator for Aortic Dissection Detection Risk Score (ADD-RS)"""
    
    def __init__(self):
        # Risk categories and their criteria
        self.PREDISPOSING_CONDITIONS = [
            "Marfan syndrome",
            "Family history of aortic disease", 
            "Known aortic valve disease",
            "Recent aortic manipulation",
            "Known thoracic aortic aneurysm"
        ]
        
        self.PAIN_FEATURES = [
            "Abrupt onset of pain",
            "Severe pain intensity", 
            "Ripping or tearing pain quality"
        ]
        
        self.EXAMINATION_FEATURES = [
            "Pulse deficit or systolic BP differential between extremities",
            "Focal neurological deficit (in conjunction with pain)",
            "New murmur of aortic insufficiency (in conjunction with pain)",
            "Hypotension or shock state"
        ]
    
    def calculate(self, predisposing_conditions: str, pain_features: str, examination_features: str) -> Dict[str, Any]:
        """
        Calculates the ADD-RS score using the provided clinical assessment
        
        Args:
            predisposing_conditions (str): Presence of high-risk predisposing conditions ("none" or "present")
            pain_features (str): Presence of high-risk pain features ("none" or "present") 
            examination_features (str): Presence of high-risk examination features ("none" or "present")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(predisposing_conditions, pain_features, examination_features)
        
        # Calculate ADD-RS score
        score = self._calculate_score(predisposing_conditions, pain_features, examination_features)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, predisposing_conditions: str, pain_features: str, examination_features: str):
        """Validates input parameters"""
        
        valid_values = ["none", "present"]
        
        if predisposing_conditions not in valid_values:
            raise ValueError(f"predisposing_conditions must be one of: {valid_values}")
        
        if pain_features not in valid_values:
            raise ValueError(f"pain_features must be one of: {valid_values}")
            
        if examination_features not in valid_values:
            raise ValueError(f"examination_features must be one of: {valid_values}")
    
    def _calculate_score(self, predisposing_conditions: str, pain_features: str, examination_features: str) -> int:
        """Calculates the ADD-RS score based on number of high-risk categories present"""
        
        score = 0
        
        # Add 1 point for each high-risk category that is present
        if predisposing_conditions == "present":
            score += 1
            
        if pain_features == "present":
            score += 1
            
        if examination_features == "present":
            score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the risk interpretation based on the ADD-RS score
        
        Args:
            score (int): ADD-RS score (0-3)
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "No high-risk features present",
                "interpretation": "Low risk for aortic dissection. Consider chest X-ray; if widened mediastinum present or no alternative diagnosis found, consider aortic imaging. ADD-RS captures 95.7% of aortic dissections, but 4.3% of confirmed cases had no high-risk features."
            }
        elif score == 1:
            return {
                "stage": "Intermediate Risk",
                "description": "One high-risk category present", 
                "interpretation": "Intermediate risk for aortic dissection. Consider D-dimer testing or proceed to aortic imaging based on clinical judgment. If D-dimer available and negative (<500 ng/mL), may help rule out dissection in appropriate clinical context."
            }
        else:  # score >= 2
            return {
                "stage": "High Risk",
                "description": "Two or more high-risk categories present",
                "interpretation": "High risk for aortic dissection. Proceed immediately to definitive aortic imaging (CT angiography, MRA, or TEE). Do not delay imaging for additional testing."
            }


def calculate_aortic_dissection_detection_risk_score(predisposing_conditions: str, pain_features: str, examination_features: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AorticDissectionDetectionRiskScoreCalculator()
    return calculator.calculate(predisposing_conditions, pain_features, examination_features)