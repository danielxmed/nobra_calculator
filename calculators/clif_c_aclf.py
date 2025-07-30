"""
CLIF-C ACLF (Acute-on-Chronic Liver Failure) Calculator

Predicts mortality in patients with acute-on-chronic liver failure (ACLF).
The CLIF-C ACLF score is superior to MELD, MELD-Na, and Child-Pugh scores 
for mortality prediction in ACLF patients.

References:
1. Jalan R, Saliba F, Pavesi M, Amoros A, Moreau R, Ginès P, Levesque E, Durand F, 
   Angeli P, Caraceni P, Hopf C, Alessandria C, Rodriguez E, Solis-Muñoz P, Laleman W, 
   Trebicka J, Zeuzem S, Gustot T, Mookerjee R, Elkrief L, Soriano G, Cordoba J, 
   Morando F, Gerbes A, Agarwal B, Samuel D, Bernardi M, Arroyo V; CANONIC study 
   investigators of the EASL-Clif Consortium. Development and validation of a 
   prognostic score to predict mortality in patients with acute-on-chronic liver 
   failure. J Hepatol. 2014;61(5):1038-47.
2. Moreau R, Jalan R, Gines P, Pavesi M, Angeli P, Cordoba J, Durand F, Gustot T, 
   Saliba F, Domenicali M, Gerbes A, Wendon J, Alessandria C, Laleman W, Zeuzem S, 
   Trebicka J, Bernardi M, Arroyo V; CANONIC Study Investigators of the EASL-Clif 
   Consortium. Acute-on-chronic liver failure is a distinct syndrome that develops 
   in patients with acute decompensation of cirrhosis. Gastroenterology. 2013;144(7):1426-37.
"""

import math
from typing import Dict, Any


class ClifCAclfCalculator:
    """Calculator for CLIF-C ACLF Score"""
    
    def __init__(self):
        # Organ failure scoring criteria
        self.organ_failure_scoring = {
            "liver": {  # Bilirubin (mg/dL)
                "thresholds": [6, 12],
                "points": [1, 2, 3]
            },
            "kidney": {  # Creatinine (mg/dL) or RRT
                "thresholds": [2, 3.5],
                "points": [1, 2, 3]
            },
            "brain": {  # Hepatic encephalopathy grade
                "grade_0": 1,
                "grade_1_2": 2,
                "grade_3_4": 3
            },
            "coagulation": {  # INR
                "thresholds": [2.0, 2.5],
                "points": [1, 2, 3]
            },
            "circulatory": {  # MAP (mmHg) and vasopressors
                "map_threshold": 70,
                "points": [1, 2, 3]  # ≥70, <70, any MAP with vasopressors
            },
            "respiratory": {  # PaO2/FiO2 or SpO2/FiO2 ratios
                "pao2_fio2_thresholds": [200, 300],
                "spo2_fio2_thresholds": [214, 357],
                "points": [3, 2, 1]  # ≤200/214, 200-300/214-357, >300/357
            }
        }
        
        # CLIF-C ACLF formula coefficients
        self.coefficients = {
            "clif_of_coefficient": 0.33,
            "age_coefficient": 0.04,
            "wbc_coefficient": 0.63,
            "constant": -2,
            "multiplier": 10
        }
    
    def calculate(
        self,
        age: int,
        white_blood_cell_count: float,
        bilirubin: float,
        creatinine: float,
        renal_replacement_therapy: str,
        hepatic_encephalopathy_grade: str,
        inr: float,
        mean_arterial_pressure: float,
        vasopressors: str,
        respiratory_ratio_type: str,
        respiratory_ratio_value: float
    ) -> Dict[str, Any]:
        """
        Calculates CLIF-C ACLF score for acute-on-chronic liver failure prognosis
        
        Args:
            age: Patient age in years
            white_blood_cell_count: WBC count (×10⁹ cells/L)
            bilirubin: Total bilirubin (mg/dL)
            creatinine: Serum creatinine (mg/dL)
            renal_replacement_therapy: RRT status (yes/no)
            hepatic_encephalopathy_grade: HE grade (grade_0/grade_1_2/grade_3_4)
            inr: International normalized ratio
            mean_arterial_pressure: MAP (mmHg)
            vasopressors: Vasopressor use (yes/no)
            respiratory_ratio_type: Ratio type (pao2_fio2/spo2_fio2)
            respiratory_ratio_value: Respiratory ratio value
            
        Returns:
            Dict with CLIF-C ACLF score, mortality risk assessment, and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            age, white_blood_cell_count, bilirubin, creatinine,
            renal_replacement_therapy, hepatic_encephalopathy_grade,
            inr, mean_arterial_pressure, vasopressors,
            respiratory_ratio_type, respiratory_ratio_value
        )
        
        # Calculate CLIF-C OF (Organ Failure) score
        clif_of_score = self._calculate_clif_of_score(
            bilirubin, creatinine, renal_replacement_therapy,
            hepatic_encephalopathy_grade, inr, mean_arterial_pressure,
            vasopressors, respiratory_ratio_type, respiratory_ratio_value
        )
        
        # Calculate CLIF-C ACLF score
        aclf_score = self._calculate_aclf_score(clif_of_score, age, white_blood_cell_count)
        
        # Get mortality risk assessment
        risk_assessment = self._get_risk_assessment(aclf_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            age, white_blood_cell_count, bilirubin, creatinine,
            renal_replacement_therapy, hepatic_encephalopathy_grade,
            inr, mean_arterial_pressure, vasopressors,
            respiratory_ratio_type, respiratory_ratio_value,
            clif_of_score, aclf_score
        )
        
        return {
            "result": aclf_score,
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"],
            "scoring_breakdown": scoring_breakdown
        }
    
    def _validate_inputs(self, age, white_blood_cell_count, bilirubin, creatinine,
                        renal_replacement_therapy, hepatic_encephalopathy_grade,
                        inr, mean_arterial_pressure, vasopressors,
                        respiratory_ratio_type, respiratory_ratio_value):
        """Validates input parameters"""
        
        # Validate numeric ranges
        if not (18 <= age <= 100):
            raise ValueError("Age must be between 18 and 100 years")
        
        if not (0.1 <= white_blood_cell_count <= 100):
            raise ValueError("White blood cell count must be between 0.1 and 100 ×10⁹ cells/L")
        
        if not (0.1 <= bilirubin <= 50):
            raise ValueError("Bilirubin must be between 0.1 and 50 mg/dL")
        
        if not (0.1 <= creatinine <= 20):
            raise ValueError("Creatinine must be between 0.1 and 20 mg/dL")
        
        if not (0.5 <= inr <= 10):
            raise ValueError("INR must be between 0.5 and 10")
        
        if not (30 <= mean_arterial_pressure <= 150):
            raise ValueError("Mean arterial pressure must be between 30 and 150 mmHg")
        
        if not (50 <= respiratory_ratio_value <= 600):
            raise ValueError("Respiratory ratio value must be between 50 and 600")
        
        # Validate categorical parameters
        if renal_replacement_therapy not in ["yes", "no"]:
            raise ValueError("Renal replacement therapy must be 'yes' or 'no'")
        
        if hepatic_encephalopathy_grade not in ["grade_0", "grade_1_2", "grade_3_4"]:
            raise ValueError("Hepatic encephalopathy grade must be 'grade_0', 'grade_1_2', or 'grade_3_4'")
        
        if vasopressors not in ["yes", "no"]:
            raise ValueError("Vasopressors must be 'yes' or 'no'")
        
        if respiratory_ratio_type not in ["pao2_fio2", "spo2_fio2"]:
            raise ValueError("Respiratory ratio type must be 'pao2_fio2' or 'spo2_fio2'")
    
    def _calculate_clif_of_score(self, bilirubin, creatinine, renal_replacement_therapy,
                               hepatic_encephalopathy_grade, inr, mean_arterial_pressure,
                               vasopressors, respiratory_ratio_type, respiratory_ratio_value):
        """Calculates CLIF-C Organ Failure (OF) score"""
        
        total_score = 0
        
        # Liver (Bilirubin)
        if bilirubin < 6:
            total_score += 1
        elif bilirubin < 12:
            total_score += 2
        else:
            total_score += 3
        
        # Kidney (Creatinine or RRT)
        if renal_replacement_therapy == "yes":
            total_score += 3
        elif creatinine < 2:
            total_score += 1
        elif creatinine < 3.5:
            total_score += 2
        else:
            total_score += 3
        
        # Brain (Hepatic Encephalopathy)
        total_score += self.organ_failure_scoring["brain"][hepatic_encephalopathy_grade]
        
        # Coagulation (INR)
        if inr < 2.0:
            total_score += 1
        elif inr < 2.5:
            total_score += 2
        else:
            total_score += 3
        
        # Circulatory (MAP and vasopressors)
        if vasopressors == "yes":
            total_score += 3
        elif mean_arterial_pressure < 70:
            total_score += 2
        else:
            total_score += 1
        
        # Respiratory (PaO2/FiO2 or SpO2/FiO2)
        if respiratory_ratio_type == "pao2_fio2":
            if respiratory_ratio_value <= 200:
                total_score += 3
            elif respiratory_ratio_value <= 300:
                total_score += 2
            else:
                total_score += 1
        else:  # spo2_fio2
            if respiratory_ratio_value <= 214:
                total_score += 3
            elif respiratory_ratio_value <= 357:
                total_score += 2
            else:
                total_score += 1
        
        return total_score
    
    def _calculate_aclf_score(self, clif_of_score: int, age: int, wbc_count: float) -> float:
        """Calculates final CLIF-C ACLF score"""
        
        # CLIF-C ACLF = 10 × [0.33 × CLIF-C OF + 0.04 × age + 0.63 × ln(WBC) - 2]
        score = self.coefficients["multiplier"] * (
            self.coefficients["clif_of_coefficient"] * clif_of_score +
            self.coefficients["age_coefficient"] * age +
            self.coefficients["wbc_coefficient"] * math.log(wbc_count) +
            self.coefficients["constant"]
        )
        
        # Ensure score is within 0-100 range
        return max(0, min(100, score))
    
    def _get_risk_assessment(self, aclf_score: float) -> Dict[str, str]:
        """
        Determines mortality risk category and clinical recommendations
        
        Args:
            aclf_score: CLIF-C ACLF score
            
        Returns:
            Dict with risk assessment and clinical recommendations
        """
        
        if aclf_score < 45:
            stage = "Low Risk"
            description = "Lower mortality risk"
            interpretation = f"CLIF-C ACLF Score {aclf_score:.1f}: Lower mortality risk in ACLF. Standard supportive care with close monitoring. Consider hepatology consultation and optimization of liver function."
            
        elif aclf_score < 65:
            stage = "Moderate Risk"
            description = "Moderate mortality risk"
            interpretation = f"CLIF-C ACLF Score {aclf_score:.1f}: Moderate mortality risk in ACLF. Consider intensive care monitoring and advanced therapies. Evaluate for liver transplantation eligibility."
            
        elif aclf_score < 70:
            stage = "High Risk"
            description = "High mortality risk"
            interpretation = f"CLIF-C ACLF Score {aclf_score:.1f}: High mortality risk in ACLF. Urgent consideration for liver transplantation if eligible. Intensive care management required."
            
        else:  # aclf_score >= 70
            stage = "Critical Risk"
            description = "Critical mortality risk"
            interpretation = f"CLIF-C ACLF Score {aclf_score:.1f}: Critical mortality risk associated with 100% mortality at 28 days. Consider futility of intensive care measures. Focus on comfort care and family discussions."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, age, white_blood_cell_count, bilirubin, creatinine,
                             renal_replacement_therapy, hepatic_encephalopathy_grade,
                             inr, mean_arterial_pressure, vasopressors,
                             respiratory_ratio_type, respiratory_ratio_value,
                             clif_of_score, aclf_score) -> Dict[str, Any]:
        """Provides detailed scoring breakdown and clinical context"""
        
        # Calculate individual organ scores
        liver_score = 3 if bilirubin >= 12 else (2 if bilirubin >= 6 else 1)
        
        if renal_replacement_therapy == "yes":
            kidney_score = 3
        else:
            kidney_score = 3 if creatinine >= 3.5 else (2 if creatinine >= 2 else 1)
        
        brain_score = self.organ_failure_scoring["brain"][hepatic_encephalopathy_grade]
        
        coagulation_score = 3 if inr >= 2.5 else (2 if inr >= 2.0 else 1)
        
        if vasopressors == "yes":
            circulatory_score = 3
        else:
            circulatory_score = 2 if mean_arterial_pressure < 70 else 1
        
        if respiratory_ratio_type == "pao2_fio2":
            respiratory_score = 3 if respiratory_ratio_value <= 200 else (2 if respiratory_ratio_value <= 300 else 1)
        else:
            respiratory_score = 3 if respiratory_ratio_value <= 214 else (2 if respiratory_ratio_value <= 357 else 1)
        
        # HE grade descriptions
        he_descriptions = {
            "grade_0": "No hepatic encephalopathy",
            "grade_1_2": "Mild to moderate hepatic encephalopathy (Grades 1-2)",
            "grade_3_4": "Severe hepatic encephalopathy (Grades 3-4)"
        }
        
        breakdown = {
            "clif_of_components": {
                "liver": {
                    "parameter": "Bilirubin",
                    "value": f"{bilirubin} mg/dL",
                    "score": liver_score,
                    "max_score": 3,
                    "clinical_significance": "Reflects hepatocellular dysfunction and cholestasis"
                },
                "kidney": {
                    "parameter": "Creatinine/RRT",
                    "value": f"{creatinine} mg/dL" + (" (on RRT)" if renal_replacement_therapy == "yes" else ""),
                    "score": kidney_score,
                    "max_score": 3,
                    "clinical_significance": "Indicates renal dysfunction and need for renal replacement"
                },
                "brain": {
                    "parameter": "Hepatic Encephalopathy",
                    "value": he_descriptions[hepatic_encephalopathy_grade],
                    "score": brain_score,
                    "max_score": 3,
                    "clinical_significance": "Reflects neurological complications of liver failure"
                },
                "coagulation": {
                    "parameter": "INR",
                    "value": f"{inr}",
                    "score": coagulation_score,
                    "max_score": 3,
                    "clinical_significance": "Indicates coagulopathy and bleeding risk"
                },
                "circulatory": {
                    "parameter": "MAP/Vasopressors",
                    "value": f"{mean_arterial_pressure} mmHg" + (" (on vasopressors)" if vasopressors == "yes" else ""),
                    "score": circulatory_score,
                    "max_score": 3,
                    "clinical_significance": "Reflects hemodynamic instability and shock"
                },
                "respiratory": {
                    "parameter": f"{'PaO2/FiO2' if respiratory_ratio_type == 'pao2_fio2' else 'SpO2/FiO2'} Ratio",
                    "value": f"{respiratory_ratio_value}",
                    "score": respiratory_score,
                    "max_score": 3,
                    "clinical_significance": "Indicates respiratory failure and oxygenation impairment"
                }
            },
            "score_components": {
                "clif_of_score": {
                    "value": clif_of_score,
                    "max_value": 18,
                    "contribution": f"{self.coefficients['clif_of_coefficient'] * clif_of_score:.2f}",
                    "description": "CLIF-C Organ Failure score (sum of 6 organ systems)"
                },
                "age_component": {
                    "value": age,
                    "contribution": f"{self.coefficients['age_coefficient'] * age:.2f}",
                    "description": "Age contribution to mortality risk"
                },
                "wbc_component": {
                    "value": white_blood_cell_count,
                    "contribution": f"{self.coefficients['wbc_coefficient'] * math.log(white_blood_cell_count):.2f}",
                    "description": "White blood cell count (inflammatory response marker)"
                }
            },
            "score_summary": {
                "clif_of_score": clif_of_score,
                "final_aclf_score": round(aclf_score, 1),
                "max_possible_score": 100,
                "risk_category": self._get_risk_category(aclf_score)
            },
            "clinical_guidance": {
                "mortality_prediction": self._get_mortality_estimates(aclf_score),
                "treatment_recommendations": self._get_treatment_recommendations(aclf_score),
                "monitoring_intensity": self._get_monitoring_recommendations(aclf_score)
            },
            "prognostic_thresholds": {
                "score_65": "At 3-7 days after ACLF diagnosis, scores ≥65 indicate very poor prognosis",
                "score_70": "Scores ≥70 associated with 100% mortality at 28 days",
                "comparison_scores": "CLIF-C ACLF superior to MELD, MELD-Na, and Child-Pugh for ACLF mortality prediction"
            },
            "study_context": {
                "derivation_cohort": "CANONIC study (EASL-CLIF consortium)",
                "patient_population": "Patients with acute-on-chronic liver failure",
                "primary_outcome": "28-day mortality prediction",
                "validation": "AUROC 0.8 for 28-day mortality prediction"
            }
        }
        
        return breakdown
    
    def _get_risk_category(self, aclf_score: float) -> str:
        """Returns risk category description"""
        if aclf_score < 45:
            return "Low risk"
        elif aclf_score < 65:
            return "Moderate risk"
        elif aclf_score < 70:
            return "High risk"
        else:
            return "Critical risk"
    
    def _get_mortality_estimates(self, aclf_score: float) -> Dict[str, str]:
        """Returns mortality estimates based on score"""
        if aclf_score >= 70:
            return {
                "28_day": "100% (based on validation studies)",
                "90_day": "100% (expected)",
                "clinical_implication": "Universally fatal within 28 days"
            }
        elif aclf_score >= 65:
            return {
                "28_day": "Very high (>80%)",
                "90_day": "Very high (>90%)",
                "clinical_implication": "Extremely poor prognosis"
            }
        elif aclf_score >= 45:
            return {
                "28_day": "Moderate to high (30-60%)",
                "90_day": "High (50-80%)",
                "clinical_implication": "Significant mortality risk"
            }
        else:
            return {
                "28_day": "Lower (<30%)",
                "90_day": "Moderate (30-50%)",
                "clinical_implication": "Better prognosis with appropriate care"
            }
    
    def _get_treatment_recommendations(self, aclf_score: float) -> list:
        """Returns treatment recommendations based on score"""
        if aclf_score >= 70:
            return [
                "Consider transition to comfort care",
                "Family discussions regarding prognosis",
                "Avoid futile intensive interventions",
                "Focus on symptom management and dignity"
            ]
        elif aclf_score >= 65:
            return [
                "Urgent liver transplantation evaluation if eligible",
                "Intensive care unit management",
                "Consider experimental therapies or clinical trials",
                "Frequent reassessment of prognosis"
            ]
        elif aclf_score >= 45:
            return [
                "Liver transplantation evaluation",
                "Intensive care or high-dependency unit monitoring",
                "Optimize management of organ failures",
                "Consider liver support devices if available"
            ]
        else:
            return [
                "Standard hepatology care with close monitoring",
                "Optimize management of underlying liver disease",
                "Address precipitating factors",
                "Monitor for progression to higher ACLF grades"
            ]
    
    def _get_monitoring_recommendations(self, aclf_score: float) -> str:
        """Returns monitoring recommendations based on score"""
        if aclf_score >= 70:
            return "Comfort care monitoring focused on symptom management"
        elif aclf_score >= 65:
            return "Intensive care monitoring with continuous assessment"
        elif aclf_score >= 45:
            return "High-dependency unit or intensive care monitoring"
        else:
            return "Hospital ward monitoring with frequent assessments"


def calculate_clif_c_aclf(
    age: int,
    white_blood_cell_count: float,
    bilirubin: float,
    creatinine: float,
    renal_replacement_therapy: str,
    hepatic_encephalopathy_grade: str,
    inr: float,
    mean_arterial_pressure: float,
    vasopressors: str,
    respiratory_ratio_type: str,
    respiratory_ratio_value: float
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ClifCAclfCalculator()
    return calculator.calculate(
        age=age,
        white_blood_cell_count=white_blood_cell_count,
        bilirubin=bilirubin,
        creatinine=creatinine,
        renal_replacement_therapy=renal_replacement_therapy,
        hepatic_encephalopathy_grade=hepatic_encephalopathy_grade,
        inr=inr,
        mean_arterial_pressure=mean_arterial_pressure,
        vasopressors=vasopressors,
        respiratory_ratio_type=respiratory_ratio_type,
        respiratory_ratio_value=respiratory_ratio_value
    )