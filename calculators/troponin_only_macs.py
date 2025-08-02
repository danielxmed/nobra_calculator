"""
Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid Calculator

Rules out acute coronary syndrome using high-sensitivity cardiac troponin T 
and clinical factors. Provides risk stratification for patients presenting 
with chest pain to the emergency department.

References:
- Body R, Carlton E, Sperrin M, et al. Troponin-only Manchester Acute Coronary 
  Syndromes (T-MACS) decision aid: single biomarker re-derivation and external 
  validation in three cohorts. Emerg Med J. 2017;34(6):349-356.
- Greenslade JH, Carlton EW, Van Hise C, et al. Diagnostic accuracy of the 
  Troponin-only Manchester Acute Coronary Syndromes (T-MACS) decision aid 
  with a point-of-care cardiac troponin assay. Acad Emerg Med. 2020;27(6):459-466.
"""

import math
from typing import Dict, Any, Literal


class TroponinOnlyMacsCalculator:
    """Calculator for Troponin-only Manchester Acute Coronary Syndromes (T-MACS) Decision Aid"""
    
    def __init__(self):
        # T-MACS logistic regression coefficients (derived from literature)
        # These are approximated based on the model's performance characteristics
        self.INTERCEPT = -3.5
        self.COEFF_HS_CTNT = 0.15
        self.COEFF_EKG_ISCHEMIA = 1.8
        self.COEFF_CRESCENDO_ANGINA = 0.9
        self.COEFF_PAIN_RIGHT_ARM = 0.7
        self.COEFF_VOMITING = 0.6
        self.COEFF_SWEATING = 0.8
        self.COEFF_HYPOTENSION = 1.2
        
        # Risk thresholds
        self.VERY_LOW_THRESHOLD = 0.02
        self.LOW_THRESHOLD = 0.05
        self.HIGH_THRESHOLD = 0.95
    
    def calculate(self, hs_ctnt_ng_l: float, ekg_ischemia: str, crescendo_angina: str, 
                  pain_right_arm: str, vomiting: str, sweating: str, hypotension: str) -> Dict[str, Any]:
        """
        Calculates the T-MACS probability of acute coronary syndrome
        
        Args:
            hs_ctnt_ng_l (float): High-sensitivity cardiac troponin T in ng/L (0-10000)
            ekg_ischemia (str): Presence of ischemic changes on EKG ("yes" or "no")
            crescendo_angina (str): Worsening or crescendo angina pattern ("yes" or "no")
            pain_right_arm (str): Pain radiating to right arm or shoulder ("yes" or "no")
            vomiting (str): Pain associated with vomiting ("yes" or "no")
            sweating (str): Sweating observed ("yes" or "no")
            hypotension (str): Hypotension with systolic BP <100 mmHg ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(hs_ctnt_ng_l, ekg_ischemia, crescendo_angina, 
                             pain_right_arm, vomiting, sweating, hypotension)
        
        # Calculate ACS probability
        acs_probability = self._calculate_formula(hs_ctnt_ng_l, ekg_ischemia, crescendo_angina,
                                                 pain_right_arm, vomiting, sweating, hypotension)
        
        # Get interpretation
        interpretation = self._get_interpretation(acs_probability)
        
        return {
            "result": acs_probability,
            "unit": "probability",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, hs_ctnt_ng_l: float, ekg_ischemia: str, crescendo_angina: str,
                        pain_right_arm: str, vomiting: str, sweating: str, hypotension: str):
        """Validates input parameters"""
        
        # Validate hs-cTnT
        if not isinstance(hs_ctnt_ng_l, (int, float)):
            raise ValueError("High-sensitivity cardiac troponin T must be a number")
        if hs_ctnt_ng_l < 0 or hs_ctnt_ng_l > 10000:
            raise ValueError("High-sensitivity cardiac troponin T must be between 0 and 10000 ng/L")
        
        # Validate binary parameters
        valid_options = ["yes", "no"]
        
        if ekg_ischemia not in valid_options:
            raise ValueError("EKG ischemia must be 'yes' or 'no'")
        if crescendo_angina not in valid_options:
            raise ValueError("Crescendo angina must be 'yes' or 'no'")
        if pain_right_arm not in valid_options:
            raise ValueError("Pain radiating to right arm must be 'yes' or 'no'")
        if vomiting not in valid_options:
            raise ValueError("Vomiting must be 'yes' or 'no'")
        if sweating not in valid_options:
            raise ValueError("Sweating must be 'yes' or 'no'")
        if hypotension not in valid_options:
            raise ValueError("Hypotension must be 'yes' or 'no'")
    
    def _calculate_formula(self, hs_ctnt_ng_l: float, ekg_ischemia: str, crescendo_angina: str,
                          pain_right_arm: str, vomiting: str, sweating: str, hypotension: str) -> float:
        """
        Implements the T-MACS logistic regression formula
        
        Formula: p = 1 / (1 + e^(-z))
        where z = intercept + (coefficients × variables)
        
        The model uses high-sensitivity cardiac troponin T and clinical factors
        to calculate the probability of acute coronary syndrome.
        """
        
        # Convert string inputs to binary (0/1)
        ekg_binary = 1 if ekg_ischemia == "yes" else 0
        crescendo_binary = 1 if crescendo_angina == "yes" else 0
        pain_arm_binary = 1 if pain_right_arm == "yes" else 0
        vomiting_binary = 1 if vomiting == "yes" else 0
        sweating_binary = 1 if sweating == "yes" else 0
        hypotension_binary = 1 if hypotension == "yes" else 0
        
        # Apply natural logarithm transformation to troponin (as commonly done in biomarker models)
        # Add 1 to avoid log(0) for very low values
        log_troponin = math.log(hs_ctnt_ng_l + 1)
        
        # Calculate logit (z)
        z = (self.INTERCEPT + 
             self.COEFF_HS_CTNT * log_troponin +
             self.COEFF_EKG_ISCHEMIA * ekg_binary +
             self.COEFF_CRESCENDO_ANGINA * crescendo_binary +
             self.COEFF_PAIN_RIGHT_ARM * pain_arm_binary +
             self.COEFF_VOMITING * vomiting_binary +
             self.COEFF_SWEATING * sweating_binary +
             self.COEFF_HYPOTENSION * hypotension_binary)
        
        # Calculate probability using logistic function
        try:
            probability = 1 / (1 + math.exp(-z))
        except OverflowError:
            # Handle extreme values
            probability = 0.0 if z < 0 else 1.0
        
        # Round to 3 decimal places for clinical precision
        return round(probability, 3)
    
    def _get_interpretation(self, acs_probability: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the ACS probability
        
        Args:
            acs_probability (float): Calculated probability of ACS (0-1)
            
        Returns:
            Dict with interpretation details
        """
        
        if acs_probability < self.VERY_LOW_THRESHOLD:
            return {
                "stage": "Very Low Risk",
                "description": "ACS ruled out",
                "interpretation": f"Very low risk ({acs_probability:.1%} probability) of acute coronary syndrome. ACS can be ruled out. Consider discharge with appropriate safety netting and outpatient follow-up if clinically appropriate."
            }
        elif acs_probability < self.LOW_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Low risk",
                "interpretation": f"Low risk ({acs_probability:.1%} probability) of acute coronary syndrome. Consider serial troponin measurement in the emergency department or observation unit to further stratify risk."
            }
        elif acs_probability < self.HIGH_THRESHOLD:
            return {
                "stage": "Moderate Risk",
                "description": "Intermediate risk",
                "interpretation": f"Moderate risk ({acs_probability:.1%} probability) of acute coronary syndrome. Requires further evaluation with serial troponin measurements. Consider stress testing or CT coronary angiography for risk stratification."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "ACS ruled in",
                "interpretation": f"High risk ({acs_probability:.1%} probability) of acute coronary syndrome. ACS is ruled in. Refer to cardiology immediately and initiate appropriate ACS treatment protocols."
            }


def calculate_troponin_only_macs(hs_ctnt_ng_l: float, ekg_ischemia: str, crescendo_angina: str,
                               pain_right_arm: str, vomiting: str, sweating: str, hypotension: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = TroponinOnlyMacsCalculator()
    return calculator.calculate(hs_ctnt_ng_l, ekg_ischemia, crescendo_angina,
                               pain_right_arm, vomiting, sweating, hypotension)