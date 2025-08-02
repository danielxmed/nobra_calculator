"""
Mangled Extremity Severity Score (MESS) Calculator

Estimates viability of an extremity after trauma to determine need for salvage versus 
empirical amputation. Evaluates four key factors: limb ischemia, patient age, shock, 
and injury mechanism.

References:
1. Johansen K, Daines M, Howey T, Helfet D, Hansen ST Jr. Objective criteria accurately 
   predict amputation following lower extremity trauma. J Trauma. 1990 May;30(5):568-73. 
   doi: 10.1097/00005373-199005000-00007.
2. Bosse MJ, MacKenzie EJ, Kellam JF, Burgess AR, Webb LX, Swiontkowski MF, et al. 
   A prospective evaluation of the clinical utility of the lower-extremity injury-severity 
   scores. J Bone Joint Surg Am. 2001 Jan;83(1):3-14. doi: 10.2106/00004623-200101000-00002.
"""

from typing import Dict, Any


class MangledExtremitySeverityScoreCalculator:
    """Calculator for Mangled Extremity Severity Score (MESS)"""
    
    def __init__(self):
        # Thresholds and constants
        self.ISCHEMIA_DURATION_THRESHOLD = 6.0  # hours
        self.AGE_THRESHOLD_1 = 30  # years
        self.AGE_THRESHOLD_2 = 50  # years
        
        # Valid options
        self.VALID_ISCHEMIA_LEVELS = [
            "reduced_pulse_normal_perfusion",
            "pulseless_paresthesias_slow_capillary_refill", 
            "cool_paralyzed_numb_insensate"
        ]
        
        self.VALID_SHOCK_LEVELS = [
            "no_shock_sbp_greater_than_90",
            "transient_hypotension",
            "persistent_hypotension"
        ]
        
        self.VALID_INJURY_MECHANISMS = [
            "low_energy",
            "medium_energy", 
            "high_energy",
            "very_high_energy"
        ]
    
    def calculate(self, limb_ischemia: str, ischemia_duration_hours: float, 
                  patient_age: int, shock_status: str, injury_mechanism: str) -> Dict[str, Any]:
        """
        Calculates the MESS score using the provided trauma parameters
        
        Args:
            limb_ischemia (str): Level of limb ischemia
            ischemia_duration_hours (float): Duration of ischemia in hours
            patient_age (int): Patient age in years
            shock_status (str): Hemodynamic shock status
            injury_mechanism (str): Energy level and mechanism of injury
            
        Returns:
            Dict with the result, component scores, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(limb_ischemia, ischemia_duration_hours, patient_age, 
                             shock_status, injury_mechanism)
        
        # Calculate individual component scores
        ischemia_base_score = self._calculate_ischemia_score(limb_ischemia)
        ischemia_multiplier = self._get_ischemia_multiplier(ischemia_duration_hours)
        final_ischemia_score = ischemia_base_score * ischemia_multiplier
        
        age_score = self._calculate_age_score(patient_age)
        shock_score = self._calculate_shock_score(shock_status)
        mechanism_score = self._calculate_mechanism_score(injury_mechanism)
        
        # Calculate total MESS score
        total_score = final_ischemia_score + age_score + shock_score + mechanism_score
        
        # Get interpretation and recommendations
        interpretation_data = self._get_interpretation(total_score)
        
        # Get detailed assessment
        assessment_data = self._get_assessment_data(total_score, ischemia_duration_hours)
        
        return {
            "result": {
                "total_score": total_score,
                "ischemia_base_score": ischemia_base_score,
                "ischemia_multiplier": ischemia_multiplier,
                "final_ischemia_score": final_ischemia_score,
                "age_score": age_score,
                "shock_score": shock_score,
                "mechanism_score": mechanism_score,
                "ischemia_category": f"Limb ischemia: {limb_ischemia.replace('_', ' ')}",
                "ischemia_duration_category": f"Ischemia duration: {ischemia_duration_hours} hours {'(>6h, doubled)' if ischemia_duration_hours > self.ISCHEMIA_DURATION_THRESHOLD else ''}",
                "age_category": f"Age: {patient_age} years",
                "shock_category": f"Shock status: {shock_status.replace('_', ' ')}",
                "mechanism_category": f"Injury mechanism: {injury_mechanism.replace('_', ' ')}",
                "assessment_data": assessment_data
            },
            "unit": "points",
            "interpretation": interpretation_data["interpretation"],
            "stage": interpretation_data["stage"],
            "stage_description": interpretation_data["description"]
        }
    
    def _validate_inputs(self, limb_ischemia: str, ischemia_duration_hours: float,
                        patient_age: int, shock_status: str, injury_mechanism: str):
        """Validates input parameters"""
        
        # Validate limb ischemia
        if not isinstance(limb_ischemia, str):
            raise ValueError("Limb ischemia must be a string")
        
        if limb_ischemia not in self.VALID_ISCHEMIA_LEVELS:
            raise ValueError(f"Limb ischemia must be one of: {', '.join(self.VALID_ISCHEMIA_LEVELS)}")
        
        # Validate ischemia duration
        if not isinstance(ischemia_duration_hours, (int, float)):
            raise ValueError("Ischemia duration must be a number")
        
        if ischemia_duration_hours < 0.0 or ischemia_duration_hours > 24.0:
            raise ValueError("Ischemia duration must be between 0.0 and 24.0 hours")
        
        # Validate patient age
        if not isinstance(patient_age, int):
            raise ValueError("Patient age must be an integer")
        
        if patient_age < 0 or patient_age > 120:
            raise ValueError("Patient age must be between 0 and 120 years")
        
        # Validate shock status
        if not isinstance(shock_status, str):
            raise ValueError("Shock status must be a string")
        
        if shock_status not in self.VALID_SHOCK_LEVELS:
            raise ValueError(f"Shock status must be one of: {', '.join(self.VALID_SHOCK_LEVELS)}")
        
        # Validate injury mechanism
        if not isinstance(injury_mechanism, str):
            raise ValueError("Injury mechanism must be a string")
        
        if injury_mechanism not in self.VALID_INJURY_MECHANISMS:
            raise ValueError(f"Injury mechanism must be one of: {', '.join(self.VALID_INJURY_MECHANISMS)}")
    
    def _calculate_ischemia_score(self, limb_ischemia: str) -> int:
        """Calculates base score for limb ischemia"""
        
        ischemia_scores = {
            "reduced_pulse_normal_perfusion": 1,
            "pulseless_paresthesias_slow_capillary_refill": 2,
            "cool_paralyzed_numb_insensate": 3
        }
        
        return ischemia_scores[limb_ischemia]
    
    def _get_ischemia_multiplier(self, ischemia_duration_hours: float) -> int:
        """Determines multiplier for ischemia score based on duration"""
        return 2 if ischemia_duration_hours > self.ISCHEMIA_DURATION_THRESHOLD else 1
    
    def _calculate_age_score(self, patient_age: int) -> int:
        """Calculates score based on patient age"""
        
        if patient_age < self.AGE_THRESHOLD_1:
            return 0
        elif patient_age < self.AGE_THRESHOLD_2:
            return 1
        else:
            return 2
    
    def _calculate_shock_score(self, shock_status: str) -> int:
        """Calculates score based on shock status"""
        
        shock_scores = {
            "no_shock_sbp_greater_than_90": 0,
            "transient_hypotension": 1,
            "persistent_hypotension": 2
        }
        
        return shock_scores[shock_status]
    
    def _calculate_mechanism_score(self, injury_mechanism: str) -> int:
        """Calculates score based on injury mechanism"""
        
        mechanism_scores = {
            "low_energy": 1,
            "medium_energy": 2,
            "high_energy": 3,
            "very_high_energy": 4
        }
        
        return mechanism_scores[injury_mechanism]
    
    def _get_assessment_data(self, total_score: int, ischemia_duration_hours: float) -> Dict[str, str]:
        """
        Returns detailed assessment data based on MESS score
        
        Args:
            total_score (int): Total MESS score
            ischemia_duration_hours (float): Duration of ischemia
            
        Returns:
            Dict with assessment information
        """
        
        traditional_threshold = "≥7 points (traditional)"
        modern_threshold = "≥8-9 points (modern recommendation)"
        
        if total_score < 7:
            recommendation = "Limb salvage recommended"
            confidence = "High confidence for salvage success"
        elif total_score == 7:
            recommendation = "Borderline case requiring clinical judgment"
            confidence = "Consider modern thresholds and patient factors"
        else:
            recommendation = "Primary amputation may be appropriate"
            confidence = "Discuss with multidisciplinary team"
        
        return {
            "traditional_threshold": traditional_threshold,
            "modern_threshold": modern_threshold,
            "recommendation": recommendation,
            "confidence_level": confidence,
            "ischemia_concerns": "Critical factor" if ischemia_duration_hours > self.ISCHEMIA_DURATION_THRESHOLD else "Manageable",
            "decision_factors": "Consider surgeon experience, available resources, patient preferences"
        }
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the risk category and interpretation based on the total score
        
        Args:
            total_score (int): Total MESS score
            
        Returns:
            Dict with risk category and clinical interpretation
        """
        
        if total_score <= 6:  # Low risk
            return {
                "stage": "Limb Salvage Likely",
                "description": "Low risk for amputation with good salvage potential",
                "interpretation": (
                    "MESS score suggests limb salvage is likely to be successful. Proceed with "
                    "aggressive limb preservation efforts including vascular repair, fracture "
                    "stabilization, and soft tissue reconstruction. This score indicates good "
                    "potential for functional limb preservation with appropriate surgical "
                    "intervention. Close monitoring and multidisciplinary team approach "
                    "recommended including orthopedic, vascular, and plastic surgery consultation. "
                    "Early rehabilitation planning should be initiated to optimize functional outcomes."
                )
            }
        elif total_score == 7:  # Borderline
            return {
                "stage": "Borderline Decision",
                "description": "Traditional threshold for amputation consideration",
                "interpretation": (
                    "MESS score of 7 represents the traditional threshold for amputation consideration. "
                    "However, modern surgical advances have led some experts to suggest higher "
                    "thresholds (8-9 points) for amputation decisions. This borderline score requires "
                    "careful clinical judgment considering patient factors including age, comorbidities, "
                    "functional expectations, available surgical expertise, and institutional resources. "
                    "Multidisciplinary discussion strongly recommended involving experienced trauma surgeons. "
                    "Consider patient preferences and quality of life implications in decision-making."
                )
            }
        else:  # High risk (≥8)
            return {
                "stage": "Amputation Likely",
                "description": "High probability of amputation requirement",
                "interpretation": (
                    "High MESS score suggests that primary amputation may be the most appropriate "
                    "treatment option. While traditionally scores ≥7 indicated amputation, modern "
                    "practice often uses higher thresholds due to advances in surgical techniques, "
                    "vascular repair, and wound management. Even with high scores, limb salvage may "
                    "be possible in selected cases with experienced surgical teams and adequate "
                    "resources. Consider factors including patient comorbidities, functional "
                    "expectations, available expertise, and patient preferences. Discuss risks and "
                    "benefits of salvage versus amputation with patient and family."
                )
            }


def calculate_mangled_extremity_severity_score(limb_ischemia: str, ischemia_duration_hours: float,
                                             patient_age: int, shock_status: str, 
                                             injury_mechanism: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MangledExtremitySeverityScoreCalculator()
    return calculator.calculate(limb_ischemia, ischemia_duration_hours, patient_age, 
                               shock_status, injury_mechanism)