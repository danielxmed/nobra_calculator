"""
Ankylosing Spondylitis Disease Activity Score with CRP (ASDAS-CRP) Calculator

Calculates disease activity in ankylosing spondylitis using clinical parameters and 
C-reactive protein. ASAS-endorsed score for monitoring treatment response and guiding 
therapeutic decisions in axial spondyloarthritis.

References:
- Lukas C, Landewé R, Sieper J, et al. Development of an ASAS-endorsed disease activity 
  score (ASDAS) in patients with ankylosing spondylitis. Ann Rheum Dis. 2009;68(1):18-24.
- van der Heijde D, Lie E, Kvien TK, et al. ASDAS, a highly discriminatory ASAS-endorsed 
  disease activity score in patients with ankylosing spondylitis. Ann Rheum Dis. 2009;68(12):1811-8.
- Machado P, Landewé R, Lie E, et al. Ankylosing Spondylitis Disease Activity Score (ASDAS): 
  defining cut-off values for disease activity states and improvement scores. Ann Rheum Dis. 2011;70(1):47-53.
"""

import math
from typing import Dict, Any


class AsdasCrpCalculator:
    """Calculator for Ankylosing Spondylitis Disease Activity Score with CRP"""
    
    def __init__(self):
        # ASDAS-CRP formula coefficients
        self.BACK_PAIN_COEFF = 0.12
        self.MORNING_STIFFNESS_COEFF = 0.06
        self.PATIENT_GLOBAL_COEFF = 0.11
        self.PERIPHERAL_PAIN_COEFF = 0.07
        self.CRP_COEFF = 0.58
        
        # Disease activity cut-offs
        self.INACTIVE_CUTOFF = 1.3
        self.MODERATE_CUTOFF = 2.1
        self.HIGH_CUTOFF = 3.5
        
    def calculate(self, back_pain: float, morning_stiffness: float, patient_global: float,
                 peripheral_pain: float, crp: float) -> Dict[str, Any]:
        """
        Calculates the ASDAS-CRP score
        
        Args:
            back_pain (float): Back/neck/hip pain severity (0-10 scale)
            morning_stiffness (float): Morning stiffness severity (0-10 scale)
            patient_global (float): Patient global assessment (0-10 scale)
            peripheral_pain (float): Peripheral joint pain/swelling (0-10 scale)
            crp (float): C-reactive protein level (mg/L)
            
        Returns:
            Dict containing the ASDAS-CRP score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(back_pain, morning_stiffness, patient_global,
                            peripheral_pain, crp)
        
        # Calculate ASDAS-CRP score
        asdas_score = self._calculate_asdas_crp(
            back_pain, morning_stiffness, patient_global, peripheral_pain, crp
        )
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(asdas_score)
        
        return {
            "result": round(asdas_score, 2),
            "unit": "score",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, back_pain: float, morning_stiffness: float, patient_global: float,
                        peripheral_pain: float, crp: float):
        """Validates all input parameters"""
        
        # Validate clinical parameters (0-10 scale)
        clinical_params = [
            ("back_pain", back_pain),
            ("morning_stiffness", morning_stiffness),
            ("patient_global", patient_global),
            ("peripheral_pain", peripheral_pain)
        ]
        
        for param_name, param_value in clinical_params:
            if not isinstance(param_value, (int, float)):
                raise ValueError(f"{param_name} must be a number")
            
            if param_value < 0 or param_value > 10:
                raise ValueError(f"{param_name} must be between 0 and 10, got {param_value}")
        
        # Validate CRP
        if not isinstance(crp, (int, float)):
            raise ValueError("CRP must be a number")
        
        if crp < 0:
            raise ValueError(f"CRP cannot be negative, got {crp}")
        
        if crp > 300:  # Reasonable upper limit for CRP
            raise ValueError(f"CRP value seems unusually high ({crp} mg/L), please verify")
    
    def _calculate_asdas_crp(self, back_pain: float, morning_stiffness: float, 
                           patient_global: float, peripheral_pain: float, crp: float) -> float:
        """
        Calculates the ASDAS-CRP score using the validated formula
        
        Formula: ASDAS-CRP = 0.12 × Back Pain + 0.06 × Morning Stiffness + 
                             0.11 × Patient Global + 0.07 × Peripheral Pain + 
                             0.58 × Ln(CRP+1)
        """
        
        # Calculate each component
        back_pain_component = self.BACK_PAIN_COEFF * back_pain
        morning_stiffness_component = self.MORNING_STIFFNESS_COEFF * morning_stiffness
        patient_global_component = self.PATIENT_GLOBAL_COEFF * patient_global
        peripheral_pain_component = self.PERIPHERAL_PAIN_COEFF * peripheral_pain
        
        # CRP component uses natural logarithm of (CRP + 1)
        # Adding 1 prevents issues with zero CRP values
        crp_component = self.CRP_COEFF * math.log(crp + 1)
        
        # Sum all components
        asdas_score = (
            back_pain_component +
            morning_stiffness_component +
            patient_global_component +
            peripheral_pain_component +
            crp_component
        )
        
        return asdas_score
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines disease activity level and clinical recommendations
        
        Args:
            score (float): ASDAS-CRP score
            
        Returns:
            Dict with disease activity classification and treatment recommendations
        """
        
        if score < self.INACTIVE_CUTOFF:
            return {
                "stage": "Inactive Disease",
                "description": "Inactive ankylosing spondylitis",
                "interpretation": "Disease activity is in remission. Continue current therapy and monitor regularly. Consider tapering biological therapy if sustained remission achieved. Maintain physical therapy and exercise program."
            }
        elif score < self.MODERATE_CUTOFF:
            return {
                "stage": "Moderate Disease Activity",
                "description": "Moderate ankylosing spondylitis activity",
                "interpretation": "Moderate disease activity present. Optimize current treatment regimen. Consider escalation to biological therapy if not already on biologics. Increase physical therapy intensity and ensure adherence to treatment plan."
            }
        elif score <= self.HIGH_CUTOFF:
            return {
                "stage": "High Disease Activity",
                "description": "High ankylosing spondylitis activity",
                "interpretation": "High disease activity requiring treatment intensification. Consider starting or switching biological therapy (TNF inhibitors, IL-17 inhibitors, JAK inhibitors). Evaluate treatment adherence and optimize conventional therapy. Close monitoring required."
            }
        else:  # score > HIGH_CUTOFF
            return {
                "stage": "Very High Disease Activity",
                "description": "Very high ankylosing spondylitis activity",
                "interpretation": "Very high disease activity indicating urgent need for treatment modification. Immediate consideration for biological therapy initiation or switching. Evaluate for comorbidities and extra-articular manifestations. Consider short-term corticosteroids if appropriate."
            }


def calculate_asdas_crp(back_pain: float, morning_stiffness: float, patient_global: float,
                       peripheral_pain: float, crp: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates ASDAS-CRP score for ankylosing spondylitis disease activity assessment.
    """
    calculator = AsdasCrpCalculator()
    return calculator.calculate(back_pain, morning_stiffness, patient_global,
                              peripheral_pain, crp)