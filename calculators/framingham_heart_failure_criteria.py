"""
Framingham Heart Failure Diagnostic Criteria Calculator

Diagnoses heart failure based on major and minor criteria. Requires at least 2 major 
criteria or 1 major criterion plus 2 minor criteria.

References:
1. McKee PA, Castelli WP, McNamara PM, Kannel WB. The natural history of congestive 
   heart failure: the Framingham study. N Engl J Med. 1971;285(26):1441-6.
2. Carlson KJ, Lee DC, Goroll AH, Leahy M, Johnson RA. An analysis of physicians' 
   reasons for prescribing long-term digitalis therapy in outpatients. J Chronic Dis. 1985;38(9):733-9.
3. Marantz PR, Tobin JN, Wassertheil-Smoller S, et al. The relationship between left 
   ventricular systolic function and congestive heart failure diagnosed by clinical criteria. 
   Circulation. 1988;77(3):607-12.
4. Remes J, Miettinen H, Reunanen A, Pyörälä K. Validity of clinical diagnosis of heart 
   failure in primary health care. Eur Heart J. 1991;12(3):315-21.
"""

from typing import Dict, Any


class FraminghamHeartFailureCriteriaCalculator:
    """Calculator for Framingham Heart Failure Diagnostic Criteria"""
    
    def __init__(self):
        # Define major and minor criteria
        self.MAJOR_CRITERIA = [
            "acute_pulmonary_edema",
            "cardiomegaly",
            "hepatojugular_reflex",
            "neck_vein_distention",
            "paroxysmal_nocturnal_dyspnea_orthopnea",
            "pulmonary_rales",
            "third_heart_sound"
        ]
        
        self.MINOR_CRITERIA = [
            "ankle_edema",
            "dyspnea_on_exertion",
            "hepatomegaly",
            "nocturnal_cough",
            "pleural_effusion",
            "tachycardia"
        ]
    
    def calculate(self, acute_pulmonary_edema: str, cardiomegaly: str, hepatojugular_reflex: str,
                  neck_vein_distention: str, paroxysmal_nocturnal_dyspnea_orthopnea: str,
                  pulmonary_rales: str, third_heart_sound: str, ankle_edema: str,
                  dyspnea_on_exertion: str, hepatomegaly: str, nocturnal_cough: str,
                  pleural_effusion: str, tachycardia: str) -> Dict[str, Any]:
        """
        Evaluates heart failure diagnosis using Framingham criteria
        
        Args:
            Major criteria (all str "yes" or "no"):
                acute_pulmonary_edema: Acute pulmonary edema
                cardiomegaly: Cardiomegaly on chest X-ray
                hepatojugular_reflex: Hepatojugular reflex
                neck_vein_distention: Neck vein distention (JVD)
                paroxysmal_nocturnal_dyspnea_orthopnea: PND or orthopnea
                pulmonary_rales: Pulmonary rales on examination
                third_heart_sound: Third heart sound (S3 gallop)
                
            Minor criteria (all str "yes" or "no"):
                ankle_edema: Ankle edema
                dyspnea_on_exertion: Dyspnea on exertion
                hepatomegaly: Hepatomegaly
                nocturnal_cough: Nocturnal cough
                pleural_effusion: Pleural effusion
                tachycardia: Tachycardia (HR >120 bpm)
            
        Returns:
            Dict with diagnosis result and clinical interpretation
        """
        
        # Create parameter dictionary for validation
        parameters = {
            "acute_pulmonary_edema": acute_pulmonary_edema,
            "cardiomegaly": cardiomegaly,
            "hepatojugular_reflex": hepatojugular_reflex,
            "neck_vein_distention": neck_vein_distention,
            "paroxysmal_nocturnal_dyspnea_orthopnea": paroxysmal_nocturnal_dyspnea_orthopnea,
            "pulmonary_rales": pulmonary_rales,
            "third_heart_sound": third_heart_sound,
            "ankle_edema": ankle_edema,
            "dyspnea_on_exertion": dyspnea_on_exertion,
            "hepatomegaly": hepatomegaly,
            "nocturnal_cough": nocturnal_cough,
            "pleural_effusion": pleural_effusion,
            "tachycardia": tachycardia
        }
        
        # Validations
        self._validate_inputs(parameters)
        
        # Count major and minor criteria
        major_count = self._count_criteria(parameters, self.MAJOR_CRITERIA)
        minor_count = self._count_criteria(parameters, self.MINOR_CRITERIA)
        
        # Determine diagnosis
        diagnosis_result = self._evaluate_diagnosis(major_count, minor_count)
        
        # Get interpretation
        interpretation = self._get_interpretation(diagnosis_result, major_count, minor_count)
        
        return {
            "result": 1 if diagnosis_result else 0,
            "unit": "diagnosis",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        for param_name, value in parameters.items():
            if not isinstance(value, str):
                raise ValueError(f"{param_name} must be a string")
            if value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _count_criteria(self, parameters: Dict[str, str], criteria_list: list) -> int:
        """Counts the number of positive criteria"""
        
        count = 0
        for criterion in criteria_list:
            if parameters[criterion].lower() == "yes":
                count += 1
        return count
    
    def _evaluate_diagnosis(self, major_count: int, minor_count: int) -> bool:
        """
        Determines heart failure diagnosis based on criteria counts
        
        Diagnosis requires:
        - At least 2 major criteria OR
        - 1 major criterion plus at least 2 minor criteria
        
        Args:
            major_count (int): Number of positive major criteria
            minor_count (int): Number of positive minor criteria
            
        Returns:
            bool: True if diagnosis criteria met, False otherwise
        """
        
        # At least 2 major criteria
        if major_count >= 2:
            return True
        
        # 1 major criterion plus at least 2 minor criteria
        if major_count >= 1 and minor_count >= 2:
            return True
        
        # Criteria not met
        return False
    
    def _get_interpretation(self, diagnosis_result: bool, major_count: int, minor_count: int) -> Dict[str, str]:
        """
        Provides clinical interpretation of the diagnosis
        
        Args:
            diagnosis_result (bool): Whether diagnosis criteria are met
            major_count (int): Number of positive major criteria
            minor_count (int): Number of positive minor criteria
            
        Returns:
            Dict with interpretation details
        """
        
        if diagnosis_result:
            # Determine which criteria combination led to diagnosis
            if major_count >= 2:
                criteria_met = f"{major_count} major criteria"
                if minor_count > 0:
                    criteria_met += f" and {minor_count} minor criteria"
            else:
                criteria_met = f"{major_count} major criterion and {minor_count} minor criteria"
            
            return {
                "stage": "Heart Failure Diagnosed",
                "description": "Criteria met for heart failure diagnosis",
                "interpretation": (f"Framingham criteria met for heart failure diagnosis ({criteria_met} present). "
                                f"The diagnostic criteria are 97% sensitive and 79% specific for congestive heart failure. "
                                f"Initiate appropriate heart failure evaluation including echocardiography, BNP/NT-proBNP, "
                                f"and management according to current heart failure guidelines. Consider evaluation for "
                                f"underlying etiology and assessment of left ventricular function.")
            }
        else:
            return {
                "stage": "Heart Failure Not Diagnosed",
                "description": "Criteria not met for heart failure diagnosis",
                "interpretation": (f"Framingham criteria not met for heart failure diagnosis ({major_count} major "
                                f"criteria and {minor_count} minor criteria present). Fewer than 2 major criteria "
                                f"or fewer than 1 major plus 2 minor criteria. The high sensitivity (97%) of these "
                                f"criteria makes heart failure unlikely when not met (negative likelihood ratio 0.04). "
                                f"Consider alternative diagnoses for the patient's symptoms. If clinical suspicion "
                                f"remains high, consider additional evaluation with echocardiography or BNP/NT-proBNP.")
            }


def calculate_framingham_heart_failure_criteria(
    acute_pulmonary_edema: str, cardiomegaly: str, hepatojugular_reflex: str,
    neck_vein_distention: str, paroxysmal_nocturnal_dyspnea_orthopnea: str,
    pulmonary_rales: str, third_heart_sound: str, ankle_edema: str,
    dyspnea_on_exertion: str, hepatomegaly: str, nocturnal_cough: str,
    pleural_effusion: str, tachycardia: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_framingham_heart_failure_criteria pattern
    """
    calculator = FraminghamHeartFailureCriteriaCalculator()
    return calculator.calculate(
        acute_pulmonary_edema, cardiomegaly, hepatojugular_reflex,
        neck_vein_distention, paroxysmal_nocturnal_dyspnea_orthopnea,
        pulmonary_rales, third_heart_sound, ankle_edema,
        dyspnea_on_exertion, hepatomegaly, nocturnal_cough,
        pleural_effusion, tachycardia
    )