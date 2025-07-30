"""
DASH Prediction Score for Recurrent VTE Calculator

Predicts likelihood of recurrence of first unprovoked venous thromboembolism (VTE) 
to guide anticoagulation duration decisions.

References:
- Tosetto A, et al. J Thromb Haemost. 2012;10(6):1019-1025.
- Kearon C, et al. Chest. 2016;149(2):315-352.
- Ortel TL, et al. Blood Adv. 2020;4(19):4693-4738.
"""

from typing import Dict, Any, Optional


class DashPredictionScoreCalculator:
    """Calculator for DASH Prediction Score for Recurrent VTE"""
    
    def __init__(self):
        # DASH score components and weights
        self.SCORE_COMPONENTS = {
            "d_dimer_positive": 2,
            "age_50_or_under": 1,
            "male_sex": 1,
            "hormonal_therapy": -2  # Only for women
        }
        
        # Risk categories and associated data
        self.RISK_CATEGORIES = {
            "low": {
                "score_range": (-2, 1),
                "label": "Low Risk",
                "description": "Low annual recurrence risk",
                "annual_risk": "3.1%",
                "annual_risk_numeric": 3.1,
                "confidence_interval": "2.3-3.9%",
                "recommendation": "Consider discontinuing anticoagulation"
            },
            "intermediate": {
                "score_range": (2, 2),
                "label": "Intermediate Risk", 
                "description": "Moderate annual recurrence risk",
                "annual_risk": "6.4%",
                "annual_risk_numeric": 6.4,
                "confidence_interval": "4.8-7.9%",
                "recommendation": "Individualized decision based on bleeding risk"
            },
            "high": {
                "score_range": (3, 6),
                "label": "High Risk",
                "description": "High annual recurrence risk",
                "annual_risk": "12.3%",
                "annual_risk_numeric": 12.3,
                "confidence_interval": "9.9-14.7%",
                "recommendation": "Consider prolonged/indefinite anticoagulation"
            }
        }
        
        # Anticoagulation recommendations by risk category
        self.ANTICOAGULATION_RECOMMENDATIONS = {
            "low": [
                "Consider discontinuing anticoagulation after 3-6 months",
                "Monitor for signs and symptoms of VTE recurrence",
                "Patient education about VTE risk factors and prevention",
                "Regular follow-up for risk reassessment",
                "Consider mechanical prophylaxis during high-risk periods"
            ],
            "intermediate": [
                "Individualized decision-making required",
                "Assess bleeding risk using validated tools (HAS-BLED, HEMORR2HAGES)",
                "Consider patient preferences and quality of life factors",
                "Discuss risks and benefits of continued anticoagulation",
                "May consider extended anticoagulation (6-12 months) with reassessment"
            ],
            "high": [
                "Strong consideration for prolonged anticoagulation",
                "Evaluate for indefinite anticoagulation if bleeding risk acceptable",
                "Regular monitoring for bleeding complications",
                "Periodic reassessment of risk-benefit ratio",
                "Consider newer anticoagulants with improved safety profiles"
            ]
        }
    
    def calculate(self, d_dimer_positive: str, age: int, sex: str, hormonal_therapy: str,
                  vte_type: Optional[str] = None, anticoagulation_duration: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates DASH prediction score based on clinical parameters
        
        Args:
            d_dimer_positive (str): Post-anticoagulation D-dimer result ("positive" or "negative")
            age (int): Patient age in years
            sex (str): Patient biological sex ("male" or "female")
            hormonal_therapy (str): Hormonal therapy use ("yes", "no", or "not_applicable")
            vte_type (str, optional): Type of initial VTE for clinical context
            anticoagulation_duration (int, optional): Duration of initial treatment in months
            
        Returns:
            Dict with DASH score, risk assessment, and anticoagulation recommendations
        """
        
        # Validations
        self._validate_inputs(d_dimer_positive, age, sex, hormonal_therapy, 
                            vte_type, anticoagulation_duration)
        
        # Calculate DASH score
        dash_score = self._calculate_dash_score(d_dimer_positive, age, sex, hormonal_therapy)
        
        # Determine risk category
        risk_category = self._determine_risk_category(dash_score)
        
        # Get risk details
        risk_details = self.RISK_CATEGORIES[risk_category]
        
        # Generate clinical assessment
        clinical_assessment = self._get_clinical_assessment(d_dimer_positive, age, sex, 
                                                          hormonal_therapy, dash_score, risk_category)
        
        # Get anticoagulation recommendations
        anticoagulation_recommendations = self._get_anticoagulation_recommendations(
            risk_category, age, vte_type, anticoagulation_duration)
        
        # Generate interpretation
        interpretation = self._get_interpretation(risk_category, dash_score, risk_details)
        
        # Get decision support
        decision_support = self._get_decision_support(risk_category, dash_score)
        
        return {
            "result": dash_score,
            "unit": "DASH score",
            "interpretation": interpretation,
            "stage": risk_details["label"],
            "stage_description": risk_details["description"],
            "dash_score": dash_score,
            "risk_category": risk_category,
            "annual_risk": risk_details["annual_risk"],
            "annual_risk_numeric": risk_details["annual_risk_numeric"],
            "confidence_interval": risk_details["confidence_interval"],
            "recommendation": risk_details["recommendation"],
            "clinical_assessment": clinical_assessment,
            "anticoagulation_recommendations": anticoagulation_recommendations,
            "decision_support": decision_support,
            "score_components": self._get_score_breakdown(d_dimer_positive, age, sex, hormonal_therapy),
            "counseling_points": self._get_counseling_points(risk_category, dash_score),
            "follow_up_recommendations": self._get_follow_up_recommendations(risk_category)
        }
    
    def _validate_inputs(self, d_dimer_positive, age, sex, hormonal_therapy, 
                        vte_type, anticoagulation_duration):
        """Validates input parameters"""
        
        # Validate D-dimer
        if d_dimer_positive not in ["positive", "negative"]:
            raise ValueError("d_dimer_positive must be 'positive' or 'negative'")
        
        # Validate age
        if not isinstance(age, int) or not 18 <= age <= 100:
            raise ValueError("Age must be an integer between 18 and 100")
        
        # Validate sex
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        # Validate hormonal therapy
        if hormonal_therapy not in ["yes", "no", "not_applicable"]:
            raise ValueError("hormonal_therapy must be 'yes', 'no', or 'not_applicable'")
        
        # Cross-validation: hormonal therapy should be not_applicable for males
        if sex == "male" and hormonal_therapy != "not_applicable":
            raise ValueError("For male patients, hormonal_therapy should be 'not_applicable'")
        
        # Validate optional parameters
        if vte_type is not None:
            valid_vte_types = ["dvt_only", "pe_only", "dvt_and_pe", "not_specified"]
            if vte_type not in valid_vte_types:
                raise ValueError(f"vte_type must be one of: {valid_vte_types}")
        
        if anticoagulation_duration is not None:
            if not isinstance(anticoagulation_duration, int) or not 3 <= anticoagulation_duration <= 24:
                raise ValueError("anticoagulation_duration must be an integer between 3 and 24 months")
    
    def _calculate_dash_score(self, d_dimer_positive, age, sex, hormonal_therapy):
        """Calculates the DASH score using component weights"""
        
        score = 0
        
        # D-dimer component (+2 if positive)
        if d_dimer_positive == "positive":
            score += self.SCORE_COMPONENTS["d_dimer_positive"]
        
        # Age component (+1 if ≤50 years)
        if age <= 50:
            score += self.SCORE_COMPONENTS["age_50_or_under"]
        
        # Sex component (+1 if male)
        if sex == "male":
            score += self.SCORE_COMPONENTS["male_sex"]
        
        # Hormonal therapy component (-2 if yes, only for women)
        if sex == "female" and hormonal_therapy == "yes":
            score += self.SCORE_COMPONENTS["hormonal_therapy"]  # This is -2
        
        return score
    
    def _determine_risk_category(self, dash_score):
        """Determines risk category based on DASH score"""
        
        for category, details in self.RISK_CATEGORIES.items():
            score_min, score_max = details["score_range"]
            if score_min <= dash_score <= score_max:
                return category
        
        # Handle edge cases (scores outside expected range)
        if dash_score < -2:
            return "low"
        else:
            return "high"
    
    def _get_clinical_assessment(self, d_dimer_positive, age, sex, hormonal_therapy, 
                                dash_score, risk_category):
        """Generate clinical assessment based on parameters"""
        
        assessment = {
            "dash_score": dash_score,
            "risk_category": risk_category,
            "score_components": [],
            "clinical_factors": [],
            "additional_considerations": []
        }
        
        # Document score components
        if d_dimer_positive == "positive":
            assessment["score_components"].append("D-dimer positive (+2 points)")
        else:
            assessment["score_components"].append("D-dimer negative (0 points)")
        
        if age <= 50:
            assessment["score_components"].append(f"Age ≤50 years (age {age}, +1 point)")
        else:
            assessment["score_components"].append(f"Age >50 years (age {age}, 0 points)")
        
        if sex == "male":
            assessment["score_components"].append("Male sex (+1 point)")
        else:
            assessment["score_components"].append("Female sex (0 points)")
        
        if sex == "female":
            if hormonal_therapy == "yes":
                assessment["score_components"].append("Hormonal therapy at time of VTE (-2 points)")
            elif hormonal_therapy == "no":
                assessment["score_components"].append("No hormonal therapy (0 points)")
        
        # Clinical factors
        assessment["clinical_factors"] = [
            f"First unprovoked VTE requiring anticoagulation duration decision",
            f"DASH score of {dash_score} indicates {risk_category} risk for recurrence",
            f"Post-anticoagulation D-dimer: {d_dimer_positive}"
        ]
        
        # Additional considerations
        if d_dimer_positive == "positive":
            assessment["additional_considerations"].append("Positive D-dimer indicates ongoing thrombotic activity")
        
        if age > 65:
            assessment["additional_considerations"].append("Age >65 may be associated with higher recurrence risk despite low DASH score")
        
        if sex == "female" and hormonal_therapy == "yes":
            assessment["additional_considerations"].append("Hormonal therapy was a contributing factor to initial VTE")
        
        return assessment
    
    def _get_anticoagulation_recommendations(self, risk_category, age, vte_type, anticoagulation_duration):
        """Get anticoagulation recommendations based on risk assessment"""
        
        base_recommendations = self.ANTICOAGULATION_RECOMMENDATIONS[risk_category].copy()
        specific_recommendations = []
        
        # Age-specific considerations
        if age > 65:
            if risk_category == "low":
                specific_recommendations.append("Despite low DASH score, age >65 may warrant extended anticoagulation consideration")
            specific_recommendations.append("Enhanced bleeding risk assessment important in elderly patients")
        
        if age < 40:
            specific_recommendations.append("Young age may favor longer anticoagulation if bleeding risk is low")
        
        # VTE type considerations
        if vte_type == "pe_only" or vte_type == "dvt_and_pe":
            specific_recommendations.append("Pulmonary embolism may warrant more conservative approach to discontinuation")
        
        # Duration considerations
        if anticoagulation_duration is not None:
            if anticoagulation_duration >= 6:
                specific_recommendations.append(f"Already treated for {anticoagulation_duration} months - consider patient tolerance and preferences")
        
        return {
            "primary_recommendations": base_recommendations,
            "specific_considerations": specific_recommendations,
            "bleeding_assessment": self._get_bleeding_assessment_guidance(),
            "monitoring_plan": self._get_monitoring_plan(risk_category)
        }
    
    def _get_bleeding_assessment_guidance(self):
        """Get guidance for bleeding risk assessment"""
        
        return {
            "assessment_tools": [
                "HAS-BLED score for bleeding risk assessment",
                "HEMORR2HAGES score for major bleeding risk",
                "Patient-specific bleeding risk factors evaluation"
            ],
            "key_factors": [
                "History of major bleeding",
                "Age and frailty status",
                "Concurrent medications (antiplatelets, NSAIDs)",
                "Comorbidities (liver disease, kidney disease)",
                "Fall risk and cognitive status",
                "Patient lifestyle and adherence factors"
            ]
        }
    
    def _get_monitoring_plan(self, risk_category):
        """Get monitoring plan based on risk category"""
        
        if risk_category == "low":
            return [
                "Clinical follow-up at 3 and 6 months after discontinuation",
                "Patient education about VTE symptoms and when to seek care",
                "Consider repeat D-dimer at 6-12 months if clinically indicated"
            ]
        elif risk_category == "intermediate":
            return [
                "Regular clinical follow-up every 3-6 months",
                "Bleeding assessment and monitoring if continuing anticoagulation",
                "Reassessment of risk-benefit ratio at regular intervals",
                "Patient education about both thrombotic and bleeding risks"
            ]
        else:  # high risk
            return [
                "Regular monitoring for bleeding complications",
                "Clinical follow-up every 3-6 months",
                "Annual reassessment of risk-benefit ratio",
                "Consider newer anticoagulants with improved safety profiles",
                "Coordinate care with anticoagulation clinic if available"
            ]
    
    def _get_decision_support(self, risk_category, dash_score):
        """Get decision support information"""
        
        support = {
            "primary_decision": "",
            "key_considerations": [],
            "shared_decision_making": []
        }
        
        if risk_category == "low":
            support["primary_decision"] = "Anticoagulation discontinuation is reasonable"
            support["key_considerations"] = [
                "Low 3.1% annual recurrence risk",
                "Risk of continued anticoagulation may outweigh benefits",
                "Consider patient anxiety about discontinuation"
            ]
        elif risk_category == "intermediate":
            support["primary_decision"] = "Individualized decision required"
            support["key_considerations"] = [
                "Moderate 6.4% annual recurrence risk",
                "Balance thrombotic risk vs bleeding risk",
                "Patient values and preferences are crucial"
            ]
        else:  # high risk
            support["primary_decision"] = "Strong consideration for continued anticoagulation"
            support["key_considerations"] = [
                "High 12.3% annual recurrence risk",
                "Benefits likely outweigh bleeding risk for most patients",
                "Consider indefinite anticoagulation"
            ]
        
        support["shared_decision_making"] = [
            "Discuss quantitative risks with patient",
            "Explore patient values and quality of life preferences",
            "Consider bleeding risk and mitigation strategies",
            "Plan for regular reassessment and decision review"
        ]
        
        return support
    
    def _get_score_breakdown(self, d_dimer_positive, age, sex, hormonal_therapy):
        """Get detailed breakdown of score components"""
        
        components = []
        
        d_dimer_points = 2 if d_dimer_positive == "positive" else 0
        components.append({
            "component": "D-dimer",
            "value": d_dimer_positive,
            "points": d_dimer_points,
            "description": f"D-dimer {d_dimer_positive}"
        })
        
        age_points = 1 if age <= 50 else 0
        components.append({
            "component": "Age",
            "value": age,
            "points": age_points,
            "description": f"Age {age} years ({'≤50' if age <= 50 else '>50'})"
        })
        
        sex_points = 1 if sex == "male" else 0
        components.append({
            "component": "Sex",
            "value": sex,
            "points": sex_points,
            "description": f"{sex.title()} sex"
        })
        
        if sex == "female":
            hormone_points = -2 if hormonal_therapy == "yes" else 0
            components.append({
                "component": "Hormonal therapy",
                "value": hormonal_therapy,
                "points": hormone_points,
                "description": f"Hormonal therapy: {hormonal_therapy}"
            })
        
        return components
    
    def _get_counseling_points(self, risk_category, dash_score):
        """Get key counseling points for patient discussion"""
        
        general_points = [
            "VTE recurrence risk decreases over time after the initial event",
            "Most recurrences occur within the first 2 years",
            "Individual risk factors and preferences should guide decision-making",
            "Regular reassessment is important as circumstances may change"
        ]
        
        if risk_category == "low":
            specific_points = [
                "Your low DASH score indicates relatively low recurrence risk",
                "Stopping anticoagulation after 3-6 months is reasonable",
                "Continue to be aware of VTE symptoms and risk factors",
                "Mechanical prophylaxis during high-risk periods is important"
            ]
        elif risk_category == "intermediate":
            specific_points = [
                "Your DASH score indicates moderate recurrence risk",
                "Decision about continuing anticoagulation should be individualized",
                "Both thrombotic and bleeding risks need consideration",
                "Your preferences and quality of life are important factors"
            ]
        else:  # high risk
            specific_points = [
                "Your high DASH score indicates significant recurrence risk",
                "Continued anticoagulation is likely beneficial",
                "Modern anticoagulants have improved safety profiles",
                "Regular monitoring can help minimize bleeding risk"
            ]
        
        return general_points + specific_points
    
    def _get_follow_up_recommendations(self, risk_category):
        """Get follow-up recommendations based on risk category"""
        
        if risk_category == "low":
            return {
                "frequency": "3 and 6 months after discontinuation, then as needed",
                "components": [
                    "Clinical assessment for VTE symptoms",
                    "Review of new risk factors",
                    "Patient education reinforcement",
                    "Consider imaging if symptoms develop"
                ]
            }
        elif risk_category == "intermediate":
            return {
                "frequency": "Every 3-6 months",
                "components": [
                    "Risk-benefit reassessment",
                    "Bleeding risk evaluation if on anticoagulation",
                    "Patient preference and quality of life assessment",
                    "Review of new evidence and guidelines"
                ]
            }
        else:  # high risk
            return {
                "frequency": "Every 3-6 months initially, then annually",
                "components": [
                    "Bleeding assessment and monitoring",
                    "Anticoagulation effectiveness evaluation",
                    "Risk factor modification",
                    "Long-term anticoagulation planning"
                ]
            }
    
    def _get_interpretation(self, risk_category, dash_score, risk_details):
        """Get comprehensive interpretation of DASH assessment"""
        
        base_interpretation = (f"DASH score of {dash_score} indicates {risk_details['label']} "
                             f"with {risk_details['annual_risk']} annual VTE recurrence risk "
                             f"(95% CI {risk_details['confidence_interval']}).")
        
        if risk_category == "low":
            return (f"{base_interpretation} The low recurrence risk justifies discontinuing "
                   f"anticoagulation after 3-6 months of treatment, assuming bleeding risk is not elevated.")
        
        elif risk_category == "intermediate":
            return (f"{base_interpretation} The moderate recurrence risk suggests need for "
                   f"individualized decision-making, carefully weighing thrombotic risk against "
                   f"bleeding risk and considering patient preferences.")
        
        else:  # high risk
            return (f"{base_interpretation} The high recurrence risk warrants strong consideration "
                   f"for prolonged or indefinite anticoagulation if bleeding risk is acceptable.")


def calculate_dash_prediction_score(d_dimer_positive: str, age: int, sex: str, hormonal_therapy: str,
                                  vte_type: Optional[str] = None, 
                                  anticoagulation_duration: Optional[int] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DashPredictionScoreCalculator()
    return calculator.calculate(d_dimer_positive, age, sex, hormonal_therapy, 
                              vte_type, anticoagulation_duration)