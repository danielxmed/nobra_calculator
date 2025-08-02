"""
International IgA Nephropathy Prediction Tool Calculator

Predicts risk of 50% decline in eGFR or end-stage kidney disease in patients 
with IgA nephropathy based on clinical, laboratory, and histological parameters.

References (Vancouver style):
1. Barbour SJ, Coppo R, Zhang H, Liu ZH, Suzuki Y, Matsuzaki K, et al. Evaluating a New 
   International Risk-Prediction Tool in IgA Nephropathy. JAMA Intern Med. 2019 Jul 1;179(7):942-952. 
   doi: 10.1001/jamainternmed.2019.0600.
2. Kidney Disease: Improving Global Outcomes (KDIGO) Glomerular Diseases Work Group. KDIGO 2021 
   Clinical Practice Guideline for the Management of Glomerular Diseases. Kidney Int. 2021 Oct;100(4S):S1-S276. 
   doi: 10.1016/j.kint.2021.05.021.
3. Zhang J, Huang B, Liu Z, Wang X, Xie M, Guo R, et al. External validation of the International 
   IgA Nephropathy Prediction Tool. Clin J Am Soc Nephrol. 2020 Jul 7;15(7):1112-1120. 
   doi: 10.2215/CJN.16021219.
"""

import math
from typing import Dict, Any, Optional


class InternationalIganPredictionToolCalculator:
    """Calculator for International IgA Nephropathy Prediction Tool"""
    
    def __init__(self):
        # Model coefficients for race-free version (primary model)
        self.race_free_coefficients = {
            "sqrt_egfr_minus_8_8": -0.209,
            "ln_urine_protein_plus_0_26": 0.438,
            "map_minus_100_div_15": 0.254,
            "mest_m": 0.305,
            "mest_e": 0.441,
            "mest_s": 0.275,
            "mest_t": 0.304,
            "rasb_use": -0.218,
            "immunosuppression_use": -0.169,
            "intercept": -1.132
        }
        
        # Model coefficients for race-inclusive version (alternative model)
        self.race_inclusive_coefficients = {
            "sqrt_egfr_minus_8_8": -0.207,
            "ln_urine_protein_plus_0_26": 0.431,
            "map_minus_100_div_15": 0.247,
            "mest_m": 0.298,
            "mest_e": 0.431,
            "mest_s": 0.271,
            "mest_t": 0.301,
            "rasb_use": -0.213,
            "immunosuppression_use": -0.163,
            "race_chinese": 0.234,
            "race_japanese": 0.191,
            "race_other": 0.105,
            "intercept": -1.167
        }
    
    def calculate(self, age: int, egfr: float, map: float, urine_protein: float,
                  mest_m: int, mest_e: int, mest_s: int, mest_t: int,
                  rasb_use: str, immunosuppression_use: str, 
                  race: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates the 5-year risk of 50% eGFR decline or ESKD using the International IgAN Prediction Tool
        
        Args:
            age (int): Patient age in years (18-65)
            egfr (float): Estimated glomerular filtration rate in mL/min/1.73m²
            map (float): Mean arterial pressure in mmHg
            urine_protein (float): 24-hour urine protein in g/day
            mest_m (int): Oxford MEST Score - Mesangial hypercellularity (0-1)
            mest_e (int): Oxford MEST Score - Endocapillary hypercellularity (0-1)
            mest_s (int): Oxford MEST Score - Segmental sclerosis (0-1)
            mest_t (int): Oxford MEST Score - Interstitial fibrosis/tubular atrophy (0-2)
            rasb_use (str): Renin-angiotensin system blocker use ("yes" or "no")
            immunosuppression_use (str): Immunosuppressive therapy use ("yes" or "no")
            race (str, optional): Patient race ("white", "chinese", "japanese", "other")
            
        Returns:
            Dict with the 5-year risk percentage and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, egfr, map, urine_protein, mest_m, mest_e, mest_s, mest_t,
                            rasb_use, immunosuppression_use, race)
        
        # Calculate risk using appropriate model
        if race is not None:
            risk_percentage = self._calculate_race_inclusive_risk(
                age, egfr, map, urine_protein, mest_m, mest_e, mest_s, mest_t,
                rasb_use, immunosuppression_use, race
            )
        else:
            risk_percentage = self._calculate_race_free_risk(
                age, egfr, map, urine_protein, mest_m, mest_e, mest_s, mest_t,
                rasb_use, immunosuppression_use
            )
        
        # Get interpretation based on risk
        interpretation = self._get_interpretation(risk_percentage)
        
        return {
            "result": round(risk_percentage, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, egfr: float, map: float, urine_protein: float,
                        mest_m: int, mest_e: int, mest_s: int, mest_t: int,
                        rasb_use: str, immunosuppression_use: str, race: Optional[str]):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 65:
            raise ValueError("Age must be an integer between 18 and 65 years")
        
        # Validate eGFR
        if not isinstance(egfr, (int, float)) or egfr < 5 or egfr > 150:
            raise ValueError("eGFR must be between 5 and 150 mL/min/1.73m²")
        
        # Validate MAP
        if not isinstance(map, (int, float)) or map < 60 or map > 140:
            raise ValueError("Mean arterial pressure must be between 60 and 140 mmHg")
        
        # Validate urine protein
        if not isinstance(urine_protein, (int, float)) or urine_protein < 0.001 or urine_protein > 15:
            raise ValueError("Urine protein must be between 0.001 and 15 g/day")
        
        # Validate MEST scores
        if not isinstance(mest_m, int) or mest_m not in [0, 1]:
            raise ValueError("MEST M score must be 0 or 1")
        
        if not isinstance(mest_e, int) or mest_e not in [0, 1]:
            raise ValueError("MEST E score must be 0 or 1")
        
        if not isinstance(mest_s, int) or mest_s not in [0, 1]:
            raise ValueError("MEST S score must be 0 or 1")
        
        if not isinstance(mest_t, int) or mest_t not in [0, 1, 2]:
            raise ValueError("MEST T score must be 0, 1, or 2")
        
        # Validate RASB use
        if rasb_use not in ["yes", "no"]:
            raise ValueError("RASB use must be 'yes' or 'no'")
        
        # Validate immunosuppression use
        if immunosuppression_use not in ["yes", "no"]:
            raise ValueError("Immunosuppression use must be 'yes' or 'no'")
        
        # Validate race if provided
        if race is not None and race not in ["white", "chinese", "japanese", "other"]:
            raise ValueError("Race must be 'white', 'chinese', 'japanese', or 'other'")
    
    def _calculate_race_free_risk(self, age: int, egfr: float, map: float, urine_protein: float,
                                 mest_m: int, mest_e: int, mest_s: int, mest_t: int,
                                 rasb_use: str, immunosuppression_use: str) -> float:
        """Calculates risk using the race-free model"""
        
        coeffs = self.race_free_coefficients
        
        # Transform variables according to the model
        sqrt_egfr_minus_8_8 = math.sqrt(egfr) - 8.8
        ln_urine_protein_plus_0_26 = math.log(urine_protein + 0.26)
        map_minus_100_div_15 = (map - 100) / 15
        
        # Convert yes/no to 1/0
        rasb_binary = 1 if rasb_use == "yes" else 0
        immunosupp_binary = 1 if immunosuppression_use == "yes" else 0
        
        # Calculate linear predictor
        linear_predictor = (
            coeffs["sqrt_egfr_minus_8_8"] * sqrt_egfr_minus_8_8 +
            coeffs["ln_urine_protein_plus_0_26"] * ln_urine_protein_plus_0_26 +
            coeffs["map_minus_100_div_15"] * map_minus_100_div_15 +
            coeffs["mest_m"] * mest_m +
            coeffs["mest_e"] * mest_e +
            coeffs["mest_s"] * mest_s +
            coeffs["mest_t"] * mest_t +
            coeffs["rasb_use"] * rasb_binary +
            coeffs["immunosuppression_use"] * immunosupp_binary +
            coeffs["intercept"]
        )
        
        # Convert to 5-year risk percentage
        risk_5_year = (1 - math.exp(-math.exp(linear_predictor))) * 100
        
        return risk_5_year
    
    def _calculate_race_inclusive_risk(self, age: int, egfr: float, map: float, urine_protein: float,
                                     mest_m: int, mest_e: int, mest_s: int, mest_t: int,
                                     rasb_use: str, immunosuppression_use: str, race: str) -> float:
        """Calculates risk using the race-inclusive model"""
        
        coeffs = self.race_inclusive_coefficients
        
        # Transform variables according to the model
        sqrt_egfr_minus_8_8 = math.sqrt(egfr) - 8.8
        ln_urine_protein_plus_0_26 = math.log(urine_protein + 0.26)
        map_minus_100_div_15 = (map - 100) / 15
        
        # Convert yes/no to 1/0
        rasb_binary = 1 if rasb_use == "yes" else 0
        immunosupp_binary = 1 if immunosuppression_use == "yes" else 0
        
        # Convert race to binary variables (white is reference)
        race_chinese = 1 if race == "chinese" else 0
        race_japanese = 1 if race == "japanese" else 0
        race_other = 1 if race == "other" else 0
        
        # Calculate linear predictor
        linear_predictor = (
            coeffs["sqrt_egfr_minus_8_8"] * sqrt_egfr_minus_8_8 +
            coeffs["ln_urine_protein_plus_0_26"] * ln_urine_protein_plus_0_26 +
            coeffs["map_minus_100_div_15"] * map_minus_100_div_15 +
            coeffs["mest_m"] * mest_m +
            coeffs["mest_e"] * mest_e +
            coeffs["mest_s"] * mest_s +
            coeffs["mest_t"] * mest_t +
            coeffs["rasb_use"] * rasb_binary +
            coeffs["immunosuppression_use"] * immunosupp_binary +
            coeffs["race_chinese"] * race_chinese +
            coeffs["race_japanese"] * race_japanese +
            coeffs["race_other"] * race_other +
            coeffs["intercept"]
        )
        
        # Convert to 5-year risk percentage
        risk_5_year = (1 - math.exp(-math.exp(linear_predictor))) * 100
        
        return risk_5_year
    
    def _get_interpretation(self, risk_percentage: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the 5-year risk percentage
        
        Args:
            risk_percentage (float): Calculated 5-year risk percentage
            
        Returns:
            Dict with risk stratification and clinical recommendations
        """
        
        if risk_percentage < 10:
            return {
                "stage": "Very Low Risk",
                "description": "5-year risk <10%",
                "interpretation": "Very low risk of kidney function decline. Standard monitoring and conservative management appropriate. Continue RASB therapy if indicated. Regular nephrology follow-up every 6-12 months. Focus on cardiovascular risk reduction and blood pressure control. Consider watchful waiting approach for immunosuppression."
            }
        elif risk_percentage < 25:
            return {
                "stage": "Low Risk",
                "description": "5-year risk 10-25%",
                "interpretation": "Low risk of kidney function decline. Conservative management with close monitoring. Optimize RASB therapy and blood pressure control (<130/80 mmHg). Regular nephrology follow-up every 3-6 months. Monitor proteinuria and eGFR trends. Consider immunosuppression if rapid progression or high-risk features develop."
            }
        elif risk_percentage < 50:
            return {
                "stage": "Moderate Risk",
                "description": "5-year risk 25-50%",
                "interpretation": "Moderate risk of kidney function decline. Consider immunosuppressive therapy based on individual patient factors. Optimize RASB therapy and strict blood pressure control. Frequent nephrology follow-up every 2-3 months. Monitor for treatment response and side effects. Consider clinical trial participation. Prepare for potential kidney replacement therapy discussion."
            }
        elif risk_percentage < 75:
            return {
                "stage": "High Risk",
                "description": "5-year risk 50-75%",
                "interpretation": "High risk of kidney function decline. Strong consideration for immunosuppressive therapy unless contraindicated. Aggressive blood pressure control and maximize RASB therapy. Frequent nephrology follow-up every 1-2 months. Consider clinical trial enrollment. Early kidney replacement therapy planning and education. Evaluate for kidney transplant candidacy."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "5-year risk >75%",
                "interpretation": "Very high risk of kidney function decline. Urgent consideration for immunosuppressive therapy if not contraindicated. Maximal conservative management with aggressive blood pressure control. Monthly nephrology follow-up. Prioritize clinical trial participation. Immediate kidney replacement therapy planning and patient education. Accelerated kidney transplant evaluation and preparation."
            }


def calculate_international_igan_prediction_tool(age: int, egfr: float, map: float, urine_protein: float,
                                               mest_m: int, mest_e: int, mest_s: int, mest_t: int,
                                               rasb_use: str, immunosuppression_use: str, 
                                               race: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates the 5-year risk of 50% eGFR decline or ESKD in patients with IgA nephropathy
    using the International IgAN Prediction Tool.
    
    Args:
        age (int): Patient age in years
        egfr (float): Estimated glomerular filtration rate
        map (float): Mean arterial pressure
        urine_protein (float): 24-hour urine protein
        mest_m (int): Oxford MEST Score - Mesangial hypercellularity
        mest_e (int): Oxford MEST Score - Endocapillary hypercellularity
        mest_s (int): Oxford MEST Score - Segmental sclerosis
        mest_t (int): Oxford MEST Score - Interstitial fibrosis/tubular atrophy
        rasb_use (str): RASB use
        immunosuppression_use (str): Immunosuppression use
        race (str, optional): Patient race
        
    Returns:
        Dict with 5-year risk percentage and clinical interpretation
    """
    calculator = InternationalIganPredictionToolCalculator()
    return calculator.calculate(age, egfr, map, urine_protein, mest_m, mest_e, mest_s, mest_t,
                              rasb_use, immunosuppression_use, race)