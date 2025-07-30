"""
BUN Creatinine Ratio Calculator

Evaluates kidney function by calculating the ratio of blood urea nitrogen (BUN) 
to serum creatinine, helping distinguish between prerenal, intrinsic renal, 
and postrenal causes of kidney dysfunction.

References:
- Levey AS, et al. A more accurate method to estimate glomerular filtration 
  rate from serum creatinine: a new prediction equation. Ann Intern Med. 1999.
- National Kidney Foundation. K/DOQI clinical practice guidelines for chronic 
  kidney disease. Am J Kidney Dis. 2002.
"""

from typing import Dict, Any


class BunCreatinineRatioCalculator:
    """Calculator for BUN Creatinine Ratio"""
    
    def __init__(self):
        # Normal reference ranges
        self.NORMAL_BUN_MIN = 8.0  # mg/dL
        self.NORMAL_BUN_MAX = 20.0  # mg/dL
        self.NORMAL_CREATININE_MIN = 0.7  # mg/dL
        self.NORMAL_CREATININE_MAX = 1.3  # mg/dL
        
        # Ratio interpretation thresholds
        self.LOW_RATIO_THRESHOLD = 10.0
        self.HIGH_RATIO_THRESHOLD = 20.0
    
    def calculate(self, bun: float, creatinine: float) -> Dict[str, Any]:
        """
        Calculates the BUN to creatinine ratio
        
        Args:
            bun (float): Blood urea nitrogen level in mg/dL
            creatinine (float): Serum creatinine level in mg/dL
            
        Returns:
            Dict with the ratio result and clinical interpretation
        """
        
        # Validations
        self._validate_inputs(bun, creatinine)
        
        # Calculate ratio
        ratio = self._calculate_ratio(bun, creatinine)
        
        # Get interpretation
        interpretation = self._get_interpretation(ratio)
        
        # Get clinical recommendations
        recommendations = self._get_clinical_recommendations(ratio, bun, creatinine)
        
        return {
            "result": ratio,
            "unit": "ratio",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "clinical_recommendations": recommendations,
            "reference_values": self._get_reference_values()
        }
    
    def _validate_inputs(self, bun: float, creatinine: float):
        """Validates input parameters"""
        
        if not isinstance(bun, (int, float)):
            raise ValueError("BUN must be a numeric value")
        
        if not isinstance(creatinine, (int, float)):
            raise ValueError("Creatinine must be a numeric value")
        
        if bun < 1 or bun > 200:
            raise ValueError("BUN must be between 1 and 200 mg/dL")
        
        if creatinine < 0.1 or creatinine > 20:
            raise ValueError("Creatinine must be between 0.1 and 20 mg/dL")
        
        if creatinine == 0:
            raise ValueError("Creatinine cannot be zero (division by zero)")
    
    def _calculate_ratio(self, bun: float, creatinine: float) -> float:
        """Calculates the BUN to creatinine ratio"""
        
        ratio = bun / creatinine
        return round(ratio, 1)
    
    def _get_interpretation(self, ratio: float) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the ratio
        
        Args:
            ratio (float): Calculated BUN/Creatinine ratio
            
        Returns:
            Dict with interpretation details
        """
        
        if ratio < self.LOW_RATIO_THRESHOLD:
            return {
                "stage": "Low",
                "description": "Low BUN/Creatinine ratio",
                "interpretation": "Ratio <10 may suggest intrinsic renal disease, malnutrition, low protein intake, liver disease, or overhydration. Consider intrinsic kidney pathology such as acute tubular necrosis, glomerulonephritis, or interstitial nephritis."
            }
        elif ratio <= self.HIGH_RATIO_THRESHOLD:
            return {
                "stage": "Normal",
                "description": "Normal BUN/Creatinine ratio",
                "interpretation": "Normal kidney function with appropriate filtration of both BUN and creatinine. This ratio indicates healthy renal physiology and adequate glomerular filtration rate."
            }
        else:
            return {
                "stage": "High",
                "description": "High BUN/Creatinine ratio",
                "interpretation": "Ratio >20 may indicate prerenal azotemia (dehydration, heart failure, shock), gastrointestinal bleeding, high protein intake, or postrenal obstruction. The kidneys are functioning but BUN is disproportionately elevated compared to creatinine."
            }
    
    def _get_clinical_recommendations(self, ratio: float, bun: float, creatinine: float) -> Dict[str, list]:
        """
        Provides clinical recommendations based on the ratio and individual values
        
        Args:
            ratio (float): Calculated BUN/Creatinine ratio
            bun (float): BUN value
            creatinine (float): Creatinine value
            
        Returns:
            Dict with categorized clinical recommendations
        """
        
        recommendations = {
            "further_evaluation": [],
            "immediate_actions": [],
            "monitoring": [],
            "considerations": []
        }
        
        # Recommendations based on ratio
        if ratio < self.LOW_RATIO_THRESHOLD:
            recommendations["further_evaluation"].extend([
                "Evaluate for intrinsic kidney disease with urinalysis and microscopy",
                "Consider renal ultrasound to assess kidney structure",
                "Check for proteinuria and hematuria",
                "Assess for acute tubular necrosis or glomerulonephritis"
            ])
            recommendations["immediate_actions"].extend([
                "Review medications for nephrotoxic agents",
                "Assess volume status and optimize hydration if overhydrated"
            ])
            recommendations["considerations"].extend([
                "Low protein intake or malnutrition",
                "Liver disease affecting urea synthesis",
                "Recent dialysis or aggressive fluid resuscitation"
            ])
        
        elif ratio <= self.HIGH_RATIO_THRESHOLD:
            recommendations["monitoring"].extend([
                "Continue routine monitoring of kidney function",
                "Monitor trends in BUN and creatinine over time"
            ])
            recommendations["considerations"].extend([
                "Normal kidney function indicated",
                "Maintain adequate hydration and avoid nephrotoxic agents"
            ])
        
        else:  # High ratio
            recommendations["further_evaluation"].extend([
                "Assess volume status and hydration",
                "Evaluate for heart failure or shock",
                "Check for gastrointestinal bleeding",
                "Consider renal imaging if obstruction suspected"
            ])
            recommendations["immediate_actions"].extend([
                "Address dehydration with appropriate fluid resuscitation",
                "Discontinue ACE inhibitors/ARBs if hemodynamically unstable",
                "Evaluate for urinary obstruction"
            ])
            recommendations["considerations"].extend([
                "High protein diet or recent protein load",
                "Gastrointestinal bleeding with protein absorption",
                "Prerenal azotemia from volume depletion",
                "Congestive heart failure or cardiorenal syndrome"
            ])
        
        # Additional recommendations based on individual values
        if bun > self.NORMAL_BUN_MAX:
            recommendations["monitoring"].append("Monitor BUN trends - elevated above normal range")
        
        if creatinine > self.NORMAL_CREATININE_MAX:
            recommendations["further_evaluation"].append("Elevated creatinine - calculate eGFR and assess CKD staging")
        
        return recommendations
    
    def _get_reference_values(self) -> Dict[str, str]:
        """Returns normal reference ranges"""
        
        return {
            "normal_bun_range": f"{self.NORMAL_BUN_MIN}-{self.NORMAL_BUN_MAX} mg/dL",
            "normal_creatinine_range": f"{self.NORMAL_CREATININE_MIN}-{self.NORMAL_CREATININE_MAX} mg/dL",
            "normal_ratio_range": f"{self.LOW_RATIO_THRESHOLD}-{self.HIGH_RATIO_THRESHOLD}",
            "ratio_interpretation": {
                "low": "<10 (intrinsic renal disease, malnutrition, liver disease)",
                "normal": "10-20 (normal kidney function)",
                "high": ">20 (prerenal azotemia, GI bleeding, high protein intake)"
            }
        }


def calculate_bun_creatinine_ratio(bun: float, creatinine: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BunCreatinineRatioCalculator()
    return calculator.calculate(bun, creatinine)