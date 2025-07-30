"""
CHADS₂ Score for Atrial Fibrillation Stroke Risk Calculator

Clinical prediction tool that estimates annual stroke risk in patients with atrial 
fibrillation to guide anticoagulation therapy decisions.

References:
1. Gage BF, Waterman AD, Shannon W, Boechler M, Rich MW, Radford MJ. 
   Validation of clinical classification schemes for predicting stroke: results 
   from the National Registry of Atrial Fibrillation. JAMA. 2001;285(22):2864-70.
2. Gage BF, van Walraven C, Pearce L, Hart RG, Koudstaal PJ, Boode BS, Petersen P. 
   Selecting patients with atrial fibrillation for anticoagulation: stroke risk 
   stratification in patients taking aspirin. Circulation. 2004;110(16):2287-92.
3. Olesen JB, Lip GY, Hansen ML, Hansen PR, Tolstrup JS, Lindhardsen J, Selmer C, 
   Ahlehoff O, Olsen AM, Gislason GH, Torp-Pedersen C. Validation of risk 
   stratification schemes for predicting stroke and thromboembolism in patients 
   with atrial fibrillation: nationwide cohort study. BMJ. 2011;342:d124.
"""

from typing import Dict, Any


class Chads2ScoreCalculator:
    """Calculator for CHADS₂ Score for Atrial Fibrillation Stroke Risk"""
    
    def __init__(self):
        # Annual stroke risk rates by CHADS₂ score
        self.stroke_risk_rates = {
            0: {"rate": 1.9, "range": "1.2-3.0", "category": "Low"},
            1: {"rate": 2.8, "range": "2.0-3.8", "category": "Low-Intermediate"},
            2: {"rate": 4.0, "range": "3.1-5.1", "category": "Intermediate"},
            3: {"rate": 5.9, "range": "4.6-7.3", "category": "High"},
            4: {"rate": 8.5, "range": "6.3-11.1", "category": "High"},
            5: {"rate": 12.5, "range": "8.2-17.5", "category": "Very High"},
            6: {"rate": 18.2, "range": "10.5-27.4", "category": "Very High"}
        }
        
        # Anticoagulation recommendations
        self.anticoagulation_recommendations = {
            0: {
                "recommendation": "Consider further risk stratification",
                "therapy": "Consider CHA₂DS₂-VASc score or aspirin based on bleeding risk",
                "strength": "Weak recommendation"
            },
            1: {
                "recommendation": "Consider anticoagulation or further risk stratification", 
                "therapy": "CHA₂DS₂-VASc score or anticoagulation based on bleeding risk assessment",
                "strength": "Moderate recommendation"
            },
            2: {
                "recommendation": "Anticoagulation generally recommended",
                "therapy": "Warfarin or direct oral anticoagulants (DOACs) unless contraindicated",
                "strength": "Strong recommendation"
            },
            3: {
                "recommendation": "Strong recommendation for anticoagulation",
                "therapy": "Warfarin or direct oral anticoagulants (DOACs)",
                "strength": "Strong recommendation"
            },
            4: {
                "recommendation": "Strong recommendation for anticoagulation",
                "therapy": "Warfarin or direct oral anticoagulants (DOACs)",
                "strength": "Strong recommendation"
            },
            5: {
                "recommendation": "Strong recommendation for anticoagulation",
                "therapy": "Warfarin or direct oral anticoagulants (DOACs)",
                "strength": "Strong recommendation"
            },
            6: {
                "recommendation": "Strong recommendation for anticoagulation",
                "therapy": "Warfarin or direct oral anticoagulants (DOACs)",
                "strength": "Strong recommendation"
            }
        }
    
    def calculate(
        self,
        congestive_heart_failure: str,
        hypertension: str,
        age_75_or_older: str,
        diabetes_mellitus: str,
        stroke_tia_thromboembolism: str
    ) -> Dict[str, Any]:
        """
        Calculates CHADS₂ score for stroke risk in atrial fibrillation patients
        
        Args:
            congestive_heart_failure: History of CHF or LV dysfunction
            hypertension: History of hypertension or current treatment
            age_75_or_older: Patient age 75 years or older
            diabetes_mellitus: History of diabetes or current treatment
            stroke_tia_thromboembolism: Previous stroke, TIA, or thromboembolism
            
        Returns:
            Dict with CHADS₂ score, stroke risk, and anticoagulation recommendations
        """
        
        # Validate inputs
        self._validate_inputs(
            congestive_heart_failure, hypertension, age_75_or_older,
            diabetes_mellitus, stroke_tia_thromboembolism
        )
        
        # Calculate total score
        total_score = self._calculate_total_score(
            congestive_heart_failure, hypertension, age_75_or_older,
            diabetes_mellitus, stroke_tia_thromboembolism
        )
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Get anticoagulation recommendation
        anticoag_recommendation = self._get_anticoagulation_recommendation(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            congestive_heart_failure, hypertension, age_75_or_older,
            diabetes_mellitus, stroke_tia_thromboembolism
        )
        
        return {
            "result": {
                "total_score": total_score,
                "annual_stroke_risk_percent": risk_assessment["rate"],
                "stroke_risk_range": risk_assessment["range"],
                "risk_category": risk_assessment["category"],
                "anticoagulation_recommendation": anticoag_recommendation["recommendation"],
                "therapy_details": anticoag_recommendation["therapy"],
                "recommendation_strength": anticoag_recommendation["strength"],
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["stage"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, chf, htn, age, dm, stroke):
        """Validates input parameters"""
        
        parameters = [
            ("congestive_heart_failure", chf),
            ("hypertension", htn),
            ("age_75_or_older", age),
            ("diabetes_mellitus", dm),
            ("stroke_tia_thromboembolism", stroke)
        ]
        
        valid_yes_no = ["yes", "no"]
        
        for param_name, param_value in parameters:
            if param_value not in valid_yes_no:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, chf, htn, age, dm, stroke):
        """Calculates total CHADS₂ score (0-6 points)"""
        
        score = 0
        
        # Each parameter contributes 1 point if "yes", except stroke which is 2 points
        if chf == "yes":
            score += 1
        
        if htn == "yes":
            score += 1
        
        if age == "yes":
            score += 1
        
        if dm == "yes":
            score += 1
        
        if stroke == "yes":
            score += 2  # Stroke/TIA/thromboembolism worth 2 points
        
        return score
    
    def _get_risk_assessment(self, score: int) -> Dict[str, Any]:
        """Gets stroke risk assessment based on CHADS₂ score"""
        
        if score in self.stroke_risk_rates:
            risk_data = self.stroke_risk_rates[score]
            return self._format_risk_assessment(score, risk_data)
        
        # Fallback (should not occur with valid scores 0-6)
        return {
            "rate": "Unknown",
            "range": "Unknown",
            "category": "Unknown",
            "stage": "Unknown Risk",
            "description": "Score outside validated range",
            "interpretation": f"CHADS₂ Score {score}: Score outside validated range. Clinical assessment required."
        }
    
    def _format_risk_assessment(self, score: int, risk_data: Dict) -> Dict[str, Any]:
        """Formats risk assessment with detailed interpretation"""
        
        stage_mapping = {
            "Low": "Low Risk",
            "Low-Intermediate": "Low-Intermediate Risk",
            "Intermediate": "Intermediate Risk",
            "High": "High Risk",
            "Very High": "Very High Risk"
        }
        
        interpretation_templates = {
            0: f"CHADS₂ Score {score}: Low stroke risk ({risk_data['rate']}% per year, 95% CI: {risk_data['range']}%). Consider further risk stratification with CHA₂DS₂-VASc score. May consider aspirin or observation based on bleeding risk and patient preferences.",
            1: f"CHADS₂ Score {score}: Low-intermediate stroke risk ({risk_data['rate']}% per year, 95% CI: {risk_data['range']}%). Consider further risk stratification with CHA₂DS₂-VASc score or anticoagulation based on bleeding risk assessment.",
            2: f"CHADS₂ Score {score}: Intermediate stroke risk ({risk_data['rate']}% per year, 95% CI: {risk_data['range']}%). Anticoagulation generally recommended unless contraindicated due to bleeding risk.",
        }
        
        # For scores ≥3, use high-risk template
        if score >= 3:
            interpretation = f"CHADS₂ Score {score}: {risk_data['category'].lower()} stroke risk ({risk_data['rate']}% per year, 95% CI: {risk_data['range']}%). Strong recommendation for anticoagulation therapy with warfarin or direct oral anticoagulants (DOACs)."
        else:
            interpretation = interpretation_templates.get(score, f"CHADS₂ Score {score}: Clinical assessment required.")
        
        return {
            "rate": risk_data["rate"],
            "range": risk_data["range"],
            "category": risk_data["category"],
            "stage": stage_mapping.get(risk_data["category"], "Unknown Risk"),
            "description": f"{risk_data['category']} annual stroke risk",
            "interpretation": interpretation
        }
    
    def _get_anticoagulation_recommendation(self, score: int) -> Dict[str, str]:
        """Gets anticoagulation recommendation based on score"""
        
        return self.anticoagulation_recommendations.get(
            score, 
            {
                "recommendation": "Clinical assessment required",
                "therapy": "Score outside validated range",
                "strength": "Unknown"
            }
        )
    
    def _get_scoring_breakdown(self, chf, htn, age, dm, stroke):
        """Provides detailed scoring breakdown"""
        
        breakdown = {
            "chads2_components": {
                "congestive_heart_failure": {
                    "present": chf == "yes",
                    "points": 1 if chf == "yes" else 0,
                    "description": "History of congestive heart failure or left ventricular dysfunction"
                },
                "hypertension": {
                    "present": htn == "yes",
                    "points": 1 if htn == "yes" else 0,
                    "description": "History of hypertension or current antihypertensive treatment"
                },
                "age_75_or_older": {
                    "present": age == "yes",
                    "points": 1 if age == "yes" else 0,
                    "description": "Age 75 years or older"
                },
                "diabetes_mellitus": {
                    "present": dm == "yes",
                    "points": 1 if dm == "yes" else 0,
                    "description": "History of diabetes mellitus or current antidiabetic treatment"
                },
                "stroke_tia_thromboembolism": {
                    "present": stroke == "yes",
                    "points": 2 if stroke == "yes" else 0,
                    "description": "Previous stroke, TIA, or thromboembolism (worth 2 points)"
                }
            },
            "clinical_context": {
                "development": "Developed from National Registry of Atrial Fibrillation (2001)",
                "validation": "C-statistic ~0.68 for stroke prediction",
                "evolution": "Largely superseded by CHA₂DS₂-VASc score for more comprehensive assessment",
                "population": "Validated in multiple healthcare systems and populations"
            },
            "limitations": [
                "Does not capture all stroke risk factors (vascular disease, gender)",
                "Age cutoff at 75 misses moderate risk in 65-74 age group",
                "Better at identifying high-risk than truly low-risk patients",
                "Current guidelines recommend CHA₂DS₂-VASc for more accurate stratification"
            ]
        }
        
        return breakdown


def calculate_chads2_score(
    congestive_heart_failure: str,
    hypertension: str,
    age_75_or_older: str,
    diabetes_mellitus: str,
    stroke_tia_thromboembolism: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Chads2ScoreCalculator()
    return calculator.calculate(
        congestive_heart_failure=congestive_heart_failure,
        hypertension=hypertension,
        age_75_or_older=age_75_or_older,
        diabetes_mellitus=diabetes_mellitus,
        stroke_tia_thromboembolism=stroke_tia_thromboembolism
    )