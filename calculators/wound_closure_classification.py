"""
Wound Closure Classification Calculator

Classifies wound closure types to guide surgical management strategies.
Stratifies wounds based on contamination, tissue loss, timing, and other factors.

References:
1. Hollander JE, Singer AJ. Laceration management. Ann Emerg Med. 1999;34(3):356-367. 
   doi: 10.1016/s0196-0644(99)70131-9
2. Singer AJ, Hollander JE, Quinn JV. Evaluation and management of traumatic lacerations. 
   N Engl J Med. 1997;337(16):1142-1148. doi: 10.1056/NEJM199710163371607
3. Forsch RT. Essentials of skin laceration repair. Am Fam Physician. 2008;78(8):945-951
"""

from typing import Dict, Any


class WoundClosureClassificationCalculator:
    """Calculator for Wound Closure Classification"""
    
    def __init__(self):
        # Time thresholds for wound closure (hours)
        self.PRIMARY_CLOSURE_IDEAL_TIME = 8.0  # hours
        self.PRIMARY_CLOSURE_MAX_TIME_WELL_VASC = 24.0  # hours for well-vascularized wounds
        self.PRIMARY_CLOSURE_MAX_TIME_FACE = 24.0  # hours for facial wounds
        self.OBSERVATION_PERIOD_MIN = 72.0  # 3 days minimum for tertiary closure
        self.OBSERVATION_PERIOD_MAX = 168.0  # 7 days maximum for tertiary closure
        
        # Classification descriptions
        self.CLASSIFICATION_DESCRIPTIONS = {
            "primary_closure": "Direct surgical closure indicated",
            "secondary_closure": "Healing by secondary intention",
            "tertiary_closure": "Delayed closure after observation"
        }
    
    def calculate(self, contamination_level: str, tissue_loss: str, time_since_injury: float,
                 vascularization: str, wound_location: str) -> Dict[str, Any]:
        """
        Classifies wound closure type based on clinical parameters
        
        Args:
            contamination_level (str): Level of wound contamination (clean, contaminated, grossly_contaminated)
            tissue_loss (str): Extent of tissue loss (minimal, moderate, significant)
            time_since_injury (float): Time elapsed since injury in hours
            vascularization (str): Wound bed vascularization (well_vascularized, moderately_vascularized, poorly_vascularized)
            wound_location (str): Anatomical location (face_scalp, extremities, trunk, hands_feet, joints, other)
            
        Returns:
            Dict with closure classification and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(contamination_level, tissue_loss, time_since_injury, vascularization, wound_location)
        
        # Determine closure type using decision algorithm
        closure_result = self._determine_closure_type(
            contamination_level, tissue_loss, time_since_injury, vascularization, wound_location
        )
        
        # Generate interpretation and recommendations
        interpretation = self._generate_interpretation(closure_result, time_since_injury, contamination_level, tissue_loss)
        
        return {
            "result": closure_result["closure_type"],
            "unit": "categorical",
            "interpretation": interpretation["interpretation"],
            "stage": closure_result["stage"],
            "stage_description": closure_result["stage_description"],
            "rationale": closure_result["rationale"],
            "recommendations": interpretation["recommendations"],
            "contraindications": interpretation["contraindications"],
            "timing_guidance": interpretation["timing_guidance"]
        }
    
    def _validate_inputs(self, contamination_level: str, tissue_loss: str, time_since_injury: float,
                        vascularization: str, wound_location: str):
        """Validates input parameters"""
        
        valid_contamination = ["clean", "contaminated", "grossly_contaminated"]
        if contamination_level not in valid_contamination:
            raise ValueError(f"Contamination level must be one of: {valid_contamination}")
        
        valid_tissue_loss = ["minimal", "moderate", "significant"]
        if tissue_loss not in valid_tissue_loss:
            raise ValueError(f"Tissue loss must be one of: {valid_tissue_loss}")
        
        if not isinstance(time_since_injury, (int, float)):
            raise ValueError("Time since injury must be a number")
        if time_since_injury < 0.0 or time_since_injury > 168.0:
            raise ValueError("Time since injury must be between 0 and 168 hours")
        
        valid_vascularization = ["well_vascularized", "moderately_vascularized", "poorly_vascularized"]
        if vascularization not in valid_vascularization:
            raise ValueError(f"Vascularization must be one of: {valid_vascularization}")
        
        valid_locations = ["face_scalp", "extremities", "trunk", "hands_feet", "joints", "other"]
        if wound_location not in valid_locations:
            raise ValueError(f"Wound location must be one of: {valid_locations}")
    
    def _determine_closure_type(self, contamination_level: str, tissue_loss: str, time_since_injury: float,
                               vascularization: str, wound_location: str) -> Dict[str, Any]:
        """Determines appropriate wound closure type using clinical decision algorithm"""
        
        # Check for absolute indications for secondary closure
        if tissue_loss == "significant":
            return {
                "closure_type": "secondary_closure",
                "stage": "Secondary Closure",
                "stage_description": "Healing by secondary intention",
                "rationale": "Significant tissue loss prevents tension-free primary closure"
            }
        
        # Check for absolute indications for tertiary closure
        if contamination_level == "grossly_contaminated":
            return {
                "closure_type": "tertiary_closure",
                "stage": "Tertiary (Delayed Primary) Closure",
                "stage_description": "Delayed closure after observation",
                "rationale": "Grossly contaminated wound requires debridement and observation to minimize infection risk"
            }
        
        # Evaluate primary closure eligibility
        primary_closure_eligible = self._assess_primary_closure_eligibility(
            contamination_level, tissue_loss, time_since_injury, vascularization, wound_location
        )
        
        if primary_closure_eligible["eligible"]:
            return {
                "closure_type": "primary_closure",
                "stage": "Primary Closure",
                "stage_description": "Direct surgical closure indicated",
                "rationale": primary_closure_eligible["rationale"]
            }
        
        # Determine between secondary and tertiary closure
        if contamination_level == "contaminated" or time_since_injury > self.PRIMARY_CLOSURE_MAX_TIME_WELL_VASC:
            return {
                "closure_type": "tertiary_closure",
                "stage": "Tertiary (Delayed Primary) Closure",
                "stage_description": "Delayed closure after observation",
                "rationale": "Contaminated wound or delayed presentation - requires observation before closure"
            }
        
        # Default to secondary closure if other criteria not met
        return {
            "closure_type": "secondary_closure",
            "stage": "Secondary Closure",
            "stage_description": "Healing by secondary intention",
            "rationale": "Wound characteristics favor healing by secondary intention"
        }
    
    def _assess_primary_closure_eligibility(self, contamination_level: str, tissue_loss: str,
                                          time_since_injury: float, vascularization: str,
                                          wound_location: str) -> Dict[str, Any]:
        """Assesses eligibility for primary closure"""
        
        reasons = []
        
        # Check contamination level
        if contamination_level != "clean":
            return {"eligible": False, "rationale": "Non-clean wound not suitable for primary closure"}
        
        # Check tissue loss
        if tissue_loss not in ["minimal", "moderate"]:
            return {"eligible": False, "rationale": "Significant tissue loss prevents primary closure"}
        
        # Check timing based on location and vascularization
        max_time = self._get_max_primary_closure_time(wound_location, vascularization)
        if time_since_injury > max_time:
            return {"eligible": False, "rationale": f"Time since injury ({time_since_injury:.1f}h) exceeds maximum for primary closure ({max_time}h)"}
        
        # Check vascularization
        if vascularization == "poorly_vascularized" and time_since_injury > self.PRIMARY_CLOSURE_IDEAL_TIME:
            return {"eligible": False, "rationale": "Poorly vascularized wound with delayed presentation not suitable for primary closure"}
        
        # Build rationale for eligible wounds
        if time_since_injury <= self.PRIMARY_CLOSURE_IDEAL_TIME:
            reasons.append("within ideal time window")
        elif time_since_injury <= max_time:
            reasons.append("within acceptable time window")
        
        if vascularization == "well_vascularized":
            reasons.append("well-vascularized wound bed")
        
        if wound_location == "face_scalp":
            reasons.append("facial location with excellent blood supply")
        
        rationale = f"Clean wound with {tissue_loss} tissue loss, " + ", ".join(reasons)
        
        return {"eligible": True, "rationale": rationale}
    
    def _get_max_primary_closure_time(self, wound_location: str, vascularization: str) -> float:
        """Determines maximum time for primary closure based on location and vascularization"""
        
        # Facial wounds have extended window due to excellent blood supply
        if wound_location == "face_scalp":
            return self.PRIMARY_CLOSURE_MAX_TIME_FACE
        
        # Well-vascularized wounds can be closed up to 24 hours
        if vascularization == "well_vascularized":
            return self.PRIMARY_CLOSURE_MAX_TIME_WELL_VASC
        
        # Other wounds ideally within 8 hours
        return self.PRIMARY_CLOSURE_IDEAL_TIME
    
    def _generate_interpretation(self, closure_result: Dict[str, Any], time_since_injury: float,
                               contamination_level: str, tissue_loss: str) -> Dict[str, Any]:
        """Generates clinical interpretation and recommendations"""
        
        closure_type = closure_result["closure_type"]
        
        if closure_type == "primary_closure":
            interpretation = f"PRIMARY CLOSURE recommended. {closure_result['rationale']}. Perform thorough irrigation and debridement before closure. Consider layered closure for deep wounds."
            
            recommendations = [
                "Thorough wound irrigation with normal saline",
                "Adequate anesthesia (local, regional, or systemic)",
                "Careful debridement of devitalized tissue",
                "Layered closure if deep subcutaneous involvement",
                "Appropriate suture selection based on location",
                "Post-procedure wound care instructions"
            ]
            
            contraindications = [
                "Signs of infection",
                "Grossly contaminated wound",
                "Significant tissue loss",
                "Patient unable to maintain wound care"
            ]
            
            timing_guidance = f"Closure within {self._get_max_primary_closure_time('face_scalp' if 'face' in closure_result.get('rationale', '') else 'other', 'well_vascularized')} hours optimal"
            
        elif closure_type == "secondary_closure":
            interpretation = f"SECONDARY CLOSURE (healing by secondary intention) recommended. {closure_result['rationale']}. Allow wound to heal through granulation tissue formation and wound contraction."
            
            recommendations = [
                "Daily dressing changes with appropriate wound care products",
                "Maintain moist wound environment",
                "Monitor for signs of infection",
                "Nutritional optimization for wound healing",
                "Consider negative pressure wound therapy if appropriate",
                "Regular wound assessment and documentation"
            ]
            
            contraindications = [
                "Functional or cosmetic areas where scarring unacceptable",
                "Large wounds where healing time would be excessive",
                "Patient unable to maintain daily dressing changes"
            ]
            
            timing_guidance = "Healing typically 2-6 weeks depending on wound size and patient factors"
            
        else:  # tertiary_closure
            interpretation = f"TERTIARY (DELAYED PRIMARY) CLOSURE recommended. {closure_result['rationale']}. Observe wound for 3-7 days before considering surgical closure."
            
            recommendations = [
                "Thorough wound exploration and debridement",
                "Copious irrigation with normal saline",
                "Daily wound assessment and dressing changes",
                "Antibiotic prophylaxis consideration based on contamination",
                "Re-evaluate for closure in 3-7 days",
                "Consider skin grafting if delayed closure not feasible"
            ]
            
            contraindications = [
                "Active signs of infection",
                "Continued contamination or foreign bodies",
                "Poor wound bed preparation",
                "Patient factors preventing delayed procedure"
            ]
            
            timing_guidance = f"Observe for {self.OBSERVATION_PERIOD_MIN/24:.0f}-{self.OBSERVATION_PERIOD_MAX/24:.0f} days before closure attempt"
        
        return {
            "interpretation": interpretation,
            "recommendations": recommendations,
            "contraindications": contraindications,
            "timing_guidance": timing_guidance
        }


def calculate_wound_closure_classification(contamination_level, tissue_loss, time_since_injury,
                                         vascularization, wound_location) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_wound_closure_classification pattern
    """
    calculator = WoundClosureClassificationCalculator()
    return calculator.calculate(contamination_level, tissue_loss, time_since_injury, vascularization, wound_location)