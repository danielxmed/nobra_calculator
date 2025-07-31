"""
Edmonton Symptom Assessment System-revised (ESAS-r) Calculator

Assesses symptoms of patients receiving palliative care through a standardized 9-item 
self-report symptom intensity tool with improved clarity and definitions.

References:
1. Watanabe S, Nekolaichuk C, Beaumont C, Johnson L, Myers J, Strasser F. A multicenter study 
   comparing two numerical versions of the Edmonton Symptom Assessment System in palliative 
   care patients. J Pain Symptom Manage. 2011;41(2):456-68. doi: 10.1016/j.jpainsymman.2010.04.020.
2. Hui D, Bruera E. The Edmonton Symptom Assessment System 25 years later: Past, present, and 
   future developments. J Pain Symptom Manage. 2017;53(3):630-643. doi: 10.1016/j.jpainsymman.2016.10.370.
"""

from typing import Dict, Any


class EdmontonSymptomAssessmentSystemRevisedCalculator:
    """Calculator for Edmonton Symptom Assessment System-revised (ESAS-r)"""
    
    def __init__(self):
        # ESAS-r symptom definitions
        self.SYMPTOMS = {
            'pain': 'Pain intensity right now',
            'tiredness': 'Tiredness (weariness, weakness, or lack of energy) right now',
            'drowsiness': 'Drowsiness (feeling sleepy) right now',
            'nausea': 'Nausea (feeling sick to your stomach) right now',
            'lack_of_appetite': 'Lack of appetite (not feeling like eating) right now',
            'shortness_of_breath': 'Shortness of breath (difficulty breathing) right now',
            'depression': 'Depression (feeling sad, blue, or unhappy) right now',
            'anxiety': 'Anxiety (feeling nervous, worried, or fearful) right now',
            'wellbeing': 'Wellbeing (how you feel overall) right now'
        }
        
        # Symptom burden thresholds
        self.SEVERITY_THRESHOLDS = {
            'mild': (0, 17),      # Mild total symptom burden
            'moderate': (18, 35),  # Moderate total symptom burden
            'severe': (36, 90)     # Severe total symptom burden
        }
        
        # Individual symptom significance threshold
        self.CLINICALLY_SIGNIFICANT_SYMPTOM = 4
    
    def calculate(self, pain: int, tiredness: int, drowsiness: int, nausea: int, 
                  lack_of_appetite: int, shortness_of_breath: int, depression: int, 
                  anxiety: int, wellbeing: int) -> Dict[str, Any]:
        """
        Calculates the ESAS-r total score using the provided parameters
        
        Args:
            pain (int): Pain intensity right now (0-10)
            tiredness (int): Tiredness (weariness, weakness, or lack of energy) right now (0-10)
            drowsiness (int): Drowsiness (feeling sleepy) right now (0-10)
            nausea (int): Nausea (feeling sick to your stomach) right now (0-10)
            lack_of_appetite (int): Lack of appetite (not feeling like eating) right now (0-10)
            shortness_of_breath (int): Shortness of breath (difficulty breathing) right now (0-10)
            depression (int): Depression (feeling sad, blue, or unhappy) right now (0-10)
            anxiety (int): Anxiety (feeling nervous, worried, or fearful) right now (0-10)
            wellbeing (int): Wellbeing (how you feel overall) right now (0-10)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Map parameters for easier processing
        parameters = {
            'pain': pain,
            'tiredness': tiredness,
            'drowsiness': drowsiness,
            'nausea': nausea,
            'lack_of_appetite': lack_of_appetite,
            'shortness_of_breath': shortness_of_breath,
            'depression': depression,
            'anxiety': anxiety,
            'wellbeing': wellbeing
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate ESAS-r total score
        total_score = self._calculate_total_score(parameters)
        
        # Identify clinically significant symptoms
        significant_symptoms = self._identify_significant_symptoms(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, significant_symptoms)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, Any]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"Parameter '{param_name}' must be an integer")
            
            if value < 0 or value > 10:
                raise ValueError(f"Parameter '{param_name}' must be between 0 and 10, got {value}")
    
    def _calculate_total_score(self, parameters: Dict[str, Any]) -> int:
        """Calculates the ESAS-r total score"""
        
        # Sum all symptom scores
        total_score = sum(parameters.values())
        
        return total_score
    
    def _identify_significant_symptoms(self, parameters: Dict[str, Any]) -> Dict[str, int]:
        """Identifies clinically significant symptoms (score ≥4)"""
        
        significant_symptoms = {}
        
        for symptom_name, score in parameters.items():
            if score >= self.CLINICALLY_SIGNIFICANT_SYMPTOM:
                significant_symptoms[symptom_name] = score
        
        return significant_symptoms
    
    def _get_interpretation(self, total_score: int, significant_symptoms: Dict[str, int]) -> Dict[str, str]:
        """
        Determines the interpretation based on the ESAS-r total score and significant symptoms
        
        Args:
            total_score (int): Calculated ESAS-r total score
            significant_symptoms (Dict): Clinically significant symptoms (score ≥4)
            
        Returns:
            Dict with interpretation
        """
        
        # Determine severity category based on total score
        if total_score <= 17:
            severity_info = {
                "stage": "Mild",
                "description": "Mild total symptom burden",
                "base_text": ("Mild overall symptom burden. Symptoms are present but manageable with "
                            "standard palliative care interventions. Continue current symptom management "
                            "approach and monitor regularly for changes.")
            }
        elif total_score <= 35:
            severity_info = {
                "stage": "Moderate",
                "description": "Moderate total symptom burden",
                "base_text": ("Moderate overall symptom burden. Symptoms may be impacting quality of life "
                            "and daily functioning. Consider intensifying symptom management interventions "
                            "and more frequent assessments. Review current medications and palliative care plan.")
            }
        else:  # total_score >= 36
            severity_info = {
                "stage": "Severe",
                "description": "Severe total symptom burden",
                "base_text": ("Severe overall symptom burden significantly impacting quality of life. "
                            "Urgent review and optimization of symptom management required. Consider "
                            "specialist palliative care consultation, medication adjustments, and "
                            "comprehensive care plan revision. Daily or more frequent monitoring recommended.")
            }
        
        # Add information about significant individual symptoms
        interpretation_text = severity_info["base_text"]
        
        if significant_symptoms:
            symptom_names = []
            for symptom_name, score in significant_symptoms.items():
                # Convert snake_case to readable format
                readable_name = symptom_name.replace('_', ' ').title()
                if symptom_name == 'lack_of_appetite':
                    readable_name = 'Lack of Appetite'
                elif symptom_name == 'shortness_of_breath':
                    readable_name = 'Shortness of Breath'
                symptom_names.append(f"{readable_name} ({score}/10)")
            
            interpretation_text += (f" Clinically significant symptoms (≥4/10) requiring targeted "
                                  f"intervention: {', '.join(symptom_names)}.")
        else:
            interpretation_text += " No individual symptoms reach the clinically significant threshold (≥4/10)."
        
        # Add general monitoring guidance
        interpretation_text += (" Use ESAS-r for longitudinal monitoring to track symptom changes "
                              "and treatment response over time.")
        
        return {
            "stage": severity_info["stage"],
            "description": severity_info["description"],
            "interpretation": interpretation_text
        }


def calculate_edmonton_symptom_assessment_system_revised(pain: int, tiredness: int, drowsiness: int, 
                                                       nausea: int, lack_of_appetite: int, 
                                                       shortness_of_breath: int, depression: int, 
                                                       anxiety: int, wellbeing: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_edmonton_symptom_assessment_system_revised pattern
    """
    calculator = EdmontonSymptomAssessmentSystemRevisedCalculator()
    return calculator.calculate(pain, tiredness, drowsiness, nausea, lack_of_appetite, 
                               shortness_of_breath, depression, anxiety, wellbeing)