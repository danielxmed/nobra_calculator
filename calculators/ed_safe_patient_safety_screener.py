"""
ED-SAFE Patient Safety Screener 3 (PSS-3) Calculator

Screens for suicidality in emergency patients through universal screening with a 
validated 3-question tool. Designed for rapid assessment of suicide risk in the 
emergency department setting for patients with any chief complaint.

References:
1. Boudreaux ED, Camargo CA Jr, Arias SA, Blais RK, Horton BJ, Jaques ML, et al. 
   Improving Suicide Risk Screening and Detection in the Emergency Department. 
   Am J Prev Med. 2016;50(4):445-453. doi: 10.1016/j.amepre.2015.09.029.
2. Boudreaux ED, Jaques ML, Brady KM, Matson A, Allen MH. The patient safety screener: 
   validation of a brief suicide risk screener for emergency department settings. 
   Arch Suicide Res. 2015;19(2):151-60. doi: 10.1080/13811118.2015.1034604.
"""

from typing import Dict, Any


class EdSafePatientSafetyScreenerCalculator:
    """Calculator for ED-SAFE Patient Safety Screener 3 (PSS-3)"""
    
    def __init__(self):
        # PSS-3 questions for reference
        self.QUESTIONS = {
            'depression_past_2_weeks': 'Over the past 2 weeks, have you felt down, depressed, or hopeless?',
            'suicidal_thoughts_past_2_weeks': 'Over the past 2 weeks, have you had thoughts of killing yourself?',
            'lifetime_suicide_attempt': 'Have you ever in your lifetime made a suicide attempt?'
        }
        
        # Screening logic criteria
        self.POSITIVE_CRITERIA = [
            'suicidal_thoughts_past_2_weeks',  # Active suicidal ideation in past 2 weeks
            'lifetime_suicide_attempt'        # Lifetime history of suicide attempt
        ]
    
    def calculate(self, depression_past_2_weeks: str, suicidal_thoughts_past_2_weeks: str, 
                  lifetime_suicide_attempt: str) -> Dict[str, Any]:
        """
        Performs the PSS-3 suicide risk screening assessment
        
        Args:
            depression_past_2_weeks (str): Felt down, depressed, or hopeless in past 2 weeks (yes/no)
            suicidal_thoughts_past_2_weeks (str): Thoughts of killing yourself in past 2 weeks (yes/no)
            lifetime_suicide_attempt (str): Ever made a suicide attempt in lifetime (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'depression_past_2_weeks': depression_past_2_weeks,
            'suicidal_thoughts_past_2_weeks': suicidal_thoughts_past_2_weeks,
            'lifetime_suicide_attempt': lifetime_suicide_attempt
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Perform screening assessment
        screening_result = self._assess_screening_status(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(screening_result, parameters)
        
        return {
            "result": screening_result["status"],
            "unit": "status",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"Parameter '{param_name}' must be a string")
            
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"Parameter '{param_name}' must be 'yes' or 'no', got '{value}'")
    
    def _assess_screening_status(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Assesses PSS-3 screening status based on established criteria"""
        
        # Check positive screening criteria
        positive_indicators = []
        
        # Check each positive criterion
        for criterion in self.POSITIVE_CRITERIA:
            if parameters[criterion].lower() == 'yes':
                positive_indicators.append(criterion)
        
        # Determine screening result
        if len(positive_indicators) > 0:
            screening_status = "Positive Screen"
            is_positive = True
        else:
            screening_status = "Negative Screen"
            is_positive = False
        
        # Get additional context from depression question
        depression_present = parameters['depression_past_2_weeks'].lower() == 'yes'
        
        return {
            "status": screening_status,
            "is_positive": is_positive,
            "positive_indicators": positive_indicators,
            "depression_present": depression_present,
            "total_positive_criteria": len(positive_indicators)
        }
    
    def _get_interpretation(self, screening_result: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines the interpretation based on the PSS-3 screening result
        
        Args:
            screening_result (Dict): Results from PSS-3 screening assessment
            parameters (Dict): Original input parameters
            
        Returns:
            Dict with interpretation
        """
        
        if not screening_result["is_positive"]:
            # Negative screening
            interpretation = (
                "Negative screen for suicide risk. No current suicidal ideation or lifetime "
                "suicide attempt reported. Continue with routine emergency care. Consider "
                "documenting negative screen in medical record for continuity of care and "
                "quality improvement purposes."
            )
            
            # Add context if depression is present without suicidality
            if screening_result["depression_present"]:
                interpretation += (
                    " Note: Patient reported feeling down, depressed, or hopeless in past 2 weeks. "
                    "While not meeting PSS-3 positive screening criteria, consider addressing "
                    "depressive symptoms as clinically appropriate."
                )
            
            return {
                "stage": "Negative Screen",
                "description": "No current suicide risk indicators",
                "interpretation": interpretation
            }
        
        else:
            # Positive screening - determine specific indicators
            positive_indicators = screening_result["positive_indicators"]
            indicator_descriptions = []
            
            if 'suicidal_thoughts_past_2_weeks' in positive_indicators:
                indicator_descriptions.append("active suicidal ideation in past 2 weeks")
            
            if 'lifetime_suicide_attempt' in positive_indicators:
                indicator_descriptions.append("lifetime history of suicide attempt")
            
            indicators_text = " AND ".join(indicator_descriptions)
            
            interpretation = (
                f"Positive screen for suicide risk. Patient reports {indicators_text}. "
                "Requires immediate further assessment by treating clinician. Consider mental "
                "health consultation, comprehensive suicide risk assessment, and safety planning. "
                "Risk stratification with ED-SAFE Secondary Screener (ESS-6) recommended if available. "
                "Patient should not be left alone and requires continuous monitoring until "
                "comprehensive assessment is completed."
            )
            
            # Add context about depression if present
            if screening_result["depression_present"]:
                interpretation += (
                    " Patient also reports feeling down, depressed, or hopeless in past 2 weeks, "
                    "which may contribute to overall suicide risk profile."
                )
            
            return {
                "stage": "Positive Screen",
                "description": "Positive for suicide risk indicators",
                "interpretation": interpretation
            }


def calculate_ed_safe_patient_safety_screener(depression_past_2_weeks: str, suicidal_thoughts_past_2_weeks: str,
                                            lifetime_suicide_attempt: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ed_safe_patient_safety_screener pattern
    """
    calculator = EdSafePatientSafetyScreenerCalculator()
    return calculator.calculate(depression_past_2_weeks, suicidal_thoughts_past_2_weeks, lifetime_suicide_attempt)