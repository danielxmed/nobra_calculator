"""
ROSE (Risk Stratification of Syncope in the Emergency Department) Rule Calculator

Predicts 1-month serious outcome or death in patients presenting with syncope to the 
emergency department. The ROSE rule identifies high-risk patients who require admission 
and further workup versus those who can be safely discharged using 7 readily available 
clinical variables to stratify syncope patients.

References (Vancouver style):
1. Reed MJ, Newby DE, Coull AJ, Prescott RJ, Jacques KG, Gray AJ. The ROSE (risk 
   stratification of syncope in the emergency department) study. J Am Coll Cardiol. 
   2010 Feb 23;55(8):713-21. doi: 10.1016/j.jacc.2009.09.049.
2. Reed MJ, Mills NL, Weir CJ. Sensitive troponin assay predicts outcome in syncope. 
   Emerg Med J. 2012 Dec;29(12):1001-3. doi: 10.1136/emermed-2011-200456.
3. Colivicchi F, Ammirati F, Melina D, Guido V, Imperoli G, Santini M; OESIL 
   (Osservatorio Epidemiologico sulla Sincope nel Lazio) Study Investigators. 
   Development and prospective validation of a risk stratification system for patients 
   with syncope in the emergency department: the OESIL risk score. Eur Heart J. 
   2003 May;24(9):811-9. doi: 10.1016/s0195-668x(02)00713-0.
"""

from typing import Dict, Any


class RoseRuleCalculator:
    """Calculator for ROSE (Risk Stratification of Syncope in the Emergency Department) Rule"""
    
    def __init__(self):
        # ROSE rule constants
        self.TOTAL_CRITERIA = 7
        self.HIGH_RISK_THRESHOLD = 1  # ANY criterion present = high risk
    
    def calculate(
        self,
        bnp_level: str,
        bradycardia: str,
        fecal_occult_blood: str,
        anemia: str,
        chest_pain: str,
        q_wave_ecg: str,
        oxygen_saturation: str
    ) -> Dict[str, Any]:
        """
        Applies ROSE rule criteria for syncope risk stratification
        
        ROSE rule considers a patient HIGH RISK if ANY of the following are present:
        1. BNP level ≥300 pg/ml
        2. Bradycardia ≤50 bpm in ED or pre-hospital
        3. Rectal examination showing fecal occult blood
        4. Anemia (Hemoglobin ≤90 g/l)
        5. Chest pain associated with syncope
        6. ECG showing Q wave (not in lead III)
        7. Oxygen saturation ≤94% on room air
        
        Args:
            bnp_level (str): BNP ≥300 pg/ml ("yes"/"no")
            bradycardia (str): Heart rate ≤50 bpm ("yes"/"no")
            fecal_occult_blood (str): Positive fecal occult blood ("yes"/"no")
            anemia (str): Hemoglobin ≤90 g/l ("yes"/"no")
            chest_pain (str): Chest pain with syncope ("yes"/"no")
            q_wave_ecg (str): Q wave on ECG (not lead III) ("yes"/"no")
            oxygen_saturation (str): O2 sat ≤94% on room air ("yes"/"no")
            
        Returns:
            Dict with risk assessment and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            bnp_level,
            bradycardia,
            fecal_occult_blood,
            anemia,
            chest_pain,
            q_wave_ecg,
            oxygen_saturation
        )
        
        # Count positive criteria
        positive_criteria = self._count_positive_criteria(
            bnp_level,
            bradycardia,
            fecal_occult_blood,
            anemia,
            chest_pain,
            q_wave_ecg,
            oxygen_saturation
        )
        
        # Determine risk level
        is_high_risk = positive_criteria >= self.HIGH_RISK_THRESHOLD
        
        # Get interpretation
        interpretation = self._get_interpretation(is_high_risk, positive_criteria)
        
        return {
            "result": "High Risk" if is_high_risk else "Low Risk",
            "unit": "risk level",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(
        self,
        bnp_level: str,
        bradycardia: str,
        fecal_occult_blood: str,
        anemia: str,
        chest_pain: str,
        q_wave_ecg: str,
        oxygen_saturation: str
    ):
        """Validates all input parameters"""
        
        parameters = [
            ("bnp_level", bnp_level),
            ("bradycardia", bradycardia),
            ("fecal_occult_blood", fecal_occult_blood),
            ("anemia", anemia),
            ("chest_pain", chest_pain),
            ("q_wave_ecg", q_wave_ecg),
            ("oxygen_saturation", oxygen_saturation)
        ]
        
        for param_name, param_value in parameters:
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string ('yes' or 'no')")
            
            if param_value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no', got: {param_value}")
    
    def _count_positive_criteria(
        self,
        bnp_level: str,
        bradycardia: str,
        fecal_occult_blood: str,
        anemia: str,
        chest_pain: str,
        q_wave_ecg: str,
        oxygen_saturation: str
    ) -> int:
        """
        Counts positive ROSE criteria
        
        Returns:
            int: Number of positive criteria (0-7)
        """
        criteria_met = 0
        
        # Criterion 1: BNP ≥300 pg/ml
        if bnp_level.lower() == "yes":
            criteria_met += 1
        
        # Criterion 2: Bradycardia ≤50 bpm
        if bradycardia.lower() == "yes":
            criteria_met += 1
        
        # Criterion 3: Positive fecal occult blood
        if fecal_occult_blood.lower() == "yes":
            criteria_met += 1
        
        # Criterion 4: Anemia (Hgb ≤90 g/l)
        if anemia.lower() == "yes":
            criteria_met += 1
        
        # Criterion 5: Chest pain with syncope
        if chest_pain.lower() == "yes":
            criteria_met += 1
        
        # Criterion 6: Q wave on ECG (not lead III)
        if q_wave_ecg.lower() == "yes":
            criteria_met += 1
        
        # Criterion 7: Oxygen saturation ≤94%
        if oxygen_saturation.lower() == "yes":
            criteria_met += 1
        
        return criteria_met
    
    def _get_interpretation(self, is_high_risk: bool, positive_criteria: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on ROSE rule assessment
        
        Args:
            is_high_risk (bool): Whether patient meets high-risk criteria
            positive_criteria (int): Number of positive criteria present
            
        Returns:
            Dict with clinical interpretation
        """
        
        if is_high_risk:
            return {
                "stage": "High Risk",
                "description": "One or more ROSE criteria present",
                "interpretation": (
                    f"High risk for 1-month serious outcome or death ({positive_criteria} "
                    f"positive criteria). Strong consideration for hospital admission and further "
                    f"workup is recommended. Patients meeting ROSE criteria have significantly "
                    f"increased risk of cardiovascular events, arrhythmias, or death within 30 days. "
                    f"Appropriate evaluation may include cardiac monitoring, echocardiography, "
                    f"stress testing, electrophysiology consultation, and other investigations "
                    f"based on specific risk factors present. The most predictive single factor "
                    f"is elevated BNP (associated with 36% of serious cardiovascular outcomes "
                    f"and 89% of deaths)."
                )
            }
        else:
            return {
                "stage": "Low Risk",
                "description": "No ROSE criteria present",
                "interpretation": (
                    "Low risk for 1-month serious outcome or death. Patient may be considered "
                    "for discharge with appropriate follow-up. The ROSE rule has a negative "
                    "predictive value of 98.5% when no criteria are present. Consider outpatient "
                    "cardiology follow-up, primary care follow-up within 24-48 hours, and "
                    "patient education about return precautions. Ensure no other clinical "
                    "concerns that would warrant admission independent of syncope risk stratification."
                )
            }


def calculate_rose_rule(
    bnp_level: str,
    bradycardia: str,
    fecal_occult_blood: str,
    anemia: str,
    chest_pain: str,
    q_wave_ecg: str,
    oxygen_saturation: str
) -> Dict[str, Any]:
    """
    Convenience function for ROSE rule syncope risk stratification
    
    Applies the validated ROSE rule to determine 1-month risk of serious outcomes 
    or death in emergency department patients presenting with syncope.
    
    Args:
        bnp_level (str): BNP ≥300 pg/ml ("yes"/"no")
        bradycardia (str): Heart rate ≤50 bpm in ED or pre-hospital ("yes"/"no")
        fecal_occult_blood (str): Positive fecal occult blood test ("yes"/"no")
        anemia (str): Hemoglobin ≤90 g/l (≤9.0 g/dl) ("yes"/"no")
        chest_pain (str): Chest pain associated with syncope ("yes"/"no")
        q_wave_ecg (str): Q wave on ECG (not in lead III) ("yes"/"no")
        oxygen_saturation (str): O2 saturation ≤94% on room air ("yes"/"no")
        
    Returns:
        Dict[str, Any]: Risk assessment with clinical interpretation and disposition recommendations
    """
    calculator = RoseRuleCalculator()
    return calculator.calculate(
        bnp_level,
        bradycardia,
        fecal_occult_blood,
        anemia,
        chest_pain,
        q_wave_ecg,
        oxygen_saturation
    )