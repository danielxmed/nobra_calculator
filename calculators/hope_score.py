"""
Hypothermia Outcome Prediction after ECLS (HOPE) Score Calculator

Predicts survival probability for patients with hypothermic cardiac arrest undergoing 
extracorporeal life support (ECLS) rewarming to guide clinical decision-making.

References:
- Pasquier M, Hugli O, Paal P, Darocha T, Blancher M, Husby P, et al. Hypothermia outcome 
  prediction after extracorporeal life support for hypothermic cardiac arrest patients: 
  The HOPE score. Resuscitation. 2018 May;126:58-64.
- Darocha T, Kosinski S, Jarosz A, et al. The chain of survival in hypothermic circulatory 
  arrest: encouraging preliminary results when using early identification, risk stratification 
  and extracorporeal rewarming. Scand J Trauma Resusc Emerg Med. 2016;24:85.
"""

import math
from typing import Dict, Any


class HopeScoreCalculator:
    """Calculator for HOPE Score (Hypothermia Outcome Prediction after ECLS)"""
    
    def __init__(self):
        # HOPE Score formula coefficients from Pasquier et al. 2018
        self.intercept = 2.44
        self.sex_coeff = -1.55          # Male = 1, Female = 0
        self.asphyxia_coeff = -1.95     # Yes = 1, No = 0
        self.age_coeff = -0.0191
        self.potassium_coeff = -2.07    # log₂(potassium)
        self.cpr_coeff = -0.573         # log₂(CPR duration)
        self.temp_coeff = 0.937         # temperature
        self.temp_squared_coeff = -0.0247  # temperature²
        
        # Clinical decision threshold
        self.ecls_threshold = 10.0  # 10% survival probability
    
    def calculate(self, sex: str, hypothermia_with_asphyxia: str, age_years: int,
                 potassium_mmol_l: float, cpr_duration_minutes: int, 
                 core_temperature_celsius: float) -> Dict[str, Any]:
        """
        Calculates HOPE Score and survival probability
        
        Args:
            sex (str): Patient sex ("male" or "female")
            hypothermia_with_asphyxia (str): Asphyxia present ("yes" or "no")
            age_years (int): Age in years
            potassium_mmol_l (float): Serum potassium in mmol/L
            cpr_duration_minutes (int): CPR duration in minutes
            core_temperature_celsius (float): Core temperature in °C
            
        Returns:
            Dict with survival probability and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(sex, hypothermia_with_asphyxia, age_years, 
                            potassium_mmol_l, cpr_duration_minutes, core_temperature_celsius)
        
        # Calculate HOPE score
        hope_score = self._calculate_hope_score(
            sex, hypothermia_with_asphyxia, age_years, potassium_mmol_l,
            cpr_duration_minutes, core_temperature_celsius
        )
        
        # Calculate survival probability
        survival_probability = self._calculate_survival_probability(hope_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(survival_probability)
        
        return {
            "result": round(survival_probability, 1),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "hope_score": round(hope_score, 3),
            "ecls_recommended": survival_probability >= self.ecls_threshold,
            "clinical_recommendation": interpretation["recommendation"],
            "decision_threshold": f"{self.ecls_threshold}%"
        }
    
    def _validate_inputs(self, sex: str, hypothermia_with_asphyxia: str, age_years: int,
                        potassium_mmol_l: float, cpr_duration_minutes: int,
                        core_temperature_celsius: float):
        """Validates input parameters"""
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if hypothermia_with_asphyxia not in ["yes", "no"]:
            raise ValueError("Hypothermia with asphyxia must be 'yes' or 'no'")
        
        if not isinstance(age_years, int) or age_years < 0 or age_years > 120:
            raise ValueError("Age must be an integer between 0 and 120 years")
        
        if not isinstance(potassium_mmol_l, (int, float)) or potassium_mmol_l < 1.0 or potassium_mmol_l > 20.0:
            raise ValueError("Potassium must be between 1.0 and 20.0 mmol/L")
        
        if not isinstance(cpr_duration_minutes, int) or cpr_duration_minutes < 1 or cpr_duration_minutes > 600:
            raise ValueError("CPR duration must be between 1 and 600 minutes")
        
        if not isinstance(core_temperature_celsius, (int, float)) or core_temperature_celsius < 10.0 or core_temperature_celsius > 35.0:
            raise ValueError("Core temperature must be between 10.0 and 35.0°C")
    
    def _calculate_hope_score(self, sex: str, hypothermia_with_asphyxia: str, 
                             age_years: int, potassium_mmol_l: float,
                             cpr_duration_minutes: int, core_temperature_celsius: float) -> float:
        """
        Calculates the HOPE score using the validated formula
        
        Formula: HOPE Score = 2.44 - 1.55*(Sex) - 1.95*(Asphyxia) - 0.0191*(Age) 
                - 2.07*log₂(Potassium) - 0.573*log₂(CPR duration) + 0.937*(Temperature) - 0.0247*(Temperature)²
        
        Args:
            All input parameters
            
        Returns:
            float: HOPE score
        """
        
        # Convert categorical variables to numeric
        sex_numeric = 1 if sex == "male" else 0
        asphyxia_numeric = 1 if hypothermia_with_asphyxia == "yes" else 0
        
        # Calculate logarithms (base 2)
        log2_potassium = math.log2(potassium_mmol_l)
        log2_cpr = math.log2(cpr_duration_minutes)
        
        # Calculate temperature squared
        temperature_squared = core_temperature_celsius ** 2
        
        # Calculate HOPE score
        hope_score = (
            self.intercept +
            self.sex_coeff * sex_numeric +
            self.asphyxia_coeff * asphyxia_numeric +
            self.age_coeff * age_years +
            self.potassium_coeff * log2_potassium +
            self.cpr_coeff * log2_cpr +
            self.temp_coeff * core_temperature_celsius +
            self.temp_squared_coeff * temperature_squared
        )
        
        return hope_score
    
    def _calculate_survival_probability(self, hope_score: float) -> float:
        """
        Converts HOPE score to survival probability using logistic transformation
        
        Args:
            hope_score (float): Calculated HOPE score
            
        Returns:
            float: Survival probability as percentage (0-100)
        """
        
        # Logistic transformation: e^x / (1 + e^x) * 100%
        try:
            exp_score = math.exp(hope_score)
            probability = (exp_score / (1 + exp_score)) * 100
            return max(0.0, min(100.0, probability))  # Ensure 0-100% range
        except OverflowError:
            # Handle extreme values
            if hope_score > 0:
                return 100.0
            else:
                return 0.0
    
    def _get_interpretation(self, survival_probability: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on survival probability
        
        Args:
            survival_probability (float): Calculated survival probability
            
        Returns:
            Dict with interpretation details
        """
        
        if survival_probability < self.ecls_threshold:
            return {
                "stage": "Low Survival Probability",
                "description": f"<{self.ecls_threshold}% survival probability",
                "interpretation": f"Survival probability is {survival_probability:.1f}%, which is below the {self.ecls_threshold}% threshold for ECLS initiation. ECLS is unlikely to confer benefit. Consider withholding ECLS and focus on compassionate end-of-life care. Discuss goals of care with family and consider comfort measures.",
                "recommendation": "ECLS NOT recommended - Poor prognosis with minimal chance of meaningful recovery"
            }
        else:
            return {
                "stage": "Favorable for ECLS",
                "description": f"≥{self.ecls_threshold}% survival probability",
                "interpretation": f"Survival probability is {survival_probability:.1f}%, which meets the threshold for ECLS initiation. ECLS rewarming is recommended. Immediately notify ECLS-capable center and activate rewarming protocol while maintaining high-quality CPR. Patient has reasonable chance of survival with good neurological outcome.",
                "recommendation": "ECLS recommended - Proceed with extracorporeal rewarming"
            }


def calculate_hope_score(sex: str, hypothermia_with_asphyxia: str, age_years: int,
                        potassium_mmol_l: float, cpr_duration_minutes: int,
                        core_temperature_celsius: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HopeScoreCalculator()
    return calculator.calculate(sex, hypothermia_with_asphyxia, age_years,
                              potassium_mmol_l, cpr_duration_minutes, core_temperature_celsius)