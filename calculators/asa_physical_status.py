"""
ASA Physical Status Classification System Calculator

The American Society of Anesthesiologists Physical Status Classification System
classifies patients based on their systemic disease and functional limitations
to help assess preoperative risk.

References (Vancouver style):
1. American Society of Anesthesiologists. ASA Physical Status Classification System. 
   Last amended December 13, 2020.
2. Hendrix JM, Garmon EH. American Society of Anesthesiologists Physical Status 
   Classification System. StatPearls Publishing; 2025.
3. Hurwitz EE, Simon M, Vinta SR, et al. Adding Examples to the ASA-Physical Status 
   Classification Improves Correct Assignment to Patients. Anesthesiology. 
   2017;126(4):614-622.
4. Mayhew D, Mendonca V, Murthy BVS. A review of ASA physical status - historical 
   perspectives and modern developments. Anaesthesia. 2019;74(3):373-379.
"""

from typing import Dict, Any


class AsaPhysicalStatusCalculator:
    """Calculator for ASA Physical Status Classification System"""
    
    def __init__(self):
        # ASA Classifications with descriptions and risk levels
        self.asa_classifications = {
            "asa_1": {
                "class": "ASA I",
                "description": "Normal healthy patient",
                "interpretation": "A normal healthy patient with no systemic disease. Examples: healthy non-smoking patient with no or minimal alcohol use, normal BMI.",
                "perioperative_risk": "Minimal risk"
            },
            "asa_2": {
                "class": "ASA II",
                "description": "Patient with mild systemic disease",
                "interpretation": "A patient with mild systemic disease without substantive functional limitations. Examples: current smoker, social alcohol drinker, pregnancy, obesity (BMI 30-40), well-controlled diabetes/hypertension, mild lung disease.",
                "perioperative_risk": "Low risk"
            },
            "asa_3": {
                "class": "ASA III",
                "description": "Patient with severe systemic disease",
                "interpretation": "A patient with severe systemic disease with substantive functional limitations. Examples: poorly controlled diabetes or hypertension, COPD, morbid obesity (BMI ≥40), active hepatitis, alcohol dependence, pacemaker, ESRD on dialysis, history of MI/CVA/TIA >3 months.",
                "perioperative_risk": "Moderate risk"
            },
            "asa_4": {
                "class": "ASA IV",
                "description": "Patient with severe systemic disease that is constant threat to life",
                "interpretation": "A patient with severe systemic disease that is a constant threat to life. Examples: recent (<3 months) MI/CVA/TIA, ongoing cardiac ischemia, severe valve dysfunction, shock, sepsis, DIC, ESRD not on scheduled dialysis.",
                "perioperative_risk": "High risk"
            },
            "asa_5": {
                "class": "ASA V",
                "description": "Moribund patient not expected to survive without operation",
                "interpretation": "A moribund patient who is not expected to survive without the operation. Examples: ruptured abdominal/thoracic aneurysm, massive trauma, intracranial bleed with mass effect, ischemic bowel with significant cardiac pathology.",
                "perioperative_risk": "Very high risk"
            },
            "asa_6": {
                "class": "ASA VI",
                "description": "Brain-dead patient for organ donation",
                "interpretation": "A declared brain-dead patient whose organs are being removed for donor purposes.",
                "perioperative_risk": "Not applicable"
            }
        }
    
    def calculate(self, physical_status: str, emergency_surgery: str) -> Dict[str, Any]:
        """
        Determines ASA Physical Status Classification
        
        Args:
            physical_status (str): Patient's physical status (asa_1, asa_2, asa_3, asa_4, asa_5, asa_6)
            emergency_surgery (str): Whether this is emergency surgery ("yes" or "no")
            
        Returns:
            Dict with the classification and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(physical_status, emergency_surgery)
        
        # Get classification details
        classification_info = self.asa_classifications[physical_status]
        
        # Determine final classification with emergency modifier
        final_classification = self._get_final_classification(
            classification_info["class"], 
            emergency_surgery
        )
        
        # Build comprehensive interpretation
        interpretation = self._build_interpretation(classification_info, emergency_surgery)
        
        return {
            "result": final_classification,
            "unit": "",
            "interpretation": interpretation,
            "stage": classification_info["class"],
            "stage_description": classification_info["description"]
        }
    
    def _validate_inputs(self, physical_status: str, emergency_surgery: str):
        """Validates input parameters"""
        
        valid_statuses = ["asa_1", "asa_2", "asa_3", "asa_4", "asa_5", "asa_6"]
        if physical_status not in valid_statuses:
            raise ValueError(f"Physical status must be one of: {', '.join(valid_statuses)}")
        
        if emergency_surgery not in ["yes", "no"]:
            raise ValueError("Emergency surgery must be 'yes' or 'no'")
    
    def _get_final_classification(self, base_class: str, emergency_surgery: str) -> str:
        """
        Determines final classification with emergency modifier
        
        Args:
            base_class (str): Base ASA class (e.g., "ASA I")
            emergency_surgery (str): Whether emergency surgery ("yes" or "no")
            
        Returns:
            str: Final classification with E modifier if applicable
        """
        if emergency_surgery == "yes":
            return f"{base_class}E"
        else:
            return base_class
    
    def _build_interpretation(self, classification_info: Dict[str, str], emergency_surgery: str) -> str:
        """
        Builds comprehensive interpretation based on classification and emergency status
        
        Args:
            classification_info (Dict): Classification details
            emergency_surgery (str): Whether emergency surgery
            
        Returns:
            str: Comprehensive interpretation
        """
        interpretation = classification_info["interpretation"]
        risk_level = classification_info["perioperative_risk"]
        
        # Add risk assessment
        interpretation += f" Perioperative risk: {risk_level}."
        
        # Add emergency modifier information if applicable
        if emergency_surgery == "yes":
            interpretation += " Emergency surgery modifier (E) applied - delay in treatment would significantly increase threat to life or body part."
        
        # Add general notes
        interpretation += " The ASA Physical Status Classification should be used alongside other factors such as type of surgery, patient frailty, and procedural complexity for comprehensive perioperative risk assessment."
        
        return interpretation


def calculate_asa_physical_status(physical_status: str, emergency_surgery: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_asa_physical_status pattern
    """
    calculator = AsaPhysicalStatusCalculator()
    return calculator.calculate(physical_status, emergency_surgery)
