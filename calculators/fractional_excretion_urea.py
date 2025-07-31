"""
Fractional Excretion of Urea (FEUrea) Calculator

Determines the cause of renal failure. Similar to FENa, but can be used in patients 
on diuretics. More sensitive and specific than FENa for differentiating prerenal 
azotemia from acute tubular necrosis.

References:
1. Carvounis CP, Nisar S, Guro-Razuman S. Significance of the fractional excretion of 
   urea in the differential diagnosis of acute renal failure. Kidney Int. 2002;62(6):2223-9.
2. Kaplan AA, Kohn OF. Fractional excretion of urea as a guide to renal dysfunction. 
   Am J Nephrol. 1992;12(1-2):49-54.
3. Diskin CJ, Stokes TJ, Dansby LM, et al. The comparative benefits of the fractional 
   excretion of urea and sodium in various azotemic oliguric states. Nephron Clin Pract. 
   2010;114(2):c145-50.
4. Pahwa AK, Sperati CJ. Urinary Fractional Excretion Indices in the Evaluation of 
   Acute Kidney Injury. J Hosp Med. 2016;11(1):77-80.
"""

from typing import Dict, Any
import math


class FractionalExcretionUreaCalculator:
    """Calculator for Fractional Excretion of Urea (FEUrea)"""
    
    def __init__(self):
        # Interpretation thresholds
        self.PRERENAL_THRESHOLD = 35.0  # FEUrea < 35% suggests prerenal
        self.INTRINSIC_THRESHOLD = 50.0  # FEUrea > 50% suggests intrinsic
    
    def calculate(self, serum_urea: float, urine_urea: float, 
                  serum_creatinine: float, urine_creatinine: float) -> Dict[str, Any]:
        """
        Calculates the Fractional Excretion of Urea (FEUrea)
        
        Args:
            serum_urea (float): Serum/plasma urea concentration (mg/dL)
            urine_urea (float): Urine urea concentration (mg/dL)
            serum_creatinine (float): Serum/plasma creatinine concentration (mg/dL)
            urine_creatinine (float): Urine creatinine concentration (mg/dL)
            
        Returns:
            Dict with the FEUrea percentage and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(serum_urea, urine_urea, serum_creatinine, urine_creatinine)
        
        # Calculate FEUrea using the standard formula
        feurea_percentage = self._calculate_feurea(serum_urea, urine_urea, 
                                                  serum_creatinine, urine_creatinine)
        
        # Get interpretation
        interpretation = self._get_interpretation(feurea_percentage)
        
        return {
            "result": feurea_percentage,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, serum_urea: float, urine_urea: float, 
                        serum_creatinine: float, urine_creatinine: float):
        """Validates input parameters"""
        
        # Validate serum urea
        if not isinstance(serum_urea, (int, float)):
            raise ValueError("Serum urea must be a number")
        if serum_urea < 5 or serum_urea > 300:
            raise ValueError("Serum urea must be between 5 and 300 mg/dL")
        
        # Validate urine urea
        if not isinstance(urine_urea, (int, float)):
            raise ValueError("Urine urea must be a number")
        if urine_urea < 50 or urine_urea > 5000:
            raise ValueError("Urine urea must be between 50 and 5000 mg/dL")
        
        # Validate serum creatinine
        if not isinstance(serum_creatinine, (int, float)):
            raise ValueError("Serum creatinine must be a number")
        if serum_creatinine < 0.1 or serum_creatinine > 20.0:
            raise ValueError("Serum creatinine must be between 0.1 and 20.0 mg/dL")
        
        # Validate urine creatinine
        if not isinstance(urine_creatinine, (int, float)):
            raise ValueError("Urine creatinine must be a number")
        if urine_creatinine < 1 or urine_creatinine > 500:
            raise ValueError("Urine creatinine must be between 1 and 500 mg/dL")
        
        # Check for zero values that would cause division by zero
        if serum_urea == 0:
            raise ValueError("Serum urea cannot be zero")
        if urine_creatinine == 0:
            raise ValueError("Urine creatinine cannot be zero")
    
    def _calculate_feurea(self, serum_urea: float, urine_urea: float, 
                         serum_creatinine: float, urine_creatinine: float) -> float:
        """
        Calculates FEUrea using the standard formula
        
        Formula: FEUrea (%) = [(Urine Urea × Serum Creatinine) / (Serum Urea × Urine Creatinine)] × 100
        """
        
        # Calculate numerator and denominator
        numerator = urine_urea * serum_creatinine
        denominator = serum_urea * urine_creatinine
        
        # Calculate FEUrea as percentage
        feurea_percentage = (numerator / denominator) * 100
        
        # Round to 2 decimal places
        return round(feurea_percentage, 2)
    
    def _get_interpretation(self, feurea_percentage: float) -> Dict[str, str]:
        """
        Determines the interpretation based on FEUrea percentage
        
        Args:
            feurea_percentage (float): Calculated FEUrea percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if feurea_percentage < self.PRERENAL_THRESHOLD:
            return {
                "stage": "Prerenal AKI",
                "description": "Suggests prerenal azotemia",
                "interpretation": (f"FEUrea {feurea_percentage}% indicates prerenal cause of acute kidney injury. "
                                f"The kidneys are conserving urea due to decreased blood flow or volume depletion. "
                                f"Common causes include dehydration, heart failure, cirrhosis, or hepatorenal syndrome. "
                                f"Consider volume resuscitation and address underlying cause. FEUrea is reliable even "
                                f"in patients receiving diuretics.")
            }
        elif feurea_percentage < self.INTRINSIC_THRESHOLD:
            return {
                "stage": "Indeterminate",
                "description": "Intermediate range requiring clinical correlation",
                "interpretation": (f"FEUrea {feurea_percentage}% is in the intermediate range and may suggest early "
                                f"intrinsic renal disease or mixed conditions. This range can occur in early acute "
                                f"tubular necrosis or recovery phase. Further clinical correlation, additional testing, "
                                f"and careful assessment of the patient's clinical status are needed to determine the "
                                f"underlying cause of acute kidney injury.")
            }
        else:  # feurea_percentage >= 50.0
            return {
                "stage": "Intrinsic AKI",
                "description": "Suggests intrinsic renal pathology",
                "interpretation": (f"FEUrea {feurea_percentage}% indicates intrinsic renal pathology, most commonly "
                                f"acute tubular necrosis (ATN). May also suggest acute interstitial nephritis or other "
                                f"causes of intrinsic kidney failure with impaired urea reabsorption. Consider nephrology "
                                f"consultation and evaluate for specific causes of intrinsic AKI. FEUrea >70% is "
                                f"typically seen with established ATN.")
            }


def calculate_fractional_excretion_urea(serum_urea: float, urine_urea: float, 
                                       serum_creatinine: float, urine_creatinine: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fractional_excretion_urea pattern
    """
    calculator = FractionalExcretionUreaCalculator()
    return calculator.calculate(serum_urea, urine_urea, serum_creatinine, urine_creatinine)