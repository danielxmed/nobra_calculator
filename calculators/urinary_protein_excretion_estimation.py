"""
Urinary Protein Excretion Estimation Calculator

Quantifies 24h proteinuria with protein/creatinine ratio in single urine sample.
Provides a convenient alternative to 24-hour urine collection for estimating 
daily protein excretion in patients with stable renal function.

References:
- Ginsberg JM, Chang BS, Matarese RA, Garella S. Use of single voided urine samples 
  to estimate quantitative proteinuria. N Engl J Med. 1983;309(25):1543-6.
- Wahbeh AM, Ewais MH, Elsharif ME. Comparison of 24-hour urinary protein and 
  protein-to-creatinine ratio in the assessment of proteinuria. 
  Saudi J Kidney Dis Transpl. 2009;20(3):443-7.
"""

from typing import Dict, Any


class UrinaryProteinExcretionEstimationCalculator:
    """Calculator for Urinary Protein Excretion Estimation"""
    
    def __init__(self):
        # Clinical thresholds for protein excretion (g/day)
        self.NORMAL_THRESHOLD = 0.2
        self.NEPHROTIC_THRESHOLD = 3.5
    
    def calculate(self, urine_protein_mg_dl: float, urine_creatinine_mg_dl: float) -> Dict[str, Any]:
        """
        Calculates the estimated 24-hour urinary protein excretion using the 
        protein/creatinine ratio from a single urine sample
        
        Args:
            urine_protein_mg_dl (float): Urine protein concentration in mg/dL (0-1000)
            urine_creatinine_mg_dl (float): Urine creatinine concentration in mg/dL (10-500)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(urine_protein_mg_dl, urine_creatinine_mg_dl)
        
        # Calculate 24-hour protein excretion
        protein_excretion_24h = self._calculate_formula(urine_protein_mg_dl, urine_creatinine_mg_dl)
        
        # Get interpretation
        interpretation = self._get_interpretation(protein_excretion_24h)
        
        return {
            "result": protein_excretion_24h,
            "unit": "g/day",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, urine_protein_mg_dl: float, urine_creatinine_mg_dl: float):
        """Validates input parameters"""
        
        # Validate urine protein
        if not isinstance(urine_protein_mg_dl, (int, float)) or urine_protein_mg_dl < 0:
            raise ValueError("Urine protein must be a non-negative number")
        if urine_protein_mg_dl > 1000:
            raise ValueError("Urine protein must be ≤1000 mg/dL")
        
        # Validate urine creatinine
        if not isinstance(urine_creatinine_mg_dl, (int, float)) or urine_creatinine_mg_dl <= 0:
            raise ValueError("Urine creatinine must be a positive number")
        if urine_creatinine_mg_dl < 10:
            raise ValueError("Urine creatinine must be ≥10 mg/dL")
        if urine_creatinine_mg_dl > 500:
            raise ValueError("Urine creatinine must be ≤500 mg/dL")
    
    def _calculate_formula(self, urine_protein_mg_dl: float, urine_creatinine_mg_dl: float) -> float:
        """
        Implements the urinary protein excretion estimation formula
        
        Formula: 24-hour Urinary Protein Excretion (g/day) = Urine Protein (mg/dL) / Urine Creatinine (mg/dL)
        
        The ratio of protein to creatinine in mg/dL approximates the 24-hour protein excretion in g/day
        because creatinine excretion is relatively constant at approximately 1 g/day in most adults.
        """
        
        # Calculate protein/creatinine ratio
        protein_excretion_24h = urine_protein_mg_dl / urine_creatinine_mg_dl
        
        # Round to 2 decimal places
        return round(protein_excretion_24h, 2)
    
    def _get_interpretation(self, protein_excretion_24h: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the estimated 24-hour protein excretion
        
        Args:
            protein_excretion_24h (float): Calculated 24-hour protein excretion in g/day
            
        Returns:
            Dict with interpretation details
        """
        
        if protein_excretion_24h < self.NORMAL_THRESHOLD:
            return {
                "stage": "Normal",
                "description": "Within normal limits",
                "interpretation": f"Estimated 24-hour protein excretion of {protein_excretion_24h} g/day is within normal limits (<0.2 g/day). No evidence of significant proteinuria. Continue routine monitoring as clinically indicated. No specific nephrology intervention required at this time."
            }
        elif protein_excretion_24h < self.NEPHROTIC_THRESHOLD:
            return {
                "stage": "Abnormal Proteinuria",
                "description": "Investigate further",
                "interpretation": f"Estimated 24-hour protein excretion of {protein_excretion_24h} g/day indicates abnormal proteinuria (0.2-3.5 g/day). This level warrants further investigation to determine the underlying cause. Consider additional testing including serum creatinine, eGFR, urinalysis with microscopy, and nephrology consultation if persistent. Rule out diabetes, hypertension, and other causes of chronic kidney disease."
            }
        else:
            return {
                "stage": "Nephrotic Range",
                "description": "Nephrotic range proteinuria",
                "interpretation": f"Estimated 24-hour protein excretion of {protein_excretion_24h} g/day indicates nephrotic range proteinuria (>3.5 g/day). This suggests significant glomerular disease and requires urgent nephrology evaluation. Investigate for nephrotic syndrome causes including minimal change disease, focal segmental glomerulosclerosis, membranous nephropathy, and systemic diseases. Consider renal biopsy, lipid profile, and albumin levels."
            }


def calculate_urinary_protein_excretion_estimation(urine_protein_mg_dl: float, urine_creatinine_mg_dl: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = UrinaryProteinExcretionEstimationCalculator()
    return calculator.calculate(urine_protein_mg_dl, urine_creatinine_mg_dl)