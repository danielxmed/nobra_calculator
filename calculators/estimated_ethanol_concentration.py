"""
Estimated Ethanol (and Toxic Alcohol) Serum Concentration Based on Ingestion Calculator

Predicts serum concentration of ethanol and toxic alcohols based on amount ingested
and patient weight using volume of distribution principles.

References:
1. Baselt RC. Disposition of toxic drugs and chemicals in man. 11th ed. 
   Seal Beach, CA: Biomedical Publications; 2017.
2. Barceloux DG, Bond GR, Krenzelok EP, Cooper H, Vale JA; American Academy of 
   Clinical Toxicology Ad Hoc Committee on the Treatment Guidelines for Methanol 
   Poisoning. American Academy of Clinical Toxicology practice guidelines on the 
   treatment of methanol poisoning. J Toxicol Clin Toxicol. 2002;40(4):415-46.
3. Brent J, McMartin K, Phillips S, Aaron C, Kulig K; Methylpyrazole for Toxic 
   Alcohols Study Group. Fomepizole for the treatment of methanol poisoning. 
   N Engl J Med. 2001 Feb 8;344(6):424-9.
"""

from typing import Dict, Any, Optional


class EstimatedEthanolConcentrationCalculator:
    """Calculator for Estimated Ethanol and Toxic Alcohol Serum Concentration"""
    
    def __init__(self):
        """Initialize calculator with constants"""
        # Volume of distribution (L/kg)
        self.VOLUME_OF_DISTRIBUTION = 0.6
        
        # Alcohol densities (g/mL)
        self.ALCOHOL_DENSITIES = {
            "ethanol": 0.789,
            "methanol": 0.792,
            "ethylene_glycol": 1.113,
            "isopropanol": 0.785
        }
        
        # Molecular weights (g/mol) for conversion factors
        self.MOLECULAR_WEIGHTS = {
            "ethanol": 46.07,
            "methanol": 32.04,
            "ethylene_glycol": 62.07,
            "isopropanol": 60.1
        }
        
        # Conversion factors to convert mg/dL to mmol/L
        self.CONVERSION_FACTORS = {
            "ethanol": 4.6,     # mg/dL ÷ 4.6 = mmol/L
            "methanol": 3.2,    # mg/dL ÷ 3.2 = mmol/L
            "ethylene_glycol": 6.2,  # mg/dL ÷ 6.2 = mmol/L
            "isopropanol": 6.0   # mg/dL ÷ 6.0 = mmol/L
        }
        
        # Treatment thresholds (mg/dL)
        self.TREATMENT_THRESHOLDS = {
            "methanol": 20,
            "ethylene_glycol": 20
        }
    
    def calculate(self, alcohol_type: str, amount_ingested_ml: float, 
                 weight_kg: float, alcohol_percentage: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates estimated serum alcohol concentration
        
        Args:
            alcohol_type (str): Type of alcohol (ethanol, methanol, ethylene_glycol, isopropanol)
            amount_ingested_ml (float): Amount of pure alcohol ingested in mL
            weight_kg (float): Patient body weight in kg
            alcohol_percentage (float, optional): Percentage of alcohol in beverage
            
        Returns:
            Dict with estimated concentration and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(alcohol_type, amount_ingested_ml, weight_kg, alcohol_percentage)
        
        # Calculate actual amount of pure alcohol if percentage given
        if alcohol_percentage is not None:
            actual_amount_ml = amount_ingested_ml * (alcohol_percentage / 100)
        else:
            actual_amount_ml = amount_ingested_ml
        
        # Calculate serum concentration
        concentration_mg_dl = self._calculate_concentration(alcohol_type, actual_amount_ml, weight_kg)
        
        # Convert to mmol/L
        concentration_mmol_l = concentration_mg_dl / self.CONVERSION_FACTORS[alcohol_type]
        
        # Get interpretation
        interpretation = self._get_interpretation(alcohol_type, concentration_mg_dl)
        
        return {
            "result": "calculated_concentration",
            "unit": "various",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "concentration_mg_dl": round(concentration_mg_dl, 1),
            "concentration_mmol_l": round(concentration_mmol_l, 1),
            "alcohol_type": alcohol_type,
            "amount_pure_alcohol_ml": round(actual_amount_ml, 1)
        }
    
    def _validate_inputs(self, alcohol_type: str, amount_ingested_ml: float, 
                        weight_kg: float, alcohol_percentage: Optional[float]):
        """Validates input parameters"""
        
        valid_alcohol_types = ["ethanol", "methanol", "ethylene_glycol", "isopropanol"]
        if alcohol_type not in valid_alcohol_types:
            raise ValueError(f"alcohol_type must be one of {valid_alcohol_types}")
        
        if not isinstance(amount_ingested_ml, (int, float)) or amount_ingested_ml < 0:
            raise ValueError("amount_ingested_ml must be a non-negative number")
        
        if amount_ingested_ml > 1000:
            raise ValueError("amount_ingested_ml must be ≤1000 mL")
        
        if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
            raise ValueError("weight_kg must be a positive number")
        
        if weight_kg > 300:
            raise ValueError("weight_kg must be ≤300 kg")
        
        if alcohol_percentage is not None:
            if not isinstance(alcohol_percentage, (int, float)):
                raise ValueError("alcohol_percentage must be a number")
            if alcohol_percentage < 0 or alcohol_percentage > 100:
                raise ValueError("alcohol_percentage must be between 0 and 100")
    
    def _calculate_concentration(self, alcohol_type: str, amount_ml: float, weight_kg: float) -> float:
        """
        Calculates serum concentration using volume of distribution
        
        Args:
            alcohol_type (str): Type of alcohol
            amount_ml (float): Amount in mL
            weight_kg (float): Body weight in kg
            
        Returns:
            float: Serum concentration in mg/dL
        """
        
        # Convert volume to mass (mg)
        density_g_ml = self.ALCOHOL_DENSITIES[alcohol_type]
        amount_mg = amount_ml * density_g_ml * 1000  # Convert g to mg
        
        # Calculate volume of distribution (L)
        vd_l = self.VOLUME_OF_DISTRIBUTION * weight_kg
        
        # Calculate concentration (mg/L)
        concentration_mg_l = amount_mg / vd_l
        
        # Convert to mg/dL
        concentration_mg_dl = concentration_mg_l / 10
        
        return concentration_mg_dl
    
    def _get_interpretation(self, alcohol_type: str, concentration_mg_dl: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on alcohol type and concentration
        
        Args:
            alcohol_type (str): Type of alcohol
            concentration_mg_dl (float): Concentration in mg/dL
            
        Returns:
            Dict with interpretation details
        """
        
        if alcohol_type == "ethanol":
            return self._interpret_ethanol(concentration_mg_dl)
        elif alcohol_type in ["methanol", "ethylene_glycol"]:
            return self._interpret_toxic_alcohol(alcohol_type, concentration_mg_dl)
        else:  # isopropanol
            return self._interpret_isopropanol(concentration_mg_dl)
    
    def _interpret_ethanol(self, concentration: float) -> Dict[str, str]:
        """Interprets ethanol concentration"""
        
        if concentration < 50:
            return {
                "stage": "Mild Intoxication",
                "description": "Mild effects",
                "interpretation": (
                    f"Estimated ethanol concentration: {concentration:.1f} mg/dL "
                    f"({concentration/4.6:.1f} mmol/L). Mild intoxication. May cause euphoria, "
                    f"decreased inhibition, and mild impairment of judgment and coordination. "
                    f"Monitor patient and provide supportive care as needed."
                )
            }
        elif concentration < 100:
            return {
                "stage": "Moderate Intoxication",
                "description": "Moderate effects", 
                "interpretation": (
                    f"Estimated ethanol concentration: {concentration:.1f} mg/dL "
                    f"({concentration/4.6:.1f} mmol/L). Moderate intoxication. Significant "
                    f"impairment of motor control, reaction time, and judgment. Legal intoxication "
                    f"in most jurisdictions. Monitor closely and provide supportive care."
                )
            }
        elif concentration < 300:
            return {
                "stage": "Severe Intoxication",
                "description": "Severe effects",
                "interpretation": (
                    f"Estimated ethanol concentration: {concentration:.1f} mg/dL "
                    f"({concentration/4.6:.1f} mmol/L). Severe intoxication. Risk of respiratory "
                    f"depression, coma, and death. Requires immediate medical attention and "
                    f"intensive monitoring."
                )
            }
        else:
            return {
                "stage": "Life-threatening",
                "description": "Critical level",
                "interpretation": (
                    f"Estimated ethanol concentration: {concentration:.1f} mg/dL "
                    f"({concentration/4.6:.1f} mmol/L). Life-threatening alcohol poisoning. "
                    f"High risk of respiratory failure, coma, and death. Requires emergency "
                    f"intervention including possible intubation and hemodialysis."
                )
            }
    
    def _interpret_toxic_alcohol(self, alcohol_type: str, concentration: float) -> Dict[str, str]:
        """Interprets methanol or ethylene glycol concentration"""
        
        threshold = self.TREATMENT_THRESHOLDS[alcohol_type]
        conversion_factor = self.CONVERSION_FACTORS[alcohol_type]
        
        if concentration >= threshold:
            return {
                "stage": "Treatment Required",
                "description": "Above treatment threshold",
                "interpretation": (
                    f"Estimated {alcohol_type.replace('_', ' ')} concentration: {concentration:.1f} mg/dL "
                    f"({concentration/conversion_factor:.1f} mmol/L). Level ≥{threshold} mg/dL requires "
                    f"immediate treatment with fomepizole (preferred) or ethanol, plus hemodialysis. "
                    f"{alcohol_type.replace('_', ' ').title()} is highly toxic and can cause severe "
                    f"metabolic acidosis and end-organ damage."
                )
            }
        else:
            return {
                "stage": "Below Treatment Threshold",
                "description": "Monitor closely",
                "interpretation": (
                    f"Estimated {alcohol_type.replace('_', ' ')} concentration: {concentration:.1f} mg/dL "
                    f"({concentration/conversion_factor:.1f} mmol/L). Below treatment threshold of "
                    f"{threshold} mg/dL, but monitor closely for symptoms and obtain serial levels. "
                    f"Consider treatment if patient is symptomatic or has metabolic acidosis."
                )
            }
    
    def _interpret_isopropanol(self, concentration: float) -> Dict[str, str]:
        """Interprets isopropanol concentration"""
        
        return {
            "stage": "Isopropanol Exposure",
            "description": "Monitor for CNS effects",
            "interpretation": (
                f"Estimated isopropanol concentration: {concentration:.1f} mg/dL "
                f"({concentration/6.0:.1f} mmol/L). Isopropanol is less toxic than methanol "
                f"or ethylene glycol but can cause significant CNS depression. Monitor for "
                f"altered mental status, respiratory depression, and hypotension. Supportive "
                f"care is usually sufficient. Hemodialysis reserved for severe cases."
            )
        }


def calculate_estimated_ethanol_concentration(alcohol_type: str, amount_ingested_ml: float,
                                            weight_kg: float, alcohol_percentage: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_estimated_ethanol_concentration pattern
    """
    calculator = EstimatedEthanolConcentrationCalculator()
    return calculator.calculate(alcohol_type, amount_ingested_ml, weight_kg, alcohol_percentage)