"""
Maximum Allowable Blood Loss (ABL) Without Transfusion Calculator

Estimates maximum allowable blood loss intraoperatively before transfusion
should be considered, based on patient weight, age group, initial hemoglobin,
and acceptable final hemoglobin levels.

References:
1. Gross JB. Estimating allowable blood loss: corrected for dilution. 
   Anesthesiology. 1983 Mar;58(3):277-80. doi: 10.1097/00000542-198303000-00016.
2. Miller RD, ed. Miller's Anesthesia. 8th ed. Philadelphia, PA: Elsevier Saunders; 2015.
3. American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
   Practice guidelines for perioperative blood management: an updated report by the 
   American Society of Anesthesiologists Task Force on Perioperative Blood Management. 
   Anesthesiology. 2015;122(2):241-75.
"""

from typing import Dict, Any


class MaximumAllowableBloodLossWithoutTransfusionCalculator:
    """Calculator for Maximum Allowable Blood Loss Without Transfusion"""
    
    def __init__(self):
        # Blood volume coefficients by age group (mL/kg)
        self.BLOOD_VOLUME_COEFFICIENTS = {
            "adult_man": 75,
            "adult_woman": 65,
            "infant": 80,
            "neonate": 85,
            "premature_neonate": 96
        }
        
        # Clinical thresholds
        self.ACCURACY_THRESHOLD_PERCENTAGE = 20  # Calculation becomes inaccurate >20% EBV loss
        self.MINIMUM_TRANSFUSION_HB = 6.0  # Almost always require transfusion below 6 g/dL
        self.TYPICAL_TRANSFUSION_RANGE = (7.0, 10.0)  # Typical transfusion threshold range
        
        # Valid age groups
        self.VALID_AGE_GROUPS = list(self.BLOOD_VOLUME_COEFFICIENTS.keys())
        
        # Age group descriptions for clinical context
        self.AGE_GROUP_DESCRIPTIONS = {
            "adult_man": "Adult male (≥18 years)",
            "adult_woman": "Adult female (≥18 years)", 
            "infant": "Infant (1 month - 2 years)",
            "neonate": "Neonate (birth - 1 month)",
            "premature_neonate": "Premature neonate (<37 weeks gestation)"
        }
    
    def calculate(self, age_group: str, body_weight: float, initial_hemoglobin: float, 
                  final_hemoglobin: float) -> Dict[str, Any]:
        """
        Calculates maximum allowable blood loss without transfusion
        
        Args:
            age_group (str): Patient age group for blood volume coefficient
            body_weight (float): Patient weight in kg
            initial_hemoglobin (float): Preoperative hemoglobin in g/dL
            final_hemoglobin (float): Lowest acceptable hemoglobin in g/dL
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_group, body_weight, initial_hemoglobin, final_hemoglobin)
        
        # Calculate estimated blood volume
        estimated_blood_volume = self._calculate_estimated_blood_volume(age_group, body_weight)
        
        # Calculate average hemoglobin
        average_hemoglobin = self._calculate_average_hemoglobin(initial_hemoglobin, final_hemoglobin)
        
        # Calculate maximum allowable blood loss
        abl = self._calculate_abl(estimated_blood_volume, initial_hemoglobin, 
                                 final_hemoglobin, average_hemoglobin)
        
        # Get clinical assessment
        clinical_assessment = self._get_clinical_assessment(
            abl, estimated_blood_volume, age_group, body_weight, 
            initial_hemoglobin, final_hemoglobin
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(abl)
        
        return {
            "result": {
                "maximum_allowable_blood_loss_ml": round(abl, 1),
                "estimated_blood_volume_ml": round(estimated_blood_volume, 1),
                "blood_volume_coefficient_ml_kg": self.BLOOD_VOLUME_COEFFICIENTS[age_group],
                "average_hemoglobin_g_dl": round(average_hemoglobin, 2),
                "hemoglobin_difference_g_dl": round(initial_hemoglobin - final_hemoglobin, 2),
                "percentage_of_blood_volume": round((abl / estimated_blood_volume) * 100, 1),
                "clinical_assessment": clinical_assessment
            },
            "unit": "mL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_group: str, body_weight: float, 
                        initial_hemoglobin: float, final_hemoglobin: float):
        """Validates input parameters"""
        
        # Validate age group
        if not isinstance(age_group, str):
            raise ValueError("Age group must be a string")
        
        if age_group not in self.VALID_AGE_GROUPS:
            raise ValueError(f"Age group must be one of {self.VALID_AGE_GROUPS}")
        
        # Validate body weight
        if not isinstance(body_weight, (int, float)):
            raise ValueError("Body weight must be a number")
        
        if body_weight < 0.5 or body_weight > 200:
            raise ValueError("Body weight must be between 0.5 and 200 kg")
        
        # Validate hemoglobin values
        if not isinstance(initial_hemoglobin, (int, float)):
            raise ValueError("Initial hemoglobin must be a number")
        
        if not isinstance(final_hemoglobin, (int, float)):
            raise ValueError("Final hemoglobin must be a number")
        
        if initial_hemoglobin < 3.0 or initial_hemoglobin > 25.0:
            raise ValueError("Initial hemoglobin must be between 3.0 and 25.0 g/dL")
        
        if final_hemoglobin < 3.0 or final_hemoglobin > 15.0:
            raise ValueError("Final hemoglobin must be between 3.0 and 15.0 g/dL")
        
        # Clinical validation
        if final_hemoglobin >= initial_hemoglobin:
            raise ValueError("Final hemoglobin must be lower than initial hemoglobin")
    
    def _calculate_estimated_blood_volume(self, age_group: str, body_weight: float) -> float:
        """
        Calculates estimated blood volume based on age group and weight
        
        Args:
            age_group (str): Patient age group
            body_weight (float): Patient weight in kg
            
        Returns:
            float: Estimated blood volume in mL
        """
        
        blood_volume_coefficient = self.BLOOD_VOLUME_COEFFICIENTS[age_group]
        estimated_blood_volume = body_weight * blood_volume_coefficient
        
        return estimated_blood_volume
    
    def _calculate_average_hemoglobin(self, initial_hemoglobin: float, 
                                    final_hemoglobin: float) -> float:
        """
        Calculates average hemoglobin for the Gross formula
        
        Args:
            initial_hemoglobin (float): Initial hemoglobin in g/dL
            final_hemoglobin (float): Final hemoglobin in g/dL
            
        Returns:
            float: Average hemoglobin in g/dL
        """
        
        return (initial_hemoglobin + final_hemoglobin) / 2
    
    def _calculate_abl(self, estimated_blood_volume: float, initial_hemoglobin: float,
                      final_hemoglobin: float, average_hemoglobin: float) -> float:
        """
        Calculates maximum allowable blood loss using Gross formula
        
        Args:
            estimated_blood_volume (float): EBV in mL
            initial_hemoglobin (float): Initial Hb in g/dL
            final_hemoglobin (float): Final Hb in g/dL
            average_hemoglobin (float): Average Hb in g/dL
            
        Returns:
            float: Maximum allowable blood loss in mL
        """
        
        # Gross formula: ABL = [EBV × (Hi - Hf)] / Hav
        hemoglobin_difference = initial_hemoglobin - final_hemoglobin
        abl = (estimated_blood_volume * hemoglobin_difference) / average_hemoglobin
        
        # Ensure non-negative result
        return max(0.0, abl)
    
    def _get_clinical_assessment(self, abl: float, estimated_blood_volume: float,
                               age_group: str, body_weight: float, initial_hemoglobin: float,
                               final_hemoglobin: float) -> Dict[str, Any]:
        """
        Provides clinical assessment of the ABL calculation
        
        Args:
            abl (float): Maximum allowable blood loss in mL
            estimated_blood_volume (float): Estimated blood volume in mL
            age_group (str): Patient age group
            body_weight (float): Patient weight in kg
            initial_hemoglobin (float): Initial hemoglobin in g/dL
            final_hemoglobin (float): Final hemoglobin in g/dL
            
        Returns:
            Dict with clinical assessment data
        """
        
        # Calculate percentage of blood volume
        percentage_ebv = (abl / estimated_blood_volume) * 100
        
        # Assess accuracy reliability
        accuracy_reliable = percentage_ebv <= self.ACCURACY_THRESHOLD_PERCENTAGE
        
        # Assess transfusion threshold appropriateness
        if final_hemoglobin < self.MINIMUM_TRANSFUSION_HB:
            threshold_assessment = "Very low - transfusion almost always required"
        elif self.TYPICAL_TRANSFUSION_RANGE[0] <= final_hemoglobin <= self.TYPICAL_TRANSFUSION_RANGE[1]:
            threshold_assessment = "Within typical transfusion threshold range"
        else:
            threshold_assessment = "Above typical transfusion threshold"
        
        # Assess patient size category
        if age_group in ["premature_neonate", "neonate"]:
            size_category = "Very small patient - small volumes clinically significant"
        elif age_group == "infant":
            size_category = "Small patient - careful monitoring required"
        elif body_weight < 50:
            size_category = "Small adult - moderate blood loss tolerance"
        elif body_weight > 100:
            size_category = "Large patient - higher blood loss tolerance"
        else:
            size_category = "Average-sized patient - standard monitoring"
        
        # Risk stratification
        if abl < 300:
            risk_level = "High risk - minimal blood loss tolerance"
        elif abl < 800:
            risk_level = "Moderate risk - limited blood loss tolerance"
        elif abl < 2000:
            risk_level = "Standard risk - typical blood loss tolerance"
        else:
            risk_level = "Low risk - good blood loss tolerance"
        
        return {
            "age_group_description": self.AGE_GROUP_DESCRIPTIONS[age_group],
            "percentage_of_blood_volume": round(percentage_ebv, 1),
            "accuracy_reliable": accuracy_reliable,
            "accuracy_note": "Calculation reliable" if accuracy_reliable else f"Calculation may be inaccurate >20% EBV loss",
            "transfusion_threshold_assessment": threshold_assessment,
            "patient_size_category": size_category,
            "risk_stratification": risk_level,
            "hemoglobin_reserve": round(initial_hemoglobin - final_hemoglobin, 1),
            "clinical_significance": "High" if percentage_ebv > 15 else "Moderate" if percentage_ebv > 10 else "Standard"
        }
    
    def _get_interpretation(self, abl: float) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on ABL value
        
        Args:
            abl (float): Maximum allowable blood loss in mL
            
        Returns:
            Dict with interpretation details
        """
        
        if abl <= 500:
            return {
                "stage": "Low Volume Loss",
                "description": "Small allowable blood loss",
                "interpretation": (
                    f"Maximum allowable blood loss of {abl:.1f} mL indicates limited tolerance "
                    f"for intraoperative bleeding. This may reflect small patient size, low initial "
                    f"hemoglobin, or conservative transfusion threshold. Requires meticulous hemostasis "
                    f"and frequent hemoglobin monitoring during surgery. Consider blood conservation "
                    f"strategies including autologous blood collection, antifibrinolytic agents, and "
                    f"cell salvage techniques. Prepare for early transfusion if blood loss approaches "
                    f"this threshold, and ensure adequate intravenous access for rapid blood product "
                    f"administration if needed."
                )
            }
        elif abl <= 1500:
            return {
                "stage": "Moderate Volume Loss",
                "description": "Moderate allowable blood loss",
                "interpretation": (
                    f"Maximum allowable blood loss of {abl:.1f} mL represents moderate tolerance "
                    f"for surgical bleeding, suitable for most routine procedures. Standard "
                    f"intraoperative monitoring protocols apply, including periodic hemoglobin "
                    f"checks and vital sign assessment. Consider blood conservation measures for "
                    f"procedures with anticipated moderate blood loss. Transfusion should be "
                    f"considered when blood loss approaches this calculated threshold, taking "
                    f"into account patient hemodynamic status, ongoing bleeding, and clinical "
                    f"condition. Ensure type and screen or crossmatch is current."
                )
            }
        elif abl <= 3000:
            return {
                "stage": "High Volume Loss",
                "description": "Large allowable blood loss",
                "interpretation": (
                    f"Maximum allowable blood loss of {abl:.1f} mL indicates good tolerance for "
                    f"significant surgical bleeding, appropriate for major surgical procedures. "
                    f"This favorable calculation suggests either large patient size, high initial "
                    f"hemoglobin, or conservative transfusion threshold. Suitable for procedures "
                    f"with anticipated substantial blood loss such as major orthopedic, cardiac, "
                    f"or hepatic surgery. Maintain close hemodynamic monitoring and serial "
                    f"hemoglobin assessment. Consider blood conservation techniques and prepare "
                    f"for potential massive transfusion protocols if blood loss exceeds expectations."
                )
            }
        else:  # Very high volume loss
            return {
                "stage": "Very High Volume Loss",
                "description": "Very large allowable blood loss",
                "interpretation": (
                    f"Maximum allowable blood loss of {abl:.1f} mL indicates excellent tolerance "
                    f"for major surgical bleeding, suitable for extensive procedures with high "
                    f"blood loss potential. This calculation reflects favorable baseline parameters "
                    f"including large patient size and/or high initial hemoglobin with conservative "
                    f"transfusion threshold. Appropriate for complex procedures such as major "
                    f"vascular surgery, extensive cancer resections, or multi-organ transplantation. "
                    f"Consider preoperative autologous blood donation, intraoperative cell salvage, "
                    f"and acute normovolemic hemodilution. Prepare massive transfusion protocols "
                    f"and ensure adequate blood bank resources for prolonged high-volume procedures."
                )
            }


def calculate_maximum_allowable_blood_loss_without_transfusion(
    age_group: str, body_weight: float, initial_hemoglobin: float, 
    final_hemoglobin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MaximumAllowableBloodLossWithoutTransfusionCalculator()
    return calculator.calculate(age_group, body_weight, initial_hemoglobin, final_hemoglobin)