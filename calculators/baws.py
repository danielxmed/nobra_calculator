"""
Brief Alcohol Withdrawal Scale (BAWS) Calculator

Assesses alcohol withdrawal symptoms using 5 simple criteria: agitation, sweats, 
tremor, orientation, and hallucinations. Developed as a simplified alternative 
to CIWA-Ar that provides rapid assessment in clinical settings.

References:
- Rastegar DA, et al. Brief Alcohol Withdrawal Scale (BAWS): A practical tool 
  for the evaluation of alcohol withdrawal symptoms. Subst Abus. 2017;38(4):463-469.
- Chaudhry RA, Schreck JS. Evaluation of the Brief Alcohol Withdrawal Scale 
  Protocol at an Academic Medical Center. J Intensive Care Med. 2020;35(3):268-272.
"""

from typing import Dict, Any


class BawsCalculator:
    """Calculator for Brief Alcohol Withdrawal Scale (BAWS)"""
    
    def __init__(self):
        # Score interpretation thresholds
        self.MILD_THRESHOLD = 3
        self.MODERATE_THRESHOLD = 6
        self.SEVERE_THRESHOLD = 9
        
        # Parameter descriptions for validation
        self.PARAMETER_DESCRIPTIONS = {
            'tremor': {
                0: 'No tremor',
                1: 'Not visible, but can be felt',
                2: 'Moderate, with arms extended',
                3: 'At rest, without arms extended'
            },
            'sweats': {
                0: 'No sweats',
                1: 'Mild, barely visible',
                2: 'Beads of sweat',
                3: 'Drenching sweats'
            },
            'agitation': {
                0: 'Alert and calm (RASS = 0)',
                1: 'Restless, anxious, apprehensive (RASS = 1)',
                2: 'Agitated, frequent non-purposeful movement (RASS = 2)',
                3: 'Very agitated or combative (RASS = 3 or 4)'
            },
            'orientation': {
                0: 'Oriented to person, place, time',
                1: 'Disoriented to time or place, but not both',
                2: 'Disoriented to time and place',
                3: 'Disoriented to person'
            },
            'hallucinations': {
                0: 'None',
                1: 'Mild (vague report, reality testing intact)',
                2: 'Moderate (more defined hallucinations)',
                3: 'Severe (responding to internal stimuli, poor reality testing)'
            }
        }
    
    def calculate(self, tremor: int, sweats: int, agitation: int, 
                 orientation: int, hallucinations: int) -> Dict[str, Any]:
        """
        Calculates the BAWS score using the provided parameters
        
        Args:
            tremor (int): Tremor severity (0-3)
            sweats (int): Diaphoresis/sweating severity (0-3)
            agitation (int): Agitation level based on RASS scale (0-3)
            orientation (int): Orientation to person, place, and time (0-3)
            hallucinations (int): Presence and severity of hallucinations (0-3)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(tremor, sweats, agitation, orientation, hallucinations)
        
        # Calculate total score
        total_score = self._calculate_total_score(tremor, sweats, agitation, 
                                                orientation, hallucinations)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "components": {
                "tremor": tremor,
                "sweats": sweats,
                "agitation": agitation,
                "orientation": orientation,
                "hallucinations": hallucinations
            }
        }
    
    def _validate_inputs(self, tremor: int, sweats: int, agitation: int, 
                        orientation: int, hallucinations: int):
        """Validates input parameters"""
        
        parameters = {
            'tremor': tremor,
            'sweats': sweats,
            'agitation': agitation,
            'orientation': orientation,
            'hallucinations': hallucinations
        }
        
        for param_name, value in parameters.items():
            if not isinstance(value, int):
                raise ValueError(f"{param_name.capitalize()} must be an integer")
            
            if value < 0 or value > 3:
                raise ValueError(f"{param_name.capitalize()} must be between 0 and 3")
    
    def _calculate_total_score(self, tremor: int, sweats: int, agitation: int, 
                             orientation: int, hallucinations: int) -> int:
        """Calculates the total BAWS score"""
        
        return tremor + sweats + agitation + orientation + hallucinations
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            score (int): Total BAWS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.MILD_THRESHOLD:
            return {
                "stage": "Mild",
                "description": "Mild withdrawal symptoms",
                "interpretation": "Minimal intervention required. Continue monitoring and supportive care. Consider oral hydration and vitamins. No pharmacological intervention typically needed."
            }
        elif score < self.MODERATE_THRESHOLD:
            return {
                "stage": "Moderate", 
                "description": "Moderate withdrawal symptoms",
                "interpretation": "Moderate intervention required. Consider benzodiazepine treatment (e.g., diazepam 10mg PO q4h until BAWS <3). Monitor closely for progression. Ensure adequate hydration and electrolyte replacement."
            }
        elif score < self.SEVERE_THRESHOLD:
            return {
                "stage": "Severe",
                "description": "Severe withdrawal symptoms", 
                "interpretation": "Significant intervention required. Increased benzodiazepine dosing (e.g., diazepam 20mg PO q2h until BAWS <6). Consider ICU monitoring. Frequent vital sign monitoring and neurological assessment."
            }
        else:
            return {
                "stage": "Very Severe",
                "description": "Very severe withdrawal symptoms",
                "interpretation": "Immediate physician notification required. High-dose benzodiazepines, ICU care, and aggressive supportive measures. Risk of delirium tremens. Consider continuous monitoring and advanced airway management if needed."
            }


def calculate_baws(tremor: int, sweats: int, agitation: int, 
                  orientation: int, hallucinations: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_baws pattern
    """
    calculator = BawsCalculator()
    return calculator.calculate(tremor, sweats, agitation, orientation, hallucinations)