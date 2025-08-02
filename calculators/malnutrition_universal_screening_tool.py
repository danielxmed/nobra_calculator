"""
Malnutrition Universal Screening Tool (MUST)

BAPEN-developed screening tool that identifies patients who are malnourished 
or at risk of malnutrition using BMI, weight loss, and acute disease effects.

References:
- Elia M. The 'MUST' report. Nutritional screening of adults: a multidisciplinary responsibility. Redditch: BAPEN; 2003.
- Stratton RJ, et al. Malnutrition in hospital outpatients and inpatients: prevalence, concurrent validity and ease of use of the 'malnutrition universal screening tool' ('MUST') for adults. Br J Nutr. 2004;92(5):799-808.
"""

import math
from typing import Dict, Any


class MalnutritionUniversalScreeningToolCalculator:
    """Calculator for Malnutrition Universal Screening Tool (MUST)"""
    
    def __init__(self):
        # BMI scoring thresholds
        self.BMI_NORMAL_THRESHOLD = 20.0
        self.BMI_MILD_RISK_THRESHOLD = 18.5
        
        # Weight loss scoring thresholds
        self.WEIGHT_LOSS_MILD_THRESHOLD = 5.0
        self.WEIGHT_LOSS_HIGH_THRESHOLD = 10.0
    
    def calculate(self, bmi: float, weight_loss_percentage: float, 
                 acute_disease_effect: str) -> Dict[str, Any]:
        """
        Calculates the MUST score to assess malnutrition risk
        
        Args:
            bmi (float): Body Mass Index in kg/m² (10.0-60.0)
            weight_loss_percentage (float): Unplanned weight loss in past 3-6 months as % of body weight (0.0-50.0)
            acute_disease_effect (str): Patient acutely ill with no nutritional intake for >5 days ('yes' or 'no')
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(bmi, weight_loss_percentage, acute_disease_effect)
        
        # Calculate individual component scores
        bmi_score = self._calculate_bmi_score(bmi)
        weight_loss_score = self._calculate_weight_loss_score(weight_loss_percentage)
        disease_score = self._calculate_disease_score(acute_disease_effect)
        
        # Calculate total MUST score
        total_score = bmi_score + weight_loss_score + disease_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": {
                "total_score": total_score,
                "bmi_score": bmi_score,
                "weight_loss_score": weight_loss_score,
                "disease_score": disease_score,
                "bmi_category": self._get_bmi_category(bmi),
                "weight_loss_category": self._get_weight_loss_category(weight_loss_percentage)
            },
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bmi, weight_loss_percentage, acute_disease_effect):
        """Validates input parameters"""
        
        # BMI validation
        if not isinstance(bmi, (int, float)) or bmi < 10.0 or bmi > 60.0:
            raise ValueError("BMI must be a number between 10.0 and 60.0 kg/m²")
        
        # Weight loss validation
        if not isinstance(weight_loss_percentage, (int, float)) or weight_loss_percentage < 0.0 or weight_loss_percentage > 50.0:
            raise ValueError("Weight loss percentage must be a number between 0.0 and 50.0%")
        
        # Acute disease effect validation
        if acute_disease_effect not in ["yes", "no"]:
            raise ValueError("Acute disease effect must be 'yes' or 'no'")
    
    def _calculate_bmi_score(self, bmi: float) -> int:
        """Calculates BMI component score"""
        
        if bmi >= self.BMI_NORMAL_THRESHOLD:
            return 0  # BMI ≥20.0
        elif bmi >= self.BMI_MILD_RISK_THRESHOLD:
            return 1  # BMI 18.5-19.9
        else:
            return 2  # BMI <18.5
    
    def _calculate_weight_loss_score(self, weight_loss_percentage: float) -> int:
        """Calculates weight loss component score"""
        
        if weight_loss_percentage < self.WEIGHT_LOSS_MILD_THRESHOLD:
            return 0  # <5% weight loss
        elif weight_loss_percentage < self.WEIGHT_LOSS_HIGH_THRESHOLD:
            return 1  # 5-10% weight loss
        else:
            return 2  # >10% weight loss
    
    def _calculate_disease_score(self, acute_disease_effect: str) -> int:
        """Calculates acute disease effect score"""
        
        if acute_disease_effect == "yes":
            return 2  # Acutely ill with no intake >5 days
        else:
            return 0  # No acute disease effect
    
    def _get_bmi_category(self, bmi: float) -> str:
        """Gets BMI category description"""
        
        if bmi >= self.BMI_NORMAL_THRESHOLD:
            return f"Normal/Overweight (≥20.0 kg/m²): {bmi:.1f}"
        elif bmi >= self.BMI_MILD_RISK_THRESHOLD:
            return f"Mild underweight (18.5-19.9 kg/m²): {bmi:.1f}"
        else:
            return f"Underweight (<18.5 kg/m²): {bmi:.1f}"
    
    def _get_weight_loss_category(self, weight_loss_percentage: float) -> str:
        """Gets weight loss category description"""
        
        if weight_loss_percentage < self.WEIGHT_LOSS_MILD_THRESHOLD:
            return f"Minimal weight loss (<5%): {weight_loss_percentage:.1f}%"
        elif weight_loss_percentage < self.WEIGHT_LOSS_HIGH_THRESHOLD:
            return f"Moderate weight loss (5-10%): {weight_loss_percentage:.1f}%"
        else:
            return f"Significant weight loss (>10%): {weight_loss_percentage:.1f}%"
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the MUST score
        
        Args:
            score (int): Total MUST score
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low Risk",
                "description": "Low risk of malnutrition",
                "interpretation": (
                    "Low risk of malnutrition. Routine clinical care with repeat screening: "
                    "in hospital weekly, in care homes monthly, and in community annually "
                    "for special groups (>75 years, concern about underlying conditions). "
                    "Continue normal diet and monitor as per routine clinical care."
                )
            }
        elif score == 1:
            return {
                "stage": "Medium Risk",
                "description": "Medium risk of malnutrition",
                "interpretation": (
                    "Medium risk of malnutrition. Document dietary intake and observe for 3 days. "
                    "If improved intake - little clinical concern, continue monitoring. "
                    "If no improvement, follow clinical guidelines for high-risk patients. "
                    "Repeat screening: in hospital weekly and in care homes/community monthly."
                )
            }
        else:  # score >= 2
            return {
                "stage": "High Risk",
                "description": "High risk of malnutrition",
                "interpretation": (
                    "High risk of malnutrition. Refer to dietitian, nutritional support team "
                    "or implement local policy. Improve and increase overall nutritional intake "
                    "through food fortification, supplements, or enteral/parenteral nutrition as appropriate. "
                    "Monitor and review care plan regularly. Repeat screening: in hospital weekly "
                    "and in care homes/community monthly."
                )
            }


def calculate_malnutrition_universal_screening_tool(bmi, weight_loss_percentage, 
                                                  acute_disease_effect) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MalnutritionUniversalScreeningToolCalculator()
    return calculator.calculate(bmi, weight_loss_percentage, acute_disease_effect)