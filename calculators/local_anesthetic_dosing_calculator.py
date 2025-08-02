"""
Local Anesthetic Dosing Calculator

Calculates maximum safe doses of local anesthetics to prevent Local Anesthetic 
Systemic Toxicity (LAST). Helps clinicians avoid toxic doses during regional 
anesthesia and local infiltration procedures.

References:
1. Neal JM, Woodward CM, Harrison TK. The American Society of Regional Anesthesia 
   and Pain Medicine Checklist for Managing Local Anesthetic Systemic Toxicity: 
   2017 Version. Reg Anesth Pain Med. 2018 Feb;43(2):150-153.
2. El-Boghdadly K, Pawa A, Chin KJ. Local anesthetic systemic toxicity: current 
   perspectives. Local Reg Anesth. 2018 Aug 8;11:35-44.
"""

from typing import Dict, Any


class LocalAnestheticDosingCalculator:
    """Calculator for Local Anesthetic Maximum Safe Dosing"""
    
    def __init__(self):
        # Maximum doses in mg/kg for each drug (subcutaneous/infiltration)
        self.MAX_DOSES = {
            "bupivacaine": 2.0,    # mg/kg
            "lidocaine": 4.5,      # mg/kg
            "mepivacaine": 4.4,    # mg/kg
            "ropivacaine": 3.0     # mg/kg
        }
        
        # Drug properties for clinical guidance
        self.DRUG_PROPERTIES = {
            "bupivacaine": {
                "name": "Bupivacaine",
                "onset": "Slow (15-30 min)",
                "duration": "Long (4-8 hours)",
                "potency": "High",
                "cardiotoxicity": "High"
            },
            "lidocaine": {
                "name": "Lidocaine",
                "onset": "Fast (2-5 min)",
                "duration": "Intermediate (1-3 hours)",
                "potency": "Intermediate",
                "cardiotoxicity": "Low"
            },
            "mepivacaine": {
                "name": "Mepivacaine",
                "onset": "Intermediate (5-15 min)",
                "duration": "Intermediate (2-4 hours)",
                "potency": "Intermediate",
                "cardiotoxicity": "Low"
            },
            "ropivacaine": {
                "name": "Ropivacaine",
                "onset": "Slow (15-30 min)",
                "duration": "Long (4-6 hours)",
                "potency": "High",
                "cardiotoxicity": "Lower than bupivacaine"
            }
        }
    
    def calculate(
        self,
        drug_type: str,
        patient_weight: float,
        concentration_percentage: float
    ) -> Dict[str, Any]:
        """
        Calculates maximum safe dose of local anesthetic
        
        Args:
            drug_type (str): Type of local anesthetic
            patient_weight (float): Patient weight in kg
            concentration_percentage (float): Concentration as percentage
            
        Returns:
            Dict with maximum doses and clinical guidance
        """
        
        # Validate inputs
        self._validate_inputs(drug_type, patient_weight, concentration_percentage)
        
        # Calculate maximum dose in mg
        max_dose_mg = self._calculate_max_dose_mg(drug_type, patient_weight)
        
        # Calculate concentration in mg/mL
        concentration_mg_ml = concentration_percentage * 10
        
        # Calculate maximum volume in mL
        max_volume_ml = max_dose_mg / concentration_mg_ml
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(
            drug_type, patient_weight, max_dose_mg, max_volume_ml, 
            concentration_percentage, concentration_mg_ml
        )
        
        return {
            "result": {
                "max_dose_mg": round(max_dose_mg, 1),
                "max_volume_ml": round(max_volume_ml, 1),
                "concentration_mg_ml": round(concentration_mg_ml, 1)
            },
            "unit": "mg and mL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, drug_type, patient_weight, concentration_percentage):
        """Validates input parameters"""
        
        if drug_type not in self.MAX_DOSES:
            raise ValueError(f"Drug type must be one of: {list(self.MAX_DOSES.keys())}")
        
        if not isinstance(patient_weight, (int, float)) or patient_weight < 1.0 or patient_weight > 200.0:
            raise ValueError("Patient weight must be between 1.0 and 200.0 kg")
        
        if not isinstance(concentration_percentage, (int, float)) or concentration_percentage < 0.1 or concentration_percentage > 5.0:
            raise ValueError("Concentration percentage must be between 0.1 and 5.0%")
    
    def _calculate_max_dose_mg(self, drug_type: str, patient_weight: float) -> float:
        """Calculates maximum dose in mg"""
        max_dose_per_kg = self.MAX_DOSES[drug_type]
        return max_dose_per_kg * patient_weight
    
    def _get_interpretation(
        self, drug_type, patient_weight, max_dose_mg, max_volume_ml, 
        concentration_percentage, concentration_mg_ml
    ) -> Dict[str, str]:
        """
        Provides clinical interpretation and safety guidance
        """
        
        drug_info = self.DRUG_PROPERTIES[drug_type]
        drug_name = drug_info["name"]
        
        # Build comprehensive clinical interpretation
        interpretation = (
            f"Local Anesthetic Dosing Calculation for {drug_name}:\n\n"
            f"Patient Parameters:\n"
            f"• Weight: {patient_weight:.1f} kg\n"
            f"• Drug: {drug_name} {concentration_percentage:.1f}% solution\n"
            f"• Concentration: {concentration_mg_ml:.1f} mg/mL\n\n"
            f"Maximum Safe Doses:\n"
            f"• Maximum total dose: {max_dose_mg:.1f} mg\n"
            f"• Maximum volume: {max_volume_ml:.1f} mL\n"
            f"• Dose limit: {self.MAX_DOSES[drug_type]:.1f} mg/kg\n\n"
            f"Drug Properties:\n"
            f"• Onset: {drug_info['onset']}\n"
            f"• Duration: {drug_info['duration']}\n"
            f"• Potency: {drug_info['potency']}\n"
            f"• Cardiotoxicity risk: {drug_info['cardiotoxicity']}\n\n"
            f"Safety Considerations:\n"
            f"• These doses are for subcutaneous infiltration and nerve blocks\n"
            f"• Consider lower doses in elderly patients, cardiac disease, or hepatic impairment\n"
            f"• Monitor for signs of Local Anesthetic Systemic Toxicity (LAST)\n"
            f"• CNS symptoms: altered mental status, seizures, metallic taste\n"
            f"• Cardiovascular symptoms: arrhythmias, hypotension, cardiac arrest\n"
            f"• Have lipid emulsion (Intralipid) readily available for LAST treatment\n\n"
            f"Clinical Recommendations:\n"
            f"• Always aspirate before injection to avoid intravascular administration\n"
            f"• Inject slowly with frequent aspiration\n"
            f"• Use smallest effective dose for desired clinical effect\n"
            f"• Consider fractionated dosing for large volumes\n"
            f"• Maintain continuous monitoring during and after administration"
        )
        
        return {
            "stage": "Safe Dosing Range",
            "stage_description": "Maximum safe dose calculated to prevent LAST",
            "interpretation": interpretation
        }


def calculate_local_anesthetic_dosing_calculator(
    drug_type: str,
    patient_weight: float,
    concentration_percentage: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_local_anesthetic_dosing_calculator pattern
    """
    calculator = LocalAnestheticDosingCalculator()
    return calculator.calculate(drug_type, patient_weight, concentration_percentage)