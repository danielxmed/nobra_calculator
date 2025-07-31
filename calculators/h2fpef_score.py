"""
H2FPEF Score Calculator

Estimates probability of heart failure with preserved ejection fraction (HFpEF) 
in euvolemic patients with unexplained exertional dyspnea who have had an echocardiogram.

References:
1. Reddy YNV, Carter RE, Obokata M, Redfield MM, Borlaug BA. A Simple, Evidence-Based 
   Approach to Help Guide Diagnosis of Heart Failure With Preserved Ejection Fraction. 
   Circulation. 2018;138(9):861-870. doi: 10.1161/CIRCULATIONAHA.118.034646
2. Borlaug BA, Reddy YNV. The Role of the Pulmonary Circulation in Heart Failure With 
   Preserved Ejection Fraction. JACC Heart Fail. 2019;7(5):393-403.
"""

import math
from typing import Dict, Any


class H2fpefScoreCalculator:
    """Calculator for H2FPEF Score for Heart Failure with Preserved Ejection Fraction"""
    
    def __init__(self):
        # Formula constants from the original validation study
        self.INTERCEPT = -9.1917
        self.AGE_COEFFICIENT = 0.0451
        self.BMI_COEFFICIENT = 0.1307
        self.E_E_PRIME_COEFFICIENT = 0.0859
        self.PASP_COEFFICIENT = 0.0520
        self.ATRIAL_FIB_COEFFICIENT = 1.6997
    
    def calculate(self, age: int, bmi: float, e_e_prime_ratio: float, 
                  pasp: int, atrial_fibrillation: str) -> Dict[str, Any]:
        """
        Calculates the H2FPEF Score probability using the provided parameters
        
        Args:
            age (int): Patient age in years
            bmi (float): Body mass index in kg/m²
            e_e_prime_ratio (float): Echocardiographic E/e' ratio
            pasp (int): Pulmonary artery systolic pressure in mmHg
            atrial_fibrillation (str): History of atrial fibrillation ("yes" or "no")
            
        Returns:
            Dict with the probability result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, bmi, e_e_prime_ratio, pasp, atrial_fibrillation)
        
        # Calculate probability using the H2FPEF formula
        probability = self._calculate_probability(age, bmi, e_e_prime_ratio, pasp, atrial_fibrillation)
        
        # Get interpretation
        interpretation = self._get_interpretation(probability, age, bmi, e_e_prime_ratio, pasp, atrial_fibrillation)
        
        return {
            "result": round(probability, 1),
            "unit": "percentage",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, bmi: float, e_e_prime_ratio: float, 
                        pasp: int, atrial_fibrillation: str):
        """Validates input parameters"""
        
        # Age validation
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        # BMI validation
        if not isinstance(bmi, (int, float)) or bmi < 10.0 or bmi > 80.0:
            raise ValueError("BMI must be between 10.0 and 80.0 kg/m²")
        
        # E/e' ratio validation
        if not isinstance(e_e_prime_ratio, (int, float)) or e_e_prime_ratio < 1.0 or e_e_prime_ratio > 50.0:
            raise ValueError("E/e' ratio must be between 1.0 and 50.0")
        
        # PASP validation
        if not isinstance(pasp, int) or pasp < 15 or pasp > 120:
            raise ValueError("PASP must be an integer between 15 and 120 mmHg")
        
        # Atrial fibrillation validation
        if atrial_fibrillation not in ["yes", "no"]:
            raise ValueError("Atrial fibrillation must be 'yes' or 'no'")
    
    def _calculate_probability(self, age: int, bmi: float, e_e_prime_ratio: float, 
                              pasp: int, atrial_fibrillation: str) -> float:
        """
        Implements the H2FPEF probability calculation formula
        
        Formula: Probability = (Z / (1 + Z)) × 100
        Where Z = e^y and y = -9.1917 + (0.0451 × age) + (0.1307 × BMI) + 
                  (0.0859 × E/e' ratio) + (0.0520 × PASP) + (1.6997 × atrial fibrillation)
        """
        
        # Convert atrial fibrillation to numeric value
        af_value = 1 if atrial_fibrillation == "yes" else 0
        
        # Calculate y value
        y = (self.INTERCEPT + 
             (self.AGE_COEFFICIENT * age) + 
             (self.BMI_COEFFICIENT * bmi) + 
             (self.E_E_PRIME_COEFFICIENT * e_e_prime_ratio) + 
             (self.PASP_COEFFICIENT * pasp) + 
             (self.ATRIAL_FIB_COEFFICIENT * af_value))
        
        # Calculate Z = e^y
        try:
            z = math.exp(y)
        except OverflowError:
            # Handle very large exponentials
            z = float('inf')
        
        # Calculate probability = (Z / (1 + Z)) × 100
        if z == float('inf'):
            probability = 100.0
        else:
            probability = (z / (1 + z)) * 100
        
        return min(100.0, max(0.0, probability))
    
    def _get_interpretation(self, probability: float, age: int, bmi: float, 
                           e_e_prime_ratio: float, pasp: int, atrial_fibrillation: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the probability result
        
        Args:
            probability (float): Calculated HFpEF probability
            age, bmi, e_e_prime_ratio, pasp, atrial_fibrillation: Input parameters
            
        Returns:
            Dict with interpretation details
        """
        
        # Format patient characteristics
        af_text = "present" if atrial_fibrillation == "yes" else "absent"
        
        patient_summary = (f"Patient characteristics: {age} years old, BMI {bmi:.1f} kg/m², "
                          f"E/e' ratio {e_e_prime_ratio:.1f}, PASP {pasp} mmHg, "
                          f"atrial fibrillation {af_text}.")
        
        # Determine risk category and recommendations
        if probability < 25:
            stage = "Low Probability"
            description = "Low probability of HFpEF"
            clinical_recs = (
                "Low probability of heart failure with preserved ejection fraction "
                f"({probability:.1f}%). Consider alternate causes of dyspnea including "
                "pulmonary causes (asthma, COPD, interstitial lung disease, pulmonary "
                "embolism), metabolic causes (anemia, thyroid disorders, deconditioning), "
                "or other cardiac causes (coronary artery disease, valvular disease). "
                "HFpEF is unlikely and further cardiac workup may not be indicated unless "
                "other clinical features suggest cardiac etiology."
            )
        elif probability <= 75:
            stage = "Intermediate Probability"
            description = "Intermediate probability of HFpEF"
            clinical_recs = (
                f"Intermediate probability of heart failure with preserved ejection fraction "
                f"({probability:.1f}%). Additional testing is recommended to confirm or rule out "
                "HFpEF. Consider: (1) Invasive hemodynamic exercise testing (gold standard), "
                "(2) Natriuretic peptides (BNP/NT-proBNP), (3) Stress echocardiography, "
                "(4) Cardiac catheterization if indicated, (5) Advanced imaging (cardiac MRI, "
                "cardiac CT). Clinical correlation with symptoms, functional capacity, and "
                "response to diuretics may also provide diagnostic insights."
            )
        else:
            stage = "High Probability"
            description = "High probability of HFpEF"
            clinical_recs = (
                f"High probability of heart failure with preserved ejection fraction "
                f"({probability:.1f}%). HFpEF is likely and empiric treatment should be "
                "considered. Initiate guideline-directed medical therapy including: "
                "(1) ACE inhibitors/ARBs or ARNIs, (2) Aldosterone receptor antagonists, "
                "(3) SGLT2 inhibitors, (4) Beta-blockers if indicated. Address comorbidities: "
                "hypertension control, diabetes management, obesity reduction, sleep apnea "
                "treatment. Lifestyle modifications: sodium restriction, fluid management, "
                "exercise training as tolerated. Regular cardiology follow-up and monitoring "
                "for progression or decompensation."
            )
        
        # Important considerations
        considerations = (
            "Important considerations: The H2FPEF score was derived and validated in "
            "patients with unexplained exertional dyspnea and provides probability estimates "
            "for HFpEF diagnosis. This score should be used in euvolemic patients who have "
            "undergone echocardiographic assessment. Clinical judgment remains essential, "
            "and individual patient factors may modify the diagnostic probability. The score "
            "demonstrates superior performance compared to consensus-based algorithms with "
            "an area under the curve of 0.841 in validation studies."
        )
        
        full_interpretation = f"{patient_summary} H2FPEF probability: {probability:.1f}%. Risk Category: {stage} ({description}). Clinical recommendations: {clinical_recs} {considerations}"
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": full_interpretation
        }


def calculate_h2fpef_score(age: int, bmi: float, e_e_prime_ratio: float, 
                          pasp: int, atrial_fibrillation: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_h2fpef_score pattern
    """
    calculator = H2fpefScoreCalculator()
    return calculator.calculate(age, bmi, e_e_prime_ratio, pasp, atrial_fibrillation)