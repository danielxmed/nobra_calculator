"""
Ottawa COPD Risk Scale Calculator

Predicts 30-day mortality or serious adverse events in emergency department COPD patients.
Uses 10 clinical variables to stratify risk.

References:
1. Stiell IG, et al. CMAJ. 2014;186(15):E563-73.
2. Stiell IG, et al. CMAJ. 2018;190(41):E1202-E1211.
"""

from typing import Dict, Any


class OttawaCopdRiskScaleCalculator:
    """Calculator for Ottawa COPD Risk Scale"""
    
    def __init__(self):
        # Point values for each criterion
        self.SCORING = {
            "coronary_bypass_graft": 1,
            "peripheral_vascular_intervention": 1,
            "intubation_respiratory_distress": 2,
            "heart_rate_110_or_higher": 2,
            "too_ill_for_walk_test": 2,
            "acute_ischemic_changes_ecg": 2,
            "pulmonary_congestion_xray": 1,
            "hemoglobin_less_than_10": 3,
            "urea_12_or_higher": 1,
            "serum_co2_35_or_higher": 1
        }
    
    def calculate(self, **kwargs) -> Dict[str, Any]:
        """
        Calculates the Ottawa COPD Risk Scale score
        
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
        """Calculates the total Ottawa COPD Risk Scale score"""
        
        total_score = 0
        
        for param, value in params.items():
            if value == "yes":
                total_score += self.SCORING[param]
        
        return total_score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (int): Calculated Ottawa COPD Risk Scale score
            
        Returns:
            Dict with interpretation
        """
        
        if result == 0:
            return {
                "stage": "Low risk",
                "description": "2.2% risk of serious adverse events",
                "interpretation": "This patient has a low risk (2.2%) of serious adverse events within 30 days. Serious adverse events include death, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse requiring hospital admission within 14 days."
            }
        elif result <= 2:
            return {
                "stage": "Medium risk",
                "description": "4.0-7.2% risk of serious adverse events",
                "interpretation": "This patient has a medium risk (4.0-7.2%) of serious adverse events within 30 days. Consider closer monitoring and follow-up arrangements. Serious adverse events include death, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse requiring hospital admission within 14 days."
            }
        elif result <= 4:
            return {
                "stage": "High risk",
                "description": "12.5-20.9% risk of serious adverse events",
                "interpretation": "This patient has a high risk (12.5-20.9%) of serious adverse events within 30 days. Strong consideration should be given to admission or intensive outpatient monitoring. Serious adverse events include death, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse requiring hospital admission within 14 days."
            }
        elif result <= 8:
            return {
                "stage": "Very high risk",
                "description": "32.9-75.6% risk of serious adverse events",
                "interpretation": "This patient has a very high risk (32.9-75.6%) of serious adverse events within 30 days. Admission is strongly recommended with close monitoring and aggressive treatment. Serious adverse events include death, admission to monitored unit, intubation, noninvasive ventilation, myocardial infarction, or relapse requiring hospital admission within 14 days."
            }
        else:  # score 9-10
            return {
                "stage": "Extremely high risk",
                "description": "Risk >75% (not well studied)",
                "interpretation": "This patient has an extremely high risk (>75%) of serious adverse events within 30 days. Immediate admission with intensive monitoring is indicated. Note: Scores of 9-10 were not well studied in the original derivation and validation cohorts."
            }


def calculate_ottawa_copd_risk_scale(coronary_bypass_graft: str,
                                     peripheral_vascular_intervention: str,
                                     intubation_respiratory_distress: str,
                                     heart_rate_110_or_higher: str,
                                     too_ill_for_walk_test: str,
                                     acute_ischemic_changes_ecg: str,
                                     pulmonary_congestion_xray: str,
                                     hemoglobin_less_than_10: str,
                                     urea_12_or_higher: str,
                                     serum_co2_35_or_higher: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OttawaCopdRiskScaleCalculator()
    
    params = {
        "coronary_bypass_graft": coronary_bypass_graft,
        "peripheral_vascular_intervention": peripheral_vascular_intervention,
        "intubation_respiratory_distress": intubation_respiratory_distress,
        "heart_rate_110_or_higher": heart_rate_110_or_higher,
        "too_ill_for_walk_test": too_ill_for_walk_test,
        "acute_ischemic_changes_ecg": acute_ischemic_changes_ecg,
        "pulmonary_congestion_xray": pulmonary_congestion_xray,
        "hemoglobin_less_than_10": hemoglobin_less_than_10,
        "urea_12_or_higher": urea_12_or_higher,
        "serum_co2_35_or_higher": serum_co2_35_or_higher
    }
    
    return calculator.calculate(**params)