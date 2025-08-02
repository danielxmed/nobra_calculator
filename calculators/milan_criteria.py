"""
Milan Criteria for Liver Transplantation Calculator

Assesses suitability of patients for liver transplant with cirrhosis and 
hepatocellular carcinoma (HCC), recommended by AASLD guidelines.

References:
1. Mazzaferro V, et al. N Engl J Med. 1996;334(11):693-9.
2. Mazzaferro V, et al. Lancet Oncol. 2009;10(1):35-43.
3. Mazzaferro V, et al. Liver Transpl. 2011;17 Suppl 2:S44-57.
4. Marrero JA, et al. Hepatology. 2018;68(2):723-750.
"""

from typing import Dict, Any, Optional


class MilanCriteriaCalculator:
    """Calculator for Milan Criteria for Liver Transplantation"""
    
    def calculate(self, tumor_count: str, single_tumor_size: Optional[float],
                  largest_tumor_size: Optional[float], extrahepatic_involvement: str,
                  major_vessel_involvement: str) -> Dict[str, Any]:
        """
        Determines if patient meets Milan criteria for liver transplantation
        
        Args:
            tumor_count: Number of tumors ("single", "two_three", "more_than_three")
            single_tumor_size: Size of single tumor in cm (if single tumor)
            largest_tumor_size: Size of largest tumor in cm (if 2-3 tumors)
            extrahepatic_involvement: Evidence of extrahepatic disease ("yes"/"no")
            major_vessel_involvement: Major vascular invasion ("yes"/"no")
            
        Returns:
            Dict with Milan criteria eligibility and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(tumor_count, single_tumor_size, largest_tumor_size,
                            extrahepatic_involvement, major_vessel_involvement)
        
        # Check exclusion criteria first
        if extrahepatic_involvement == "yes" or major_vessel_involvement == "yes":
            meets_criteria = False
        elif tumor_count == "more_than_three":
            meets_criteria = False
        elif tumor_count == "single":
            # Single tumor must be ≤5 cm
            meets_criteria = single_tumor_size <= 5.0
        elif tumor_count == "two_three":
            # 2-3 tumors, each must be ≤3 cm
            meets_criteria = largest_tumor_size <= 3.0
        else:
            meets_criteria = False
        
        # Get interpretation
        interpretation = self._get_interpretation(meets_criteria)
        
        return {
            "result": "Meets Criteria" if meets_criteria else "Does Not Meet Criteria",
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, tumor_count: str, single_tumor_size: Optional[float],
                        largest_tumor_size: Optional[float], extrahepatic_involvement: str,
                        major_vessel_involvement: str):
        """Validates input parameters"""
        
        # Validate tumor count
        valid_counts = ["single", "two_three", "more_than_three"]
        if tumor_count not in valid_counts:
            raise ValueError(f"tumor_count must be one of: {', '.join(valid_counts)}")
        
        # Validate size parameters based on tumor count
        if tumor_count == "single":
            if single_tumor_size is None:
                raise ValueError("single_tumor_size is required when tumor_count is 'single'")
            if single_tumor_size < 0 or single_tumor_size > 20:
                raise ValueError("single_tumor_size must be between 0 and 20 cm")
        
        if tumor_count == "two_three":
            if largest_tumor_size is None:
                raise ValueError("largest_tumor_size is required when tumor_count is 'two_three'")
            if largest_tumor_size < 0 or largest_tumor_size > 20:
                raise ValueError("largest_tumor_size must be between 0 and 20 cm")
        
        # Validate yes/no parameters
        valid_options = ["yes", "no"]
        if extrahepatic_involvement not in valid_options:
            raise ValueError(f"extrahepatic_involvement must be one of: {', '.join(valid_options)}")
        if major_vessel_involvement not in valid_options:
            raise ValueError(f"major_vessel_involvement must be one of: {', '.join(valid_options)}")
    
    def _get_interpretation(self, meets_criteria: bool) -> Dict[str, str]:
        """
        Provides interpretation based on whether Milan criteria are met
        
        Args:
            meets_criteria: Boolean indicating if criteria are met
            
        Returns:
            Dict with interpretation details
        """
        
        if meets_criteria:
            return {
                "stage": "Meets Criteria",
                "description": "Eligible for liver transplantation",
                "interpretation": ("Patient meets Milan criteria and is eligible for liver "
                                 "transplantation consideration. Excellent post-transplant outcomes "
                                 "expected with 4-year survival ~75%. Qualifies for MELD exception "
                                 "points (MMaT-3) after 6-month waiting period.")
            }
        else:
            return {
                "stage": "Does Not Meet Criteria",
                "description": "Not eligible for liver transplantation",
                "interpretation": ("Patient does not meet Milan criteria. Consider downstaging "
                                 "strategies with locoregional therapies (TACE, Y90 radioembolization, "
                                 "ablation). If successfully downstaged to within Milan criteria and "
                                 "maintained for 3-6 months, may become transplant eligible. Monitor "
                                 "AFP levels - must be <500 ng/mL for eligibility.")
            }


def calculate_milan_criteria(tumor_count: str, single_tumor_size: Optional[float] = None,
                           largest_tumor_size: Optional[float] = None,
                           extrahepatic_involvement: str = "no",
                           major_vessel_involvement: str = "no") -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MilanCriteriaCalculator()
    return calculator.calculate(tumor_count, single_tumor_size, largest_tumor_size,
                              extrahepatic_involvement, major_vessel_involvement)