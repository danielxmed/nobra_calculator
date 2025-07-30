"""
CRUSADE Score for Post-MI Bleeding Risk Calculator

Risk stratifies patients with NSTEMI undergoing anticoagulation to determine 
their risk of major bleeding during hospitalization.

References:
- Subherwal S, Bach RG, Chen AY, et al. Circulation. 2009;119(14):1873-1882.
- Abu-Assi E, Raposeiras-Roubin S, Lear P, et al. Thromb Res. 2013;132(6):652-658.
"""

from typing import Dict, Any


class CrusadeBleedingRiskCalculator:
    """Calculator for CRUSADE Score for Post-MI Bleeding Risk"""
    
    def __init__(self):
        # Scoring tables for each variable
        self.HEMATOCRIT_SCORES = [
            (31.0, 9),    # <31%
            (34.0, 7),    # 31-33.9%
            (37.0, 3),    # 34-36.9%
            (40.0, 2),    # 37-39.9%
            (float('inf'), 0)  # ≥40%
        ]
        
        self.CREATININE_CLEARANCE_SCORES = [
            (15.0, 39),   # ≤15
            (30.0, 35),   # 15-30
            (60.0, 28),   # 30-60
            (90.0, 17),   # 60-90
            (120.0, 7),   # 90-120
            (float('inf'), 0)  # >120
        ]
        
        self.HEART_RATE_SCORES = [
            (70, 0),      # ≤70
            (80, 1),      # 71-80
            (90, 3),      # 81-90
            (100, 6),     # 91-100
            (110, 8),     # 101-110
            (120, 10),    # 111-120
            (float('inf'), 11)  # ≥121
        ]
        
        self.SYSTOLIC_BP_SCORES = [
            (90, 10),     # ≤90
            (100, 8),     # 91-100
            (120, 5),     # 101-120
            (180, 1),     # 121-180
            (200, 3),     # 181-200
            (float('inf'), 5)  # ≥201
        ]
        
        # Fixed scores for categorical variables
        self.SEX_SCORES = {
            "male": 0,
            "female": 8
        }
        
        self.CHF_SCORE = 7        # If signs of CHF present
        self.DIABETES_SCORE = 6   # If diabetes present
        self.VASCULAR_DISEASE_SCORE = 6  # If prior vascular disease present
    
    def calculate(self, baseline_hematocrit: float, creatinine_clearance: float,
                  heart_rate: int, patient_sex: str, signs_chf: str,
                  diabetes_mellitus: str, prior_vascular_disease: str,
                  systolic_blood_pressure: int) -> Dict[str, Any]:
        """
        Calculates the CRUSADE bleeding risk score
        
        Args:
            baseline_hematocrit (float): Baseline hematocrit percentage
            creatinine_clearance (float): Creatinine clearance in mL/min
            heart_rate (int): Heart rate in bpm
            patient_sex (str): Patient biological sex
            signs_chf (str): Signs of CHF at presentation
            diabetes_mellitus (str): History of diabetes
            prior_vascular_disease (str): History of vascular disease
            systolic_blood_pressure (int): Systolic BP in mmHg
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(baseline_hematocrit, creatinine_clearance, heart_rate,
                            patient_sex, signs_chf, diabetes_mellitus,
                            prior_vascular_disease, systolic_blood_pressure)
        
        # Calculate individual component scores
        component_scores = self._calculate_component_scores(
            baseline_hematocrit, creatinine_clearance, heart_rate, patient_sex,
            signs_chf, diabetes_mellitus, prior_vascular_disease, systolic_blood_pressure
        )
        
        # Calculate total score
        total_score = sum(component_scores.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "component_breakdown": self._format_component_breakdown(component_scores),
            "bleeding_risk_percentage": self._get_bleeding_risk_percentage(total_score),
            "clinical_recommendations": self._get_clinical_recommendations(total_score)
        }
    
    def _validate_inputs(self, baseline_hematocrit: float, creatinine_clearance: float,
                        heart_rate: int, patient_sex: str, signs_chf: str,
                        diabetes_mellitus: str, prior_vascular_disease: str,
                        systolic_blood_pressure: int):
        """Validates input parameters"""
        
        if not 15.0 <= baseline_hematocrit <= 55.0:
            raise ValueError("Baseline hematocrit must be between 15.0 and 55.0%")
        
        if not 5.0 <= creatinine_clearance <= 200.0:
            raise ValueError("Creatinine clearance must be between 5.0 and 200.0 mL/min")
        
        if not 30 <= heart_rate <= 200:
            raise ValueError("Heart rate must be between 30 and 200 bpm")
        
        if patient_sex not in ["male", "female"]:
            raise ValueError("Patient sex must be 'male' or 'female'")
        
        if signs_chf not in ["yes", "no"]:
            raise ValueError("Signs of CHF must be 'yes' or 'no'")
        
        if diabetes_mellitus not in ["yes", "no"]:
            raise ValueError("Diabetes mellitus must be 'yes' or 'no'")
        
        if prior_vascular_disease not in ["yes", "no"]:
            raise ValueError("Prior vascular disease must be 'yes' or 'no'")
        
        if not 60 <= systolic_blood_pressure <= 250:
            raise ValueError("Systolic blood pressure must be between 60 and 250 mmHg")
    
    def _calculate_component_scores(self, baseline_hematocrit: float, creatinine_clearance: float,
                                  heart_rate: int, patient_sex: str, signs_chf: str,
                                  diabetes_mellitus: str, prior_vascular_disease: str,
                                  systolic_blood_pressure: int) -> Dict[str, int]:
        """Calculate individual component scores"""
        
        scores = {}
        
        # Hematocrit score
        scores["hematocrit"] = self._get_range_score(baseline_hematocrit, self.HEMATOCRIT_SCORES)
        
        # Creatinine clearance score
        scores["creatinine_clearance"] = self._get_range_score(creatinine_clearance, self.CREATININE_CLEARANCE_SCORES)
        
        # Heart rate score
        scores["heart_rate"] = self._get_range_score(heart_rate, self.HEART_RATE_SCORES)
        
        # Sex score
        scores["sex"] = self.SEX_SCORES[patient_sex]
        
        # CHF signs
        scores["chf"] = self.CHF_SCORE if signs_chf == "yes" else 0
        
        # Diabetes
        scores["diabetes"] = self.DIABETES_SCORE if diabetes_mellitus == "yes" else 0
        
        # Vascular disease
        scores["vascular_disease"] = self.VASCULAR_DISEASE_SCORE if prior_vascular_disease == "yes" else 0
        
        # Systolic blood pressure
        scores["systolic_bp"] = self._get_range_score(systolic_blood_pressure, self.SYSTOLIC_BP_SCORES)
        
        return scores
    
    def _get_range_score(self, value: float, score_ranges: list) -> int:
        """Get score based on value ranges"""
        for threshold, score in score_ranges:
            if value <= threshold:
                return score
        return 0
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the bleeding risk interpretation based on the total score
        
        Args:
            total_score (int): Total CRUSADE score
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score <= 20:
            return {
                "stage": "Very Low Risk",
                "description": "Very low bleeding risk",
                "interpretation": (f"CRUSADE score of {total_score} indicates very low bleeding risk "
                                 "(3.1% major bleeding rate). Standard antithrombotic therapy is "
                                 "appropriate. Monitor for bleeding but expect low incidence.")
            }
        elif total_score <= 30:
            return {
                "stage": "Low Risk",
                "description": "Low bleeding risk",
                "interpretation": (f"CRUSADE score of {total_score} indicates low bleeding risk "
                                 "(5.5% major bleeding rate). Standard antithrombotic therapy is "
                                 "appropriate with routine monitoring for bleeding complications.")
            }
        elif total_score <= 40:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate bleeding risk",
                "interpretation": (f"CRUSADE score of {total_score} indicates moderate bleeding risk "
                                 "(8.6% major bleeding rate). Consider reduced-dose antithrombotic "
                                 "therapy and enhanced bleeding monitoring. Balance ischemic vs bleeding risk.")
            }
        elif total_score <= 50:
            return {
                "stage": "High Risk",
                "description": "High bleeding risk",
                "interpretation": (f"CRUSADE score of {total_score} indicates high bleeding risk "
                                 "(11.9% major bleeding rate). Consider reduced-dose antithrombotic "
                                 "regimens, shorter duration therapy, and intensive bleeding monitoring.")
            }
        else:  # > 50
            return {
                "stage": "Very High Risk",
                "description": "Very high bleeding risk",
                "interpretation": (f"CRUSADE score of {total_score} indicates very high bleeding risk "
                                 "(19.5% major bleeding rate). Strongly consider alternative treatment "
                                 "strategies, minimal effective antithrombotic therapy, and very close monitoring.")
            }
    
    def _format_component_breakdown(self, component_scores: Dict[str, int]) -> Dict[str, Dict[str, Any]]:
        """Format component breakdown for response"""
        
        return {
            "hematocrit": {
                "score": component_scores["hematocrit"],
                "description": "Baseline hematocrit level",
                "rationale": "Lower hematocrit indicates bleeding risk and anemia"
            },
            "creatinine_clearance": {
                "score": component_scores["creatinine_clearance"],
                "description": "Kidney function assessment",
                "rationale": "Reduced kidney function affects drug clearance and bleeding risk"
            },
            "heart_rate": {
                "score": component_scores["heart_rate"],
                "description": "Heart rate on admission",
                "rationale": "Elevated heart rate may indicate hemodynamic instability"
            },
            "sex": {
                "score": component_scores["sex"],
                "description": "Patient biological sex",
                "rationale": "Female sex independently associated with increased bleeding risk"
            },
            "chf": {
                "score": component_scores["chf"],
                "description": "Signs of congestive heart failure",
                "rationale": "CHF indicates higher severity and comorbidity burden"
            },
            "diabetes": {
                "score": component_scores["diabetes"],
                "description": "History of diabetes mellitus",
                "rationale": "Diabetes associated with vascular complications and bleeding risk"
            },
            "vascular_disease": {
                "score": component_scores["vascular_disease"],
                "description": "Prior vascular disease history",
                "rationale": "Previous vascular disease indicates systemic atherosclerosis"
            },
            "systolic_bp": {
                "score": component_scores["systolic_bp"],
                "description": "Systolic blood pressure",
                "rationale": "Both low and very high BP associated with bleeding complications"
            }
        }
    
    def _get_bleeding_risk_percentage(self, total_score: int) -> Dict[str, Any]:
        """Get estimated bleeding risk percentage"""
        
        if total_score <= 20:
            risk_percentage = 3.1
        elif total_score <= 30:
            risk_percentage = 5.5
        elif total_score <= 40:
            risk_percentage = 8.6
        elif total_score <= 50:
            risk_percentage = 11.9
        else:
            risk_percentage = 19.5
        
        return {
            "estimated_bleeding_risk": f"{risk_percentage}%",
            "definition": "Major bleeding defined as hematocrit drop ≥12%, RBC transfusion (if baseline Hct ≥28%), or RBC transfusion with witnessed bleeding (if baseline Hct <28%)",
            "timeframe": "During hospitalization for acute coronary syndrome"
        }
    
    def _get_clinical_recommendations(self, total_score: int) -> Dict[str, Any]:
        """Get clinical recommendations based on score"""
        
        if total_score <= 20:
            return {
                "antithrombotic_therapy": "Standard dose dual antiplatelet therapy",
                "monitoring": "Routine bleeding monitoring",
                "duration": "Standard duration per guidelines",
                "special_considerations": [
                    "Standard care protocols apply",
                    "Monitor for bleeding per routine protocols",
                    "Consider patient-specific factors"
                ]
            }
        elif total_score <= 30:
            return {
                "antithrombotic_therapy": "Standard dose with routine monitoring",
                "monitoring": "Routine bleeding assessment",
                "duration": "Standard duration per guidelines",
                "special_considerations": [
                    "Routine bleeding monitoring protocols",
                    "Consider patient education on bleeding signs",
                    "Standard follow-up schedule"
                ]
            }
        elif total_score <= 40:
            return {
                "antithrombotic_therapy": "Consider dose modification or alternative agents",
                "monitoring": "Enhanced bleeding monitoring",
                "duration": "Consider shorter duration if clinically appropriate",
                "special_considerations": [
                    "Balance ischemic vs bleeding risk carefully",
                    "Enhanced patient education on bleeding signs",
                    "More frequent monitoring",
                    "Consider proton pump inhibitor"
                ]
            }
        elif total_score <= 50:
            return {
                "antithrombotic_therapy": "Reduced dose regimens preferred",
                "monitoring": "Intensive bleeding monitoring",
                "duration": "Shorter duration therapy when possible",
                "special_considerations": [
                    "Consider alternative antithrombotic strategies",
                    "Intensive monitoring protocols",
                    "Proton pump inhibitor recommended",
                    "Frequent clinical assessments",
                    "Early intervention for bleeding"
                ]
            }
        else:
            return {
                "antithrombotic_therapy": "Minimal effective therapy",
                "monitoring": "Very close bleeding monitoring",
                "duration": "Shortest effective duration",
                "special_considerations": [
                    "Alternative treatment strategies strongly recommended",
                    "Consider mechanical interventions over pharmacologic",
                    "Very close monitoring required",
                    "Immediate access to bleeding management",
                    "Multidisciplinary team approach",
                    "Consider bleeding risk vs benefit daily"
                ]
            }


def calculate_crusade_bleeding_risk(baseline_hematocrit: float, creatinine_clearance: float,
                                  heart_rate: int, patient_sex: str, signs_chf: str,
                                  diabetes_mellitus: str, prior_vascular_disease: str,
                                  systolic_blood_pressure: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CrusadeBleedingRiskCalculator()
    return calculator.calculate(baseline_hematocrit, creatinine_clearance, heart_rate,
                              patient_sex, signs_chf, diabetes_mellitus,
                              prior_vascular_disease, systolic_blood_pressure)