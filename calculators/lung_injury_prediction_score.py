"""
Lung Injury Prediction Score (LIPS) Calculator

Identifies patients at high risk for developing acute lung injury (ALI) using
predisposing conditions, high-risk procedures, and risk modifiers.

References:
1. Gajic O, Dabbagh O, Park PK, Adesanya A, Chang SY, Hou P, et al. Early identification 
   of patients at risk of acute lung injury: evaluation of lung injury prediction score 
   in a multicenter cohort study. Am J Respir Crit Care Med. 2011 Feb 15;183(4):462-70.
2. Kor DJ, Warner DO, Alsara A, Fernández-Pérez ER, Malinchoc M, Kashyap R, et al. 
   Derivation and diagnostic accuracy of the surgical lung injury prediction model. 
   Anesthesiology. 2011 Jul;115(1):117-28.
"""

from typing import Dict, Any


class LungInjuryPredictionScoreCalculator:
    """Calculator for Lung Injury Prediction Score (LIPS)"""
    
    def __init__(self):
        # Predisposing conditions scores
        self.PREDISPOSING_CONDITIONS = {
            "shock": 2.0,
            "aspiration": 2.0,
            "sepsis": 1.0,
            "pneumonia": 1.5,
            "pancreatitis": 1.0
        }
        
        # High-risk surgery scores
        self.HIGH_RISK_SURGERY = {
            "none": 0.0,
            "orthopedic_spine": 1.0,
            "acute_abdomen": 2.0,
            "cardiac": 2.5,
            "aortic_vascular": 3.5,
            "emergency_surgery": 1.5
        }
        
        # High-risk trauma scores
        self.HIGH_RISK_TRAUMA = {
            "none": 0.0,
            "traumatic_brain_injury": 2.0,
            "smoke_inhalation": 2.0,
            "near_drowning": 2.0,
            "lung_contusion": 1.5,
            "multiple_fractures": 1.5
        }
        
        # Risk modifiers scores
        self.RISK_MODIFIERS = {
            "alcohol_abuse": 1.0,
            "obesity": 1.0,
            "hypoalbuminemia": 1.0,
            "chemotherapy": 1.0,
            "fio2_over_35": 2.0,
            "tachypnea": 1.5,
            "spo2_under_95": 1.0,
            "acidosis": 1.5,
            "diabetes_with_sepsis": -1.0  # Protective factor if sepsis present
        }
        
        # Risk threshold
        self.HIGH_RISK_THRESHOLD = 4.0
        
        # Prevention strategies by risk level
        self.PREVENTION_STRATEGIES = {
            "low_risk": {
                "monitoring": "Standard clinical monitoring",
                "ventilation": "Standard ventilation practices if required",
                "fluid_management": "Standard fluid management",
                "interventions": "Routine care with continued risk assessment"
            },
            "high_risk": {
                "monitoring": "Close SpO₂ monitoring and frequent assessment",
                "ventilation": "Lung-protective ventilation (low tidal volume 6-8 mL/kg PBW, PEEP 5-10 cmH₂O)",
                "fluid_management": "Conservative IV fluid strategy, avoid fluid overload",
                "interventions": "Minimize high FiO₂, avoid unnecessary procedures, treat underlying conditions"
            }
        }
    
    def calculate(self, shock: str, aspiration: str, sepsis: str, pneumonia: str, 
                 pancreatitis: str, high_risk_surgery: str, high_risk_trauma: str,
                 alcohol_abuse: str, obesity: str, hypoalbuminemia: str, 
                 chemotherapy: str, fio2_over_35: str, tachypnea: str,
                 spo2_under_95: str, acidosis: str, diabetes_with_sepsis: str) -> Dict[str, Any]:
        """
        Calculates LIPS score using predisposing conditions and risk factors
        
        Args:
            shock (str): Shock requiring vasopressors (yes/no)
            aspiration (str): Aspiration witnessed or suspected (yes/no)
            sepsis (str): Sepsis present (yes/no)
            pneumonia (str): Pneumonia present (yes/no)
            pancreatitis (str): Pancreatitis present (yes/no)
            high_risk_surgery (str): Type of high-risk surgery
            high_risk_trauma (str): Type of high-risk trauma
            alcohol_abuse (str): Alcohol abuse present (yes/no)
            obesity (str): BMI >30 kg/m² (yes/no)
            hypoalbuminemia (str): Albumin <3.5 g/dL (yes/no)
            chemotherapy (str): Recent chemotherapy (yes/no)
            fio2_over_35 (str): FiO₂ >35% (yes/no)
            tachypnea (str): Respiratory rate >30/min (yes/no)
            spo2_under_95 (str): SpO₂ <95% (yes/no)
            acidosis (str): pH <7.35 (yes/no)
            diabetes_with_sepsis (str): Diabetes mellitus (protective if sepsis) (yes/no)
            
        Returns:
            Dict with LIPS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(shock, aspiration, sepsis, pneumonia, pancreatitis,
                            high_risk_surgery, high_risk_trauma, alcohol_abuse,
                            obesity, hypoalbuminemia, chemotherapy, fio2_over_35,
                            tachypnea, spo2_under_95, acidosis, diabetes_with_sepsis)
        
        # Calculate component scores
        predisposing_score = self._calculate_predisposing_score(
            shock, aspiration, sepsis, pneumonia, pancreatitis
        )
        surgery_score = self.HIGH_RISK_SURGERY[high_risk_surgery]
        trauma_score = self.HIGH_RISK_TRAUMA[high_risk_trauma]
        modifiers_score = self._calculate_risk_modifiers_score(
            alcohol_abuse, obesity, hypoalbuminemia, chemotherapy, fio2_over_35,
            tachypnea, spo2_under_95, acidosis, diabetes_with_sepsis, sepsis
        )
        
        # Calculate total LIPS score
        total_score = predisposing_score + surgery_score + trauma_score + modifiers_score
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(
            total_score, predisposing_score, surgery_score, trauma_score, modifiers_score
        )
        
        return {
            "result": round(total_score, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        # Validate predisposing conditions (first 5 parameters)
        predisposing_params = ["shock", "aspiration", "sepsis", "pneumonia", "pancreatitis"]
        for i, param_name in enumerate(predisposing_params):
            if args[i] not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
        
        # Validate surgery parameter (index 5)
        high_risk_surgery = args[5]
        if high_risk_surgery not in self.HIGH_RISK_SURGERY:
            valid_options = list(self.HIGH_RISK_SURGERY.keys())
            raise ValueError(f"High-risk surgery must be one of: {valid_options}")
        
        # Validate trauma parameter (index 6)
        high_risk_trauma = args[6]
        if high_risk_trauma not in self.HIGH_RISK_TRAUMA:
            valid_options = list(self.HIGH_RISK_TRAUMA.keys())
            raise ValueError(f"High-risk trauma must be one of: {valid_options}")
        
        # Validate risk modifier parameters (indices 7-15)
        risk_modifier_params = [
            "alcohol_abuse", "obesity", "hypoalbuminemia", "chemotherapy",
            "fio2_over_35", "tachypnea", "spo2_under_95", "acidosis", "diabetes_with_sepsis"
        ]
        for i, param_name in enumerate(risk_modifier_params):
            param_index = i + 7  # Start from index 7
            if args[param_index] not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_predisposing_score(self, shock, aspiration, sepsis, pneumonia, pancreatitis):
        """Calculate predisposing conditions score"""
        score = 0.0
        
        conditions = {
            "shock": shock,
            "aspiration": aspiration, 
            "sepsis": sepsis,
            "pneumonia": pneumonia,
            "pancreatitis": pancreatitis
        }
        
        for condition, present in conditions.items():
            if present == "yes":
                score += self.PREDISPOSING_CONDITIONS[condition]
        
        return score
    
    def _calculate_risk_modifiers_score(self, alcohol_abuse, obesity, hypoalbuminemia,
                                      chemotherapy, fio2_over_35, tachypnea,
                                      spo2_under_95, acidosis, diabetes_with_sepsis, sepsis):
        """Calculate risk modifiers score"""
        score = 0.0
        
        modifiers = {
            "alcohol_abuse": alcohol_abuse,
            "obesity": obesity,
            "hypoalbuminemia": hypoalbuminemia,
            "chemotherapy": chemotherapy,
            "fio2_over_35": fio2_over_35,
            "tachypnea": tachypnea,
            "spo2_under_95": spo2_under_95,
            "acidosis": acidosis
        }
        
        for modifier, present in modifiers.items():
            if present == "yes":
                score += self.RISK_MODIFIERS[modifier]
        
        # Diabetes is protective only if sepsis is present
        if diabetes_with_sepsis == "yes" and sepsis == "yes":
            score += self.RISK_MODIFIERS["diabetes_with_sepsis"]
        
        return score
    
    def _get_interpretation(self, total_score: float, predisposing_score: float,
                          surgery_score: float, trauma_score: float, modifiers_score: float) -> Dict[str, str]:
        """
        Provides comprehensive clinical interpretation and prevention strategies
        """
        
        # Determine risk category
        if total_score <= self.HIGH_RISK_THRESHOLD:
            risk_category = "low_risk"
            stage = "Low Risk"
            stage_description = "Low risk for acute lung injury"
            ali_probability = "<10%"
        else:
            risk_category = "high_risk"
            stage = "High Risk"
            stage_description = "High risk for acute lung injury"
            ali_probability = "15-25%"
        
        strategies = self.PREVENTION_STRATEGIES[risk_category]
        
        # Build detailed interpretation
        interpretation = (
            f"Lung Injury Prediction Score (LIPS) Assessment:\\n\\n"
            f"Component Scores:\\n"
            f"• Predisposing conditions: {predisposing_score} points\\n"
            f"• High-risk surgery: {surgery_score} points\\n"
            f"• High-risk trauma: {trauma_score} points\\n"
            f"• Risk modifiers: {modifiers_score} points\\n"
            f"• Total LIPS score: {total_score}/20+ points\\n\\n"
            f"Risk Assessment:\\n"
            f"• Risk category: {stage}\\n"
            f"• Probability of ALI development: {ali_probability}\\n"
            f"• Typical time to ALI development: 2 days (median)\\n\\n"
            f"Prevention Strategies:\\n"
            f"• Monitoring: {strategies['monitoring']}\\n"
            f"• Ventilation: {strategies['ventilation']}\\n"
            f"• Fluid management: {strategies['fluid_management']}\\n"
            f"• Interventions: {strategies['interventions']}\\n\\n"
        )
        
        # Add risk-specific clinical guidance
        if risk_category == "low_risk":
            interpretation += (
                f"Low Risk Management (Score ≤4):\\n"
                f"• Continue standard clinical monitoring and care\\n"
                f"• Reassess LIPS score if clinical condition changes\\n"
                f"• ALI development unlikely but maintain clinical vigilance\\n"
                f"• Standard ventilation practices if mechanical ventilation required\\n"
                f"• Normal fluid management protocols appropriate\\n"
                f"• Continue treatment of underlying conditions\\n\\n"
            )
        else:  # high risk
            interpretation += (
                f"High Risk Management (Score >4):\\n"
                f"• Implement lung-protective ventilation strategies:\\n"
                f"  - Low tidal volume (6-8 mL/kg predicted body weight)\\n"
                f"  - PEEP 5-10 cmH₂O to maintain adequate oxygenation\\n"
                f"  - Plateau pressure <30 cmH₂O\\n"
                f"  - FiO₂ as low as possible to maintain SpO₂ >88%\\n"
                f"• Conservative fluid management strategy:\\n"
                f"  - Avoid fluid overload\\n"
                f"  - Use colloids judiciously\\n"
                f"  - Monitor fluid balance closely\\n"
                f"• Additional preventive measures:\\n"
                f"  - Minimize blood transfusions\\n"
                f"  - Avoid high driving pressures\\n"
                f"  - Treat underlying infections aggressively\\n"
                f"  - Consider prone positioning if ARDS develops\\n\\n"
            )
        
        # Add general considerations
        interpretation += (
            f"Clinical Considerations:\\n"
            f"• LIPS should be calculated within 24 hours of admission or ICU transfer\\n"
            f"• Score aids in risk stratification but does not replace clinical judgment\\n"
            f"• ALI frequency varies by predisposing condition (3% pancreatitis to 26% smoke inhalation)\\n"
            f"• Useful for identifying patients for ALI prevention trials\\n"
            f"• Consider early involvement of critical care and pulmonary specialists for high-risk patients\\n"
            f"• Monitor for early signs of ALI: bilateral infiltrates, PaO₂/FiO₂ ratio <300\\n\\n"
            f"LIPS Performance Characteristics:\\n"
            f"• Sensitivity: 69% for ALI development\\n"
            f"• Specificity: 78% for ALI development\\n"
            f"• Positive likelihood ratio: 3.1\\n"
            f"• Negative likelihood ratio: 0.4\\n"
            f"• Area under ROC curve: 0.84 (95% CI 0.80-0.89)\\n\\n"
            f"Key Risk Factors Contributing Most Points:\\n"
            f"• Aortic vascular surgery: 3.5 points\\n"
            f"• Cardiac surgery: 2.5 points\\n"
            f"• Shock, aspiration, smoke inhalation, TBI, near drowning: 2.0 points each\\n"
            f"• High FiO₂ requirement: 2.0 points\\n"
            f"• Note: Diabetes is protective in presence of sepsis (-1 point)"
        )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_lung_injury_prediction_score(shock: str, aspiration: str, sepsis: str, 
                                         pneumonia: str, pancreatitis: str, 
                                         high_risk_surgery: str, high_risk_trauma: str,
                                         alcohol_abuse: str, obesity: str, 
                                         hypoalbuminemia: str, chemotherapy: str,
                                         fio2_over_35: str, tachypnea: str,
                                         spo2_under_95: str, acidosis: str,
                                         diabetes_with_sepsis: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_lung_injury_prediction_score pattern
    """
    calculator = LungInjuryPredictionScoreCalculator()
    return calculator.calculate(shock, aspiration, sepsis, pneumonia, pancreatitis,
                              high_risk_surgery, high_risk_trauma, alcohol_abuse,
                              obesity, hypoalbuminemia, chemotherapy, fio2_over_35,
                              tachypnea, spo2_under_95, acidosis, diabetes_with_sepsis)