"""
Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale Calculator

Assesses disease severity and functional status in patients with myasthenia gravis 
by evaluating 8 activities of daily living commonly affected by MG symptoms.

References:
1. Wolfe GI, Herbelin L, Nations SP, Foster B, Bryan WW, Barohn RJ. Myasthenia gravis 
   activities of daily living profile. Neurology. 1999;52(7):1487-9. 
   doi: 10.1212/wnl.52.7.1487.
2. Muppidi S, Wolfe GI, Conaway M, Burns TM; MG Composite and MG-QOL15 Study Group. 
   MG-ADL: still a relevant outcome measure. Muscle Nerve. 2011;44(5):727-31. 
   doi: 10.1002/mus.22140.
"""

from typing import Dict, Any


class MgAdlCalculator:
    """Calculator for Myasthenia Gravis Activities of Daily Living (MG-ADL) Scale"""
    
    def __init__(self):
        # Score range for each item
        self.MIN_SCORE = 0
        self.MAX_SCORE = 3
        self.MAX_TOTAL_SCORE = 24  # 8 items × 3 points each
        
        # Clinical interpretation thresholds
        self.MINIMAL_THRESHOLD = 2
        self.MILD_THRESHOLD = 6
        self.MODERATE_THRESHOLD = 12
        self.SEVERE_THRESHOLD = 18
    
    def calculate(self, talking: int, chewing: int, swallowing: int, breathing: int,
                 brushing_teeth_combing_hair: int, rising_from_chair: int,
                 eyelid_droop: int, double_vision: int) -> Dict[str, Any]:
        """
        Calculates the MG-ADL score for myasthenia gravis functional assessment
        
        Args:
            talking (int): Speech difficulty score (0-3)
            chewing (int): Chewing difficulty score (0-3)
            swallowing (int): Swallowing difficulty score (0-3)
            breathing (int): Breathing difficulty score (0-3)
            brushing_teeth_combing_hair (int): Arm function score (0-3)
            rising_from_chair (int): Leg function score (0-3)
            eyelid_droop (int): Ptosis severity score (0-3)
            double_vision (int): Diplopia severity score (0-3)
            
        Returns:
            Dict with the MG-ADL score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(talking, chewing, swallowing, breathing,
                            brushing_teeth_combing_hair, rising_from_chair,
                            eyelid_droop, double_vision)
        
        # Calculate total score
        total_score = (talking + chewing + swallowing + breathing +
                      brushing_teeth_combing_hair + rising_from_chair +
                      eyelid_droop + double_vision)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, talking: int, chewing: int, swallowing: int, 
                        breathing: int, brushing_teeth_combing_hair: int,
                        rising_from_chair: int, eyelid_droop: int, double_vision: int):
        """Validates input parameters"""
        
        parameters = [
            ("talking", talking),
            ("chewing", chewing),
            ("swallowing", swallowing),
            ("breathing", breathing),
            ("brushing_teeth_combing_hair", brushing_teeth_combing_hair),
            ("rising_from_chair", rising_from_chair),
            ("eyelid_droop", eyelid_droop),
            ("double_vision", double_vision)
        ]
        
        for param_name, param_value in parameters:
            if not isinstance(param_value, int):
                raise ValueError(f"{param_name} must be an integer")
            
            if param_value < self.MIN_SCORE or param_value > self.MAX_SCORE:
                raise ValueError(f"{param_name} must be between {self.MIN_SCORE} and {self.MAX_SCORE}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on MG-ADL score
        
        Args:
            score (int): Total MG-ADL score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= self.MINIMAL_THRESHOLD:
            return {
                "stage": "Minimal",
                "description": "Minimal functional impairment",
                "interpretation": f"MINIMAL FUNCTIONAL IMPAIRMENT (MG-ADL Score: {score}): Normal or near-normal "
                                "daily activities with little to no impact on quality of life. MANAGEMENT: Regular "
                                "monitoring and maintenance therapy as needed. Continue current treatment regimen if "
                                "stable. PROGNOSIS: Excellent functional status with minimal disease impact. "
                                "MONITORING: Routine follow-up every 3-6 months or as clinically indicated. "
                                "PATIENT EDUCATION: Continue medication compliance and report any symptom changes."
            }
        elif score <= self.MILD_THRESHOLD:
            return {
                "stage": "Mild",
                "description": "Mild functional impairment",
                "interpretation": f"MILD FUNCTIONAL IMPAIRMENT (MG-ADL Score: {score}): Some limitation in daily "
                                "activities with minor adjustments needed but generally maintains independence. "
                                "MANAGEMENT: Consider treatment optimization if symptoms are progressive. Monitor "
                                "for response to current therapy. TREATMENT: Adjust anticholinesterase dosing, "
                                "consider immunosuppressive therapy if not already on treatment. MONITORING: "
                                "Follow-up every 2-4 months to assess stability and treatment response. "
                                "QUALITY OF LIFE: Generally good with minor adaptations to daily routine."
            }
        elif score <= self.MODERATE_THRESHOLD:
            return {
                "stage": "Moderate",
                "description": "Moderate functional impairment",
                "interpretation": f"MODERATE FUNCTIONAL IMPAIRMENT (MG-ADL Score: {score}): Noticeable limitations "
                                "in daily activities requiring some assistance and therapeutic intervention. "
                                "MANAGEMENT: Active treatment optimization needed. Consider immunosuppressive "
                                "therapy if not already implemented. TREATMENT: Evaluate for steroid therapy, "
                                "immunosuppressants (azathioprine, mycophenolate), or other disease-modifying "
                                "treatments. MONITORING: Close follow-up every 1-2 months. Assess for treatment "
                                "response and side effects. SUPPORT: May benefit from physical therapy and "
                                "occupational therapy consultation."
            }
        elif score <= self.SEVERE_THRESHOLD:
            return {
                "stage": "Severe",
                "description": "Severe functional impairment",
                "interpretation": f"SEVERE FUNCTIONAL IMPAIRMENT (MG-ADL Score: {score}): Significant limitations "
                                "requiring assistance for many daily activities with active treatment optimization "
                                "needed. MANAGEMENT: Aggressive immunosuppressive therapy and consideration for "
                                "rescue treatments. TREATMENT: High-dose corticosteroids, intensive immunosuppression, "
                                "consider plasma exchange or IVIG. Evaluate for thymectomy if appropriate. "
                                "MONITORING: Intensive monitoring every 2-4 weeks. Watch for myasthenic or "
                                "cholinergic crisis. SUPPORT: Comprehensive multidisciplinary care including "
                                "respiratory monitoring, nutritional support, and rehabilitation services."
            }
        else:  # score > 18
            return {
                "stage": "Very Severe",
                "description": "Very severe functional impairment",
                "interpretation": f"VERY SEVERE FUNCTIONAL IMPAIRMENT (MG-ADL Score: {score}): Dependency for most "
                                "daily activities with potential need for intensive care support. MANAGEMENT: "
                                "Emergency evaluation for myasthenic crisis. Immediate aggressive treatment required. "
                                "TREATMENT: High-dose corticosteroids, plasma exchange or IVIG, intensive care "
                                "monitoring. Consider mechanical ventilation if respiratory compromise. "
                                "MONITORING: Continuous monitoring in intensive care setting. Respiratory function "
                                "assessment, nutritional support via gastric tube if needed. PROGNOSIS: Critical "
                                "functional status requiring immediate intervention and intensive medical support. "
                                "MULTIDISCIPLINARY: Neurology, critical care, respiratory therapy, and rehabilitation teams."
            }


def calculate_mg_adl(talking: int, chewing: int, swallowing: int, breathing: int,
                    brushing_teeth_combing_hair: int, rising_from_chair: int,
                    eyelid_droop: int, double_vision: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MgAdlCalculator()
    return calculator.calculate(talking, chewing, swallowing, breathing,
                               brushing_teeth_combing_hair, rising_from_chair,
                               eyelid_droop, double_vision)