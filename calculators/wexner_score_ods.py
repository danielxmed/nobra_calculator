"""
Wexner Score for Obstructed Defecation Syndrome (ODS) Calculator

Stratifies severity of fecal incontinence using the Cleveland Clinic Fecal Incontinence Score.

References:
1. Jorge JM, Wexner SD. Etiology and management of fecal incontinence. 
   Dis Colon Rectum. 1993;36(1):77-97. doi: 10.1007/BF02050307
2. Rockwood TH, Church JM, Fleshman JW, et al. Fecal Incontinence Quality of Life Scale: 
   quality of life instrument for patients with fecal incontinence. Dis Colon Rectum. 
   2000;43(1):9-16. doi: 10.1007/BF02237236
3. Vaizey CJ, Carapeti E, Cahill JA, Kamm MA. Prospective comparison of faecal 
   incontinence grading systems. Gut. 1999;44(1):77-80. doi: 10.1136/gut.44.1.77
"""

from typing import Dict, Any


class WexnerScoreOdsCalculator:
    """Calculator for Wexner Score for Obstructed Defecation Syndrome (ODS)"""
    
    def __init__(self):
        # Frequency scoring scale for all parameters
        self.FREQUENCY_DESCRIPTIONS = {
            0: "Never",
            1: "Less than once a month",
            2: "Less than once a week but at least once a month", 
            3: "Less than once a day but at least once a week",
            4: "At least once a day"
        }
        
        # Clinical significance thresholds
        self.PERFECT_CONTINENCE = 0
        self.CLINICAL_INCONTINENCE_THRESHOLD = 10
        self.MAX_SCORE = 20
    
    def calculate(self, incontinence_solid_stool: int, incontinence_liquid_stool: int,
                 incontinence_gas: int, wears_pad: int, lifestyle_alteration: int) -> Dict[str, Any]:
        """
        Calculates the Wexner Score for fecal incontinence severity
        
        Args:
            incontinence_solid_stool (int): Frequency of solid stool incontinence (0-4)
            incontinence_liquid_stool (int): Frequency of liquid stool incontinence (0-4)
            incontinence_gas (int): Frequency of gas incontinence (0-4)
            wears_pad (int): Frequency of wearing protective pads (0-4)
            lifestyle_alteration (int): Extent of lifestyle alteration (0-4)
            
        Returns:
            Dict with the Wexner score result and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            incontinence_solid_stool, incontinence_liquid_stool, incontinence_gas,
            wears_pad, lifestyle_alteration
        )
        
        # Calculate total score
        parameters = {
            "incontinence_solid_stool": incontinence_solid_stool,
            "incontinence_liquid_stool": incontinence_liquid_stool,
            "incontinence_gas": incontinence_gas,
            "wears_pad": wears_pad,
            "lifestyle_alteration": lifestyle_alteration
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
        
        for i, score in enumerate(args):
            if not isinstance(score, int):
                raise ValueError(f"Parameter {i+1} must be an integer")
            
            if score < 0 or score > 4:
                raise ValueError(f"Parameter {i+1} must be between 0 and 4")
    
    def _calculate_total_score(self, parameters: Dict[str, int]) -> int:
        """
        Calculates the total Wexner score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            
        Returns:
            int: Total Wexner score
        """
        
        return sum(parameters.values())
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the Wexner score
        
        Args:
            score (int): Calculated Wexner score
            
        Returns:
            Dict with interpretation details
        """
        
        if score == self.PERFECT_CONTINENCE:
            return {
                "stage": "Perfect Continence",
                "stage_description": "Perfect continence with no symptoms",
                "interpretation": f"Wexner score of {score} indicates perfect continence with no fecal incontinence "
                               f"symptoms. No treatment is typically required for incontinence. Continue routine "
                               f"care and lifestyle modifications as appropriate for any underlying gastrointestinal "
                               f"conditions. Regular follow-up may be beneficial to monitor for symptom development."
            }
        elif score < self.CLINICAL_INCONTINENCE_THRESHOLD:
            return {
                "stage": "Mild Incontinence",
                "stage_description": "Mild fecal incontinence",
                "interpretation": f"Wexner score of {score} indicates mild fecal incontinence that may have minimal "
                               f"impact on quality of life. Consider conservative management including dietary "
                               f"modifications (fiber supplementation, avoiding trigger foods), pelvic floor "
                               f"exercises, bowel training programs, and behavioral modifications. Monitor symptoms "
                               f"and reassess regularly. Patient education about normal bowel function and "
                               f"lifestyle modifications may be beneficial."
            }
        else:
            return {
                "stage": "Clinical Incontinence",
                "stage_description": "Clinically significant fecal incontinence",
                "interpretation": f"Wexner score of {score} indicates clinically significant fecal incontinence "
                               f"requiring active management. Consider comprehensive evaluation including anorectal "
                               f"physiology testing (manometry, endoanal ultrasound), imaging studies, and "
                               f"gastroenterology or colorectal surgery specialist referral. Treatment options may "
                               f"include advanced conservative therapies, biofeedback training, sacral nerve "
                               f"stimulation, injectable bulking agents, or surgical interventions depending on "
                               f"underlying etiology and patient factors."
            }
    
    def _generate_component_breakdown(self, parameters: Dict[str, int], total_score: int) -> Dict[str, Any]:
        """
        Generates detailed component breakdown of the Wexner score
        
        Args:
            parameters (Dict): Dictionary of all parameters
            total_score (int): Total calculated score
            
        Returns:
            Dict with component breakdown
        """
        
        component_scores = {}
        severity_assessment = {}
        
        # Map parameter names to clinical descriptions
        parameter_descriptions = {
            "incontinence_solid_stool": "Solid Stool Incontinence",
            "incontinence_liquid_stool": "Liquid Stool Incontinence", 
            "incontinence_gas": "Gas Incontinence",
            "wears_pad": "Protective Pad Use",
            "lifestyle_alteration": "Lifestyle Impact"
        }
        
        for parameter, score in parameters.items():
            component_scores[parameter] = {
                "score": score,
                "frequency": self.FREQUENCY_DESCRIPTIONS[score],
                "description": parameter_descriptions[parameter]
            }
            
            # Assess severity for each component
            if score == 0:
                severity = "No symptoms"
            elif score <= 2:
                severity = "Mild symptoms"
            elif score == 3:
                severity = "Moderate symptoms"
            else:
                severity = "Severe symptoms"
            
            severity_assessment[parameter] = severity
        
        # Identify most problematic areas
        most_severe_components = [
            param for param, score in parameters.items() if score >= 3
        ]
        
        # Generate clinical recommendations
        recommendations = self._get_clinical_recommendations(total_score, parameters, most_severe_components)
        
        return {
            "total_score": total_score,
            "severity_category": self._get_severity_category(total_score),
            "component_scores": component_scores,
            "severity_assessment": severity_assessment,
            "most_severe_components": [
                parameter_descriptions[comp] for comp in most_severe_components
            ],
            "clinical_recommendations": recommendations,
            "quality_of_life_impact": self._assess_qol_impact(total_score),
            "score_interpretation": {
                "perfect_continence": total_score == 0,
                "clinical_incontinence": total_score >= self.CLINICAL_INCONTINENCE_THRESHOLD,
                "requires_specialist_referral": total_score >= self.CLINICAL_INCONTINENCE_THRESHOLD,
                "score_range": f"{total_score}/{self.MAX_SCORE}"
            }
        }
    
    def _get_severity_category(self, score: int) -> str:
        """Returns the severity category based on score"""
        if score == 0:
            return "Perfect Continence"
        elif score < self.CLINICAL_INCONTINENCE_THRESHOLD:
            return "Mild Incontinence"
        else:
            return "Clinical Incontinence"
    
    def _assess_qol_impact(self, score: int) -> str:
        """Assesses quality of life impact based on score"""
        if score == 0:
            return "No impact on quality of life"
        elif score <= 5:
            return "Minimal impact on quality of life"
        elif score < self.CLINICAL_INCONTINENCE_THRESHOLD:
            return "Moderate impact on quality of life"
        elif score <= 15:
            return "Significant impact on quality of life"
        else:
            return "Severe impact on quality of life"
    
    def _get_clinical_recommendations(self, score: int, parameters: Dict[str, int], 
                                    severe_components: list) -> list:
        """
        Generates clinical recommendations based on Wexner score and component analysis
        
        Args:
            score (int): Total Wexner score
            parameters (Dict): Individual component scores
            severe_components (list): Components with scores ≥3
            
        Returns:
            list: Clinical recommendations
        """
        
        recommendations = []
        
        if score == 0:
            recommendations.append("No specific treatment required for incontinence")
            recommendations.append("Continue routine gastrointestinal care")
            recommendations.append("Monitor for symptom development")
            
        elif score < self.CLINICAL_INCONTINENCE_THRESHOLD:
            recommendations.append("Conservative management approach")
            recommendations.append("Dietary modifications and fiber supplementation")
            recommendations.append("Pelvic floor exercises and bowel training")
            recommendations.append("Patient education about bowel function")
            
            # Component-specific recommendations
            if parameters["incontinence_gas"] >= 2:
                recommendations.append("Consider dietary triggers for gas incontinence")
            
            if parameters["lifestyle_alteration"] >= 2:
                recommendations.append("Lifestyle counseling and behavioral modifications")
                
        else:
            recommendations.append("Comprehensive gastroenterology evaluation")
            recommendations.append("Anorectal physiology testing (manometry, ultrasound)")
            recommendations.append("Consider specialist referral (colorectal surgery)")
            
            # Advanced treatment options based on severity
            if score >= 15:
                recommendations.append("Consider surgical intervention options")
                recommendations.append("Evaluate for sacral nerve stimulation")
            elif score >= 12:
                recommendations.append("Advanced conservative therapies")
                recommendations.append("Biofeedback training evaluation")
            
            # Component-specific advanced recommendations
            if "incontinence_solid_stool" in severe_components:
                recommendations.append("Evaluate for structural abnormalities")
            
            if "incontinence_liquid_stool" in severe_components:
                recommendations.append("Assess for inflammatory bowel conditions")
            
            if "wears_pad" in severe_components:
                recommendations.append("Assess impact on skin integrity and hygiene")
            
            if "lifestyle_alteration" in severe_components:
                recommendations.append("Psychological support and counseling")
                recommendations.append("Quality of life assessment and support")
        
        return recommendations


def calculate_wexner_score_ods(incontinence_solid_stool, incontinence_liquid_stool,
                              incontinence_gas, wears_pad, lifestyle_alteration) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_wexner_score_ods pattern
    """
    calculator = WexnerScoreOdsCalculator()
    return calculator.calculate(
        incontinence_solid_stool, incontinence_liquid_stool, incontinence_gas,
        wears_pad, lifestyle_alteration
    )