"""
Karnofsky Performance Status Scale Calculator

Determines patient's ability to tolerate therapies in serious illness, specifically for chemotherapy.
This validated functional status scale ranges from 100% (normal, no evidence of disease) 
to 0% (death) and correlates with treatment tolerance, survival, and quality of life in cancer patients.

References:
1. Karnofsky DA, Abelmann WH, Craver LF, Burchenal JH. The use of the nitrogen mustards 
   in the palliative treatment of carcinoma. With particular reference to bronchogenic 
   carcinoma. Cancer. 1948;1(4):634-656.
2. Karnofsky DA, Burchenal JH. The clinical evaluation of chemotherapeutic agents in cancer. 
   In: MacLeod CM, editor. Evaluation of chemotherapeutic agents. New York: Columbia 
   University Press; 1949. p. 196.
3. Schag CC, Heinrich RL, Ganz PA. Karnofsky performance status revisited reliability, 
   validity, and guidelines. J Clin Oncol. 1984;2(3):187-193.
4. Yates JW, Chalmer B, McKegney FP. Evaluation of patients with advanced cancer using 
   the Karnofsky performance status. Cancer. 1980;45(8):2220-2224.
"""

from typing import Dict, Any


class KarnofskyPerformanceStatusCalculator:
    """Calculator for Karnofsky Performance Status Scale"""
    
    def __init__(self):
        # Performance status descriptions mapping
        self.performance_descriptions = {
            100: {
                "category": "Normal activity",
                "description": "Normal, no complaints, no evidence of disease",
                "functional_capability": "Able to carry on normal activity and to work",
                "care_requirement": "No special care needed"
            },
            90: {
                "category": "Normal activity",
                "description": "Able to carry on normal activity; minor signs or symptoms of disease",
                "functional_capability": "Able to carry on normal activity and to work",
                "care_requirement": "No special care needed"
            },
            80: {
                "category": "Normal activity",
                "description": "Normal activity with some effort; some signs or symptoms of disease",
                "functional_capability": "Able to carry on normal activity and to work",
                "care_requirement": "No special care needed"
            },
            70: {
                "category": "Unable to work",
                "description": "Cares for self; unable to carry on normal activity or active work",
                "functional_capability": "Unable to work but able to live at home and care for most personal needs",
                "care_requirement": "Varying amount of assistance needed"
            },
            60: {
                "category": "Unable to work",
                "description": "Requires occasional assistance but able to care for most of personal needs",
                "functional_capability": "Unable to work but able to live at home and care for most personal needs",
                "care_requirement": "Varying amount of assistance needed"
            },
            50: {
                "category": "Unable to work",
                "description": "Requires considerable assistance and frequent medical care",
                "functional_capability": "Unable to work but able to live at home and care for most personal needs",
                "care_requirement": "Varying amount of assistance needed"
            },
            40: {
                "category": "Unable to care for self",
                "description": "Disabled; requires special care and assistance",
                "functional_capability": "Unable to care for self; requires equivalent of institutional or hospital care",
                "care_requirement": "Disease may be progressing rapidly"
            },
            30: {
                "category": "Unable to care for self",
                "description": "Severely disabled; hospitalization indicated though death not imminent",
                "functional_capability": "Unable to care for self; requires equivalent of institutional or hospital care",
                "care_requirement": "Disease may be progressing rapidly"
            },
            20: {
                "category": "Unable to care for self",
                "description": "Very sick; hospitalization necessary; active supportive treatment necessary",
                "functional_capability": "Unable to care for self; requires equivalent of institutional or hospital care",
                "care_requirement": "Disease may be progressing rapidly"
            },
            10: {
                "category": "Moribund",
                "description": "Moribund; fatal processes progressing rapidly",
                "functional_capability": "Moribund; fatal processes progressing rapidly",
                "care_requirement": "Fatal processes progressing rapidly"
            },
            0: {
                "category": "Death",
                "description": "Death",
                "functional_capability": "Death",
                "care_requirement": "Death"
            }
        }
    
    def calculate(self, performance_status: int) -> Dict[str, Any]:
        """
        Evaluates Karnofsky Performance Status and provides clinical interpretation
        
        Args:
            performance_status (int): Karnofsky score (0-100% in 10% increments)
            
        Returns:
            Dict with the result and comprehensive interpretation
        """
        
        # Validate inputs
        self._validate_inputs(performance_status)
        
        # Get detailed interpretation
        interpretation_data = self._get_interpretation(performance_status)
        
        return {
            "result": performance_status,
            "unit": "percentage",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["stage_description"]
        }
    
    def _validate_inputs(self, performance_status: int):
        """Validates input parameters"""
        
        if not isinstance(performance_status, int):
            raise ValueError("Performance status must be an integer")
        
        valid_scores = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        if performance_status not in valid_scores:
            raise ValueError(f"Performance status must be one of: {valid_scores}")
    
    def _get_interpretation(self, performance_status: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the Karnofsky score
        
        Args:
            performance_status (int): Karnofsky score
            
        Returns:
            Dict with interpretation details
        """
        
        status_info = self.performance_descriptions[performance_status]
        
        # Get clinical recommendations based on score ranges
        if performance_status >= 80:
            clinical_interpretation = (
                f"Excellent functional status (KPS {performance_status}%). {status_info['description']}. "
                "Patient is suitable for aggressive treatments including high-dose chemotherapy, "
                "clinical trials, and complex procedures. Generally associated with better treatment "
                "tolerance and survival outcomes."
            )
            treatment_eligibility = "Eligible for all treatment options"
            
        elif performance_status >= 60:
            clinical_interpretation = (
                f"Good functional status (KPS {performance_status}%). {status_info['description']}. "
                "Patient may be suitable for standard chemotherapy regimens and active treatments. "
                "Consider dose modifications based on individual tolerance. Regular monitoring recommended."
            )
            treatment_eligibility = "Suitable for standard treatments with monitoring"
            
        elif performance_status >= 40:
            clinical_interpretation = (
                f"Poor functional status (KPS {performance_status}%). {status_info['description']}. "
                "Patient may benefit from palliative treatments or reduced-intensity regimens. "
                "Quality of life considerations should guide treatment decisions. Supportive care emphasis."
            )
            treatment_eligibility = "Consider palliative or reduced-intensity treatments"
            
        elif performance_status >= 10:
            clinical_interpretation = (
                f"Very poor functional status (KPS {performance_status}%). {status_info['description']}. "
                "Focus should be on comfort care and symptom management. Aggressive treatments "
                "generally not appropriate. Hospice care may be considered."
            )
            treatment_eligibility = "Comfort care and symptom management focus"
            
        else:  # 0%
            clinical_interpretation = (
                f"Death (KPS {performance_status}%). Patient has died."
            )
            treatment_eligibility = "Not applicable"
        
        # Determine stage based on functional categories
        if performance_status >= 80:
            stage = "Excellent Performance"
            stage_description = "Normal activity with minimal symptoms"
        elif performance_status >= 50:
            stage = "Good Performance"
            stage_description = "Unable to work but independent at home"
        elif performance_status >= 20:
            stage = "Poor Performance"
            stage_description = "Requires assistance and medical care"
        elif performance_status >= 10:
            stage = "Very Poor Performance"
            stage_description = "Moribund state"
        else:
            stage = "Death"
            stage_description = "Death"
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": (
                f"{clinical_interpretation} "
                f"Treatment eligibility: {treatment_eligibility}. "
                f"Functional capability: {status_info['functional_capability']}."
            )
        }


def calculate_karnofsky_performance_status(performance_status: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_karnofsky_performance_status pattern
    """
    calculator = KarnofskyPerformanceStatusCalculator()
    return calculator.calculate(performance_status)