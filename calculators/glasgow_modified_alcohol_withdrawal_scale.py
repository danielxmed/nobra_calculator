"""
Glasgow Modified Alcohol Withdrawal Scale (GMAWS) Calculator

The Glasgow Modified Alcohol Withdrawal Scale is a clinical tool used to assess and 
monitor the severity of alcohol withdrawal symptoms. It evaluates five clinical 
characteristics: tremor, sweating, hallucinations, orientation, and agitation, 
each scored from 0-2 points. The scale is part of the Glasgow Assessment and 
Management of Alcohol (GAMA) protocol and is used to guide benzodiazepine 
treatment dosing and monitoring intervals.

References (Vancouver style):
1. Sullivan JT, Sykora K, Schneiderman J, Naranjo CA, Sellers EM. Assessment of 
   alcohol withdrawal: the revised clinical institute withdrawal assessment for 
   alcohol scale (CIWA-Ar). Br J Addict. 1989;84(11):1353-1357.
2. Macleod AD, Peden NR, Pryde EA, Proctor SJ. Glasgow assessment and management 
   of alcohol guideline: an evidence-based guideline for the assessment and 
   management of patients with harmful alcohol use in acute medical units. 
   QJM. 2012;105(7):649-666.
3. Ferguson C, O'Neill A, Hameed A, Kenny RA, O'Neill D. FAST alcohol screening 
   and the modified Glasgow alcoholic hepatitis score in the general hospital. 
   QJM. 2009;102(4):269-273.
"""

from typing import Dict, Any


class GlasgowModifiedAlcoholWithdrawalScaleCalculator:
    """Calculator for Glasgow Modified Alcohol Withdrawal Scale (GMAWS)"""
    
    def __init__(self):
        # Component descriptions for interpretation
        self.TREMOR_DESCRIPTIONS = {
            0: "None",
            1: "Present with arms extended",
            2: "Present with arms at rest"
        }
        
        self.SWEATING_DESCRIPTIONS = {
            0: "None",
            1: "Moist skin", 
            2: "Drenching sweat"
        }
        
        self.HALLUCINATIONS_DESCRIPTIONS = {
            0: "None",
            1: "Uncertain, or patient reports but not distressed",
            2: "Present and distressed"
        }
        
        self.ORIENTATION_DESCRIPTIONS = {
            0: "Oriented",
            1: "Uncertain or disoriented in one domain",
            2: "Disoriented in ≥2 domains"
        }
        
        self.AGITATION_DESCRIPTIONS = {
            0: "None",
            1: "Anxious/restless",
            2: "Distressed or pacing"
        }
        
        # Treatment thresholds
        self.NO_TREATMENT_THRESHOLD = 0  # Score 0
        self.MILD_THRESHOLD = 3  # Scores 1-3
        self.MODERATE_THRESHOLD = 8  # Scores 4-8
        # Severe is 9-10
    
    def calculate(self, tremor: int, sweating: int, hallucinations: int, 
                 orientation: int, agitation: int) -> Dict[str, Any]:
        """
        Calculates GMAWS score using the five clinical components
        
        Args:
            tremor (int): Tremor assessment (0-2)
            sweating (int): Sweating assessment (0-2)
            hallucinations (int): Hallucinations assessment (0-2)
            orientation (int): Orientation assessment (0-2)
            agitation (int): Agitation assessment (0-2)
            
        Returns:
            Dict with the total score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(tremor, sweating, hallucinations, orientation, agitation)
        
        # Calculate total score
        total_score = tremor + sweating + hallucinations + orientation + agitation
        
        # Get interpretation
        interpretation = self._get_interpretation(
            total_score, tremor, sweating, hallucinations, orientation, agitation
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, tremor: int, sweating: int, hallucinations: int,
                        orientation: int, agitation: int):
        """Validates input parameters"""
        
        components = [
            ("tremor", tremor),
            ("sweating", sweating), 
            ("hallucinations", hallucinations),
            ("orientation", orientation),
            ("agitation", agitation)
        ]
        
        for name, value in components:
            if not isinstance(value, int) or value < 0 or value > 2:
                raise ValueError(f"{name.capitalize()} must be an integer between 0 and 2")
    
    def _get_interpretation(self, total_score: int, tremor: int, sweating: int,
                          hallucinations: int, orientation: int, agitation: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the GMAWS score
        
        Args:
            total_score (int): Total GMAWS score
            Individual component scores for detailed interpretation
            
        Returns:
            Dict with interpretation details
        """
        
        # Build component summary
        tremor_desc = self.TREMOR_DESCRIPTIONS[tremor]
        sweating_desc = self.SWEATING_DESCRIPTIONS[sweating]
        hallucinations_desc = self.HALLUCINATIONS_DESCRIPTIONS[hallucinations]
        orientation_desc = self.ORIENTATION_DESCRIPTIONS[orientation]
        agitation_desc = self.AGITATION_DESCRIPTIONS[agitation]
        
        component_summary = (
            f"Tremor: {tremor_desc}, "
            f"Sweating: {sweating_desc}, "
            f"Hallucinations: {hallucinations_desc}, "
            f"Orientation: {orientation_desc}, "
            f"Agitation: {agitation_desc}"
        )
        
        # Determine severity level and treatment recommendations
        if total_score == self.NO_TREATMENT_THRESHOLD:
            return {
                "stage": "No Withdrawal", 
                "description": "No significant withdrawal symptoms",
                "interpretation": (
                    f"GMAWS Score: {total_score}/10. [{component_summary}]. "
                    f"No significant alcohol withdrawal symptoms present. No benzodiazepines "
                    f"required at this time. Continue supportive care and monitoring. "
                    f"Reassess with GMAWS in 2 hours. Consider thiamine supplementation "
                    f"(100mg IV/PO daily) for Wernicke's encephalopathy prevention. "
                    f"Monitor for symptom progression and maintain adequate hydration."
                )
            }
        elif total_score <= self.MILD_THRESHOLD:
            return {
                "stage": "Mild Withdrawal",
                "description": "Mild alcohol withdrawal symptoms", 
                "interpretation": (
                    f"GMAWS Score: {total_score}/10. [{component_summary}]. "
                    f"Mild alcohol withdrawal symptoms present. Administer Diazepam 10mg "
                    f"PO or Lorazepam 2mg PO as first-line treatment. Reassess with GMAWS "
                    f"in 2 hours. Monitor vital signs and provide supportive care. "
                    f"Ensure thiamine supplementation (100mg IV/PO daily). Maintain "
                    f"adequate hydration and electrolyte balance. Consider environmental "
                    f"modifications (quiet room, minimal stimulation)."
                )
            }
        elif total_score <= self.MODERATE_THRESHOLD:
            return {
                "stage": "Moderate to Severe Withdrawal",
                "description": "Moderate to severe withdrawal symptoms",
                "interpretation": (
                    f"GMAWS Score: {total_score}/10. [{component_summary}]. "
                    f"Moderate to severe withdrawal symptoms requiring immediate treatment. "
                    f"Administer Diazepam 20mg PO or Lorazepam 4mg PO. Reassess with "
                    f"GMAWS in 1 hour. Close monitoring of vital signs required. "
                    f"Ensure thiamine 100mg IV/PO daily and consider IV multivitamins. "
                    f"Monitor for seizure activity and delirium tremens. Consider "
                    f"ICU-level care if symptoms progress. If score remains ≥8 for "
                    f">1 hour, urgent medical evaluation is required."
                )
            }
        else:  # Scores 9-10
            return {
                "stage": "Severe Withdrawal",
                "description": "Severe withdrawal symptoms with high risk of complications",
                "interpretation": (
                    f"GMAWS Score: {total_score}/10. [{component_summary}]. "
                    f"Severe alcohol withdrawal with high risk of delirium tremens and "
                    f"life-threatening complications. Administer Diazepam 20mg PO or "
                    f"Lorazepam 4mg PO immediately. Consider IV route if unable to take "
                    f"oral medications. Reassess with GMAWS in 1 hour. Continuous "
                    f"monitoring required - consider ICU admission. Thiamine 100mg IV "
                    f"plus IV multivitamins essential. Monitor for seizures, hyperthermia, "
                    f"and cardiovascular instability. If GMAWS ≥8 persists >1 hour, "
                    f"urgent medical evaluation and possible escalation of care required."
                )
            }


def calculate_glasgow_modified_alcohol_withdrawal_scale(tremor: int, sweating: int, 
                                                       hallucinations: int, orientation: int, 
                                                       agitation: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glasgow_modified_alcohol_withdrawal_scale pattern
    """
    calculator = GlasgowModifiedAlcoholWithdrawalScaleCalculator()
    return calculator.calculate(tremor, sweating, hallucinations, orientation, agitation)