"""
Gillmore Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM) Calculator

The Gillmore staging system is a prognostic classification system for patients with 
transthyretin amyloid cardiomyopathy (ATTR-CM) developed by the UK National Amyloidosis 
Centre. It uses two readily available biomarkers (NT-proBNP and eGFR) to stratify 
patients into three prognostic categories applicable to both wild-type and variant ATTR-CM.

References (Vancouver style):
1. Gillmore JD, Damy T, Fontana M, et al. A new staging system for cardiac transthyretin 
   amyloidosis. Eur Heart J. 2018;39(30):2799-2806. doi: 10.1093/eurheartj/ehx589.
2. Fontana M, Corovic A, Scully P, Moon JC. Myocardial amyloidosis: the exemplar 
   interstitial disease. JACC Cardiovasc Imaging. 2019;12(11 Pt 2):2345-2356. 
   doi: 10.1016/j.jcmg.2019.06.023.
3. Grogan M, Scott CG, Kyle RA, et al. Natural history of wild-type transthyretin cardiac 
   amyloidosis and risk stratification using a novel staging system. J Am Coll Cardiol. 
   2016;68(10):1014-1020. doi: 10.1016/j.jacc.2016.06.033.
"""

from typing import Dict, Any


class GillmoreStagingAttrCmCalculator:
    """Calculator for Gillmore Staging System for ATTR-CM"""
    
    def __init__(self):
        # Biomarker thresholds
        self.NT_PROBNP_THRESHOLD = 3000.0  # ng/L
        self.EGFR_THRESHOLD = 45.0  # ml/min
        
        # Median survival data (months)
        self.STAGE_SURVIVAL = {
            "Stage I": 69.2,
            "Stage II": 46.7,
            "Stage III": 24.1
        }
        
        # Hazard ratios compared to Stage I
        self.HAZARD_RATIOS = {
            "Stage I": 1.0,  # Reference
            "Stage II": 2.05,
            "Stage III": 3.80
        }
    
    def calculate(self, nt_probnp: float, egfr: float) -> Dict[str, Any]:
        """
        Calculates Gillmore staging for ATTR-CM using NT-proBNP and eGFR
        
        Args:
            nt_probnp (float): N-terminal pro-B-type natriuretic peptide level (ng/L)
            egfr (float): Estimated glomerular filtration rate (ml/min)
            
        Returns:
            Dict with the staging result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(nt_probnp, egfr)
        
        # Determine staging
        stage = self._calculate_stage(nt_probnp, egfr)
        
        # Get interpretation
        interpretation = self._get_interpretation(stage, nt_probnp, egfr)
        
        return {
            "result": stage,
            "unit": "stage",
            "interpretation": interpretation["interpretation"],
            "stage": stage,
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, nt_probnp: float, egfr: float):
        """Validates input parameters"""
        
        if not isinstance(nt_probnp, (int, float)):
            raise ValueError("NT-proBNP must be a number")
        
        if not isinstance(egfr, (int, float)):
            raise ValueError("eGFR must be a number")
        
        if nt_probnp < 0:
            raise ValueError("NT-proBNP cannot be negative")
        
        if nt_probnp > 50000:
            raise ValueError("NT-proBNP value seems unusually high (>50,000 ng/L)")
        
        if egfr < 5:
            raise ValueError("eGFR cannot be less than 5 ml/min")
        
        if egfr > 150:
            raise ValueError("eGFR value seems unusually high (>150 ml/min)")
    
    def _calculate_stage(self, nt_probnp: float, egfr: float) -> str:
        """Determines the Gillmore stage based on biomarker criteria"""
        
        # Stage I: NT-proBNP ≤3000 ng/L AND eGFR ≥45 ml/min
        if nt_probnp <= self.NT_PROBNP_THRESHOLD and egfr >= self.EGFR_THRESHOLD:
            return "Stage I"
        
        # Stage III: NT-proBNP >3000 ng/L AND eGFR <45 ml/min
        elif nt_probnp > self.NT_PROBNP_THRESHOLD and egfr < self.EGFR_THRESHOLD:
            return "Stage III"
        
        # Stage II: All other combinations
        else:
            return "Stage II"
    
    def _get_interpretation(self, stage: str, nt_probnp: float, egfr: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the staging result
        
        Args:
            stage (str): Calculated Gillmore stage
            nt_probnp (float): NT-proBNP value for context
            egfr (float): eGFR value for context
            
        Returns:
            Dict with interpretation details
        """
        
        # Format biomarker values for reporting
        nt_probnp_formatted = f"{nt_probnp:.0f}"
        egfr_formatted = f"{egfr:.1f}"
        
        if stage == "Stage I":
            return {
                "stage": "Stage I",
                "description": "Best prognosis",
                "interpretation": (
                    f"Gillmore Staging: {stage} (NT-proBNP: {nt_probnp_formatted} ng/L, eGFR: {egfr_formatted} ml/min). "
                    f"Best prognostic category with median survival of {self.STAGE_SURVIVAL[stage]} months. "
                    f"Both biomarkers within favorable ranges (NT-proBNP ≤3000 ng/L and eGFR ≥45 ml/min). "
                    f"Continue standard ATTR-CM management with regular monitoring. Consider for clinical trials. "
                    f"Optimize heart failure therapy and manage comorbidities. Monitor for disease progression "
                    f"with serial biomarker assessment and imaging."
                )
            }
        elif stage == "Stage II":
            return {
                "stage": "Stage II", 
                "description": "Intermediate prognosis",
                "interpretation": (
                    f"Gillmore Staging: {stage} (NT-proBNP: {nt_probnp_formatted} ng/L, eGFR: {egfr_formatted} ml/min). "
                    f"Intermediate prognostic category with median survival of {self.STAGE_SURVIVAL[stage]} months. "
                    f"Hazard ratio {self.HAZARD_RATIOS[stage]} compared to Stage I. One biomarker elevated while "
                    f"the other remains in favorable range. Enhanced monitoring recommended with consideration "
                    f"for ATTR-specific therapies. Optimize heart failure management and assess for treatment "
                    f"intensification. Regular biomarker and functional assessment to monitor progression."
                )
            }
        else:  # Stage III
            return {
                "stage": "Stage III",
                "description": "Worst prognosis", 
                "interpretation": (
                    f"Gillmore Staging: {stage} (NT-proBNP: {nt_probnp_formatted} ng/L, eGFR: {egfr_formatted} ml/min). "
                    f"Highest risk prognostic category with median survival of {self.STAGE_SURVIVAL[stage]} months. "
                    f"Hazard ratio {self.HAZARD_RATIOS[stage]} compared to Stage I. Both biomarkers in unfavorable "
                    f"ranges indicating advanced disease with significant cardiac and renal involvement. Urgent "
                    f"consideration for ATTR-specific therapies and advanced heart failure management. May require "
                    f"multidisciplinary care including cardiology, nephrology, and palliative care consultation. "
                    f"Close monitoring for complications and consideration of advanced therapies."
                )
            }


def calculate_gillmore_staging_attr_cm(nt_probnp: float, egfr: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_gillmore_staging_attr_cm pattern
    """
    calculator = GillmoreStagingAttrCmCalculator()
    return calculator.calculate(nt_probnp, egfr)