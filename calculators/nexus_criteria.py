"""
NEXUS Criteria for C-Spine Imaging Calculator

Clinically clears cervical spine fracture without imaging in alert, stable trauma patients.

The NEXUS (National Emergency X-Radiography Utilization Study) criteria help determine 
which blunt trauma patients do not require cervical spine imaging.

Reference: Hoffman JR, Mower WR, Wolfson AB, Todd KH, Zucker MI. Validity of a set 
of clinical criteria to rule out injury to the cervical spine in patients with blunt trauma. 
N Engl J Med. 2000;343(2):94-99.
"""

from typing import Dict, Any


class NexusCriteriaCalculator:
    """Calculator for NEXUS Criteria for C-Spine Imaging"""
    
    def __init__(self):
        # Valid options for each criterion
        self.VALID_TENDERNESS = ["absent", "present"]
        self.VALID_DEFICIT = ["absent", "present"]
        self.VALID_ALERTNESS = ["normal", "altered"]
        self.VALID_INTOXICATION = ["absent", "present"]
        self.VALID_DISTRACTION = ["absent", "present"]
    
    def calculate(self, midline_cervical_tenderness: str, focal_neurologic_deficit: str, 
                  altered_alertness: str, intoxication: str, distracting_injury: str) -> Dict[str, Any]:
        """
        Calculates NEXUS criteria assessment using the provided parameters
        
        Args:
            midline_cervical_tenderness (str): "absent" or "present"
            focal_neurologic_deficit (str): "absent" or "present"  
            altered_alertness (str): "normal" or "altered"
            intoxication (str): "absent" or "present"
            distracting_injury (str): "absent" or "present"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(midline_cervical_tenderness, focal_neurologic_deficit, 
                             altered_alertness, intoxication, distracting_injury)
        
        # Determine risk level based on all criteria
        risk_assessment = self._assess_risk(midline_cervical_tenderness, focal_neurologic_deficit, 
                                          altered_alertness, intoxication, distracting_injury)
        
        # Get interpretation
        interpretation = self._get_interpretation(risk_assessment)
        
        return {
            "result": risk_assessment,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, midline_cervical_tenderness, focal_neurologic_deficit, 
                        altered_alertness, intoxication, distracting_injury):
        """Validates input parameters"""
        
        if midline_cervical_tenderness not in self.VALID_TENDERNESS:
            raise ValueError(f"midline_cervical_tenderness must be one of: {self.VALID_TENDERNESS}")
        
        if focal_neurologic_deficit not in self.VALID_DEFICIT:
            raise ValueError(f"focal_neurologic_deficit must be one of: {self.VALID_DEFICIT}")
        
        if altered_alertness not in self.VALID_ALERTNESS:
            raise ValueError(f"altered_alertness must be one of: {self.VALID_ALERTNESS}")
        
        if intoxication not in self.VALID_INTOXICATION:
            raise ValueError(f"intoxication must be one of: {self.VALID_INTOXICATION}")
        
        if distracting_injury not in self.VALID_DISTRACTION:
            raise ValueError(f"distracting_injury must be one of: {self.VALID_DISTRACTION}")
    
    def _assess_risk(self, midline_cervical_tenderness, focal_neurologic_deficit, 
                    altered_alertness, intoxication, distracting_injury):
        """Implements the NEXUS criteria logic"""
        
        # For low risk, ALL criteria must be met:
        # 1. No midline cervical tenderness (absent)
        # 2. No focal neurologic deficit (absent)
        # 3. Normal alertness (normal)
        # 4. No intoxication (absent)
        # 5. No painful distracting injury (absent)
        
        criteria_met = [
            midline_cervical_tenderness == "absent",
            focal_neurologic_deficit == "absent",
            altered_alertness == "normal",
            intoxication == "absent",
            distracting_injury == "absent"
        ]
        
        # All criteria must be met for low risk
        if all(criteria_met):
            return "Low Risk - No Imaging Required"
        else:
            return "High Risk - Imaging Recommended"
    
    def _get_interpretation(self, risk_assessment: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the risk assessment
        
        Args:
            risk_assessment (str): Risk level determined by criteria
            
        Returns:
            Dict with interpretation
        """
        
        if risk_assessment == "Low Risk - No Imaging Required":
            return {
                "stage": "Low Risk",
                "description": "No cervical spine imaging required",
                "interpretation": "Patient meets all five NEXUS criteria and is at low risk for cervical spine injury. Cervical spine imaging can be safely avoided. Sensitivity 99.6% for detecting clinically significant cervical spine injuries."
            }
        else:
            return {
                "stage": "High Risk", 
                "description": "Cervical spine imaging recommended",
                "interpretation": "Patient does not meet all NEXUS criteria. Cervical spine imaging (CT scan preferred) is recommended to rule out cervical spine injury. Clinical assessment alone is insufficient to exclude injury."
            }


def calculate_nexus_criteria(midline_cervical_tenderness, focal_neurologic_deficit, 
                           altered_alertness, intoxication, distracting_injury) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_nexus_criteria pattern
    """
    calculator = NexusCriteriaCalculator()
    return calculator.calculate(midline_cervical_tenderness, focal_neurologic_deficit, 
                              altered_alertness, intoxication, distracting_injury)