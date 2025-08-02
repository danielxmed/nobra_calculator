"""
Pulmonary Embolism Severity Index (PESI) Calculator

Predicts 30-day outcome of patients with pulmonary embolism using 11 clinical 
criteria. This validated prognostic tool stratifies mortality risk into five 
severity classes to guide treatment decisions and disposition planning.

References:
1. Aujesky D, Obrosky DS, Stone RA, Auble TE, Perrier A, Cornuz J, et al. 
   Derivation and validation of a prognostic model for pulmonary embolism. 
   Am J Respir Crit Care Med. 2005;172(8):1041-6. doi: 10.1164/rccm.200506-862OC.
2. Aujesky D, Roy PM, Verschuren F, Righini M, Osterwalder J, Egloff M, et al. 
   Outpatient versus inpatient treatment for patients with acute pulmonary 
   embolism: an international, open-label, randomised, non-inferiority trial. 
   Lancet. 2011;378(9785):41-8. doi: 10.1016/S0140-6736(11)60824-6.
3. Jiménez D, Aujesky D, Moores L, Gómez V, Lobo JL, Uresandi F, et al. 
   Simplification of the pulmonary embolism severity index for prognostication 
   in patients with acute symptomatic pulmonary embolism. Arch Intern Med. 
   2010;170(15):1383-9. doi: 10.1001/archinternmed.2010.199.
"""

from typing import Dict, Any


class PesiCalculator:
    """Calculator for Pulmonary Embolism Severity Index (PESI)"""
    
    def __init__(self):
        # Risk class thresholds
        self.CLASS_I_THRESHOLD = 65
        self.CLASS_II_THRESHOLD = 85
        self.CLASS_III_THRESHOLD = 105
        self.CLASS_IV_THRESHOLD = 125
    
    def calculate(self, age: int, sex: str, cancer_history: str, heart_failure_history: str,
                 chronic_lung_disease_history: str, heart_rate_110_or_higher: str,
                 systolic_bp_less_than_100: str, respiratory_rate_30_or_higher: str,
                 temperature_less_than_36: str, altered_mental_status: str,
                 oxygen_saturation_less_than_90: str) -> Dict[str, Any]:
        """
        Calculates PESI score for pulmonary embolism severity assessment
        
        Args:
            age (int): Patient age in years
            sex (str): Patient sex ('male' or 'female')
            cancer_history (str): History of cancer
            heart_failure_history (str): History of heart failure
            chronic_lung_disease_history (str): History of chronic lung disease
            heart_rate_110_or_higher (str): Heart rate ≥110 bpm
            systolic_bp_less_than_100 (str): Systolic BP <100 mmHg
            respiratory_rate_30_or_higher (str): Respiratory rate ≥30/min
            temperature_less_than_36 (str): Temperature <36°C
            altered_mental_status (str): Altered mental status present
            oxygen_saturation_less_than_90 (str): O2 saturation <90%
            
        Returns:
            Dict with PESI score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age, sex, cancer_history, heart_failure_history, chronic_lung_disease_history,
            heart_rate_110_or_higher, systolic_bp_less_than_100, respiratory_rate_30_or_higher,
            temperature_less_than_36, altered_mental_status, oxygen_saturation_less_than_90
        )
        
        # Calculate total PESI score
        total_score = self._calculate_total_score(
            age, sex, cancer_history, heart_failure_history, chronic_lung_disease_history,
            heart_rate_110_or_higher, systolic_bp_less_than_100, respiratory_rate_30_or_higher,
            temperature_less_than_36, altered_mental_status, oxygen_saturation_less_than_90
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
    
    def _validate_inputs(self, age: int, sex: str, cancer_history: str, heart_failure_history: str,
                        chronic_lung_disease_history: str, heart_rate_110_or_higher: str,
                        systolic_bp_less_than_100: str, respiratory_rate_30_or_higher: str,
                        temperature_less_than_36: str, altered_mental_status: str,
                        oxygen_saturation_less_than_90: str):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
            
        # Validate yes/no parameters
        yes_no_params = [
            (cancer_history, "cancer_history"),
            (heart_failure_history, "heart_failure_history"),
            (chronic_lung_disease_history, "chronic_lung_disease_history"),
            (heart_rate_110_or_higher, "heart_rate_110_or_higher"),
            (systolic_bp_less_than_100, "systolic_bp_less_than_100"),
            (respiratory_rate_30_or_higher, "respiratory_rate_30_or_higher"),
            (temperature_less_than_36, "temperature_less_than_36"),
            (altered_mental_status, "altered_mental_status"),
            (oxygen_saturation_less_than_90, "oxygen_saturation_less_than_90")
        ]
        
        for param, name in yes_no_params:
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, age: int, sex: str, cancer_history: str, heart_failure_history: str,
                              chronic_lung_disease_history: str, heart_rate_110_or_higher: str,
                              systolic_bp_less_than_100: str, respiratory_rate_30_or_higher: str,
                              temperature_less_than_36: str, altered_mental_status: str,
                              oxygen_saturation_less_than_90: str) -> int:
        """Calculates the total PESI score"""
        
        score = 0
        
        # Age contributes its absolute value
        score += age
        
        # Demographics
        if sex == "male":
            score += 10
            
        # Comorbidities
        if cancer_history == "yes":
            score += 30
        if heart_failure_history == "yes":
            score += 10
        if chronic_lung_disease_history == "yes":
            score += 10
            
        # Clinical findings
        if heart_rate_110_or_higher == "yes":
            score += 20
        if systolic_bp_less_than_100 == "yes":
            score += 30
        if respiratory_rate_30_or_higher == "yes":
            score += 20
        if temperature_less_than_36 == "yes":
            score += 20
        if altered_mental_status == "yes":
            score += 60
        if oxygen_saturation_less_than_90 == "yes":
            score += 20
            
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines clinical interpretation based on PESI score
        
        Args:
            score (int): Calculated PESI score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= self.CLASS_I_THRESHOLD:  # ≤65
            return {
                "stage": "Class I (Very Low Risk)",
                "description": "Very low 30-day mortality risk",
                "interpretation": "Very low risk for mortality (0.0-1.6%). Patient may be suitable for outpatient treatment with proper anticoagulation and close follow-up. Consider discharge with oral anticoagulation if no other contraindications exist. Ensure adequate social support and follow-up arrangements."
            }
        elif score <= self.CLASS_II_THRESHOLD:  # 66-85
            return {
                "stage": "Class II (Low Risk)",
                "description": "Low 30-day mortality risk",
                "interpretation": "Low risk for mortality (1.7-3.5%). Patient may be suitable for outpatient treatment or brief observation. Consider discharge with appropriate anticoagulation therapy and close outpatient follow-up within 24-72 hours. Evaluate social factors and patient preferences."
            }
        elif score <= self.CLASS_III_THRESHOLD:  # 86-105
            return {
                "stage": "Class III (Intermediate Risk)",
                "description": "Intermediate 30-day mortality risk",
                "interpretation": "Intermediate risk for mortality (3.2-7.1%). Consider inpatient management with standard monitoring and anticoagulation therapy. Requires careful evaluation for outpatient management eligibility. Monitor for clinical deterioration and response to treatment."
            }
        elif score <= self.CLASS_IV_THRESHOLD:  # 106-125
            return {
                "stage": "Class IV (High Risk)",
                "description": "High 30-day mortality risk",
                "interpretation": "High risk for mortality (4.0-11.4%). Requires inpatient management with close monitoring and aggressive anticoagulation. Consider advanced therapies if clinically appropriate. Monitor for complications including right heart failure and hemodynamic instability."
            }
        else:  # ≥126
            return {
                "stage": "Class V (Very High Risk)",
                "description": "Very high 30-day mortality risk",
                "interpretation": "Very high risk for mortality (10.0-24.5%). Requires immediate inpatient management with intensive monitoring. Consider ICU care, advanced therapies (thrombolysis, catheter-directed therapy, embolectomy), and aggressive supportive measures. Monitor for shock and respiratory failure."
            }


def calculate_pesi(age: int, sex: str, cancer_history: str, heart_failure_history: str,
                  chronic_lung_disease_history: str, heart_rate_110_or_higher: str,
                  systolic_bp_less_than_100: str, respiratory_rate_30_or_higher: str,
                  temperature_less_than_36: str, altered_mental_status: str,
                  oxygen_saturation_less_than_90: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = PesiCalculator()
    return calculator.calculate(
        age, sex, cancer_history, heart_failure_history, chronic_lung_disease_history,
        heart_rate_110_or_higher, systolic_bp_less_than_100, respiratory_rate_30_or_higher,
        temperature_less_than_36, altered_mental_status, oxygen_saturation_less_than_90
    )