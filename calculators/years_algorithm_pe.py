"""
YEARS Algorithm for Pulmonary Embolism (PE) Calculator

Simplified diagnostic algorithm to rule out pulmonary embolism using variable D-dimer 
thresholds based on clinical criteria.

References:
1. van der Hulle T, Cheung WY, Kooij S, et al. Simplified diagnostic management of suspected 
   pulmonary embolism (the YEARS study): a prospective, multicentre, cohort study. 
   Lancet. 2017;390(10091):289-297. doi: 10.1016/S0140-6736(17)30885-1
2. van der Pol LM, Tromeur C, Bistervels IM, et al. Pregnancy-Adapted YEARS Algorithm for 
   Diagnosis of Suspected Pulmonary Embolism. N Engl J Med. 2019;380(12):1139-1149.
"""

from typing import Dict, Any


class YearsAlgorithmPeCalculator:
    """Calculator for YEARS Algorithm for Pulmonary Embolism"""
    
    def __init__(self):
        # YEARS criteria items
        self.YEARS_ITEMS = [
            "clinical_signs_dvt",
            "hemoptysis", 
            "pe_most_likely"
        ]
        
        # D-dimer thresholds (ng/mL FEU)
        self.D_DIMER_THRESHOLD_NO_ITEMS = 1000.0  # 0 YEARS items
        self.D_DIMER_THRESHOLD_WITH_ITEMS = 500.0  # ≥1 YEARS items
    
    def calculate(self, clinical_signs_dvt: str, hemoptysis: str, pe_most_likely: str, 
                 d_dimer: float) -> Dict[str, Any]:
        """
        Calculates YEARS Algorithm recommendation for pulmonary embolism
        
        Args:
            clinical_signs_dvt (str): Clinical signs of deep vein thrombosis
            hemoptysis (str): Hemoptysis present
            pe_most_likely (str): PE is the most likely diagnosis
            d_dimer (float): D-dimer level in ng/mL FEU
            
        Returns:
            Dict with YEARS assessment and diagnostic recommendation
        """
        
        # Validate inputs
        self._validate_inputs(clinical_signs_dvt, hemoptysis, pe_most_likely, d_dimer)
        
        # Count YEARS items
        years_count = self._count_years_items(clinical_signs_dvt, hemoptysis, pe_most_likely)
        
        # Determine D-dimer threshold
        d_dimer_threshold = self._get_d_dimer_threshold(years_count)
        
        # Make diagnostic recommendation
        recommendation = self._get_recommendation(years_count, d_dimer, d_dimer_threshold)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(years_count, d_dimer, d_dimer_threshold, recommendation)
        
        return {
            "result": recommendation["recommendation"],
            "unit": "categorical",
            "interpretation": interpretation["interpretation"],
            "stage": recommendation["stage"],
            "stage_description": recommendation["description"],
            "years_count": years_count,
            "d_dimer_threshold": d_dimer_threshold,
            "d_dimer_value": d_dimer,
            "years_items": {
                "clinical_signs_dvt": clinical_signs_dvt == "yes",
                "hemoptysis": hemoptysis == "yes", 
                "pe_most_likely": pe_most_likely == "yes"
            },
            "clinical_decision": interpretation["clinical_decision"],
            "safety_information": interpretation["safety_information"]
        }
    
    def _validate_inputs(self, clinical_signs_dvt: str, hemoptysis: str, pe_most_likely: str, d_dimer: float):
        """Validates input parameters"""
        
        valid_options = ["yes", "no"]
        
        if clinical_signs_dvt not in valid_options:
            raise ValueError(f"Clinical signs of DVT must be one of: {valid_options}")
        
        if hemoptysis not in valid_options:
            raise ValueError(f"Hemoptysis must be one of: {valid_options}")
        
        if pe_most_likely not in valid_options:
            raise ValueError(f"PE most likely must be one of: {valid_options}")
        
        if not isinstance(d_dimer, (int, float)):
            raise ValueError("D-dimer must be a number")
        
        if d_dimer < 0:
            raise ValueError("D-dimer cannot be negative")
        
        if d_dimer > 50000:
            raise ValueError("D-dimer value seems unusually high (>50,000 ng/mL)")
    
    def _count_years_items(self, clinical_signs_dvt: str, hemoptysis: str, pe_most_likely: str) -> int:
        """Counts the number of positive YEARS items"""
        
        count = 0
        if clinical_signs_dvt == "yes":
            count += 1
        if hemoptysis == "yes":
            count += 1
        if pe_most_likely == "yes":
            count += 1
        
        return count
    
    def _get_d_dimer_threshold(self, years_count: int) -> float:
        """Determines the appropriate D-dimer threshold based on YEARS count"""
        
        if years_count == 0:
            return self.D_DIMER_THRESHOLD_NO_ITEMS  # 1000 ng/mL
        else:
            return self.D_DIMER_THRESHOLD_WITH_ITEMS  # 500 ng/mL
    
    def _get_recommendation(self, years_count: int, d_dimer: float, d_dimer_threshold: float) -> Dict[str, str]:
        """Determines the diagnostic recommendation"""
        
        if d_dimer < d_dimer_threshold:
            return {
                "recommendation": "PE Excluded",
                "stage": "PE Excluded",
                "description": "Pulmonary embolism excluded"
            }
        else:
            return {
                "recommendation": "CTPA Required",
                "stage": "CTPA Required", 
                "description": "CT pulmonary angiography indicated"
            }
    
    def _generate_interpretation(self, years_count: int, d_dimer: float, d_dimer_threshold: float, 
                               recommendation: Dict[str, str]) -> Dict[str, Any]:
        """Generates clinical interpretation and recommendations"""
        
        # Base interpretation
        if recommendation["recommendation"] == "PE Excluded":
            interpretation = (f"Based on YEARS Algorithm: {years_count} YEARS items present, "
                            f"D-dimer {d_dimer:.1f} ng/mL is below threshold of {d_dimer_threshold:.0f} ng/mL. "
                            f"Pulmonary embolism is excluded. No further imaging required.")
            
            clinical_decision = {
                "next_steps": "No further diagnostic testing for PE required",
                "follow_up": "Consider alternative diagnoses for patient's symptoms",
                "monitoring": "3-month VTE incidence of 0.43% for patients not undergoing CTPA",
                "contraindications": "Algorithm not validated in patients on therapeutic anticoagulation"
            }
        else:
            interpretation = (f"Based on YEARS Algorithm: {years_count} YEARS items present, "
                            f"D-dimer {d_dimer:.1f} ng/mL exceeds threshold of {d_dimer_threshold:.0f} ng/mL. "
                            f"CT pulmonary angiography (CTPA) is required to exclude pulmonary embolism.")
            
            clinical_decision = {
                "next_steps": "Proceed with CT pulmonary angiography (CTPA)",
                "urgency": "Based on clinical assessment and hemodynamic stability",
                "alternative": "Consider ventilation-perfusion scan if CTPA contraindicated",
                "anticoagulation": "Consider interim anticoagulation pending imaging if high clinical suspicion"
            }
        
        # Safety information
        safety_information = {
            "validated_population": "Hemodynamically stable patients ≥18 years old with suspected PE",
            "exclusions": [
                "Patients on therapeutic anticoagulation",
                "Life expectancy <3 months", 
                "Geographic follow-up limitations",
                "Contrast agent allergies"
            ],
            "pregnancy": "Requires modified Pregnancy-Adapted YEARS Algorithm",
            "performance": "Reduces CTPA by 14% compared to standard algorithms with maintained safety"
        }
        
        return {
            "interpretation": interpretation,
            "clinical_decision": clinical_decision,
            "safety_information": safety_information
        }


def calculate_years_algorithm_pe(clinical_signs_dvt, hemoptysis, pe_most_likely, d_dimer) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_years_algorithm_pe pattern
    """
    calculator = YearsAlgorithmPeCalculator()
    return calculator.calculate(clinical_signs_dvt, hemoptysis, pe_most_likely, d_dimer)