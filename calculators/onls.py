"""
Overall Neuropathy Limitations Scale (ONLS) Calculator

Quantifies the severity of functional disability in peripheral neuropathy by 
assessing upper and lower extremity functional activities. Validated scale 
for tracking disease progression and treatment response in neuropathic conditions.

References:
1. Graham RC, Hughes RA. A modified peripheral neuropathy scale: the Overall 
   Neuropathy Limitations Scale. J Neurol Neurosurg Psychiatry. 2006;77(8):973-6. 
   doi: 10.1136/jnnp.2005.081547.
2. Hughes RA, Donofrio P, Bril V, Dalakas MC, Deng C, Hanna K, et al. 
   Intravenous immune globulin (10% caprylate-chromatography purified) for the 
   treatment of chronic inflammatory demyelinating polyradiculoneuropathy 
   (ICE study): a randomised placebo-controlled trial. Lancet Neurol. 
   2008;7(2):136-44. doi: 10.1016/S1474-4422(07)70329-0.
"""

from typing import Dict, Any


class OnlsCalculator:
    """Calculator for Overall Neuropathy Limitations Scale (ONLS)"""
    
    def __init__(self):
        # ONLS scoring ranges
        self.MIN_ARMS_SCORE = 0
        self.MAX_ARMS_SCORE = 5
        self.MIN_LEGS_SCORE = 0
        self.MAX_LEGS_SCORE = 7
        self.MIN_TOTAL_SCORE = 0
        self.MAX_TOTAL_SCORE = 12
        
        # Interpretation thresholds
        self.MILD_THRESHOLD = 1
        self.MODERATE_THRESHOLD = 4
        self.SEVERE_THRESHOLD = 7
        self.VERY_SEVERE_THRESHOLD = 10
    
    def calculate(self, arms_grade: int, legs_grade: int) -> Dict[str, Any]:
        """
        Calculates the Overall Neuropathy Limitations Scale (ONLS) score
        
        Args:
            arms_grade (int): Arms functional disability grade (0-5)
            legs_grade (int): Legs functional disability grade (0-7)
            
        Returns:
            Dict with the total score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(arms_grade, legs_grade)
        
        # Calculate total score
        total_score = arms_grade + legs_grade
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, arms_grade, legs_grade)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, arms_grade: int, legs_grade: int):
        """Validates input parameters"""
        
        if not isinstance(arms_grade, int):
            raise ValueError("Arms grade must be an integer")
        
        if not isinstance(legs_grade, int):
            raise ValueError("Legs grade must be an integer")
        
        if arms_grade < self.MIN_ARMS_SCORE or arms_grade > self.MAX_ARMS_SCORE:
            raise ValueError(f"Arms grade must be between {self.MIN_ARMS_SCORE} and {self.MAX_ARMS_SCORE}")
        
        if legs_grade < self.MIN_LEGS_SCORE or legs_grade > self.MAX_LEGS_SCORE:
            raise ValueError(f"Legs grade must be between {self.MIN_LEGS_SCORE} and {self.MAX_LEGS_SCORE}")
    
    def _get_interpretation(self, total_score: int, arms_grade: int, legs_grade: int) -> Dict[str, str]:
        """
        Determines the interpretation based on total ONLS score
        
        Args:
            total_score (int): Total ONLS score
            arms_grade (int): Arms functional grade
            legs_grade (int): Legs functional grade
            
        Returns:
            Dict with interpretation details
        """
        
        # Create component description
        arms_description = self._get_arms_description(arms_grade)
        legs_description = self._get_legs_description(legs_grade)
        
        if total_score == 0:
            return {
                "stage": "No Disability",
                "description": "No functional limitations",
                "interpretation": f"NO FUNCTIONAL DISABILITY (ONLS Score: {total_score}): Normal function in both "
                                f"arms and legs with no evidence of functional disability from peripheral neuropathy. "
                                f"ARMS: {arms_description} LEGS: {legs_description} CLINICAL SIGNIFICANCE: Excellent "
                                f"functional status with preserved independence in all activities of daily living. "
                                f"MONITORING: Continue regular neurological assessments to detect early changes. "
                                f"PROGNOSIS: Favorable functional outlook with current treatment regimen."
            }
        elif total_score < self.MODERATE_THRESHOLD:
            return {
                "stage": "Mild Disability",
                "description": "Minimal functional limitations",
                "interpretation": f"MILD FUNCTIONAL DISABILITY (ONLS Score: {total_score}): Mild peripheral neuropathy "
                                f"with minimal impact on daily activities. ARMS: {arms_description} LEGS: {legs_description} "
                                f"FUNCTIONAL STATUS: Some symptoms present but function largely preserved. Patient remains "
                                f"independent in most activities. MANAGEMENT: Continue current treatment, monitor for "
                                f"progression, consider physical therapy for symptom management. PROGNOSIS: Generally "
                                f"good functional outcome with appropriate management."
            }
        elif total_score < self.SEVERE_THRESHOLD:
            return {
                "stage": "Moderate Disability",
                "description": "Moderate functional limitations",
                "interpretation": f"MODERATE FUNCTIONAL DISABILITY (ONLS Score: {total_score}): Moderate peripheral "
                                f"neuropathy with noticeable impact on daily activities. ARMS: {arms_description} "
                                f"LEGS: {legs_description} FUNCTIONAL STATUS: May require assistive devices, "
                                f"environmental modifications, or adaptive strategies. MANAGEMENT: Consider treatment "
                                f"optimization, physical/occupational therapy, assistive devices as needed. "
                                f"MONITORING: Regular assessment for progression and treatment response required."
            }
        elif total_score < self.VERY_SEVERE_THRESHOLD:
            return {
                "stage": "Severe Disability",
                "description": "Significant functional limitations",
                "interpretation": f"SEVERE FUNCTIONAL DISABILITY (ONLS Score: {total_score}): Severe peripheral "
                                f"neuropathy with substantial functional impairment. ARMS: {arms_description} "
                                f"LEGS: {legs_description} FUNCTIONAL STATUS: Requires significant assistance, "
                                f"adaptive equipment, or environmental modifications for daily activities. "
                                f"MANAGEMENT: Aggressive treatment optimization, comprehensive rehabilitation, "
                                f"mobility aids, and care coordination. SUPPORT: Consider disability services "
                                f"and caregiver support systems."
            }
        else:  # score >= 10
            return {
                "stage": "Very Severe Disability",
                "description": "Profound functional limitations",
                "interpretation": f"VERY SEVERE FUNCTIONAL DISABILITY (ONLS Score: {total_score}): Very severe "
                                f"peripheral neuropathy with profound disability. ARMS: {arms_description} "
                                f"LEGS: {legs_description} FUNCTIONAL STATUS: Requires extensive care and "
                                f"assistance for most activities of daily living. MANAGEMENT: Comprehensive "
                                f"multidisciplinary care including aggressive treatment, extensive rehabilitation, "
                                f"full-time care assistance. SUPPORT: Disability services, home modifications, "
                                f"and comprehensive caregiver support essential."
            }
    
    def _get_arms_description(self, arms_grade: int) -> str:
        """Returns description of arms functional status"""
        descriptions = {
            0: "Normal arm function",
            1: "Minor symptoms not affecting function",
            2: "Mild disability affecting but not preventing function",
            3: "Moderate disability preventing some functions",
            4: "Severe disability preventing all functions, some purposeful movement remains",
            5: "Complete disability preventing all purposeful movements"
        }
        return descriptions.get(arms_grade, "Unknown")
    
    def _get_legs_description(self, legs_grade: int) -> str:
        """Returns description of legs functional status"""
        descriptions = {
            0: "Normal walking, stair climbing, and running",
            1: "Affected walking/stairs/running but normal gait",
            2: "Independent walking with abnormal gait", 
            3: "Requires unilateral support to walk 10 meters",
            4: "Requires bilateral support to walk 10 meters",
            5: "Wheelchair-bound but can stand/walk 1m with help",
            6: "Wheelchair-restricted with some purposeful leg movements",
            7: "Wheelchair/bed-restricted with no purposeful leg movements"
        }
        return descriptions.get(legs_grade, "Unknown")


def calculate_onls(arms_grade: int, legs_grade: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OnlsCalculator()
    return calculator.calculate(arms_grade, legs_grade)