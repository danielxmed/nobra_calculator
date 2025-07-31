"""
GALAD Model for Hepatocellular Carcinoma (HCC) Calculator

Diagnoses HCC based on serum biomarkers in patients with chronic liver disease.

References:
1. Johnson PJ, Pirrie SJ, Cox TF, et al. The detection of hepatocellular carcinoma using 
   a prospectively developed and validated model based on serological biomarkers. Cancer 
   Epidemiol Biomarkers Prev. 2014;23(1):144-53. doi: 10.1158/1055-9965.EPI-13-0870.
2. Best J, Bechmann LP, Sowa JP, et al. GALAD Score Detects Early Hepatocellular Carcinoma 
   in an International Cohort of Patients With Nonalcoholic Steatohepatitis. Clin Gastroenterol 
   Hepatol. 2020;18(3):728-735.e4. doi: 10.1016/j.cgh.2019.08.012.
3. Yang JD, Addissie BD, Mara KC, et al. GALAD Score for Hepatocellular Carcinoma Detection 
   in Comparison with Liver Ultrasound and Proposal of GALADUS Score. Cancer Epidemiol 
   Biomarkers Prev. 2019;28(3):531-538. doi: 10.1158/1055-9965.EPI-18-0281.

The GALAD model combines Gender, Age, AFP-L3, AFP, and DCP to provide superior diagnostic 
accuracy for HCC detection compared to individual biomarkers.
"""

import math
from typing import Dict, Any


class GaladModelHccCalculator:
    """Calculator for GALAD Model for Hepatocellular Carcinoma Detection"""
    
    def __init__(self):
        # GALAD model coefficients from validated studies
        self.INTERCEPT = -10.08
        self.AGE_COEFFICIENT = 0.09
        self.SEX_COEFFICIENT = 1.67  # 1 for males, 0 for females
        self.AFP_COEFFICIENT = 2.34
        self.AFP_L3_COEFFICIENT = 0.04
        self.DCP_COEFFICIENT = 1.33
        
        # Clinical threshold for HCC probability
        self.HCC_THRESHOLD = -0.63  # GALAD score threshold for high HCC probability
        
        # Lower limits of quantitation (LLOQ) for biomarkers
        self.AFP_LLOQ = 0.5  # ng/mL
        self.AFP_L3_LLOQ = 0.5  # %
        self.DCP_LLOQ = 7.5  # mAU/mL
    
    def calculate(self, age: int, sex: str, afp: float, 
                  afp_l3_percentage: float, dcp: float) -> Dict[str, Any]:
        """
        Calculates the GALAD score for HCC detection
        
        Args:
            age (int): Patient's age in years
            sex (str): Patient's biological sex ('male' or 'female')
            afp (float): Alpha-fetoprotein level in ng/mL
            afp_l3_percentage (float): AFP-L3 percentage (0-100%)
            dcp (float): Des-gamma-carboxy prothrombin level in mAU/mL
            
        Returns:
            Dict with GALAD score and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(age, sex, afp, afp_l3_percentage, dcp)
        
        # Apply LLOQ when values are below detection limits
        afp_adjusted = max(afp, self.AFP_LLOQ)
        afp_l3_adjusted = max(afp_l3_percentage, self.AFP_L3_LLOQ)
        dcp_adjusted = max(dcp, self.DCP_LLOQ)
        
        # Calculate GALAD score
        galad_score = self._calculate_galad_score(
            age, sex, afp_adjusted, afp_l3_adjusted, dcp_adjusted
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(galad_score)
        
        return {
            "result": round(galad_score, 3),
            "unit": "score",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, afp: float, 
                        afp_l3_percentage: float, dcp: float):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Age must be an integer between 18 and 100 years")
        
        if sex not in ['male', 'female']:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(afp, (int, float)) or afp < 0.1 or afp > 100000:
            raise ValueError("AFP must be a number between 0.1 and 100,000 ng/mL")
        
        if not isinstance(afp_l3_percentage, (int, float)) or afp_l3_percentage < 0 or afp_l3_percentage > 100:
            raise ValueError("AFP-L3 percentage must be between 0 and 100%")
        
        if not isinstance(dcp, (int, float)) or dcp < 1 or dcp > 100000:
            raise ValueError("DCP must be a number between 1 and 100,000 mAU/mL")
    
    def _calculate_galad_score(self, age: int, sex: str, afp: float, 
                              afp_l3_percentage: float, dcp: float) -> float:
        """
        Implements the GALAD model mathematical formula
        
        Formula: Z = -10.08 + 0.09 × age + 1.67 × sex + 2.34 × log₁₀(AFP) + 0.04 × AFP-L3 + 1.33 × log₁₀(DCP)
        Where sex = 1 for males, 0 for females
        """
        
        # Convert sex to numeric value
        sex_numeric = 1 if sex == 'male' else 0
        
        # Calculate log base 10 values with safety checks
        log_afp = math.log10(max(afp, 0.1))  # Ensure positive value for log
        log_dcp = math.log10(max(dcp, 1.0))  # Ensure positive value for log
        
        # Apply GALAD formula
        galad_score = (
            self.INTERCEPT +
            self.AGE_COEFFICIENT * age +
            self.SEX_COEFFICIENT * sex_numeric +
            self.AFP_COEFFICIENT * log_afp +
            self.AFP_L3_COEFFICIENT * afp_l3_percentage +
            self.DCP_COEFFICIENT * log_dcp
        )
        
        return galad_score
    
    def _get_interpretation(self, galad_score: float) -> Dict[str, str]:
        """
        Determines clinical interpretation based on GALAD score
        
        Args:
            galad_score (float): Calculated GALAD score
            
        Returns:
            Dict with interpretation
        """
        
        if galad_score < self.HCC_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low probability of HCC",
                "interpretation": (f"GALAD score of {galad_score:.3f} is below the threshold of {self.HCC_THRESHOLD}, "
                                f"suggesting low probability of hepatocellular carcinoma. Continue routine surveillance "
                                f"in high-risk patients with chronic liver disease. Consider repeat assessment in "
                                f"3-6 months or if clinical status changes. This result does not rule out HCC entirely; "
                                f"clinical correlation and imaging may still be indicated based on other risk factors.")
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High probability of HCC",
                "interpretation": (f"GALAD score of {galad_score:.3f} meets or exceeds the threshold of {self.HCC_THRESHOLD}, "
                                f"suggesting high probability of hepatocellular carcinoma. Recommend urgent further "
                                f"diagnostic evaluation including contrast-enhanced CT or MRI imaging of the liver. "
                                f"Consider multidisciplinary team consultation with hepatology and oncology. "
                                f"The GALAD model has 85.6% sensitivity and 93.3% specificity for HCC detection. "
                                f"Early detection and treatment improve outcomes significantly.")
            }


def calculate_galad_model_hcc(age: int, sex: str, afp: float, 
                             afp_l3_percentage: float, dcp: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_galad_model_hcc pattern
    """
    calculator = GaladModelHccCalculator()
    return calculator.calculate(age, sex, afp, afp_l3_percentage, dcp)