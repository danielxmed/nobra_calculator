"""
MACOCHA Score Calculator

Predicts difficult intubation in ICU patients using patient-related,
pathology-related, and operator-related factors.

References:
1. De Jong A, Molinari N, Terzi N, Mongardon N, Arnal JM, Guitton C, et al. 
   Early identification of patients at risk for difficult intubation in the 
   intensive care unit: development and validation of the MACOCHA score in a 
   multicenter cohort study. Am J Respir Crit Care Med. 2013 Apr 15;187(8):832-9.
2. De Jong A, Clavieras N, Conseil M, Coisel Y, Moury PH, Pouzeratte Y, et al. 
   Implementation of a combo videolaryngoscope for intubation in critically ill 
   patients: a before-after comparative study. Intensive Care Med. 2013 Dec;39(12):2144-52.
"""

from typing import Dict, Any


class MacochaScoreCalculator:
    """Calculator for MACOCHA Score"""
    
    def __init__(self):
        # MACOCHA Score parameters
        self.SCORE_FACTORS = {
            "mallampati_3_or_4": 5,          # Patient-related
            "obstructive_sleep_apnea": 2,    # Patient-related
            "reduced_cervical_mobility": 1,   # Patient-related
            "limited_mouth_opening": 1,       # Patient-related
            "coma": 1,                       # Pathology-related
            "severe_hypoxemia": 1,           # Pathology-related
            "non_anesthesiologist": 1        # Operator-related
        }
        
        # Risk thresholds
        self.LOW_RISK_THRESHOLD = 2
        self.INTERMEDIATE_RISK_THRESHOLD = 5
        
        # Equipment and preparation recommendations by risk level
        self.PREPARATION_RECOMMENDATIONS = {
            "low_risk": {
                "preparation": "Standard intubation preparation",
                "equipment": "Standard laryngoscope, endotracheal tubes, bag-mask ventilation",
                "personnel": "Standard medical team",
                "backup_plan": "Standard backup airway management"
            },
            "intermediate_risk": {
                "preparation": "Enhanced preparation with additional equipment",
                "equipment": "Video laryngoscope, supraglottic airway devices, fiberoptic bronchoscope availability",
                "personnel": "Experienced intubator, additional skilled assistant",
                "backup_plan": "Supraglottic airway device, consider awake fiberoptic intubation"
            },
            "high_risk": {
                "preparation": "Comprehensive difficult airway preparation",
                "equipment": "Video laryngoscope, fiberoptic bronchoscope, supraglottic airways, surgical airway kit",
                "personnel": "Most experienced available intubator, anesthesiologist if available, surgical backup",
                "backup_plan": "Immediate surgical airway capability, consider awake fiberoptic intubation"
            }
        }
    
    def calculate(self, mallampati_3_or_4: str, obstructive_sleep_apnea: str, 
                 reduced_cervical_mobility: str, limited_mouth_opening: str,
                 coma: str, severe_hypoxemia: str, non_anesthesiologist: str) -> Dict[str, Any]:
        """
        Calculates MACOCHA score for difficult intubation prediction
        
        Args:
            mallampati_3_or_4 (str): Mallampati score III or IV (yes/no)
            obstructive_sleep_apnea (str): Obstructive sleep apnea syndrome (yes/no)
            reduced_cervical_mobility (str): Reduced cervical spine mobility (yes/no)
            limited_mouth_opening (str): Limited mouth opening <3 cm (yes/no)
            coma (str): Coma present (yes/no)
            severe_hypoxemia (str): Severe hypoxemia SpO₂ <80% (yes/no)
            non_anesthesiologist (str): Non-anesthesiologist operator (yes/no)
            
        Returns:
            Dict with MACOCHA score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(mallampati_3_or_4, obstructive_sleep_apnea, 
                            reduced_cervical_mobility, limited_mouth_opening,
                            coma, severe_hypoxemia, non_anesthesiologist)
        
        # Calculate component scores
        patient_factors_score = self._calculate_patient_factors(
            mallampati_3_or_4, obstructive_sleep_apnea, 
            reduced_cervical_mobility, limited_mouth_opening
        )
        pathology_factors_score = self._calculate_pathology_factors(coma, severe_hypoxemia)
        operator_factors_score = self._calculate_operator_factors(non_anesthesiologist)
        
        # Calculate total MACOCHA score
        total_score = patient_factors_score + pathology_factors_score + operator_factors_score
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(
            total_score, patient_factors_score, pathology_factors_score, operator_factors_score
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        param_names = [
            "mallampati_3_or_4", "obstructive_sleep_apnea", "reduced_cervical_mobility",
            "limited_mouth_opening", "coma", "severe_hypoxemia", "non_anesthesiologist"
        ]
        
        # Validate all parameters are yes/no
        for i, param_name in enumerate(param_names):
            if args[i] not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_patient_factors(self, mallampati_3_or_4, obstructive_sleep_apnea,
                                 reduced_cervical_mobility, limited_mouth_opening):
        """Calculate patient-related factors score"""
        score = 0
        
        patient_factors = {
            "mallampati_3_or_4": mallampati_3_or_4,
            "obstructive_sleep_apnea": obstructive_sleep_apnea,
            "reduced_cervical_mobility": reduced_cervical_mobility,
            "limited_mouth_opening": limited_mouth_opening
        }
        
        for factor, present in patient_factors.items():
            if present == "yes":
                score += self.SCORE_FACTORS[factor]
        
        return score
    
    def _calculate_pathology_factors(self, coma, severe_hypoxemia):
        """Calculate pathology-related factors score"""
        score = 0
        
        pathology_factors = {
            "coma": coma,
            "severe_hypoxemia": severe_hypoxemia
        }
        
        for factor, present in pathology_factors.items():
            if present == "yes":
                score += self.SCORE_FACTORS[factor]
        
        return score
    
    def _calculate_operator_factors(self, non_anesthesiologist):
        """Calculate operator-related factors score"""
        score = 0
        
        if non_anesthesiologist == "yes":
            score += self.SCORE_FACTORS["non_anesthesiologist"]
        
        return score
    
    def _get_interpretation(self, total_score: int, patient_score: int, 
                          pathology_score: int, operator_score: int) -> Dict[str, str]:
        """
        Provides comprehensive clinical interpretation and preparation recommendations
        """
        
        # Determine risk category
        if total_score <= self.LOW_RISK_THRESHOLD:
            risk_category = "low_risk"
            stage = "Low Risk"
            stage_description = "Low risk for difficult intubation"
            difficulty_probability = "<10%"
        elif total_score <= self.INTERMEDIATE_RISK_THRESHOLD:
            risk_category = "intermediate_risk"
            stage = "Intermediate Risk"
            stage_description = "Intermediate risk for difficult intubation"
            difficulty_probability = "10-30%"
        else:
            risk_category = "high_risk"
            stage = "High Risk"
            stage_description = "High risk for difficult intubation"
            difficulty_probability = ">30%"
        
        recommendations = self.PREPARATION_RECOMMENDATIONS[risk_category]
        
        # Build detailed interpretation
        interpretation = (
            f"MACOCHA Score Assessment:\\n\\n"
            f"Component Scores:\\n"
            f"• Patient-related factors: {patient_score} points\\n"
            f"• Pathology-related factors: {pathology_score} points\\n"
            f"• Operator-related factors: {operator_score} points\\n"
            f"• Total MACOCHA score: {total_score}/12 points\\n\\n"
            f"Risk Assessment:\\n"
            f"• Risk category: {stage}\\n"
            f"• Probability of difficult intubation: {difficulty_probability}\\n"
            f"• Negative predictive value: 98% (if score ≤2)\\n\\n"
            f"Preparation Recommendations:\\n"
            f"• Preparation level: {recommendations['preparation']}\\n"
            f"• Required equipment: {recommendations['equipment']}\\n"
            f"• Personnel requirements: {recommendations['personnel']}\\n"
            f"• Backup plan: {recommendations['backup_plan']}\\n\\n"
        )
        
        # Add risk-specific clinical guidance
        if risk_category == "low_risk":
            interpretation += (
                f"Low Risk Management (Score ≤2):\\n"
                f"• Standard intubation protocols and equipment appropriate\\n"
                f"• Routine preparation with standard laryngoscope and ETT\\n"
                f"• Standard medical team sufficient for intubation\\n"
                f"• Difficult intubation very unlikely (NPV 98%)\\n"
                f"• Continue with planned intubation approach\\n"
                f"• Monitor for unexpected complications\\n\\n"
            )
        elif risk_category == "intermediate_risk":
            interpretation += (
                f"Intermediate Risk Management (Score 3-5):\\n"
                f"• Enhanced preparation with additional equipment ready\\n"
                f"• Consider video laryngoscopy as first-line approach\\n"
                f"• Have supraglottic airway device immediately available\\n"
                f"• Ensure experienced intubator performs procedure\\n"
                f"• Pre-oxygenate thoroughly and optimize positioning\\n"
                f"• Consider awake fiberoptic intubation if high suspicion\\n"
                f"• Have backup airway plan clearly defined\\n\\n"
            )
        else:  # high risk
            interpretation += (
                f"High Risk Management (Score ≥6):\\n"
                f"• Comprehensive difficult airway preparation mandatory\\n"
                f"• Video laryngoscopy recommended as first-line technique\\n"
                f"• Fiberoptic bronchoscope immediately available\\n"
                f"• Consider awake fiberoptic intubation strongly\\n"
                f"• Surgical airway capability must be immediately available\\n"
                f"• Most experienced available operator should perform procedure\\n"
                f"• Anesthesiologist consultation if available\\n"
                f"• Multiple backup plans prepared and communicated\\n"
                f"• Consider postponing non-emergent intubation for optimization\\n\\n"
            )
        
        # Add general considerations
        interpretation += (
            f"Clinical Considerations:\\n"
            f"• MACOCHA score should be calculated before all ICU intubations\\n"
            f"• Score helps predict complications: difficult intubation associated with 51% vs 36% severe complications\\n"
            f"• Mallampati III/IV is the strongest predictor (5 points)\\n"
            f"• Consider patient positioning, pre-oxygenation, and hemodynamic optimization\\n"
            f"• Video laryngoscopy improves success rates in ICU setting\\n"
            f"• Have rescue medications (epinephrine, atropine) immediately available\\n\\n"
            f"MACOCHA Performance Characteristics:\\n"
            f"• Area under curve: 0.89 (development), 0.86 (validation)\\n"
            f"• Sensitivity: 73% for difficult intubation\\n"
            f"• Specificity: 89% for difficult intubation\\n"
            f"• Negative predictive value: 98% (excellent for ruling out)\\n"
            f"• Positive predictive value: 36%\\n\\n"
            f"Factor Contributions:\\n"
            f"• Mallampati III/IV: 5 points (strongest predictor)\\n"
            f"• Obstructive sleep apnea: 2 points\\n"
            f"• All other factors: 1 point each\\n"
            f"• Maximum possible score: 12 points\\n"
            f"• Score validated in >1,000 ICU intubations from 42 centers"
        )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_macocha_score(mallampati_3_or_4: str, obstructive_sleep_apnea: str,
                           reduced_cervical_mobility: str, limited_mouth_opening: str,
                           coma: str, severe_hypoxemia: str, non_anesthesiologist: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_macocha_score pattern
    """
    calculator = MacochaScoreCalculator()
    return calculator.calculate(mallampati_3_or_4, obstructive_sleep_apnea,
                              reduced_cervical_mobility, limited_mouth_opening,
                              coma, severe_hypoxemia, non_anesthesiologist)