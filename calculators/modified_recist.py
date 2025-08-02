"""
Modified Response Evaluation Criteria in Solid Tumors (mRECIST) Calculator

Assesses treatment response in hepatocellular carcinoma (HCC) patients based on 
viable tumor enhancement. Designed specifically for patients receiving targeted 
therapies and locoregional treatments.

References:
1. Lencioni R, Llovet JM. Semin Liver Dis. 2010;30(1):52-60.
2. Forner A, et al. Cancer. 2009;115(3):616-23.
3. Edeline J, et al. Cancer. 2012;118(1):147-56.
"""

from typing import Dict, Any


class ModifiedRecistCalculator:
    """Calculator for Modified Response Evaluation Criteria in Solid Tumors (mRECIST)"""
    
    def __init__(self):
        # Enhancement status mappings
        self.ENHANCEMENT_MAPPING = {
            "present": "present",
            "absent": "absent", 
            "new_lesions": "new_lesions"
        }
        
        # Response thresholds
        self.PARTIAL_RESPONSE_THRESHOLD = 0.30  # ≥30% decrease
        self.PROGRESSIVE_DISEASE_THRESHOLD = 0.20  # ≥20% increase
    
    def calculate(self, baseline_sum_diameters: float, current_sum_diameters: float,
                  intratumoral_enhancement: str) -> Dict[str, Any]:
        """
        Calculates mRECIST response category based on viable tumor assessment
        
        Args:
            baseline_sum_diameters (float): Sum of baseline diameters of viable target lesions (cm)
            current_sum_diameters (float): Sum of current diameters of viable target lesions (cm)
            intratumoral_enhancement (str): Presence of intratumoral arterial enhancement
            
        Returns:
            Dict with mRECIST response category and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(baseline_sum_diameters, current_sum_diameters, intratumoral_enhancement)
        
        # Determine mRECIST response category
        response_category = self._determine_response_category(
            baseline_sum_diameters, current_sum_diameters, intratumoral_enhancement
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(response_category, baseline_sum_diameters, current_sum_diameters)
        
        return {
            "result": response_category,
            "unit": "response_category",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, baseline_sum_diameters: float, current_sum_diameters: float, 
                        intratumoral_enhancement: str):
        """Validates input parameters"""
        
        if not isinstance(baseline_sum_diameters, (int, float)) or baseline_sum_diameters < 0.1:
            raise ValueError("Baseline sum of diameters must be a positive number ≥0.1 cm")
        
        if baseline_sum_diameters > 50.0:
            raise ValueError("Baseline sum of diameters must be ≤50.0 cm")
            
        if not isinstance(current_sum_diameters, (int, float)) or current_sum_diameters < 0.0:
            raise ValueError("Current sum of diameters must be a non-negative number")
            
        if current_sum_diameters > 50.0:
            raise ValueError("Current sum of diameters must be ≤50.0 cm")
        
        if intratumoral_enhancement not in self.ENHANCEMENT_MAPPING:
            raise ValueError(f"Intratumoral enhancement must be one of: {list(self.ENHANCEMENT_MAPPING.keys())}")
    
    def _determine_response_category(self, baseline: float, current: float, enhancement: str) -> str:
        """
        Determines mRECIST response category based on measurements and enhancement
        
        mRECIST Response Categories:
        - Complete Response: Disappearance of arterial enhancement
        - Partial Response: ≥30% decrease in viable tumor diameters
        - Progressive Disease: ≥20% increase in viable tumor or new lesions
        - Stable Disease: Neither PR nor PD criteria met
        """
        
        # Complete Response: Disappearance of any intratumoral arterial enhancement
        if enhancement == "absent":
            return "Complete Response"
        
        # Progressive Disease: New lesions or ≥20% increase in viable tumor
        if enhancement == "new_lesions":
            return "Progressive Disease"
            
        # Calculate percentage change for viable tumor
        if baseline > 0:
            percent_change = (current - baseline) / baseline
            
            # Progressive Disease: ≥20% increase in sum of diameters
            if percent_change >= self.PROGRESSIVE_DISEASE_THRESHOLD:
                return "Progressive Disease"
            
            # Partial Response: ≥30% decrease in sum of diameters  
            elif percent_change <= -self.PARTIAL_RESPONSE_THRESHOLD:
                return "Partial Response"
        
        # Stable Disease: Neither PR nor PD criteria met
        return "Stable Disease"
    
    def _get_interpretation(self, response_category: str, baseline: float, current: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mRECIST response category
        
        Args:
            response_category (str): mRECIST response category
            baseline (float): Baseline sum of diameters
            current (float): Current sum of diameters
            
        Returns:
            Dict with interpretation details
        """
        
        # Calculate percentage change for context
        percent_change = 0.0
        if baseline > 0:
            percent_change = ((current - baseline) / baseline) * 100
        
        interpretations = {
            "Complete Response": {
                "stage": "Complete Response",
                "description": "Disappearance of arterial enhancement",
                "interpretation": (f"mRECIST Complete Response: Disappearance of any intratumoral arterial "
                                f"enhancement in all target lesions. This represents the best possible "
                                f"treatment response in hepatocellular carcinoma. Complete response indicates "
                                f"excellent treatment efficacy with complete devascularization of viable "
                                f"tumor tissue. Patients achieving complete response have significantly "
                                f"improved prognosis and survival outcomes. Continue current treatment "
                                f"regimen and monitor for sustained response.")
            },
            "Partial Response": {
                "stage": "Partial Response", 
                "description": "≥30% decrease in viable tumor",
                "interpretation": (f"mRECIST Partial Response: At least 30% decrease in the sum of diameters "
                                f"of viable (enhancement in arterial phase) target lesions "
                                f"(change: {percent_change:.1f}%). This indicates good treatment response "
                                f"with significant reduction in viable tumor burden. Partial response "
                                f"correlates with improved overall survival in HCC patients. Continue "
                                f"current treatment and reassess response in 1-2 months. Consider "
                                f"consolidation therapy or continuation of current regimen.")
            },
            "Stable Disease": {
                "stage": "Stable Disease",
                "description": "Neither PR nor PD criteria met",
                "interpretation": (f"mRECIST Stable Disease: Neither sufficient shrinkage to qualify for "
                                f"partial response nor sufficient increase to qualify for progressive "
                                f"disease (change: {percent_change:+.1f}%). Disease stabilization can "
                                f"represent clinical benefit, particularly with targeted therapies. "
                                f"Continue current treatment and monitor closely for changes in tumor "
                                f"enhancement and size. Consider treatment modification if prolonged "
                                f"stable disease without clinical benefit.")
            },
            "Progressive Disease": {
                "stage": "Progressive Disease",
                "description": "≥20% increase in viable tumor",
                "interpretation": (f"mRECIST Progressive Disease: At least 20% increase in the sum of "
                                f"diameters of viable (enhancing) target lesions and/or appearance of "
                                f"new lesions (change: {percent_change:+.1f}%). This indicates treatment "
                                f"failure with tumor progression. Immediate reassessment of treatment "
                                f"strategy is required. Consider alternative systemic therapy, "
                                f"locoregional treatments, or best supportive care based on patient "
                                f"performance status and liver function.")
            }
        }
        
        return interpretations.get(response_category, {
            "stage": response_category,
            "description": "Unknown response category",
            "interpretation": f"mRECIST {response_category}: Unable to determine interpretation."
        })


def calculate_modified_recist(baseline_sum_diameters: float, current_sum_diameters: float,
                             intratumoral_enhancement: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedRecistCalculator()
    return calculator.calculate(baseline_sum_diameters, current_sum_diameters, intratumoral_enhancement)