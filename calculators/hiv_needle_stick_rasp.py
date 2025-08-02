"""
HIV Needle Stick Risk Assessment Stratification Protocol (RASP) Calculator

Quantifies HIV exposure risk to guide post-exposure prophylaxis decisions.

References:
- Vertesi L. CJEM. 2003;5(1):46-8.
- Panlilio AL, et al. MMWR Recomm Rep. 2005;54(RR-9):1-17.
"""

from typing import Dict, Any


class HivNeedleStickRaspCalculator:
    """Calculator for HIV Needle Stick Risk Assessment Stratification Protocol (RASP)"""
    
    def __init__(self):
        # Source population risk factors
        self.source_population_values = {
            "hiv_acute_aids": 1,  # Known HIV+: acute AIDS illness
            "hiv_asymptomatic": 10,  # Known HIV+: asymptomatic HIV
            "unknown_high_risk": 100,  # Unknown HIV status: high-risk situation
            "unknown_low_risk": 1000  # Unknown HIV status: low-risk situation
        }
        
        # Inoculum type risk factors
        self.inoculum_type_values = {
            "fresh_blood": 1,  # Fresh blood
            "high_risk_fluids": 10,  # Other high-risk fluids (e.g., semen)
            "dried_old_blood": 100,  # Dried old blood
            "low_risk_secretions": 1000  # Low-risk secretions (e.g., tears, urine, saliva)
        }
        
        # Method of transmission risk factors
        self.transmission_method_values = {
            "intravenous": 1,  # Intravenous
            "deep_intramuscular": 10,  # Deep intramuscular
            "deep_transcutaneous_bleeding": 100,  # Deep transcutaneous with visible bleeding
            "superficial_transcutaneous": 200,  # Superficial transcutaneous without bleeding
            "mucosal_contact": 500,  # Mucosal contact only
            "intact_skin": 1000  # Intact skin
        }
        
        # Volume of inoculum risk factors
        self.inoculum_volume_values = {
            "massive_transfusion": 100,  # Massive (e.g., transfusion)
            "measurable_over_1ml": 10,  # Measurable (>1 mL)
            "moderate_large_bore": 5,  # Moderate (large-bore, hollow needle >22 g)
            "small_small_bore": 3,  # Small (small-bore, hollow needle <22 g)
            "trace_surface_only": 1  # Trace surface only (e.g., suture needle)
        }
    
    def calculate(self, source_population: str, inoculum_type: str,
                  transmission_method: str, inoculum_volume: str) -> Dict[str, Any]:
        """
        Calculates the HIV transmission risk using RASP protocol
        
        Args:
            source_population (str): HIV status of source patient
            inoculum_type (str): Type of body fluid
            transmission_method (str): Method of exposure
            inoculum_volume (str): Volume of exposure
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(source_population, inoculum_type,
                            transmission_method, inoculum_volume)
        
        # Get risk values
        source_value = self.source_population_values[source_population]
        inoculum_type_value = self.inoculum_type_values[inoculum_type]
        transmission_value = self.transmission_method_values[transmission_method]
        volume_value = self.inoculum_volume_values[inoculum_volume]
        
        # Calculate basic risk
        # Basic risk = 1 / (Source population × Inoculum type × Method of transmission)
        basic_risk_denominator = source_value * inoculum_type_value * transmission_value
        
        # Total risk = Basic risk × Volume of inoculum
        # Risk is expressed as 1 in X
        total_risk_denominator = basic_risk_denominator / volume_value
        
        # Round to nearest integer for risk expression
        risk_ratio = round(total_risk_denominator)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_ratio)
        
        return {
            "result": risk_ratio,
            "unit": "risk_ratio",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, source_population: str, inoculum_type: str,
                        transmission_method: str, inoculum_volume: str):
        """Validates input parameters"""
        
        if source_population not in self.source_population_values:
            raise ValueError(f"Invalid source_population: {source_population}")
        
        if inoculum_type not in self.inoculum_type_values:
            raise ValueError(f"Invalid inoculum_type: {inoculum_type}")
        
        if transmission_method not in self.transmission_method_values:
            raise ValueError(f"Invalid transmission_method: {transmission_method}")
        
        if inoculum_volume not in self.inoculum_volume_values:
            raise ValueError(f"Invalid inoculum_volume: {inoculum_volume}")
    
    def _get_interpretation(self, risk_ratio: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the risk ratio
        
        Args:
            risk_ratio (int): Risk expressed as 1 in X
            
        Returns:
            Dict with interpretation
        """
        
        if risk_ratio <= 1000:
            return {
                "stage": "Definitely Indicated",
                "description": "Risk ≥1/1000",
                "interpretation": "Post-exposure prophylaxis (PEP) is definitely indicated. "
                                "Begin PEP as soon as possible, ideally within 2 hours but "
                                "up to 72 hours post-exposure. Continue for 28 days with "
                                "appropriate antiretroviral regimen."
            }
        elif risk_ratio <= 10000:
            return {
                "stage": "Recommended",
                "description": "Risk 1/1001-1/10000",
                "interpretation": "PEP is recommended but optional. Discuss risks and benefits "
                                "with the exposed individual. Consider severity of exposure, "
                                "source patient factors, and time since exposure."
            }
        elif risk_ratio <= 100000:
            return {
                "stage": "Optional",
                "description": "Risk 1/10001-1/100000",
                "interpretation": "PEP is optional but not generally recommended. May consider "
                                "in special circumstances or if exposed person has high anxiety. "
                                "Ensure appropriate counseling and follow-up."
            }
        else:
            return {
                "stage": "Not Indicated",
                "description": "Risk ≤1/100000",
                "interpretation": "PEP is not indicated. Risk of HIV transmission is negligible. "
                                "Provide reassurance and standard follow-up care. Consider "
                                "baseline HIV testing if warranted."
            }


def calculate_hiv_needle_stick_rasp(source_population: str, inoculum_type: str,
                                    transmission_method: str, inoculum_volume: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HivNeedleStickRaspCalculator()
    return calculator.calculate(source_population, inoculum_type,
                              transmission_method, inoculum_volume)