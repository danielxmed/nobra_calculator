"""
Eastern Cooperative Oncology Group (ECOG) Performance Status Calculator

Determines patient's ability to tolerate therapies in severe illness, specifically for 
chemotherapy. This is a simple 5-point scale (0-4) that describes a patient's level 
of functioning in terms of their ability to care for themselves, daily activity, 
and physical ability.

References:
1. Oken MM, Creech RH, Tormey DC, Horton J, Davis TE, McFadden ET, et al. Toxicity 
   and response criteria of the Eastern Cooperative Oncology Group. Am J Clin Oncol. 
   1982;5(6):649-55. doi: 10.1097/00000421-198212000-00014.
2. Zubrod CG, Schneiderman M, Frei E, Brindley C, Gold GL, Shnider B, et al. Appraisal 
   of methods for the study of chemotherapy of cancer in man. J Chronic Dis. 1960;11:7-33.
"""

from typing import Dict, Any


class EcogPerformanceStatusCalculator:
    """Calculator for Eastern Cooperative Oncology Group (ECOG) Performance Status"""
    
    def __init__(self):
        # ECOG Performance Status definitions and scores
        self.ECOG_SCORES = {
            'ecog_0': 0,
            'ecog_1': 1,
            'ecog_2': 2,
            'ecog_3': 3,
            'ecog_4': 4
        }
        
        # Performance descriptions for validation and interpretation
        self.ECOG_DESCRIPTIONS = {
            0: {
                "stage": "ECOG 0",
                "description": "Fully active",
                "definition": "Fully active, able to carry on all pre-disease performance without restriction"
            },
            1: {
                "stage": "ECOG 1", 
                "description": "Restricted in strenuous activity",
                "definition": "Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature"
            },
            2: {
                "stage": "ECOG 2",
                "description": "Ambulatory but unable to work", 
                "definition": "Ambulatory and capable of all self-care but unable to carry out any work activities. Up and about more than 50% of waking hours"
            },
            3: {
                "stage": "ECOG 3",
                "description": "Limited self-care",
                "definition": "Capable of only limited self-care, confined to bed or chair more than 50% of waking hours"
            },
            4: {
                "stage": "ECOG 4",
                "description": "Completely disabled",
                "definition": "Completely disabled. Cannot carry on any self-care. Totally confined to bed or chair"
            }
        }
    
    def calculate(self, performance_status: str) -> Dict[str, Any]:
        """
        Determines the ECOG Performance Status score
        
        Args:
            performance_status (str): Patient's performance status level (ecog_0 through ecog_4)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate input
        self._validate_inputs(performance_status)
        
        # Get numeric score
        ecog_score = self._get_ecog_score(performance_status)
        
        # Get interpretation
        interpretation = self._get_interpretation(ecog_score)
        
        return {
            "result": ecog_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, performance_status: str):
        """Validates input parameters"""
        
        if not isinstance(performance_status, str):
            raise ValueError("Performance status must be a string")
        
        if performance_status.lower() not in self.ECOG_SCORES:
            valid_options = list(self.ECOG_SCORES.keys())
            raise ValueError(f"Performance status must be one of {valid_options}, got '{performance_status}'")
    
    def _get_ecog_score(self, performance_status: str) -> int:
        """Converts performance status string to numeric score"""
        
        return self.ECOG_SCORES[performance_status.lower()]
    
    def _get_interpretation(self, ecog_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ECOG score
        
        Args:
            ecog_score (int): ECOG Performance Status score (0-4)
            
        Returns:
            Dict with interpretation
        """
        
        # Get basic score information
        score_info = self.ECOG_DESCRIPTIONS[ecog_score]
        
        # Generate detailed clinical interpretation
        if ecog_score == 0:
            interpretation = (
                f"ECOG Performance Status 0 - {score_info['definition']}. "
                "Excellent candidate for chemotherapy with optimal tolerance expected. "
                "Suitable for all clinical trials and aggressive treatment regimens. "
                "Prognosis is generally favorable."
            )
        elif ecog_score == 1:
            interpretation = (
                f"ECOG Performance Status 1 - {score_info['definition']}. "
                "Good candidate for chemotherapy with acceptable tolerance. "
                "Suitable for most clinical trials. Generally good prognosis with appropriate treatment."
            )
        elif ecog_score == 2:
            interpretation = (
                f"ECOG Performance Status 2 - {score_info['definition']}. "
                "Borderline candidate for chemotherapy - requires careful evaluation. "
                "May benefit from supportive care and nutrition optimization. "
                "Consider less intensive treatment regimens. Prognosis varies significantly."
            )
        elif ecog_score == 3:
            interpretation = (
                f"ECOG Performance Status 3 - {score_info['definition']}. "
                "Generally NOT suitable for cytotoxic chemotherapy per clinical guidelines. "
                "Focus should be on palliative care and symptom management. "
                "May consider targeted therapy or immunotherapy in select cases. Poor prognosis."
            )
        else:  # ecog_score == 4
            interpretation = (
                f"ECOG Performance Status 4 - {score_info['definition']}. "
                "NOT suitable for chemotherapy - focus on comfort care and hospice services. "
                "Symptom management and quality of life are primary goals. "
                "Very poor prognosis with life expectancy typically measured in weeks to months."
            )
        
        return {
            "stage": score_info["stage"],
            "description": score_info["description"],
            "interpretation": interpretation
        }


def calculate_ecog_performance_status(performance_status: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ecog_performance_status pattern
    """
    calculator = EcogPerformanceStatusCalculator()
    return calculator.calculate(performance_status)