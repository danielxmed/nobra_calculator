"""
Fractional Excretion of Sodium (FENa) Calculator

Determines if renal failure is due to pre-renal or intrinsic pathology. Calculates 
the percentage of filtered sodium that is excreted in the urine.

References:
1. Espinel CH. The FENa test. Use in the differential diagnosis of acute renal failure. 
   JAMA. 1976;236(6):579-81.
2. Miller TR, Anderson RJ, Linas SL, et al. Urinary diagnostic indices in acute renal 
   failure: a prospective study. Ann Intern Med. 1978;89(1):47-50.
3. Steiner RW. Interpreting the fractional excretion of sodium. Am J Med. 1984;77(4):699-702.
4. Pahwa AK, Sperati CJ. Urinary Fractional Excretion Indices in the Evaluation of 
   Acute Kidney Injury. J Hosp Med. 2016;11(1):77-80.
"""

from typing import Dict, Any
import math


class FractionalExcretionSodiumCalculator:
    """Calculator for Fractional Excretion of Sodium (FENa)"""
    
    def __init__(self):
        # Interpretation thresholds
        self.PRERENAL_THRESHOLD = 1.0  # FENa < 1% suggests prerenal
        self.INTRINSIC_THRESHOLD = 2.0  # FENa > 2% suggests intrinsic
    
    def calculate(self, serum_sodium: float, urine_sodium: float, 
                  serum_creatinine: float, urine_creatinine: float) -> Dict[str, Any]:
        """
        Calculates the Fractional Excretion of Sodium (FENa)
        
        Args:
            serum_sodium (float): Serum/plasma sodium concentration (mEq/L)
            urine_sodium (float): Urine sodium concentration (mEq/L)
            serum_creatinine (float): Serum/plasma creatinine concentration (mg/dL)
            urine_creatinine (float): Urine creatinine concentration (mg/dL)
            
        Returns:
            Dict with the FENa percentage and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(serum_sodium, urine_sodium, serum_creatinine, urine_creatinine)
        
        # Calculate FENa using the standard formula
        fena_percentage = self._calculate_fena(serum_sodium, urine_sodium, 
                                              serum_creatinine, urine_creatinine)
        
        # Get interpretation
        interpretation = self._get_interpretation(fena_percentage)
        
        return {
            "result": fena_percentage,
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, serum_sodium: float, urine_sodium: float, 
                        serum_creatinine: float, urine_creatinine: float):
        """Validates input parameters"""
        
        # Validate serum sodium
        if not isinstance(serum_sodium, (int, float)):
            raise ValueError("Serum sodium must be a number")
        if serum_sodium < 120 or serum_sodium > 180:
            raise ValueError("Serum sodium must be between 120 and 180 mEq/L")
        
        # Validate urine sodium
        if not isinstance(urine_sodium, (int, float)):
            raise ValueError("Urine sodium must be a number")
        if urine_sodium < 1 or urine_sodium > 300:
            raise ValueError("Urine sodium must be between 1 and 300 mEq/L")
        
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
        if serum_sodium == 0:
            raise ValueError("Serum sodium cannot be zero")
        if urine_creatinine == 0:
            raise ValueError("Urine creatinine cannot be zero")
    
    def _calculate_fena(self, serum_sodium: float, urine_sodium: float, 
                       serum_creatinine: float, urine_creatinine: float) -> float:
        """
        Calculates FENa using the standard formula
        
        Formula: FENa (%) = [(Urine Sodium × Serum Creatinine) / (Serum Sodium × Urine Creatinine)] × 100
        """
        
        # Calculate numerator and denominator
        numerator = urine_sodium * serum_creatinine
        denominator = serum_sodium * urine_creatinine
        
        # Calculate FENa as percentage
        fena_percentage = (numerator / denominator) * 100
        
        # Round to 2 decimal places
        return round(fena_percentage, 2)
    
    def _get_interpretation(self, fena_percentage: float) -> Dict[str, str]:
        """
        Determines the interpretation based on FENa percentage
        
        Args:
            fena_percentage (float): Calculated FENa percentage
            
        Returns:
            Dict with interpretation details
        """
        
        if fena_percentage < self.PRERENAL_THRESHOLD:
            return {
                "stage": "Prerenal AKI",
                "description": "Suggests prerenal azotemia",
                "interpretation": (f"FENa {fena_percentage}% typically indicates prerenal cause of acute kidney injury. "
                                f"The kidneys are conserving sodium due to decreased blood flow or volume depletion. "
                                f"Common causes include dehydration, heart failure, cirrhosis, or hepatorenal syndrome. "
                                f"Consider volume resuscitation and address underlying cause.")
            }
        elif fena_percentage < self.INTRINSIC_THRESHOLD:
            return {
                "stage": "Indeterminate",
                "description": "Intermediate range requiring clinical correlation",
                "interpretation": (f"FENa {fena_percentage}% is in the intermediate range and can be seen in both prerenal "
                                f"and intrinsic renal conditions. Further clinical correlation, additional testing, "
                                f"and careful assessment of the patient's volume status are needed to determine the "
                                f"underlying cause of acute kidney injury.")
            }
        else:  # fena_percentage >= 2.0
            return {
                "stage": "Intrinsic AKI",
                "description": "Suggests intrinsic renal pathology",
                "interpretation": (f"FENa {fena_percentage}% typically indicates intrinsic renal pathology, most commonly "
                                f"acute tubular necrosis (ATN). May also suggest severe obstruction or other causes of "
                                f"intrinsic kidney failure with impaired sodium reabsorption. Consider nephrology "
                                f"consultation and evaluate for specific causes of intrinsic AKI.")
            }


def calculate_fractional_excretion_sodium(serum_sodium: float, urine_sodium: float, 
                                         serum_creatinine: float, urine_creatinine: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_fractional_excretion_sodium pattern
    """
    calculator = FractionalExcretionSodiumCalculator()
    return calculator.calculate(serum_sodium, urine_sodium, serum_creatinine, urine_creatinine)