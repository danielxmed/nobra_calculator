"""
Maddrey's Discriminant Function Calculator

Predicts prognosis and steroid benefit in alcoholic hepatitis using
prothrombin time and total bilirubin.

References:
1. Maddrey WC, Boitnott JK, Bedine MS, Weber FL Jr, Mezey E, White RI Jr. 
   Corticosteroid therapy of alcoholic hepatitis. Gastroenterology. 1978 Aug;75(2):193-9.
2. Carithers RL Jr, Herlong HF, Diehl AM, Shaw EW, Combes B, Fallon HJ, Maddrey WC. 
   Methylprednisolone therapy in patients with severe alcoholic hepatitis. A randomized 
   multicenter trial. Ann Intern Med. 1989 May 1;110(9):685-90.
"""

from typing import Dict, Any
import math


class MaddreysDiscriminantFunctionCalculator:
    """Calculator for Maddrey's Discriminant Function"""
    
    def __init__(self):
        # Maddrey's formula coefficient
        self.PT_COEFFICIENT = 4.6
        
        # Severity threshold
        self.SEVERE_THRESHOLD = 32.0
        
        # Typical control PT range (for reference)
        self.TYPICAL_CONTROL_PT_MIN = 11.0
        self.TYPICAL_CONTROL_PT_MAX = 13.0
        
        # Treatment recommendations by severity
        self.TREATMENT_RECOMMENDATIONS = {
            "mild_moderate": {
                "steroid_therapy": "Not recommended",
                "prognosis": "Good (90% 30-day survival without steroids)",
                "monitoring": "Standard supportive care and monitoring",
                "additional_therapy": "Supportive care, nutritional support, alcohol cessation counseling"
            },
            "severe": {
                "steroid_therapy": "Consider corticosteroids if no contraindications",
                "prognosis": "Poor (35-45% mortality risk within first month)",
                "monitoring": "Close monitoring, consider ICU care",
                "additional_therapy": "Prednisolone 40mg daily, nutritional support, infection screening"
            }
        }
        
        # Steroid contraindications
        self.STEROID_CONTRAINDICATIONS = [
            "Active gastrointestinal bleeding",
            "Active infection or sepsis",
            "Acute pancreatitis",
            "Acute renal failure",
            "Hepatorenal syndrome",
            "Psychosis or severe psychiatric illness"
        ]
    
    def calculate(self, patient_pt: float, control_pt: float, total_bilirubin: float) -> Dict[str, Any]:
        """
        Calculates Maddrey's Discriminant Function score
        
        Args:
            patient_pt (float): Patient's prothrombin time in seconds
            control_pt (float): Control/reference prothrombin time in seconds
            total_bilirubin (float): Total bilirubin level in mg/dL
            
        Returns:
            Dict with Maddrey's score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(patient_pt, control_pt, total_bilirubin)
        
        # Calculate PT difference
        pt_difference = patient_pt - control_pt
        
        # Calculate Maddrey's Discriminant Function
        maddrey_score = (self.PT_COEFFICIENT * pt_difference) + total_bilirubin
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(maddrey_score, patient_pt, control_pt, total_bilirubin)
        
        return {
            "result": round(maddrey_score, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, patient_pt: float, control_pt: float, total_bilirubin: float):
        """Validates input parameters"""
        
        # Validate patient PT
        if not isinstance(patient_pt, (int, float)) or patient_pt < 8.0 or patient_pt > 120.0:
            raise ValueError("Patient PT must be a number between 8.0 and 120.0 seconds")
        
        # Validate control PT
        if not isinstance(control_pt, (int, float)) or control_pt < 8.0 or control_pt > 20.0:
            raise ValueError("Control PT must be a number between 8.0 and 20.0 seconds")
        
        # Validate total bilirubin
        if not isinstance(total_bilirubin, (int, float)) or total_bilirubin < 0.1 or total_bilirubin > 50.0:
            raise ValueError("Total bilirubin must be a number between 0.1 and 50.0 mg/dL")
        
        # Logical validation
        if patient_pt < control_pt:
            raise ValueError("Patient PT should typically be equal to or greater than control PT in alcoholic hepatitis")
    
    def _get_interpretation(self, maddrey_score: float, patient_pt: float, 
                          control_pt: float, total_bilirubin: float) -> Dict[str, str]:
        """
        Provides comprehensive clinical interpretation and treatment recommendations
        """
        
        # Determine severity category
        if maddrey_score < self.SEVERE_THRESHOLD:
            severity_category = "mild_moderate"
            stage = "Mild to Moderate"
            stage_description = "Good prognosis, steroid therapy not indicated"
            mortality_risk = "~10% 30-day mortality"
        else:
            severity_category = "severe"
            stage = "Severe"
            stage_description = "Poor prognosis, consider steroid therapy"
            mortality_risk = "35-45% 30-day mortality"
        
        recommendations = self.TREATMENT_RECOMMENDATIONS[severity_category]
        pt_difference = patient_pt - control_pt
        
        # Build detailed interpretation
        interpretation = (
            f"Maddrey's Discriminant Function Assessment:\\n\\n"
            f"Calculation Components:\\n"
            f"• Patient's PT: {patient_pt} seconds\\n"
            f"• Control PT: {control_pt} seconds\\n"
            f"• PT difference: {pt_difference:.1f} seconds\\n"
            f"• Total bilirubin: {total_bilirubin} mg/dL\\n"
            f"• Formula: 4.6 × ({patient_pt} - {control_pt}) + {total_bilirubin}\\n"
            f"• Maddrey's score: {maddrey_score:.1f} points\\n\\n"
            f"Severity Assessment:\\n"
            f"• Classification: {stage} Alcoholic Hepatitis\\n"
            f"• Prognosis: {mortality_risk}\\n"
            f"• Threshold: Score {'<' if maddrey_score < self.SEVERE_THRESHOLD else '≥'} 32 indicates {'mild to moderate' if maddrey_score < self.SEVERE_THRESHOLD else 'severe'} disease\\n\\n"
            f"Treatment Recommendations:\\n"
            f"• Steroid therapy: {recommendations['steroid_therapy']}\\n"
            f"• Prognosis: {recommendations['prognosis']}\\n"
            f"• Monitoring: {recommendations['monitoring']}\\n"
            f"• Additional therapy: {recommendations['additional_therapy']}\\n\\n"
        )
        
        # Add severity-specific clinical guidance
        if severity_category == "mild_moderate":
            interpretation += (
                f"Mild to Moderate Disease Management (Score <32):\\n"
                f"• Excellent prognosis with 90% 30-day survival without steroids\\n"
                f"• Corticosteroid therapy not recommended\\n"
                f"• Focus on supportive care and alcohol cessation\\n"
                f"• Nutritional support with thiamine, folate, multivitamins\\n"
                f"• Monitor for complications and disease progression\\n"
                f"• Outpatient management may be appropriate if stable\\n"
                f"• Alcohol cessation counseling and support programs\\n"
                f"• Follow-up in 1-2 weeks to reassess\\n\\n"
            )
        else:  # severe
            interpretation += (
                f"Severe Disease Management (Score ≥32):\\n"
                f"• High mortality risk requiring aggressive treatment\\n"
                f"• Consider prednisolone 40mg daily for 28 days if no contraindications\\n"
                f"• Screen for steroid contraindications before treatment:\\n"
                f"  - Active GI bleeding, infection, acute pancreatitis\\n"
                f"  - Acute renal failure, hepatorenal syndrome\\n"
                f"  - Severe psychiatric illness\\n"
                f"• Close monitoring in hospital setting, consider ICU care\\n"
                f"• Assess treatment response with Lille score at day 7\\n"
                f"• Nutritional support and infection prophylaxis\\n"
                f"• Consider liver transplant evaluation if appropriate\\n"
                f"• Monitor for steroid complications if treated\\n\\n"
            )
        
        # Add general considerations
        interpretation += (
            f"Clinical Considerations:\\n"
            f"• Maddrey's score is most useful for short-term prognosis (30 days)\\n"
            f"• Should be combined with clinical assessment and other scores\\n"
            f"• Consider MELD score for additional prognostic information\\n"
            f"• Exclude other causes of acute hepatitis before treatment\\n"
            f"• Liver biopsy may be helpful in uncertain cases\\n"
            f"• Monitor for complications: ascites, encephalopathy, bleeding\\n\\n"
            f"Steroid Contraindications to Assess:\\n"
        )
        
        for contraindication in self.STEROID_CONTRAINDICATIONS:
            interpretation += f"• {contraindication}\\n"
        
        interpretation += (
            f"\\nAdditional Assessments:\\n"
            f"• Control PT reference: Typical range {self.TYPICAL_CONTROL_PT_MIN}-{self.TYPICAL_CONTROL_PT_MAX} seconds\\n"
            f"• Consider combining with Lille score for treatment response (day 7)\\n"
            f"• MELD score may provide additional prognostic value\\n"
            f"• Regular monitoring of liver function and complications essential\\n"
            f"• Alcohol cessation is critical for long-term outcomes"
        )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_maddreys_discriminant_function(patient_pt: float, control_pt: float, 
                                           total_bilirubin: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_maddreys_discriminant_function pattern
    """
    calculator = MaddreysDiscriminantFunctionCalculator()
    return calculator.calculate(patient_pt, control_pt, total_bilirubin)