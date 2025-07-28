"""
Age-Adjusted ESR/CRP for Rheumatoid Arthritis Calculator

Calculates age-adjusted ESR and CRP in adult rheumatoid arthritis patients to account 
for age-related increases in inflammatory markers.

Based on studies showing that ESR and CRP naturally increase with age, and that 
age-adjusted upper limits help distinguish true disease activity from age-related 
increases. This is particularly important in elderly patients with rheumatoid arthritis.

References:
- Ranganath VK, Elashoff DA, Khanna D, et al. Age adjustment corrects for apparent 
  differences in erythrocyte sedimentation rate and C-reactive protein values at 
  the onset of seropositive rheumatoid arthritis in younger and older patients. 
  J Rheumatol. 2005;32(6):1040-2.
- Miller A, Green M, Robinson D. Simple rule for calculating normal erythrocyte 
  sedimentation rate. BMJ. 1983;286(6361):266.
"""

from typing import Dict, Any, Optional


class AgeAdjustedEsrCrpCalculator:
    """Calculator for Age-Adjusted ESR/CRP for Rheumatoid Arthritis"""
    
    def __init__(self):
        # Conventional upper limits for reference
        self.CONVENTIONAL_LIMITS = {
            'ESR': 22,    # mm/hr (typical upper limit)
            'CRP': 0.5    # mg/dL (typical upper limit)
        }
    
    def calculate(self, age: int, sex: str, measured_esr: Optional[float] = None, 
                 measured_crp: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates age-adjusted ESR and CRP upper limits using the provided parameters
        
        Args:
            age (int): Patient age in years
            sex (str): Patient sex ("male" or "female")
            measured_esr (float, optional): Measured ESR value for comparison
            measured_crp (float, optional): Measured CRP value for comparison
            
        Returns:
            Dict with the results and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, sex, measured_esr, measured_crp)
        
        # Calculate age-adjusted upper limits
        esr_limit = self._calculate_esr_limit(age, sex)
        crp_limit = self._calculate_crp_limit(age, sex)
        
        # Get interpretation
        interpretation = self._get_interpretation(
            age, sex, esr_limit, crp_limit, measured_esr, measured_crp
        )
        
        return {
            "result": {
                "esr_age_adjusted_limit": esr_limit,
                "crp_age_adjusted_limit": crp_limit,
                "esr_conventional_limit": self.CONVENTIONAL_LIMITS['ESR'],
                "crp_conventional_limit": self.CONVENTIONAL_LIMITS['CRP']
            },
            "unit": "various",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "measured_values": {
                "esr": measured_esr,
                "crp": measured_crp
            },
            "elevated_markers": {
                "esr_elevated": measured_esr is not None and measured_esr > esr_limit,
                "crp_elevated": measured_crp is not None and measured_crp > crp_limit
            }
        }
    
    def _validate_inputs(self, age: int, sex: str, measured_esr: Optional[float], 
                        measured_crp: Optional[float]):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 18:
            raise ValueError("Age must be ≥18 years")
        
        if age > 120:
            raise ValueError("Age must be ≤120 years")
        
        # Validate sex
        if not isinstance(sex, str):
            raise ValueError("Sex must be a string")
        
        if sex.lower() not in ['male', 'female']:
            raise ValueError("Sex must be 'male' or 'female'")
        
        # Validate ESR if provided
        if measured_esr is not None:
            if not isinstance(measured_esr, (int, float)):
                raise ValueError("Measured ESR must be a number")
            
            if measured_esr < 0:
                raise ValueError("Measured ESR cannot be negative")
            
            if measured_esr > 200:
                raise ValueError("Measured ESR seems unusually high (>200 mm/hr)")
        
        # Validate CRP if provided
        if measured_crp is not None:
            if not isinstance(measured_crp, (int, float)):
                raise ValueError("Measured CRP must be a number")
            
            if measured_crp < 0:
                raise ValueError("Measured CRP cannot be negative")
            
            if measured_crp > 50:
                raise ValueError("Measured CRP seems unusually high (>50 mg/dL)")
    
    def _calculate_esr_limit(self, age: int, sex: str) -> float:
        """Calculates age-adjusted ESR upper limit"""
        
        if sex.lower() == 'male':
            # Male: Age ÷ 2
            limit = age / 2
        else:
            # Female: (Age + 10) ÷ 2
            limit = (age + 10) / 2
        
        return round(limit, 1)
    
    def _calculate_crp_limit(self, age: int, sex: str) -> float:
        """Calculates age-adjusted CRP upper limit"""
        
        if sex.lower() == 'male':
            # Male: Age ÷ 50
            limit = age / 50
        else:
            # Female: (Age ÷ 50) + 0.6
            limit = (age / 50) + 0.6
        
        return round(limit, 2)
    
    def _get_interpretation(self, age: int, sex: str, esr_limit: float, 
                          crp_limit: float, measured_esr: Optional[float], 
                          measured_crp: Optional[float]) -> Dict[str, str]:
        """
        Determines the interpretation based on the limits and measured values
        
        Args:
            age (int): Patient age
            sex (str): Patient sex
            esr_limit (float): Age-adjusted ESR limit
            crp_limit (float): Age-adjusted CRP limit
            measured_esr (float, optional): Measured ESR value
            measured_crp (float, optional): Measured CRP value
            
        Returns:
            Dict with interpretation details
        """
        
        # Build interpretation text
        interpretation_parts = []
        
        # Age-adjusted limits
        interpretation_parts.append(
            f"Age-adjusted upper limits for {age}-year-old {sex}: "
            f"ESR ≤{esr_limit} mm/hr, CRP ≤{crp_limit} mg/dL."
        )
        
        # Comparison with conventional limits
        conventional_esr = self.CONVENTIONAL_LIMITS['ESR']
        conventional_crp = self.CONVENTIONAL_LIMITS['CRP']
        
        interpretation_parts.append(
            f"Conventional limits: ESR ≤{conventional_esr} mm/hr, CRP ≤{conventional_crp} mg/dL."
        )
        
        # Analysis of measured values if provided
        elevated_markers = []
        normal_markers = []
        
        if measured_esr is not None:
            if measured_esr > esr_limit:
                elevated_markers.append(f"ESR ({measured_esr} mm/hr)")
            else:
                normal_markers.append(f"ESR ({measured_esr} mm/hr)")
        
        if measured_crp is not None:
            if measured_crp > crp_limit:
                elevated_markers.append(f"CRP ({measured_crp} mg/dL)")
            else:
                normal_markers.append(f"CRP ({measured_crp} mg/dL)")
        
        if measured_esr is not None or measured_crp is not None:
            if elevated_markers:
                interpretation_parts.append(
                    f"ELEVATED above age-adjusted limits: {', '.join(elevated_markers)}. "
                    f"This suggests active inflammation beyond what is expected for age."
                )
                stage = "Elevated Markers"
                description = "One or more markers elevated above age-adjusted limits"
            else:
                interpretation_parts.append(
                    f"Normal (within age-adjusted limits): {', '.join(normal_markers)}. "
                    f"No evidence of significant inflammation for this age group."
                )
                stage = "Normal for Age"
                description = "All markers within age-adjusted limits"
        else:
            interpretation_parts.append(
                "No measured values provided for comparison. Use these age-adjusted "
                "limits to interpret ESR and CRP values in the context of patient age and sex."
            )
            stage = "Age-Adjusted Limits"
            description = "Calculated age-adjusted upper limits"
        
        # Additional clinical context
        interpretation_parts.append(
            "Age-adjustment helps distinguish true disease activity from age-related "
            "increases in inflammatory markers, particularly important in elderly patients."
        )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": " ".join(interpretation_parts)
        }


def calculate_age_adjusted_esr_crp(age: int, sex: str, measured_esr: Optional[float] = None,
                                  measured_crp: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_age_adjusted_esr_crp pattern
    """
    calculator = AgeAdjustedEsrCrpCalculator()
    return calculator.calculate(
        age=age,
        sex=sex,
        measured_esr=measured_esr,
        measured_crp=measured_crp
    )