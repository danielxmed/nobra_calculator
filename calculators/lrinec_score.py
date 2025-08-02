"""
LRINEC Score for Necrotizing Soft Tissue Infection Calculator

Laboratory Risk Indicator for Necrotizing Fasciitis to distinguish necrotizing 
fasciitis from other soft tissue infections using routine laboratory parameters.

References:
1. Wong CH, Khin LW, Heng KS, Tan KC, Low CO. The LRINEC (Laboratory Risk Indicator 
   for Necrotizing Fasciitis) score: a tool for distinguishing necrotizing fasciitis 
   from other soft tissue infections. Crit Care Med. 2004 Jul;32(7):1535-41.
2. Bechar J, Sepehripour S, Hardwicke J, Filobbos G. Laboratory risk indicator for 
   necrotising fasciitis (LRINEC) score for the assessment of early necrotising fasciitis: 
   a systematic review of the literature. Ann R Coll Surg Engl. 2017 Jun;99(5):341-346.
"""

from typing import Dict, Any


class LrinecScoreCalculator:
    """Calculator for LRINEC Score for Necrotizing Soft Tissue Infection"""
    
    def __init__(self):
        # Scoring thresholds for each parameter
        self.CRP_THRESHOLD = 150.0  # mg/L
        self.WBC_LOW_THRESHOLD = 15000  # cells/µL
        self.WBC_HIGH_THRESHOLD = 25000  # cells/µL
        self.HEMOGLOBIN_LOW_THRESHOLD = 11.0  # g/dL
        self.HEMOGLOBIN_MID_THRESHOLD = 13.5  # g/dL
        self.SODIUM_THRESHOLD = 135.0  # mEq/L
        self.CREATININE_THRESHOLD = 1.6  # mg/dL
        self.GLUCOSE_THRESHOLD = 180.0  # mg/dL
        
        # Risk category thresholds
        self.LOW_RISK_THRESHOLD = 5
        self.MODERATE_RISK_THRESHOLD = 7
        
        # Clinical recommendations by risk category
        self.RISK_RECOMMENDATIONS = {
            "low": {
                "probability": "<50%",
                "management": "Continue standard soft tissue infection management with close monitoring",
                "surgical_consultation": "Not routinely required unless clinical suspicion remains high",
                "monitoring": "Serial reassessment and monitoring for clinical deterioration"
            },
            "moderate": {
                "probability": "50-75%",
                "management": "Urgent evaluation for necrotizing fasciitis",
                "surgical_consultation": "Consider urgent surgical consultation",
                "monitoring": "Close monitoring with frequent reassessment"
            },
            "high": {
                "probability": ">75%",
                "management": "Immediate operative intervention strongly recommended",
                "surgical_consultation": "Urgent surgical consultation required",
                "monitoring": "Continuous monitoring in appropriate care setting"
            }
        }
    
    def calculate(self, crp: float, wbc: float, hemoglobin: float, 
                 sodium: float, creatinine: float, glucose: float) -> Dict[str, Any]:
        """
        Calculates LRINEC score using laboratory parameters
        
        Args:
            crp (float): C-Reactive Protein in mg/L
            wbc (float): White Blood Cell count in cells/µL
            hemoglobin (float): Hemoglobin in g/dL
            sodium (float): Serum sodium in mEq/L
            creatinine (float): Serum creatinine in mg/dL
            glucose (float): Serum glucose in mg/dL
            
        Returns:
            Dict with LRINEC score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(crp, wbc, hemoglobin, sodium, creatinine, glucose)
        
        # Calculate component scores
        crp_score = self._calculate_crp_score(crp)
        wbc_score = self._calculate_wbc_score(wbc)
        hemoglobin_score = self._calculate_hemoglobin_score(hemoglobin)
        sodium_score = self._calculate_sodium_score(sodium)
        creatinine_score = self._calculate_creatinine_score(creatinine)
        glucose_score = self._calculate_glucose_score(glucose)
        
        # Calculate total LRINEC score
        total_score = (crp_score + wbc_score + hemoglobin_score + 
                      sodium_score + creatinine_score + glucose_score)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(
            total_score, crp_score, wbc_score, hemoglobin_score,
            sodium_score, creatinine_score, glucose_score
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"]
        }
    
    def _validate_inputs(self, crp, wbc, hemoglobin, sodium, creatinine, glucose):
        """Validates input parameters"""
        
        if not isinstance(crp, (int, float)) or crp < 0:
            raise ValueError("C-Reactive Protein must be a positive number")
        
        if not isinstance(wbc, (int, float)) or wbc < 0:
            raise ValueError("White Blood Cell count must be a positive number")
        
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 0:
            raise ValueError("Hemoglobin must be a positive number")
        
        if not isinstance(sodium, (int, float)) or sodium < 100 or sodium > 180:
            raise ValueError("Sodium must be between 100-180 mEq/L")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0:
            raise ValueError("Creatinine must be a positive number")
        
        if not isinstance(glucose, (int, float)) or glucose < 0:
            raise ValueError("Glucose must be a positive number")
    
    def _calculate_crp_score(self, crp: float) -> int:
        """Calculate CRP component score"""
        return 4 if crp >= self.CRP_THRESHOLD else 0
    
    def _calculate_wbc_score(self, wbc: float) -> int:
        """Calculate WBC component score"""
        if wbc > self.WBC_HIGH_THRESHOLD:
            return 2
        elif wbc >= self.WBC_LOW_THRESHOLD:
            return 1
        else:
            return 0
    
    def _calculate_hemoglobin_score(self, hemoglobin: float) -> int:
        """Calculate hemoglobin component score"""
        if hemoglobin < self.HEMOGLOBIN_LOW_THRESHOLD:
            return 2
        elif hemoglobin <= self.HEMOGLOBIN_MID_THRESHOLD:
            return 1
        else:
            return 0
    
    def _calculate_sodium_score(self, sodium: float) -> int:
        """Calculate sodium component score"""
        return 2 if sodium < self.SODIUM_THRESHOLD else 0
    
    def _calculate_creatinine_score(self, creatinine: float) -> int:
        """Calculate creatinine component score"""
        return 2 if creatinine > self.CREATININE_THRESHOLD else 0
    
    def _calculate_glucose_score(self, glucose: float) -> int:
        """Calculate glucose component score"""
        return 1 if glucose > self.GLUCOSE_THRESHOLD else 0
    
    def _get_interpretation(self, total_score: int, crp_score: int, wbc_score: int,
                          hemoglobin_score: int, sodium_score: int, 
                          creatinine_score: int, glucose_score: int) -> Dict[str, str]:
        """
        Provides comprehensive clinical interpretation and management recommendations
        """
        
        # Determine risk category
        if total_score <= self.LOW_RISK_THRESHOLD:
            risk_category = "low"
            stage = "Low Risk"
            stage_description = "Necrotizing fasciitis unlikely"
        elif total_score <= self.MODERATE_RISK_THRESHOLD:
            risk_category = "moderate"
            stage = "Moderate Risk"
            stage_description = "Intermediate probability"
        else:
            risk_category = "high"
            stage = "High Risk"
            stage_description = "Necrotizing fasciitis likely"
        
        recommendations = self.RISK_RECOMMENDATIONS[risk_category]
        
        # Build detailed interpretation
        interpretation = (
            f"LRINEC Score Assessment for Necrotizing Soft Tissue Infection:\\n\\n"
            f"Component Scores:\\n"
            f"• C-Reactive Protein: {crp_score} point{'s' if crp_score != 1 else ''}\\n"
            f"• White Blood Cell count: {wbc_score} point{'s' if wbc_score != 1 else ''}\\n"
            f"• Hemoglobin: {hemoglobin_score} point{'s' if hemoglobin_score != 1 else ''}\\n"
            f"• Sodium: {sodium_score} point{'s' if sodium_score != 1 else ''}\\n"
            f"• Creatinine: {creatinine_score} point{'s' if creatinine_score != 1 else ''}\\n"
            f"• Glucose: {glucose_score} point{'s' if glucose_score != 1 else ''}\\n"
            f"• Total LRINEC score: {total_score}/13 points\\n\\n"
            f"Risk Assessment:\\n"
            f"• Risk category: {stage}\\n"
            f"• Probability of necrotizing fasciitis: {recommendations['probability']}\\n\\n"
            f"Clinical Management:\\n"
            f"• Recommended management: {recommendations['management']}\\n"
            f"• Surgical consultation: {recommendations['surgical_consultation']}\\n"
            f"• Monitoring: {recommendations['monitoring']}\\n\\n"
        )
        
        # Add risk-specific clinical guidance
        if risk_category == "low":
            interpretation += (
                f"Low Risk Management (Score ≤5):\\n"
                f"• Continue standard antibiotic therapy for soft tissue infection\\n"
                f"• Monitor for clinical improvement within 24-48 hours\\n"
                f"• IMPORTANT: 10% of patients with necrotizing fasciitis had scores <6\\n"
                f"• Maintain high clinical suspicion if patient deteriorates\\n"
                f"• Consider repeat scoring if clinical condition worsens\\n"
                f"• Patient may be managed in general medical ward with appropriate monitoring\\n\\n"
            )
        elif risk_category == "moderate":
            interpretation += (
                f"Moderate Risk Management (Score 6-7):\\n"
                f"• Urgent surgical evaluation recommended\\n"
                f"• Consider empirical broad-spectrum antibiotics\\n"
                f"• Close monitoring for signs of systemic toxicity\\n"
                f"• Serial physical examinations for progression\\n"
                f"• May require ICU-level monitoring\\n"
                f"• Prepare for potential operative intervention\\n\\n"
            )
        else:  # high risk
            interpretation += (
                f"High Risk Management (Score ≥8):\\n"
                f"• URGENT surgical consultation and operative intervention\\n"
                f"• Immediate broad-spectrum antibiotics (e.g., vancomycin + piperacillin/tazobactam + clindamycin)\\n"
                f"• ICU-level care for hemodynamic support\\n"
                f"• Aggressive fluid resuscitation as needed\\n"
                f"• Consider hyperbaric oxygen therapy if available\\n"
                f"• Serial debridements may be necessary\\n"
                f"• Multidisciplinary team approach (surgery, critical care, infectious disease)\\n\\n"
            )
        
        # Add general considerations
        interpretation += (
            f"Important Clinical Considerations:\\n"
            f"• LRINEC score should supplement, not replace, clinical judgment\\n"
            f"• High clinical suspicion warrants surgical consultation regardless of score\\n"
            f"• Score has not been prospectively validated in original development\\n"
            f"• Performance may vary in different patient populations\\n"
            f"• Early recognition and treatment are crucial for optimal outcomes\\n"
            f"• Classic signs (pain out of proportion, skin changes) may be absent early\\n"
            f"• Consider patient risk factors: diabetes, immunocompromised state, trauma\\n\\n"
            f"Laboratory Scoring Criteria Reference:\\n"
            f"• CRP ≥150 mg/L: 4 points\\n"
            f"• WBC >25,000/µL: 2 points, 15,000-25,000/µL: 1 point\\n"
            f"• Hemoglobin <11 g/dL: 2 points, 11-13.5 g/dL: 1 point\\n"
            f"• Sodium <135 mEq/L: 2 points\\n"
            f"• Creatinine >1.6 mg/dL: 2 points\\n"
            f"• Glucose >180 mg/dL: 1 point\\n\\n"
            f"Original Study Performance:\\n"
            f"• PPV: 92% for scores >6\\n"
            f"• NPV: 96% for scores >6\\n"
            f"• NOTE: Subsequent validation studies show variable performance"
        )
        
        return {
            "stage": stage,
            "stage_description": stage_description,
            "interpretation": interpretation
        }


def calculate_lrinec_score(crp: float, wbc: float, hemoglobin: float,
                          sodium: float, creatinine: float, glucose: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_lrinec_score pattern
    """
    calculator = LrinecScoreCalculator()
    return calculator.calculate(crp, wbc, hemoglobin, sodium, creatinine, glucose)