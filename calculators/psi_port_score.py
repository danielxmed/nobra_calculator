"""
PSI/PORT Score: Pneumonia Severity Index for CAP Calculator

Estimates mortality for adult patients with community-acquired pneumonia (CAP) 
and guides hospitalization decisions. This extensively validated clinical 
prediction rule helps determine appropriate care settings based on mortality 
risk assessment.

References:
1. Fine MJ, Auble TE, Yealy DM, Hanusa BH, Weissfeld LA, Singer DE, et al. 
   A prediction rule to identify low-risk patients with community-acquired 
   pneumonia. N Engl J Med. 1997;336(4):243-50. doi: 10.1056/NEJM199701233360402.
2. Fine MJ, Hanusa BH, Lave JR, Singer DE, Stone RA, Weissfeld LA, et al. 
   Comparison of a disease-specific and a generic severity of illness measure 
   for patients with community-acquired pneumonia. J Gen Intern Med. 
   1995;10(7):359-68. doi: 10.1007/BF02599829.
3. Metlay JP, Waterer GW, Long AC, Anzueto A, Brozek J, Crothers K, et al. 
   Diagnosis and Treatment of Adults with Community-acquired Pneumonia. 
   Am J Respir Crit Care Med. 2019;200(7):e45-e67. doi: 10.1164/rccm.201908-1581ST.
"""

from typing import Dict, Any, Optional


class PsiPortScoreCalculator:
    """Calculator for PSI/PORT Score: Pneumonia Severity Index"""
    
    def __init__(self):
        # Risk class thresholds
        self.CLASS_I_II_THRESHOLD = 70
        self.CLASS_III_THRESHOLD = 90
        self.CLASS_IV_THRESHOLD = 130
        
    def calculate(self, age: int, sex: str, nursing_home_resident: str,
                 neoplastic_disease: str, liver_disease: str, congestive_heart_failure: str,
                 cerebrovascular_disease: str, renal_disease: str, altered_mental_status: str,
                 respiratory_rate: int, systolic_blood_pressure: int, temperature: float,
                 pulse: int, bun: float, sodium: float, glucose: float, hematocrit: float,
                 pleural_effusion: str, ph: Optional[float] = None, 
                 pao2: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates PSI/PORT score for pneumonia severity assessment
        
        Args:
            age (int): Patient age in years
            sex (str): Patient sex ('male' or 'female')
            nursing_home_resident (str): Nursing home resident status
            neoplastic_disease (str): History of neoplastic disease
            liver_disease (str): History of liver disease
            congestive_heart_failure (str): History of CHF
            cerebrovascular_disease (str): History of cerebrovascular disease
            renal_disease (str): History of renal disease
            altered_mental_status (str): Altered mental status present
            respiratory_rate (int): Respiratory rate (breaths/min)
            systolic_blood_pressure (int): Systolic BP (mmHg)
            temperature (float): Body temperature (°C)
            pulse (int): Heart rate (bpm)
            bun (float): Blood urea nitrogen (mg/dL)
            sodium (float): Serum sodium (mmol/L)
            glucose (float): Serum glucose (mg/dL)
            hematocrit (float): Hematocrit (%)
            pleural_effusion (str): Pleural effusion on chest X-ray
            ph (float, optional): Arterial blood gas pH
            pao2 (float, optional): Partial pressure of oxygen (mmHg)
            
        Returns:
            Dict with PSI score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age, sex, nursing_home_resident, neoplastic_disease, liver_disease,
            congestive_heart_failure, cerebrovascular_disease, renal_disease,
            altered_mental_status, respiratory_rate, systolic_blood_pressure,
            temperature, pulse, bun, sodium, glucose, hematocrit, pleural_effusion,
            ph, pao2
        )
        
        # Check for Class I (low risk young patients)
        if self._is_class_i(age, sex, nursing_home_resident, neoplastic_disease,
                           liver_disease, congestive_heart_failure, cerebrovascular_disease,
                           renal_disease, altered_mental_status, respiratory_rate,
                           systolic_blood_pressure, temperature, pulse, ph, bun,
                           sodium, glucose, hematocrit, pao2, pleural_effusion):
            return {
                "result": 0,
                "unit": "points",
                "interpretation": "Low risk for mortality. Outpatient treatment recommended. 30-day mortality rate <1%. Consider outpatient oral antibiotics and close follow-up.",
                "stage": "Class I (Low Risk)",
                "stage_description": "Low mortality risk"
            }
        
        # Calculate total score for Classes II-V
        total_score = self._calculate_total_score(
            age, sex, nursing_home_resident, neoplastic_disease, liver_disease,
            congestive_heart_failure, cerebrovascular_disease, renal_disease,
            altered_mental_status, respiratory_rate, systolic_blood_pressure,
            temperature, pulse, bun, sodium, glucose, hematocrit, pleural_effusion,
            ph, pao2
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, sex: str, nursing_home_resident: str,
                        neoplastic_disease: str, liver_disease: str, congestive_heart_failure: str,
                        cerebrovascular_disease: str, renal_disease: str, altered_mental_status: str,
                        respiratory_rate: int, systolic_blood_pressure: int, temperature: float,
                        pulse: int, bun: float, sodium: float, glucose: float, hematocrit: float,
                        pleural_effusion: str, ph: Optional[float], pao2: Optional[float]):
        """Validates input parameters"""
        
        # Validate demographics
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
            
        # Validate yes/no parameters
        yes_no_params = [
            (nursing_home_resident, "nursing_home_resident"),
            (neoplastic_disease, "neoplastic_disease"),
            (liver_disease, "liver_disease"),
            (congestive_heart_failure, "congestive_heart_failure"),
            (cerebrovascular_disease, "cerebrovascular_disease"),
            (renal_disease, "renal_disease"),
            (altered_mental_status, "altered_mental_status"),
            (pleural_effusion, "pleural_effusion")
        ]
        
        for param, name in yes_no_params:
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
        
        # Validate vital signs
        if not isinstance(respiratory_rate, int) or respiratory_rate < 5 or respiratory_rate > 60:
            raise ValueError("Respiratory rate must be between 5 and 60 breaths/min")
        if not isinstance(systolic_blood_pressure, int) or systolic_blood_pressure < 50 or systolic_blood_pressure > 250:
            raise ValueError("Systolic blood pressure must be between 50 and 250 mmHg")
        if not isinstance(temperature, (int, float)) or temperature < 30.0 or temperature > 45.0:
            raise ValueError("Temperature must be between 30.0 and 45.0°C")
        if not isinstance(pulse, int) or pulse < 30 or pulse > 200:
            raise ValueError("Pulse must be between 30 and 200 bpm")
            
        # Validate laboratory values
        if not isinstance(bun, (int, float)) or bun < 1.0 or bun > 200.0:
            raise ValueError("BUN must be between 1.0 and 200.0 mg/dL")
        if not isinstance(sodium, (int, float)) or sodium < 100.0 or sodium > 170.0:
            raise ValueError("Sodium must be between 100.0 and 170.0 mmol/L")
        if not isinstance(glucose, (int, float)) or glucose < 30.0 or glucose > 800.0:
            raise ValueError("Glucose must be between 30.0 and 800.0 mg/dL")
        if not isinstance(hematocrit, (int, float)) or hematocrit < 10.0 or hematocrit > 70.0:
            raise ValueError("Hematocrit must be between 10.0 and 70.0%")
            
        # Validate optional parameters
        if ph is not None and (not isinstance(ph, (int, float)) or ph < 6.5 or ph > 8.0):
            raise ValueError("pH must be between 6.5 and 8.0")
        if pao2 is not None and (not isinstance(pao2, (int, float)) or pao2 < 20.0 or pao2 > 200.0):
            raise ValueError("PaO2 must be between 20.0 and 200.0 mmHg")
    
    def _is_class_i(self, age: int, sex: str, nursing_home_resident: str,
                   neoplastic_disease: str, liver_disease: str, congestive_heart_failure: str,
                   cerebrovascular_disease: str, renal_disease: str, altered_mental_status: str,
                   respiratory_rate: int, systolic_blood_pressure: int, temperature: float,
                   pulse: int, ph: Optional[float], bun: float, sodium: float, glucose: float,
                   hematocrit: float, pao2: Optional[float], pleural_effusion: str) -> bool:
        """
        Determines if patient qualifies for Class I (lowest risk)
        Class I: Age <50 AND no comorbidities AND no high-risk clinical findings
        """
        
        # Must be under 50 years old
        if age >= 50:
            return False
            
        # Check for any comorbidities
        comorbidities = [
            nursing_home_resident == "yes",
            neoplastic_disease == "yes",
            liver_disease == "yes", 
            congestive_heart_failure == "yes",
            cerebrovascular_disease == "yes",
            renal_disease == "yes"
        ]
        
        if any(comorbidities):
            return False
            
        # Check for high-risk clinical findings
        high_risk_findings = [
            altered_mental_status == "yes",
            respiratory_rate >= 30,
            systolic_blood_pressure < 90,
            temperature < 35.0 or temperature >= 40.0,
            pulse >= 125,
            ph is not None and ph < 7.35,
            bun >= 30,
            sodium < 130,
            glucose >= 250,
            hematocrit < 30,
            pao2 is not None and pao2 < 60,
            pleural_effusion == "yes"
        ]
        
        if any(high_risk_findings):
            return False
            
        return True
    
    def _calculate_total_score(self, age: int, sex: str, nursing_home_resident: str,
                              neoplastic_disease: str, liver_disease: str, congestive_heart_failure: str,
                              cerebrovascular_disease: str, renal_disease: str, altered_mental_status: str,
                              respiratory_rate: int, systolic_blood_pressure: int, temperature: float,
                              pulse: int, bun: float, sodium: float, glucose: float, hematocrit: float,
                              pleural_effusion: str, ph: Optional[float], pao2: Optional[float]) -> int:
        """Calculates the total PSI score"""
        
        score = 0
        
        # Demographics
        score += age  # Age contributes its absolute value
        if sex == "female":
            score -= 10  # Female sex protective factor
            
        # Comorbidities
        if nursing_home_resident == "yes":
            score += 10
        if neoplastic_disease == "yes":
            score += 30
        if liver_disease == "yes":
            score += 20
        if congestive_heart_failure == "yes":
            score += 10
        if cerebrovascular_disease == "yes":
            score += 10
        if renal_disease == "yes":
            score += 10
            
        # Clinical findings
        if altered_mental_status == "yes":
            score += 20
        if respiratory_rate >= 30:
            score += 20
        if systolic_blood_pressure < 90:
            score += 20
        if temperature < 35.0 or temperature >= 40.0:
            score += 15
        if pulse >= 125:
            score += 10
            
        # Laboratory findings
        if ph is not None and ph < 7.35:
            score += 30
        if bun >= 30:
            score += 20
        if sodium < 130:
            score += 20
        if glucose >= 250:
            score += 10
        if hematocrit < 30:
            score += 10
        if pao2 is not None and pao2 < 60:
            score += 10
        if pleural_effusion == "yes":
            score += 10
            
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on PSI score
        
        Args:
            score (int): Calculated PSI score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= self.CLASS_I_II_THRESHOLD:  # ≤70
            return {
                "stage": "Class II (Low Risk)",
                "description": "Low mortality risk",
                "interpretation": "Low risk for mortality. Outpatient treatment recommended. 30-day mortality rate <3%. Consider outpatient oral antibiotics and close follow-up."
            }
        elif score <= self.CLASS_III_THRESHOLD:  # 71-90
            return {
                "stage": "Class III (Low Risk)",
                "description": "Low mortality risk",
                "interpretation": "Low risk for mortality. Outpatient treatment vs. observation admission. 30-day mortality rate <3%. Consider brief hospitalization or intensive outpatient monitoring."
            }
        elif score <= self.CLASS_IV_THRESHOLD:  # 91-130
            return {
                "stage": "Class IV (Moderate Risk)",
                "description": "Moderate mortality risk",
                "interpretation": "Moderate risk for mortality. Inpatient admission recommended. 30-day mortality rate 8-9%. Requires hospitalization with standard care and monitoring."
            }
        else:  # >130
            return {
                "stage": "Class V (High Risk)",
                "description": "High mortality risk",
                "interpretation": "High risk for mortality. Inpatient admission with consideration for ICU care. 30-day mortality rate 27-31%. Requires aggressive treatment and close monitoring."
            }


def calculate_psi_port_score(age: int, sex: str, nursing_home_resident: str,
                           neoplastic_disease: str, liver_disease: str, congestive_heart_failure: str,
                           cerebrovascular_disease: str, renal_disease: str, altered_mental_status: str,
                           respiratory_rate: int, systolic_blood_pressure: int, temperature: float,
                           pulse: int, bun: float, sodium: float, glucose: float, hematocrit: float,
                           pleural_effusion: str, ph: Optional[float] = None, 
                           pao2: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PsiPortScoreCalculator()
    return calculator.calculate(
        age, sex, nursing_home_resident, neoplastic_disease, liver_disease,
        congestive_heart_failure, cerebrovascular_disease, renal_disease,
        altered_mental_status, respiratory_rate, systolic_blood_pressure,
        temperature, pulse, bun, sodium, glucose, hematocrit, pleural_effusion,
        ph, pao2
    )