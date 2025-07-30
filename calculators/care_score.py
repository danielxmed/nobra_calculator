"""
Cardiac Anesthesia Risk Evaluation Score (CARE) Calculator

Predicts mortality and morbidity after cardiac surgery based on cardiac status,
medical comorbidities, surgical complexity, and urgency.

References:
1. Dupuis JY, Wang F, Nathan H, et al. The cardiac anesthesia risk evaluation score: 
   a clinically useful predictor of mortality and morbidity after cardiac surgery. 
   Anesthesiology. 2001;94(2):194-204.
2. Zingone B, Pappalardo A, Dreas L. Logistic versus clinical prediction models: 
   prognostic accuracy of the EuroSCORE and the cardiac anesthesia risk evaluation score. 
   Eur J Cardiothorac Surg. 2004;26(5):883-7.
"""

from typing import Dict, Any


class CareScoreCalculator:
    """Calculator for CARE Score"""
    
    def __init__(self):
        pass
    
    def calculate(
        self,
        cardiac_disease_status: str,
        other_medical_problems: str,
        surgery_complexity: str,
        emergency_surgery: str,
        last_hope_surgery: str
    ) -> Dict[str, Any]:
        """
        Calculates the CARE Score
        
        Args:
            cardiac_disease_status: Status of cardiac disease (stable/chronic_advanced)
            other_medical_problems: Other medical problems (none/controlled/uncontrolled)
            surgery_complexity: Surgery complexity (noncomplex/complex)
            emergency_surgery: Emergency surgery required (yes/no)
            last_hope_surgery: Surgery as last hope (yes/no)
            
        Returns:
            Dict with CARE score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            cardiac_disease_status, other_medical_problems,
            surgery_complexity, emergency_surgery, last_hope_surgery
        )
        
        # Determine base CARE category
        care_category = self._determine_base_category(
            cardiac_disease_status, other_medical_problems,
            surgery_complexity, last_hope_surgery
        )
        
        # Add emergency modifier if applicable
        if emergency_surgery == "yes":
            care_category += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(care_category)
        
        return {
            "result": care_category,
            "unit": "category",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        cardiac_disease_status, other_medical_problems, surgery_complexity, emergency_surgery, last_hope_surgery = args
        
        if cardiac_disease_status not in ["stable", "chronic_advanced"]:
            raise ValueError("cardiac_disease_status must be 'stable' or 'chronic_advanced'")
        
        if other_medical_problems not in ["none", "controlled", "uncontrolled"]:
            raise ValueError("other_medical_problems must be 'none', 'controlled', or 'uncontrolled'")
        
        if surgery_complexity not in ["noncomplex", "complex"]:
            raise ValueError("surgery_complexity must be 'noncomplex' or 'complex'")
        
        if emergency_surgery not in ["yes", "no"]:
            raise ValueError("emergency_surgery must be 'yes' or 'no'")
        
        if last_hope_surgery not in ["yes", "no"]:
            raise ValueError("last_hope_surgery must be 'yes' or 'no'")
    
    def _determine_base_category(self, cardiac_status, medical_problems, surgery_complexity, last_hope):
        """Determines the base CARE category (1-5)"""
        
        # CARE 5: Last hope surgery
        if last_hope == "yes":
            return 5
        
        # For stable cardiac disease
        if cardiac_status == "stable":
            # CARE 1: Stable cardiac, no other problems, noncomplex surgery
            if medical_problems == "none" and surgery_complexity == "noncomplex":
                return 1
            
            # CARE 2: Stable cardiac, controlled problems, noncomplex surgery
            elif medical_problems == "controlled" and surgery_complexity == "noncomplex":
                return 2
            
            # CARE 3: Either uncontrolled problems OR complex surgery (but not both)
            elif (medical_problems == "uncontrolled" and surgery_complexity == "noncomplex") or \
                 (medical_problems in ["none", "controlled"] and surgery_complexity == "complex"):
                return 3
            
            # CARE 4: Both uncontrolled problems AND complex surgery
            elif medical_problems == "uncontrolled" and surgery_complexity == "complex":
                return 4
        
        # For chronic/advanced cardiac disease (not last hope)
        # These cases typically fall into higher risk categories
        if medical_problems == "none" and surgery_complexity == "noncomplex":
            return 3  # Chronic disease elevates risk
        elif medical_problems == "controlled" and surgery_complexity == "noncomplex":
            return 3
        elif (medical_problems == "uncontrolled" and surgery_complexity == "noncomplex") or \
             (medical_problems in ["none", "controlled"] and surgery_complexity == "complex"):
            return 4
        else:  # uncontrolled problems AND complex surgery
            return 4
    
    def _get_interpretation(self, category: int) -> Dict[str, str]:
        """
        Determines interpretation based on CARE category
        
        Args:
            category (int): CARE category (1-6)
            
        Returns:
            Dict with interpretation details
        """
        
        interpretations = {
            1: {
                "stage": "CARE 1",
                "description": "Very Low Risk",
                "interpretation": "Stable cardiac disease, no other medical problems, undergoing noncomplex surgery. Lowest risk category with excellent prognosis. Standard perioperative monitoring and care appropriate."
            },
            2: {
                "stage": "CARE 2",
                "description": "Low Risk",
                "interpretation": "Stable cardiac disease, one or more controlled medical problems, undergoing noncomplex surgery. Low risk with good prognosis. Enhanced monitoring may be considered based on specific comorbidities."
            },
            3: {
                "stage": "CARE 3",
                "description": "Moderate Risk",
                "interpretation": "Any uncontrolled medical problem OR undergoing complex surgery. Moderate risk requiring enhanced perioperative monitoring and management. Consider intensive care unit monitoring and specialized cardiac anesthesia techniques."
            },
            4: {
                "stage": "CARE 4",
                "description": "High Risk",
                "interpretation": "Any uncontrolled medical problem AND undergoing complex surgery. High risk requiring intensive monitoring, specialized anesthetic management, and likely ICU care. Multidisciplinary approach recommended."
            },
            5: {
                "stage": "CARE 5",
                "description": "Very High Risk",
                "interpretation": "Chronic or advanced cardiac disease undergoing cardiac surgery as last hope to save or improve life. Very high risk with guarded prognosis. Requires maximum perioperative support and family counseling regarding risks."
            },
            6: {
                "stage": "CARE 6",
                "description": "Extreme Risk",
                "interpretation": "Emergency surgery (CARE 5 + 1 point for emergency). Extreme risk with very guarded prognosis. Requires immediate operative intervention with maximum perioperative support. Extensive family discussion regarding outcomes essential."
            }
        }
        
        return interpretations.get(category, interpretations[5])


def calculate_care_score(
    cardiac_disease_status: str,
    other_medical_problems: str,
    surgery_complexity: str,
    emergency_surgery: str,
    last_hope_surgery: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CareScoreCalculator()
    return calculator.calculate(
        cardiac_disease_status=cardiac_disease_status,
        other_medical_problems=other_medical_problems,
        surgery_complexity=surgery_complexity,
        emergency_surgery=emergency_surgery,
        last_hope_surgery=last_hope_surgery
    )