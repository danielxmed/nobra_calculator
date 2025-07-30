"""
CKD Prediction in HIV+ Patients Calculator

Determines likelihood of HIV patients developing chronic kidney disease (CKD) in the next 5 years,
with and without tenofovir use. Based on a prospective cohort study of HIV-positive male veterans.

References:
1. Scherzer R, Gandhi M, Estrella MM, Tien PC, Deeks SG, Grunfeld C, Peralta CA, Shlipak MG. 
   A chronic kidney disease risk score to determine tenofovir safety in a prospective cohort of 
   HIV-positive male veterans. AIDS. 2014;28(9):1289-95.
2. Mocroft A, Lundgren JD, Ross M, Law M, Reiss P, Kirk O, Smith C, Wentworth D, Neuhaus J, 
   Fux CA, Moranne O, Morlat P, Johnson MA, Ryom L; D:A:D Study Group. Development and 
   validation of a risk score for chronic kidney disease in HIV infection using prospective 
   cohort data from the D:A:D study. PLoS Med. 2015;12(3):e1001809.
"""

from typing import Dict, Any


class CkdPredictionHivPatientsCalculator:
    """Calculator for CKD Prediction in HIV+ Patients"""
    
    def __init__(self):
        # Risk factor point values
        self.age_points = {
            "19_to_39": 0,
            "40_to_49": 2,
            "50_to_59": 4,
            "60_to_90": 6
        }
        
        # Other risk factor points
        self.risk_factor_points = {
            "glucose_elevated": 2,
            "systolic_bp_elevated": 1,
            "hypertension": 2,
            "triglycerides_elevated": 1,
            "proteinuria": 2,
            "cd4_low": 1
        }
        
        # 5-year CKD event rates by score and tenofovir use
        # Based on the original study data
        self.event_rates = {
            "tenofovir_no": {
                0: 0.7,   # <1%
                1: 1.2,
                2: 2.1,
                3: 3.6,
                4: 6.2,
                5: 10.6,
                6: 12.8,
                7: 13.9,
                8: 15.1,
                9: 16.0,   # ≥9 points
                10: 16.0,
                11: 16.0,
                12: 16.0,
                13: 16.0,
                14: 16.0,
                15: 16.0
            },
            "tenofovir_yes": {
                0: 1.4,
                1: 2.4,
                2: 4.1,
                3: 7.0,
                4: 11.9,
                5: 19.0,
                6: 21.1,
                7: 21.3,
                8: 21.4,
                9: 21.4,   # ≥9 points
                10: 21.4,
                11: 21.4,
                12: 21.4,
                13: 21.4,
                14: 21.4,
                15: 21.4
            }
        }
        
        # Number needed to harm (NNH) estimates
        self.nnh_estimates = {
            0: 108,
            1: 87,
            2: 66,
            3: 50,
            4: 38,
            5: 29,
            6: 25,
            7: 24,
            8: 23,
            9: 20,   # ≥9 points
        }
    
    def calculate(
        self,
        age_category: str,
        glucose_elevated: str,
        systolic_bp_elevated: str,
        hypertension: str,
        triglycerides_elevated: str,
        proteinuria: str,
        cd4_low: str,
        tenofovir_use: str
    ) -> Dict[str, Any]:
        """
        Calculates 5-year CKD risk in HIV+ patients
        
        Args:
            age_category: Age category (19_to_39, 40_to_49, 50_to_59, 60_to_90)
            glucose_elevated: Glucose > 140 mg/dL (yes/no)
            systolic_bp_elevated: SBP > 140 mmHg (yes/no)
            hypertension: Hypertension diagnosis (yes/no)
            triglycerides_elevated: Triglycerides > 200 mg/dL (yes/no)
            proteinuria: Presence of proteinuria (yes/no)
            cd4_low: CD4+ < 200 cells/µL (yes/no)
            tenofovir_use: Current/planned tenofovir use (yes/no)
            
        Returns:
            Dict with CKD risk assessment and clinical recommendations
        """
        
        # Validate inputs
        self._validate_inputs(age_category, glucose_elevated, systolic_bp_elevated,
                            hypertension, triglycerides_elevated, proteinuria,
                            cd4_low, tenofovir_use)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            age_category, glucose_elevated, systolic_bp_elevated,
            hypertension, triglycerides_elevated, proteinuria, cd4_low
        )
        
        # Get 5-year CKD risk
        ckd_risk = self._get_ckd_risk(risk_score, tenofovir_use)
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(ckd_risk, tenofovir_use)
        
        # Get detailed breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            age_category, glucose_elevated, systolic_bp_elevated,
            hypertension, triglycerides_elevated, proteinuria,
            cd4_low, tenofovir_use, risk_score, ckd_risk
        )
        
        return {
            "result": ckd_risk,
            "unit": "percent",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"],
            "scoring_breakdown": scoring_breakdown
        }
    
    def _validate_inputs(self, age_category, glucose_elevated, systolic_bp_elevated,
                        hypertension, triglycerides_elevated, proteinuria,
                        cd4_low, tenofovir_use):
        """Validates input parameters"""
        
        # Validate age category
        valid_ages = ["19_to_39", "40_to_49", "50_to_59", "60_to_90"]
        if age_category not in valid_ages:
            raise ValueError(f"Age category must be one of {valid_ages}")
        
        # Validate yes/no parameters
        yes_no_params = [
            ("glucose_elevated", glucose_elevated),
            ("systolic_bp_elevated", systolic_bp_elevated),
            ("hypertension", hypertension),
            ("triglycerides_elevated", triglycerides_elevated),
            ("proteinuria", proteinuria),
            ("cd4_low", cd4_low),
            ("tenofovir_use", tenofovir_use)
        ]
        
        for param_name, value in yes_no_params:
            if value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_risk_score(self, age_category, glucose_elevated, systolic_bp_elevated,
                            hypertension, triglycerides_elevated, proteinuria, cd4_low):
        """Calculates the total risk score"""
        
        score = 0
        
        # Age points
        score += self.age_points[age_category]
        
        # Other risk factor points
        if glucose_elevated == "yes":
            score += self.risk_factor_points["glucose_elevated"]
        if systolic_bp_elevated == "yes":
            score += self.risk_factor_points["systolic_bp_elevated"]
        if hypertension == "yes":
            score += self.risk_factor_points["hypertension"]
        if triglycerides_elevated == "yes":
            score += self.risk_factor_points["triglycerides_elevated"]
        if proteinuria == "yes":
            score += self.risk_factor_points["proteinuria"]
        if cd4_low == "yes":
            score += self.risk_factor_points["cd4_low"]
        
        return score
    
    def _get_ckd_risk(self, risk_score: int, tenofovir_use: str) -> float:
        """Gets 5-year CKD risk percentage based on score and tenofovir use"""
        
        # Cap score at maximum for lookup
        lookup_score = min(risk_score, 15)
        
        if tenofovir_use == "yes":
            return self.event_rates["tenofovir_yes"][lookup_score]
        else:
            return self.event_rates["tenofovir_no"][lookup_score]
    
    def _get_risk_assessment(self, ckd_risk: float, tenofovir_use: str) -> Dict[str, str]:
        """
        Determines risk category and clinical recommendations
        
        Args:
            ckd_risk: 5-year CKD risk percentage
            tenofovir_use: Whether patient uses tenofovir
            
        Returns:
            Dict with risk assessment and clinical recommendations
        """
        
        tenofovir_status = "with tenofovir use" if tenofovir_use == "yes" else "without tenofovir use"
        
        if ckd_risk < 5:
            stage = "Low Risk"
            description = "Low risk for CKD development"
            if tenofovir_use == "yes":
                interpretation = f"5-year CKD risk: {ckd_risk}% with tenofovir. Low risk - tenofovir use reasonable with routine monitoring of kidney function every 6-12 months."
            else:
                interpretation = f"5-year CKD risk: {ckd_risk}% without tenofovir. Low baseline CKD risk - tenofovir could be considered if clinically indicated."
                
        elif ckd_risk < 15:
            stage = "Moderate Risk"
            description = "Moderate risk for CKD development"
            if tenofovir_use == "yes":
                interpretation = f"5-year CKD risk: {ckd_risk}% with tenofovir. Moderate risk - careful monitoring every 3-6 months and consideration of alternative agents if CKD progression occurs."
            else:
                interpretation = f"5-year CKD risk: {ckd_risk}% without tenofovir. Moderate baseline risk - weigh benefits vs risks of tenofovir, consider alternatives if available."
                
        else:  # ckd_risk >= 15
            stage = "High Risk"
            description = "High risk for CKD development"
            if tenofovir_use == "yes":
                interpretation = f"5-year CKD risk: {ckd_risk}% with tenofovir. High risk - strong consideration for tenofovir alternative. If continued, monitor every 3 months."
            else:
                interpretation = f"5-year CKD risk: {ckd_risk}% without tenofovir. High baseline risk - avoid tenofovir if possible, use alternative antiretroviral regimen."
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, age_category, glucose_elevated, systolic_bp_elevated,
                             hypertension, triglycerides_elevated, proteinuria,
                             cd4_low, tenofovir_use, risk_score, ckd_risk) -> Dict[str, Any]:
        """Provides detailed scoring breakdown and clinical context"""
        
        # Calculate component points
        age_points = self.age_points[age_category]
        glucose_points = self.risk_factor_points["glucose_elevated"] if glucose_elevated == "yes" else 0
        sbp_points = self.risk_factor_points["systolic_bp_elevated"] if systolic_bp_elevated == "yes" else 0
        htn_points = self.risk_factor_points["hypertension"] if hypertension == "yes" else 0
        trig_points = self.risk_factor_points["triglycerides_elevated"] if triglycerides_elevated == "yes" else 0
        protein_points = self.risk_factor_points["proteinuria"] if proteinuria == "yes" else 0
        cd4_points = self.risk_factor_points["cd4_low"] if cd4_low == "yes" else 0
        
        # Age category descriptions
        age_descriptions = {
            "19_to_39": "19-39 years",
            "40_to_49": "40-49 years", 
            "50_to_59": "50-59 years",
            "60_to_90": "60-90 years"
        }
        
        # Calculate risk without tenofovir for comparison
        risk_without_tdf = self._get_ckd_risk(risk_score, "no")
        risk_with_tdf = self._get_ckd_risk(risk_score, "yes")
        
        # Get NNH estimate
        nnh_score = min(risk_score, 9)
        nnh = self.nnh_estimates.get(nnh_score, 20)
        
        breakdown = {
            "risk_factors": {
                "age": {
                    "category": age_descriptions[age_category],
                    "points": age_points,
                    "rationale": "Older age is a dominant risk factor for CKD development"
                },
                "glucose_elevated": {
                    "present": glucose_elevated == "yes",
                    "points": glucose_points,
                    "rationale": "Glucose >140 mg/dL indicates diabetes risk, major CKD predictor"
                },
                "systolic_bp_elevated": {
                    "present": systolic_bp_elevated == "yes",
                    "points": sbp_points,
                    "rationale": "SBP >140 mmHg reflects vascular damage and CKD risk"
                },
                "hypertension": {
                    "present": hypertension == "yes",
                    "points": htn_points,
                    "rationale": "Hypertension diagnosis is strongest traditional CKD risk factor"
                },
                "triglycerides_elevated": {
                    "present": triglycerides_elevated == "yes",
                    "points": trig_points,
                    "rationale": "Triglycerides >200 mg/dL indicates metabolic dysfunction"
                },
                "proteinuria": {
                    "present": proteinuria == "yes",
                    "points": protein_points,
                    "rationale": "Proteinuria indicates existing kidney damage"
                },
                "cd4_low": {
                    "present": cd4_low == "yes",
                    "points": cd4_points,
                    "rationale": "CD4 <200 reflects HIV disease severity and immune suppression"
                }
            },
            "score_summary": {
                "total_score": risk_score,
                "max_possible_score": 15,
                "risk_category": self._get_risk_category(ckd_risk)
            },
            "risk_comparison": {
                "without_tenofovir": f"{risk_without_tdf}%",
                "with_tenofovir": f"{risk_with_tdf}%",
                "absolute_risk_increase": f"{risk_with_tdf - risk_without_tdf:.1f}%",
                "relative_risk_increase": f"{((risk_with_tdf / risk_without_tdf) - 1) * 100:.0f}%" if risk_without_tdf > 0 else "N/A",
                "number_needed_to_harm": nnh
            },
            "clinical_guidance": {
                "monitoring_frequency": self._get_monitoring_frequency(ckd_risk, tenofovir_use),
                "alternative_considerations": self._get_alternative_considerations(ckd_risk),
                "additional_risk_factors": [
                    "Consider baseline eGFR and rate of decline",
                    "Assess for concurrent nephrotoxic medications",
                    "Evaluate for hepatitis B or C coinfection",
                    "Monitor for cardiovascular disease development"
                ]
            },
            "study_context": {
                "population": "HIV-positive male veterans (Veterans Health Administration)",
                "follow_up_period": "5 years prospective follow-up",
                "outcome_definition": "CKD defined as eGFR <60 mL/min/1.73m² or proteinuria",
                "tenofovir_effect": "Overall adjusted hazard ratio 2.0 (95% CI 1.8-2.2)",
                "validation": "External validation in D:A:D cohort study"
            }
        }
        
        return breakdown
    
    def _get_risk_category(self, ckd_risk: float) -> str:
        """Returns risk category description"""
        if ckd_risk < 5:
            return "Low risk"
        elif ckd_risk < 15:
            return "Moderate risk"
        else:
            return "High risk"
    
    def _get_monitoring_frequency(self, ckd_risk: float, tenofovir_use: str) -> str:
        """Returns recommended monitoring frequency"""
        if tenofovir_use == "yes":
            if ckd_risk >= 15:
                return "Every 3 months (high risk with tenofovir)"
            elif ckd_risk >= 5:
                return "Every 3-6 months (moderate risk with tenofovir)"
            else:
                return "Every 6-12 months (low risk with tenofovir)"
        else:
            return "Every 6-12 months (standard HIV care without tenofovir)"
    
    def _get_alternative_considerations(self, ckd_risk: float) -> list:
        """Returns alternative treatment considerations"""
        if ckd_risk >= 15:
            return [
                "Strong consideration for tenofovir alternatives (TAF, abacavir, rilpivirine)",
                "Nephrology consultation if eGFR declining",
                "Optimize cardiovascular risk factors",
                "Consider ACE inhibitor/ARB if hypertensive"
            ]
        elif ckd_risk >= 5:
            return [
                "Consider tenofovir alternatives if equally effective",
                "Enhanced monitoring of kidney function",
                "Optimize blood pressure and glucose control",
                "Avoid other nephrotoxic medications when possible"
            ]
        else:
            return [
                "Tenofovir use reasonable with standard monitoring",
                "Maintain good control of traditional risk factors",
                "Regular assessment for CKD risk factor development"
            ]


def calculate_ckd_prediction_hiv_patients(
    age_category: str,
    glucose_elevated: str,
    systolic_bp_elevated: str,
    hypertension: str,
    triglycerides_elevated: str,
    proteinuria: str,
    cd4_low: str,
    tenofovir_use: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CkdPredictionHivPatientsCalculator()
    return calculator.calculate(
        age_category=age_category,
        glucose_elevated=glucose_elevated,
        systolic_bp_elevated=systolic_bp_elevated,
        hypertension=hypertension,
        triglycerides_elevated=triglycerides_elevated,
        proteinuria=proteinuria,
        cd4_low=cd4_low,
        tenofovir_use=tenofovir_use
    )