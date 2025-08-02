"""
Kocher Criteria for Septic Arthritis Calculator

Clinical prediction rule to differentiate septic arthritis from transient synovitis 
in children presenting with hip pain. Developed by Kocher et al. (1999) and widely 
validated for pediatric patients aged 2-16 years.

References:
1. Kocher MS, Zurakowski D, Kasser JR. Differentiating between septic arthritis and 
   transient synovitis of the hip in children: an evidence-based clinical prediction 
   algorithm. J Bone Joint Surg Am. 1999 Dec;81(12):1662-70.
2. Caird MS, Flynn JM, Leung YL, Millman JE, D'Italia JG, Dormans JP. Factors 
   distinguishing septic arthritis from transient synovitis of the hip in children. 
   A prospective study. J Bone Joint Surg Am. 2006 Jun;88(6):1251-7.
"""

from typing import Dict, Any


class KocherCriteriaSepticArthritisCalculator:
    """Calculator for Kocher Criteria for Septic Arthritis"""
    
    def __init__(self):
        """Initialize probability ranges based on original and validation studies"""
        # Risk probabilities based on number of predictors present
        self.risk_probabilities = {
            0: {
                "min_risk": 0.2,
                "max_risk": 2.0,
                "stage": "Very Low Risk",
                "description": "0 predictors present",
                "clinical_action": "Consider transient synovitis. May manage conservatively with close monitoring."
            },
            1: {
                "min_risk": 3.0,
                "max_risk": 9.5,
                "stage": "Low Risk", 
                "description": "1 predictor present",
                "clinical_action": "Consider laboratory studies and imaging. May observe with close follow-up."
            },
            2: {
                "min_risk": 35.0,
                "max_risk": 40.0,
                "stage": "Moderate Risk",
                "description": "2 predictors present",
                "clinical_action": "Strong consideration for arthrocentesis or surgical drainage. Urgent orthopedic consultation recommended."
            },
            3: {
                "min_risk": 72.8,
                "max_risk": 93.1,
                "stage": "High Risk",
                "description": "3 predictors present",
                "clinical_action": "Arthrocentesis or urgent surgical drainage strongly indicated. Immediate orthopedic consultation and antibiotic therapy."
            },
            4: {
                "min_risk": 93.0,
                "max_risk": 99.6,
                "stage": "Very High Risk",
                "description": "4 predictors present",
                "clinical_action": "Urgent surgical drainage required. Immediate orthopedic consultation and empiric antibiotic therapy."
            }
        }
    
    def calculate(self, non_weight_bearing: str, temperature_over_38_5: str, 
                 esr_over_40: str, wbc_over_12000: str) -> Dict[str, Any]:
        """
        Calculates Kocher Criteria risk assessment for septic arthritis
        
        Args:
            non_weight_bearing (str): Patient unable to bear weight ("yes" or "no")
            temperature_over_38_5 (str): Temperature >38.5°C ("yes" or "no")
            esr_over_40 (str): ESR >40 mm/hr ("yes" or "no")
            wbc_over_12000 (str): WBC >12,000 cells/mm³ ("yes" or "no")
            
        Returns:
            Dict with risk assessment and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(non_weight_bearing, temperature_over_38_5, 
                            esr_over_40, wbc_over_12000)
        
        # Count positive predictors
        predictor_count = self._count_predictors(
            non_weight_bearing, temperature_over_38_5, esr_over_40, wbc_over_12000
        )
        
        # Get risk assessment
        risk_data = self.risk_probabilities[predictor_count]
        
        # Create detailed result
        result = {
            "predictor_count": predictor_count,
            "predictors": {
                "non_weight_bearing": non_weight_bearing == "yes",
                "temperature_over_38_5": temperature_over_38_5 == "yes",
                "esr_over_40": esr_over_40 == "yes",
                "wbc_over_12000": wbc_over_12000 == "yes"
            },
            "risk_range": {
                "min_risk_percent": risk_data["min_risk"],
                "max_risk_percent": risk_data["max_risk"]
            },
            "stage": risk_data["stage"],
            "description": risk_data["description"]
        }
        
        # Generate interpretation
        interpretation = self._generate_interpretation(predictor_count, risk_data)
        
        return {
            "result": result,
            "unit": "predictors",
            "interpretation": interpretation,
            "stage": risk_data["stage"],
            "stage_description": risk_data["description"]
        }
    
    def _validate_inputs(self, non_weight_bearing: str, temperature_over_38_5: str,
                        esr_over_40: str, wbc_over_12000: str):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        if non_weight_bearing not in valid_options:
            raise ValueError("non_weight_bearing must be 'yes' or 'no'")
        
        if temperature_over_38_5 not in valid_options:
            raise ValueError("temperature_over_38_5 must be 'yes' or 'no'")
            
        if esr_over_40 not in valid_options:
            raise ValueError("esr_over_40 must be 'yes' or 'no'")
            
        if wbc_over_12000 not in valid_options:
            raise ValueError("wbc_over_12000 must be 'yes' or 'no'")
    
    def _count_predictors(self, non_weight_bearing: str, temperature_over_38_5: str,
                         esr_over_40: str, wbc_over_12000: str) -> int:
        """Counts the number of positive predictors"""
        
        count = 0
        
        if non_weight_bearing == "yes":
            count += 1
        if temperature_over_38_5 == "yes":
            count += 1
        if esr_over_40 == "yes":
            count += 1
        if wbc_over_12000 == "yes":
            count += 1
            
        return count
    
    def _generate_interpretation(self, predictor_count: int, risk_data: Dict) -> str:
        """
        Generates comprehensive clinical interpretation
        
        Args:
            predictor_count (int): Number of positive predictors
            risk_data (Dict): Risk assessment data
            
        Returns:
            str: Detailed clinical interpretation with recommendations
        """
        
        # Base interpretation with risk assessment
        if predictor_count == 0:
            interpretation = (
                f"Very low risk of septic arthritis (<0.2-2% probability). "
                f"Clinical presentation suggests transient synovitis. "
                f"Conservative management with close monitoring is appropriate. "
                f"Educate family about signs of deterioration and ensure reliable follow-up."
            )
        elif predictor_count == 1:
            interpretation = (
                f"Low risk of septic arthritis (3-9.5% probability). "
                f"Consider obtaining inflammatory markers (CRP, ESR) and imaging if not already done. "
                f"May manage with observation and close follow-up within 24-48 hours. "
                f"Advise family to return immediately if symptoms worsen."
            )
        elif predictor_count == 2:
            interpretation = (
                f"Moderate risk of septic arthritis (35-40% probability). "
                f"Strong consideration for arthrocentesis or surgical drainage is warranted. "
                f"Urgent orthopedic consultation recommended within hours. "
                f"Consider empiric antibiotic therapy while awaiting definitive diagnosis."
            )
        elif predictor_count == 3:
            interpretation = (
                f"High risk of septic arthritis (72.8-93.1% probability). "
                f"Arthrocentesis or urgent surgical drainage strongly indicated. "
                f"Immediate orthopedic consultation and empiric antibiotic therapy recommended. "
                f"Prepare for urgent operative intervention if arthrocentesis confirms septic arthritis."
            )
        else:  # predictor_count == 4
            interpretation = (
                f"Very high risk of septic arthritis (93-99.6% probability). "
                f"Urgent surgical drainage required with immediate orthopedic consultation. "
                f"Begin empiric antibiotic therapy immediately. "
                f"Prepare for emergency operative intervention - delay increases morbidity risk."
            )
        
        # Add general clinical guidance
        interpretation += (
            f" Remember that clinical judgment remains paramount, and the Kocher criteria "
            f"should be used as an adjunct to, not a replacement for, thorough clinical assessment. "
            f"Serial evaluation may be necessary as the clinical picture can evolve rapidly."
        )
        
        return interpretation


def calculate_kocher_criteria_septic_arthritis(non_weight_bearing, temperature_over_38_5,
                                             esr_over_40, wbc_over_12000) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = KocherCriteriaSepticArthritisCalculator()
    return calculator.calculate(non_weight_bearing, temperature_over_38_5, 
                              esr_over_40, wbc_over_12000)