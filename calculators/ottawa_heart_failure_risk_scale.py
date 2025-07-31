"""
Ottawa Heart Failure Risk Scale (OHFRS) Calculator

Identifies emergency department heart failure patients at high risk for serious adverse events.
Uses 10 clinical variables to stratify risk.

References:
1. Stiell IG, et al. Acad Emerg Med. 2013;20(1):17-26.
2. Stiell IG, et al. Acad Emerg Med. 2017;24(3):316-327.
"""

from typing import Dict, Any


class OttawaHeartFailureRiskScaleCalculator:
    """Calculator for Ottawa Heart Failure Risk Scale"""
    
    def __init__(self):
        # Point values for each criterion
        self.SCORING = {
            "stroke_or_tia": 1,
            "intubation_respiratory_distress": 2,
            "heart_rate_110_or_higher_arrival": 2,
            "oxygen_saturation_less_than_90": 1,
            "heart_rate_110_or_higher_walk_test": 1,
            "new_ischemic_changes_ecg": 2,
            "urea_12_or_higher": 1,
            "serum_co2_35_or_higher": 2,
            "troponin_elevated_mi_level": 2,
            "nt_probnp_5000_or_higher": 1
        }
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates the Ottawa Heart Failure Risk Scale score
        
        Args:
            **kwargs: All 10 parameters (yes/no values)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(kwargs)
        
        # Calculate score
        result = self._calculate_score(kwargs)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, params: Dict[str, str]):
        """Validates input parameters"""
        
        expected_params = set(self.SCORING.keys())
        actual_params = set(params.keys())
        
        # Check for missing parameters
        missing = expected_params - actual_params
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")
        
        # Check for extra parameters
        extra = actual_params - expected_params
        if extra:
            raise ValueError(f"Unexpected parameters: {', '.join(extra)}")
        
        # Validate all values are yes/no
        for param, value in params.items():
            if value not in ["yes", "no"]:
                raise ValueError(f"{param} must be 'yes' or 'no'")
    
    def _calculate_score(self, params: Dict[str, str]) -> int:
        """Calculates the total Ottawa Heart Failure Risk Scale score"""
        
        total_score = 0
        
        for param, value in params.items():
            if value == "yes":
                total_score += self.SCORING[param]
        
        return total_score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (int): Calculated Ottawa Heart Failure Risk Scale score
            
        Returns:
            Dict with interpretation
        """
        
        if result == 0:
            return {
                "stage": "Low risk",
                "description": "2.8% risk of serious adverse events",
                "interpretation": "This patient has a low risk (2.8%) of serious adverse events within 14 days. Serious adverse events include death within 30 days, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse resulting in hospital admission within 14 days."
            }
        elif result <= 2:
            return {
                "stage": "Medium risk",
                "description": "5.1-9.2% risk of serious adverse events",
                "interpretation": "This patient has a medium risk (5.1-9.2%) of serious adverse events within 14 days. Consider closer monitoring and follow-up arrangements. The OHFRS has high sensitivity (91.8% without NT-proBNP, 95.8% with NT-proBNP) for detecting patients at risk."
            }
        elif result <= 4:
            return {
                "stage": "High risk",
                "description": "15.9-26.1% risk of serious adverse events",
                "interpretation": "This patient has a high risk (15.9-26.1%) of serious adverse events within 14 days. Strong consideration should be given to admission with monitoring. Serious adverse events include death within 30 days, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse resulting in hospital admission within 14 days."
            }
        else:  # score 5+
            return {
                "stage": "Very high risk",
                "description": "39.8-89%+ risk of serious adverse events",
                "interpretation": "This patient has a very high risk (39.8-89%+) of serious adverse events within 14 days. Admission with intensive monitoring is strongly recommended. Serious adverse events include death within 30 days, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse resulting in hospital admission within 14 days."
            }


def calculate_ottawa_heart_failure_risk_scale(stroke_or_tia: str,
                                              intubation_respiratory_distress: str,
                                              heart_rate_110_or_higher_arrival: str,
                                              oxygen_saturation_less_than_90: str,
                                              heart_rate_110_or_higher_walk_test: str,
                                              new_ischemic_changes_ecg: str,
                                              urea_12_or_higher: str,
                                              serum_co2_35_or_higher: str,
                                              troponin_elevated_mi_level: str,
                                              nt_probnp_5000_or_higher: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OttawaHeartFailureRiskScaleCalculator()
    
    params = {
        "stroke_or_tia": stroke_or_tia,
        "intubation_respiratory_distress": intubation_respiratory_distress,
        "heart_rate_110_or_higher_arrival": heart_rate_110_or_higher_arrival,
        "oxygen_saturation_less_than_90": oxygen_saturation_less_than_90,
        "heart_rate_110_or_higher_walk_test": heart_rate_110_or_higher_walk_test,
        "new_ischemic_changes_ecg": new_ischemic_changes_ecg,
        "urea_12_or_higher": urea_12_or_higher,
        "serum_co2_35_or_higher": serum_co2_35_or_higher,
        "troponin_elevated_mi_level": troponin_elevated_mi_level,
        "nt_probnp_5000_or_higher": nt_probnp_5000_or_higher
    }
    
    return calculator.calculate(**params)