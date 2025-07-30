"""
CEDOCS Score for Emergency Department Overcrowding Calculator

Community Emergency Department Overcrowding Scale (CEDOCS) estimates the severity 
of overcrowding in community emergency departments.

References:
1. Weiss SJ, Rogers DB, Maas F, Ernst AA, Nick TG. Evaluating community ED crowding: 
   the Community ED Overcrowding Scale study. Am J Emerg Med. 2014 Nov;32(11):1357-63. 
   doi: 10.1016/j.ajem.2014.08.035.
2. Weiss SJ, Ernst AA, Derlet R, King R, Bair A, Nick TG. Relationship between the 
   National ED Overcrowding Scale and the number of patients who leave without being 
   seen in an academic ED. Am J Emerg Med. 2005 Jul;23(4):456-61.
"""

from typing import Dict, Any


class CedocsScoreCalculator:
    """Calculator for CEDOCS Score for Emergency Department Overcrowding"""
    
    def __init__(self):
        # Formula constants
        self.BASE_CONSTANT = -29.53
        self.CRITICAL_CARE_COEFF = 3.14
        self.WAIT_TIME_COEFF = 0.52
        self.WAITING_ROOM_COEFF = 1.14
        self.PATIENT_BED_RATIO_COEFF = 20.55
        self.ANNUAL_VISITS_COEFF = 0.00124
        
        # Conditional adjustment thresholds and coefficients
        self.THRESHOLD_A = 18811
        self.THRESHOLD_B = 43012
        self.THRESHOLD_C = 49466
        self.THRESHOLD_D = 67273
        
        self.COEFF_A = -1.09e-12
        self.COEFF_B = 8.18e-12
        self.COEFF_C = -8.18e-12
        self.COEFF_D = 1.08e-12
        
        # Default scaling factor
        self.DEFAULT_SCALING_FACTOR = 2.0
        
        # Overcrowding levels
        self.overcrowding_levels = [
            {"min": 1, "max": 20, "level": "Level 1", "description": "Not busy", 
             "status": "Normal operations"},
            {"min": 21, "max": 60, "level": "Level 2", "description": "Busy", 
             "status": "Increased activity"},
            {"min": 61, "max": 100, "level": "Level 3", "description": "Extremely busy but not overcrowded", 
             "status": "High activity"},
            {"min": 101, "max": 140, "level": "Level 4", "description": "Overcrowded", 
             "status": "Overcrowding threshold exceeded"},
            {"min": 141, "max": 180, "level": "Level 5", "description": "Severely overcrowded", 
             "status": "Severe overcrowding"},
            {"min": 181, "max": 200, "level": "Level 6", "description": "Dangerously overcrowded", 
             "status": "Critical overcrowding"}
        ]
    
    def calculate(
        self,
        critical_care_patients: int,
        longest_wait_time_minutes: int,
        waiting_room_patients: int,
        total_ed_patients: int,
        ed_beds: int,
        annual_ed_visits: int,
        scaling_factor: float = None
    ) -> Dict[str, Any]:
        """
        Calculates CEDOCS Score for Emergency Department Overcrowding
        
        Args:
            critical_care_patients: Number of patients requiring critical care in ED
            longest_wait_time_minutes: Waiting time of longest admitted patient
            waiting_room_patients: Number of patients in waiting room
            total_ed_patients: Total number of patients currently in ED
            ed_beds: Total number of licensed beds in ED
            annual_ed_visits: Annual volume of ED visits
            scaling_factor: Optional scaling factor (default 2.0)
            
        Returns:
            Dict with CEDOCS score, overcrowding level, and recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            critical_care_patients, longest_wait_time_minutes, waiting_room_patients,
            total_ed_patients, ed_beds, annual_ed_visits, scaling_factor
        )
        
        # Use default scaling factor if not provided
        if scaling_factor is None:
            scaling_factor = self.DEFAULT_SCALING_FACTOR
        
        # Calculate patient-to-bed ratio
        patient_bed_ratio = total_ed_patients / ed_beds
        
        # Calculate base CEDOCS score
        raw_score = self._calculate_raw_cedocs(
            critical_care_patients, longest_wait_time_minutes, waiting_room_patients,
            patient_bed_ratio, annual_ed_visits
        )
        
        # Apply conditional adjustments
        adjustments = self._calculate_conditional_adjustments(annual_ed_visits)
        
        # Calculate final score with scaling
        final_score = (raw_score + adjustments) * scaling_factor
        
        # Ensure minimum score of 1
        final_score = max(1, final_score)
        
        # Get overcrowding assessment
        assessment = self._get_overcrowding_assessment(final_score)
        
        # Get detailed breakdown
        breakdown = self._get_calculation_breakdown(
            critical_care_patients, longest_wait_time_minutes, waiting_room_patients,
            total_ed_patients, ed_beds, annual_ed_visits, patient_bed_ratio,
            raw_score, adjustments, scaling_factor
        )
        
        return {
            "result": {
                "total_score": round(final_score, 1),
                "overcrowding_level": assessment["level"],
                "overcrowding_status": assessment["status"],
                "is_overcrowded": final_score > 100,
                "patient_bed_ratio": round(patient_bed_ratio, 2),
                "calculation_breakdown": breakdown
            },
            "unit": "points",
            "interpretation": assessment["interpretation"],
            "stage": assessment["level"],
            "stage_description": assessment["description"]
        }
    
    def _validate_inputs(self, critical_care, wait_time, waiting_room, total_patients, 
                        ed_beds, annual_visits, scaling_factor):
        """Validates input parameters"""
        
        if not isinstance(critical_care, int) or critical_care < 0 or critical_care > 100:
            raise ValueError("Critical care patients must be an integer between 0-100")
        
        if not isinstance(wait_time, int) or wait_time < 0 or wait_time > 2880:
            raise ValueError("Longest wait time must be an integer between 0-2880 minutes")
        
        if not isinstance(waiting_room, int) or waiting_room < 0 or waiting_room > 500:
            raise ValueError("Waiting room patients must be an integer between 0-500")
        
        if not isinstance(total_patients, int) or total_patients < 0 or total_patients > 1000:
            raise ValueError("Total ED patients must be an integer between 0-1000")
        
        if not isinstance(ed_beds, int) or ed_beds < 1 or ed_beds > 500:
            raise ValueError("ED beds must be an integer between 1-500")
        
        if not isinstance(annual_visits, int) or annual_visits < 1000 or annual_visits > 500000:
            raise ValueError("Annual ED visits must be an integer between 1000-500000")
        
        if scaling_factor is not None:
            if not isinstance(scaling_factor, (int, float)) or scaling_factor < 0.1 or scaling_factor > 10.0:
                raise ValueError("Scaling factor must be a number between 0.1-10.0")
    
    def _calculate_raw_cedocs(self, critical_care, wait_time, waiting_room, 
                             patient_bed_ratio, annual_visits):
        """Calculates raw CEDOCS score before adjustments"""
        
        score = (
            self.BASE_CONSTANT +
            (self.CRITICAL_CARE_COEFF * critical_care) +
            (self.WAIT_TIME_COEFF * wait_time) +
            (self.WAITING_ROOM_COEFF * waiting_room) +
            (self.PATIENT_BED_RATIO_COEFF * patient_bed_ratio) +
            (self.ANNUAL_VISITS_COEFF * annual_visits)
        )
        
        return score
    
    def _calculate_conditional_adjustments(self, annual_visits):
        """Calculates conditional adjustments A, B, C, D based on annual visit thresholds"""
        
        adjustments = 0
        
        # Adjustment A: if annual visits >= 18,811
        if annual_visits >= self.THRESHOLD_A:
            adjustments += self.COEFF_A * ((annual_visits - self.THRESHOLD_A) ** 3)
        
        # Adjustment B: if annual visits >= 43,012
        if annual_visits >= self.THRESHOLD_B:
            adjustments += self.COEFF_B * ((annual_visits - self.THRESHOLD_B) ** 3)
        
        # Adjustment C: if annual visits >= 49,466
        if annual_visits >= self.THRESHOLD_C:
            adjustments += self.COEFF_C * ((annual_visits - self.THRESHOLD_C) ** 3)
        
        # Adjustment D: if annual visits >= 67,273
        if annual_visits >= self.THRESHOLD_D:
            adjustments += self.COEFF_D * ((annual_visits - self.THRESHOLD_D) ** 3)
        
        return adjustments
    
    def _get_overcrowding_assessment(self, score: float) -> Dict[str, str]:
        """Gets overcrowding assessment based on score"""
        
        for level_info in self.overcrowding_levels:
            if level_info["min"] <= score <= level_info["max"]:
                return self._get_level_interpretation(level_info, score)
        
        # Handle scores above 200 (extreme overcrowding)
        if score > 200:
            return {
                "level": "Level 6+",
                "description": "Extreme overcrowding",
                "status": "Crisis-level overcrowding",
                "interpretation": f"CEDOCS Score {score:.1f}: Extreme overcrowding situation exceeding validated scale. Immediate crisis intervention required including emergency protocols, ambulance diversion, and urgent administrative intervention to protect patient safety."
            }
        
        # Default for edge cases
        return {
            "level": "Unknown",
            "description": "Score outside validated range",
            "status": "Unknown status",
            "interpretation": f"CEDOCS Score {score:.1f}: Score outside validated range. Clinical assessment required."
        }
    
    def _get_level_interpretation(self, level_info: Dict, score: float) -> Dict[str, str]:
        """Gets detailed interpretation for specific overcrowding level"""
        
        base_interpretation = f"CEDOCS Score {score:.1f}: {level_info['description']}. "
        
        if level_info["level"] == "Level 1":
            interpretation = base_interpretation + "Normal ED operations with minimal crowding. Adequate resources and optimal patient flow. Continue standard protocols."
        elif level_info["level"] == "Level 2":
            interpretation = base_interpretation + "Increased activity but manageable. Monitor patient flow and resource allocation. Prepare for potential volume increases."
        elif level_info["level"] == "Level 3":
            interpretation = base_interpretation + "High activity level approaching capacity. Consider proactive measures to prevent overcrowding including expedited discharge planning."
        elif level_info["level"] == "Level 4":
            interpretation = base_interpretation + "Overcrowding threshold exceeded. Implement overcrowding protocols, resource reallocation, and consider reducing non-urgent admissions."
        elif level_info["level"] == "Level 5":
            interpretation = base_interpretation + "Severe overcrowding requiring immediate intervention. Consider diversion protocols, emergency staffing, and expedited patient placement."
        elif level_info["level"] == "Level 6":
            interpretation = base_interpretation + "Critical overcrowding situation. Implement emergency measures including possible ambulance diversion and crisis management protocols."
        else:
            interpretation = base_interpretation + "Assessment required based on local protocols."
        
        return {
            "level": level_info["level"],
            "description": level_info["description"],
            "status": level_info["status"],
            "interpretation": interpretation
        }
    
    def _get_calculation_breakdown(self, critical_care, wait_time, waiting_room, 
                                  total_patients, ed_beds, annual_visits, 
                                  patient_bed_ratio, raw_score, adjustments, scaling_factor):
        """Provides detailed calculation breakdown"""
        
        return {
            "input_parameters": {
                "critical_care_patients": critical_care,
                "longest_wait_time_minutes": wait_time,
                "waiting_room_patients": waiting_room,
                "total_ed_patients": total_patients,
                "ed_beds": ed_beds,
                "annual_ed_visits": annual_visits,
                "patient_bed_ratio": round(patient_bed_ratio, 2)
            },
            "calculation_components": {
                "base_constant": self.BASE_CONSTANT,
                "critical_care_contribution": round(self.CRITICAL_CARE_COEFF * critical_care, 2),
                "wait_time_contribution": round(self.WAIT_TIME_COEFF * wait_time, 2),
                "waiting_room_contribution": round(self.WAITING_ROOM_COEFF * waiting_room, 2),
                "patient_bed_ratio_contribution": round(self.PATIENT_BED_RATIO_COEFF * patient_bed_ratio, 2),
                "annual_visits_contribution": round(self.ANNUAL_VISITS_COEFF * annual_visits, 2),
                "raw_score": round(raw_score, 2),
                "conditional_adjustments": round(adjustments, 2),
                "scaling_factor": scaling_factor
            },
            "volume_adjustments": self._get_volume_adjustment_details(annual_visits)
        }
    
    def _get_volume_adjustment_details(self, annual_visits):
        """Provides details about volume-based adjustments"""
        
        adjustments_applied = []
        
        if annual_visits >= self.THRESHOLD_A:
            adjustments_applied.append(f"Adjustment A applied (visits >= {self.THRESHOLD_A:,})")
        if annual_visits >= self.THRESHOLD_B:
            adjustments_applied.append(f"Adjustment B applied (visits >= {self.THRESHOLD_B:,})")
        if annual_visits >= self.THRESHOLD_C:
            adjustments_applied.append(f"Adjustment C applied (visits >= {self.THRESHOLD_C:,})")
        if annual_visits >= self.THRESHOLD_D:
            adjustments_applied.append(f"Adjustment D applied (visits >= {self.THRESHOLD_D:,})")
        
        if not adjustments_applied:
            adjustments_applied.append("No volume adjustments applied")
        
        return {
            "annual_visits": annual_visits,
            "adjustments_applied": adjustments_applied
        }


def calculate_cedocs_score(
    critical_care_patients: int,
    longest_wait_time_minutes: int,
    waiting_room_patients: int,
    total_ed_patients: int,
    ed_beds: int,
    annual_ed_visits: int,
    scaling_factor: float = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CedocsScoreCalculator()
    return calculator.calculate(
        critical_care_patients=critical_care_patients,
        longest_wait_time_minutes=longest_wait_time_minutes,
        waiting_room_patients=waiting_room_patients,
        total_ed_patients=total_ed_patients,
        ed_beds=ed_beds,
        annual_ed_visits=annual_ed_visits,
        scaling_factor=scaling_factor
    )