"""
VTE-BLEED Score Calculator

Assesses bleeding risk on anticoagulation therapy in patients with venous thromboembolism.

References:
1. Klok FA, Hösel V, Clemens A, et al. Prediction of bleeding events in patients with 
   venous thromboembolism on stable anticoagulation treatment. Eur Respir J. 
   2016;48(5):1369-1376. doi: 10.1183/13993003.00280-2016
2. Barco S, Klok FA, Mahé I, et al. Impact of sex, age, and risk factors for venous 
   thromboembolism on the risk of major bleeding in patients with acute venous 
   thromboembolism. Circulation. 2020;141(1):8-17. doi: 10.1161/CIRCULATIONAHA.119.042716
"""

from typing import Dict, Any


class VteBleedScoreCalculator:
    """Calculator for VTE-BLEED Score"""
    
    def __init__(self):
        # VTE-BLEED Score criteria and their point values
        self.CRITERIA_POINTS = {
            "age_60_or_older": 1.5,
            "active_cancer": 2.0,
            "male_uncontrolled_hypertension": 1.0,
            "anemia": 1.5,
            "history_of_bleeding": 1.5,
            "renal_dysfunction": 1.5
        }
        
        # Risk thresholds
        self.LOW_RISK_THRESHOLD = 2.0
    
    def calculate(self, age_60_or_older: str, active_cancer: str, 
                 male_uncontrolled_hypertension: str, anemia: str,
                 history_of_bleeding: str, renal_dysfunction: str) -> Dict[str, Any]:
        """
        Calculates the VTE-BLEED Score for bleeding risk assessment
        
        Args:
            age_60_or_older (str): Patient age 60 years or older ("yes"/"no")
            active_cancer (str): Active cancer present ("yes"/"no")
            male_uncontrolled_hypertension (str): Male with uncontrolled hypertension ("yes"/"no")
            anemia (str): Anemia present ("yes"/"no")
            history_of_bleeding (str): History of major bleeding ("yes"/"no")
            renal_dysfunction (str): Renal dysfunction (CrCl 30-60 mL/min) ("yes"/"no")
            
        Returns:
            Dict with the VTE-BLEED score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_60_or_older, active_cancer, male_uncontrolled_hypertension,
            anemia, history_of_bleeding, renal_dysfunction
        )
        
        # Calculate score
        parameters = {
            "age_60_or_older": age_60_or_older,
            "active_cancer": active_cancer,
            "male_uncontrolled_hypertension": male_uncontrolled_hypertension,
            "anemia": anemia,
            "history_of_bleeding": history_of_bleeding,
            "renal_dysfunction": renal_dysfunction
        }
        
        total_score = self._calculate_total_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        # Generate component breakdown
        component_breakdown = self._generate_component_breakdown(parameters, total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"],
            "component_breakdown": component_breakdown
        }
    
    def _validate_inputs(self, *args):
        """Validates all input parameters"""
        
        valid_responses = ["yes", "no"]
        
        for i, arg in enumerate(args):
            if not isinstance(arg, str):
                raise ValueError(f"Parameter {i+1} must be a string")
            
            if arg.lower() not in valid_responses:
                raise ValueError(f"Parameter {i+1} must be 'yes' or 'no'")
    
    def _calculate_total_score(self, parameters: Dict[str, str]) -> float:
        """
        Calculates the total VTE-BLEED score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            
        Returns:
            float: Total VTE-BLEED score
        """
        
        total_score = 0.0
        
        for parameter, value in parameters.items():
            if value.lower() == "yes":
                total_score += self.CRITERIA_POINTS[parameter]
        
        return total_score
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the VTE-BLEED score
        
        Args:
            score (float): Calculated VTE-BLEED score
            
        Returns:
            Dict with interpretation details
        """
        
        if score < self.LOW_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "stage_description": "Low bleeding risk on anticoagulation",
                "interpretation": f"VTE-BLEED score of {score} indicates low bleeding risk. Continue standard "
                               f"anticoagulation therapy with routine monitoring. The benefits of anticoagulation "
                               f"typically outweigh bleeding risks in this population. Maintain standard follow-up "
                               f"intervals and provide patient education about bleeding precautions. Consider "
                               f"extended anticoagulation duration as clinically indicated for VTE prevention."
            }
        else:
            return {
                "stage": "Elevated Risk",
                "stage_description": "Elevated bleeding risk on anticoagulation",
                "interpretation": f"VTE-BLEED score of {score} indicates elevated bleeding risk. Consider more "
                               f"frequent monitoring with enhanced surveillance for bleeding complications. "
                               f"Evaluate for careful medication selection, potential dose adjustments, and "
                               f"shorter anticoagulation duration when clinically appropriate. Implement enhanced "
                               f"bleeding precautions and comprehensive patient education. Perform individual "
                               f"risk-benefit assessment for extended anticoagulation therapy."
            }
    
    def _generate_component_breakdown(self, parameters: Dict[str, str], total_score: float) -> Dict[str, Any]:
        """
        Generates detailed component breakdown of the VTE-BLEED score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            total_score (float): Total calculated score
            
        Returns:
            Dict with component breakdown
        """
        
        component_scores = {}
        positive_criteria = []
        risk_factors_present = []
        
        for parameter, value in parameters.items():
            points = self.CRITERIA_POINTS[parameter] if value.lower() == "yes" else 0.0
            component_scores[parameter] = {
                "present": value.lower() == "yes",
                "points": points
            }
            
            if value.lower() == "yes":
                criterion_name = parameter.replace("_", " ").title()
                positive_criteria.append({
                    "criterion": criterion_name,
                    "points": self.CRITERIA_POINTS[parameter]
                })
                risk_factors_present.append(criterion_name)
        
        # Determine highest risk factors
        high_risk_factors = [
            criteria for criteria in positive_criteria 
            if criteria["points"] >= 1.5
        ]
        
        # Clinical recommendations based on score
        recommendations = self._get_clinical_recommendations(total_score, risk_factors_present)
        
        return {
            "total_score": total_score,
            "risk_category": "Low Risk" if total_score < self.LOW_RISK_THRESHOLD else "Elevated Risk",
            "positive_criteria_count": len(positive_criteria),
            "positive_criteria": positive_criteria,
            "component_scores": component_scores,
            "high_risk_factors": high_risk_factors,
            "risk_factors_present": risk_factors_present,
            "clinical_recommendations": recommendations,
            "score_validation": {
                "designed_for": "VTE patients on stable anticoagulation after 30 days",
                "validated_for": "Direct oral anticoagulants and vitamin K antagonists",
                "prediction_focus": "Major bleeding events, intracranial bleeding, fatal bleeding"
            }
        }
    
    def _get_clinical_recommendations(self, score: float, risk_factors: list) -> list:
        """
        Generates clinical recommendations based on VTE-BLEED score and risk factors
        
        Args:
            score (float): VTE-BLEED score
            risk_factors (list): List of present risk factors
            
        Returns:
            list: Clinical recommendations
        """
        
        recommendations = []
        
        if score < self.LOW_RISK_THRESHOLD:
            recommendations.append("Continue standard anticoagulation therapy")
            recommendations.append("Routine monitoring and follow-up intervals")
            recommendations.append("Standard patient education about bleeding precautions")
            if not risk_factors:
                recommendations.append("Consider extended anticoagulation if no contraindications")
        else:
            recommendations.append("Enhanced monitoring with more frequent follow-up")
            recommendations.append("Comprehensive bleeding risk assessment")
            recommendations.append("Consider dose optimization or alternative anticoagulants")
            
            # Specific recommendations based on risk factors
            if "Active Cancer" in risk_factors:
                recommendations.append("Coordinate with oncology for bleeding risk management")
                recommendations.append("Monitor for cancer-related bleeding complications")
            
            if "History Of Bleeding" in risk_factors:
                recommendations.append("Review previous bleeding episodes and triggers")
                recommendations.append("Implement strict bleeding precautions")
            
            if "Renal Dysfunction" in risk_factors:
                recommendations.append("Monitor renal function and adjust dosing accordingly")
                recommendations.append("Consider nephrology consultation")
            
            if "Anemia" in risk_factors:
                recommendations.append("Investigate and treat underlying anemia")
                recommendations.append("Monitor hemoglobin levels regularly")
            
            if "Male Uncontrolled Hypertension" in risk_factors:
                recommendations.append("Optimize blood pressure control")
                recommendations.append("Address hypertension management")
            
            recommendations.append("Individual risk-benefit assessment for anticoagulation duration")
            recommendations.append("Enhanced patient education about bleeding warning signs")
        
        return recommendations


def calculate_vte_bleed_score(age_60_or_older, active_cancer, male_uncontrolled_hypertension,
                             anemia, history_of_bleeding, renal_dysfunction) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_vte_bleed_score pattern
    """
    calculator = VteBleedScoreCalculator()
    return calculator.calculate(
        age_60_or_older, active_cancer, male_uncontrolled_hypertension,
        anemia, history_of_bleeding, renal_dysfunction
    )