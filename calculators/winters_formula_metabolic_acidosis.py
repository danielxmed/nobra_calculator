"""
Winters' Formula for Metabolic Acidosis Compensation Calculator

Calculates the expected arterial pCO₂ compensation in pure metabolic acidosis.

References:
1. Winters RW, Engel K, Dell RB. Acid-base physiology in medicine. 
   A self-instruction program. London, UK: The London Company; 1967.
2. Adrogué HJ, Madias NE. Secondary responses to altered acid-base status: 
   the rules of engagement. J Am Soc Nephrol. 2010;21(6):920-923. 
   doi: 10.1681/ASN.2009121211
3. Berend K, de Vries AP, Gans RO. Physiological approach to assessment of 
   acid-base disturbances. N Engl J Med. 2014;371(15):1434-1445. 
   doi: 10.1056/NEJMra1003327
"""

import math
from typing import Dict, Any, Optional


class WintersFormulaMetabolicAcidosisCalculator:
    """Calculator for Winters' Formula for Metabolic Acidosis Compensation"""
    
    def __init__(self):
        # Formula constants
        self.BICARBONATE_COEFFICIENT = 1.5
        self.CONSTANT_OFFSET = 8
        self.TOLERANCE_RANGE = 2  # ± 2 mmHg
        
        # Normal reference ranges
        self.NORMAL_BICARBONATE_MIN = 22  # mEq/L
        self.NORMAL_BICARBONATE_MAX = 28  # mEq/L
        self.NORMAL_PCO2_MIN = 35  # mmHg
        self.NORMAL_PCO2_MAX = 45  # mmHg
        
        # Clinical thresholds
        self.SEVERE_ACIDOSIS_THRESHOLD = 10  # mEq/L bicarbonate
        self.METABOLIC_ACIDOSIS_BICARBONATE_MAX = 21  # mEq/L
    
    def calculate(self, bicarbonate: float, measured_pco2: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates the expected pCO₂ using Winters' Formula
        
        Args:
            bicarbonate (float): Serum bicarbonate concentration in mEq/L
            measured_pco2 (Optional[float]): Measured arterial pCO₂ in mmHg (optional)
            
        Returns:
            Dict with the expected pCO₂ and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bicarbonate, measured_pco2)
        
        # Calculate expected pCO₂ using Winters' Formula
        expected_pco2 = self._calculate_expected_pco2(bicarbonate)
        
        # Calculate compensation ranges
        compensation_analysis = self._analyze_compensation(expected_pco2, measured_pco2)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(bicarbonate, expected_pco2, measured_pco2, compensation_analysis)
        
        # Generate detailed assessment
        detailed_assessment = self._generate_detailed_assessment(bicarbonate, expected_pco2, measured_pco2, compensation_analysis)
        
        return {
            "result": round(expected_pco2, 1),
            "unit": "mmHg",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["stage_description"],
            "expected_range": {
                "lower": round(expected_pco2 - self.TOLERANCE_RANGE, 1),
                "upper": round(expected_pco2 + self.TOLERANCE_RANGE, 1)
            },
            "compensation_analysis": compensation_analysis,
            "detailed_assessment": detailed_assessment
        }
    
    def _validate_inputs(self, bicarbonate: float, measured_pco2: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(bicarbonate, (int, float)):
            raise ValueError("Bicarbonate must be a number")
        
        if bicarbonate < 5 or bicarbonate > 35:
            raise ValueError("Bicarbonate must be between 5 and 35 mEq/L")
        
        if measured_pco2 is not None:
            if not isinstance(measured_pco2, (int, float)):
                raise ValueError("Measured pCO₂ must be a number")
            
            if measured_pco2 < 10 or measured_pco2 > 80:
                raise ValueError("Measured pCO₂ must be between 10 and 80 mmHg")
    
    def _calculate_expected_pco2(self, bicarbonate: float) -> float:
        """
        Calculates expected pCO₂ using Winters' Formula
        
        Formula: Expected pCO₂ = 1.5 × [HCO₃⁻] + 8 (± 2)
        
        Args:
            bicarbonate (float): Serum bicarbonate concentration
            
        Returns:
            float: Expected pCO₂ in mmHg
        """
        
        expected_pco2 = (self.BICARBONATE_COEFFICIENT * bicarbonate) + self.CONSTANT_OFFSET
        
        return expected_pco2
    
    def _analyze_compensation(self, expected_pco2: float, measured_pco2: Optional[float]) -> Dict[str, Any]:
        """
        Analyzes respiratory compensation adequacy
        
        Args:
            expected_pco2 (float): Expected pCO₂ from Winters' Formula
            measured_pco2 (Optional[float]): Measured arterial pCO₂
            
        Returns:
            Dict with compensation analysis
        """
        
        analysis = {
            "expected_pco2": round(expected_pco2, 1),
            "expected_range_lower": round(expected_pco2 - self.TOLERANCE_RANGE, 1),
            "expected_range_upper": round(expected_pco2 + self.TOLERANCE_RANGE, 1),
            "tolerance": self.TOLERANCE_RANGE
        }
        
        if measured_pco2 is not None:
            difference = measured_pco2 - expected_pco2
            analysis.update({
                "measured_pco2": measured_pco2,
                "difference": round(difference, 1),
                "within_expected_range": abs(difference) <= self.TOLERANCE_RANGE
            })
            
            # Classify compensation adequacy
            if difference < -self.TOLERANCE_RANGE:
                analysis["compensation_status"] = "overcompensation"
                analysis["compensation_description"] = "Respiratory overcompensation"
            elif difference > self.TOLERANCE_RANGE:
                analysis["compensation_status"] = "undercompensation"
                analysis["compensation_description"] = "Inadequate respiratory compensation"
            else:
                analysis["compensation_status"] = "appropriate"
                analysis["compensation_description"] = "Appropriate respiratory compensation"
        else:
            analysis.update({
                "measured_pco2": None,
                "difference": None,
                "within_expected_range": None,
                "compensation_status": "not_assessed",
                "compensation_description": "No measured pCO₂ provided for comparison"
            })
        
        return analysis
    
    def _get_interpretation(self, bicarbonate: float, expected_pco2: float, 
                          measured_pco2: Optional[float], compensation_analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines the clinical interpretation based on the calculation
        
        Args:
            bicarbonate (float): Serum bicarbonate concentration
            expected_pco2 (float): Expected pCO₂
            measured_pco2 (Optional[float]): Measured pCO₂
            compensation_analysis (Dict): Compensation analysis results
            
        Returns:
            Dict with interpretation details
        """
        
        if measured_pco2 is None:
            return {
                "stage": "Expected Compensation",
                "stage_description": "Calculated expected respiratory compensation",
                "interpretation": f"For a serum bicarbonate of {bicarbonate} mEq/L, the expected arterial pCO₂ "
                               f"should be {expected_pco2:.1f} mmHg (range: {expected_pco2-self.TOLERANCE_RANGE:.1f}-"
                               f"{expected_pco2+self.TOLERANCE_RANGE:.1f} mmHg) if respiratory compensation is appropriate. "
                               f"Obtain arterial blood gas to measure actual pCO₂ and assess compensation adequacy. "
                               f"Ensure this represents pure metabolic acidosis before applying Winters' Formula."
            }
        
        difference = measured_pco2 - expected_pco2
        
        if difference < -self.TOLERANCE_RANGE:
            return {
                "stage": "Overcompensation",
                "stage_description": "Respiratory overcompensation",
                "interpretation": f"The measured pCO₂ ({measured_pco2} mmHg) is {abs(difference):.1f} mmHg lower than "
                               f"expected ({expected_pco2:.1f} mmHg), suggesting respiratory overcompensation. This may "
                               f"indicate a concurrent primary respiratory alkalosis or mixed acid-base disorder. "
                               f"Consider evaluating for additional respiratory pathology or hyperventilation syndrome. "
                               f"Review clinical context and consider arterial pH to confirm acid-base status."
            }
        elif difference > self.TOLERANCE_RANGE:
            return {
                "stage": "Undercompensation", 
                "stage_description": "Inadequate respiratory compensation",
                "interpretation": f"The measured pCO₂ ({measured_pco2} mmHg) is {difference:.1f} mmHg higher than "
                               f"expected ({expected_pco2:.1f} mmHg), suggesting inadequate respiratory compensation. "
                               f"This may indicate respiratory impairment, fatigue, or a concurrent primary respiratory "
                               f"acidosis. Evaluate respiratory function and consider mechanical ventilation if severe. "
                               f"Assess for mixed acid-base disorder and treat underlying causes."
            }
        else:
            return {
                "stage": "Appropriate Compensation",
                "stage_description": "Expected respiratory compensation", 
                "interpretation": f"The measured pCO₂ ({measured_pco2} mmHg) is within the expected range "
                               f"({expected_pco2-self.TOLERANCE_RANGE:.1f}-{expected_pco2+self.TOLERANCE_RANGE:.1f} mmHg) "
                               f"for metabolic acidosis, indicating appropriate respiratory compensation. Focus on "
                               f"identifying and treating the underlying cause of metabolic acidosis. Monitor clinical "
                               f"response and repeat arterial blood gas as clinically indicated."
            }
    
    def _generate_detailed_assessment(self, bicarbonate: float, expected_pco2: float, 
                                    measured_pco2: Optional[float], compensation_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates detailed clinical assessment and recommendations
        
        Args:
            bicarbonate (float): Serum bicarbonate concentration
            expected_pco2 (float): Expected pCO₂
            measured_pco2 (Optional[float]): Measured pCO₂  
            compensation_analysis (Dict): Compensation analysis results
            
        Returns:
            Dict with detailed assessment
        """
        
        assessment = {
            "bicarbonate_status": self._assess_bicarbonate_status(bicarbonate),
            "severity_assessment": self._assess_acidosis_severity(bicarbonate),
            "formula_applicability": self._assess_formula_applicability(bicarbonate),
            "clinical_recommendations": self._get_clinical_recommendations(bicarbonate, measured_pco2, compensation_analysis),
            "monitoring_recommendations": self._get_monitoring_recommendations(bicarbonate, compensation_analysis),
            "differential_considerations": self._get_differential_considerations(bicarbonate, compensation_analysis)
        }
        
        return assessment
    
    def _assess_bicarbonate_status(self, bicarbonate: float) -> Dict[str, Any]:
        """Assesses bicarbonate status relative to normal range"""
        
        if bicarbonate >= self.NORMAL_BICARBONATE_MIN:
            status = "normal_or_high"
            description = "Normal or elevated bicarbonate"
            clinical_note = "Bicarbonate is not consistent with metabolic acidosis"
        elif bicarbonate > self.METABOLIC_ACIDOSIS_BICARBONATE_MAX:
            status = "mild_reduction"
            description = "Mild bicarbonate reduction"
            clinical_note = "Borderline low bicarbonate - confirm metabolic acidosis with pH"
        else:
            status = "metabolic_acidosis"
            description = "Bicarbonate consistent with metabolic acidosis"
            clinical_note = "Bicarbonate confirms metabolic acidosis"
        
        return {
            "value": bicarbonate,
            "normal_range": f"{self.NORMAL_BICARBONATE_MIN}-{self.NORMAL_BICARBONATE_MAX} mEq/L",
            "status": status,
            "description": description,
            "clinical_note": clinical_note
        }
    
    def _assess_acidosis_severity(self, bicarbonate: float) -> Dict[str, str]:
        """Assesses severity of metabolic acidosis based on bicarbonate level"""
        
        if bicarbonate >= 18:
            return {
                "severity": "mild",
                "description": "Mild metabolic acidosis",
                "clinical_significance": "Generally well-tolerated, investigate underlying cause"
            }
        elif bicarbonate >= 12:
            return {
                "severity": "moderate",
                "description": "Moderate metabolic acidosis", 
                "clinical_significance": "May require treatment, monitor closely"
            }
        elif bicarbonate >= self.SEVERE_ACIDOSIS_THRESHOLD:
            return {
                "severity": "severe",
                "description": "Severe metabolic acidosis",
                "clinical_significance": "Requires immediate evaluation and treatment"
            }
        else:
            return {
                "severity": "life_threatening",
                "description": "Life-threatening metabolic acidosis",
                "clinical_significance": "Critical condition requiring urgent intervention"
            }
    
    def _assess_formula_applicability(self, bicarbonate: float) -> Dict[str, Any]:
        """Assesses appropriateness of using Winters' Formula"""
        
        applicable = True
        limitations = []
        
        if bicarbonate < self.SEVERE_ACIDOSIS_THRESHOLD:
            limitations.append("Formula may be less accurate in severe acidosis (bicarbonate <10 mEq/L)")
        
        if bicarbonate >= self.NORMAL_BICARBONATE_MIN:
            applicable = False
            limitations.append("Formula not applicable - bicarbonate not consistent with metabolic acidosis")
        
        return {
            "applicable": applicable,
            "limitations": limitations,
            "requirements": [
                "Pure metabolic acidosis (not mixed disorder)",
                "Steady-state conditions (6-24 hours after onset)",
                "pH <7.35 to confirm acidosis",
                "No concurrent primary respiratory disorder"
            ]
        }
    
    def _get_clinical_recommendations(self, bicarbonate: float, measured_pco2: Optional[float], 
                                   compensation_analysis: Dict[str, Any]) -> list:
        """Generates clinical recommendations based on results"""
        
        recommendations = []
        
        # General recommendations
        recommendations.append("Obtain arterial blood gas for pH and accurate pCO₂ measurement")
        recommendations.append("Calculate anion gap to determine acidosis type")
        recommendations.append("Identify and treat underlying cause of metabolic acidosis")
        
        # Severity-based recommendations
        if bicarbonate < self.SEVERE_ACIDOSIS_THRESHOLD:
            recommendations.append("Consider bicarbonate therapy for severe acidosis")
            recommendations.append("Monitor for complications of severe acidosis")
        
        # Compensation-specific recommendations
        if measured_pco2 is not None:
            if compensation_analysis["compensation_status"] == "overcompensation":
                recommendations.append("Evaluate for concurrent respiratory alkalosis")
                recommendations.append("Assess for hyperventilation or respiratory pathology")
            elif compensation_analysis["compensation_status"] == "undercompensation":
                recommendations.append("Assess respiratory function and adequacy")
                recommendations.append("Consider mechanical ventilation if respiratory failure")
        
        recommendations.append("Monitor electrolytes, renal function, and lactate")
        recommendations.append("Repeat arterial blood gas in 2-4 hours or as clinically indicated")
        
        return recommendations
    
    def _get_monitoring_recommendations(self, bicarbonate: float, compensation_analysis: Dict[str, Any]) -> list:
        """Generates monitoring recommendations"""
        
        monitoring = [
            "Serial arterial blood gases every 2-4 hours initially",
            "Basic metabolic panel every 6-8 hours",
            "Continuous cardiac monitoring if severe acidosis",
            "Urine output and fluid balance",
            "Mental status and neurological examination"
        ]
        
        if bicarbonate < 12:
            monitoring.extend([
                "Intensive care unit monitoring",
                "Frequent vital signs (every 15-30 minutes)",
                "Consider invasive monitoring if unstable"
            ])
        
        return monitoring
    
    def _get_differential_considerations(self, bicarbonate: float, compensation_analysis: Dict[str, Any]) -> list:
        """Generates differential diagnosis considerations"""
        
        considerations = [
            "High anion gap metabolic acidosis (diabetic ketoacidosis, lactic acidosis, toxins)",
            "Normal anion gap metabolic acidosis (diarrhea, renal tubular acidosis, ureteral diversions)",
            "Mixed acid-base disorders",
            "Respiratory acidosis or alkalosis"
        ]
        
        if measured_pco2 := compensation_analysis.get("measured_pco2"):
            if compensation_analysis["compensation_status"] == "overcompensation":
                considerations.extend([
                    "Primary respiratory alkalosis with metabolic acidosis",
                    "Hyperventilation syndrome",
                    "Pulmonary embolism or pneumonia"
                ])
            elif compensation_analysis["compensation_status"] == "undercompensation":
                considerations.extend([
                    "Primary respiratory acidosis with metabolic acidosis", 
                    "Respiratory muscle fatigue",
                    "Pulmonary edema or pneumonia",
                    "Neuromuscular disorders affecting respiration"
                ])
        
        return considerations


def calculate_winters_formula_metabolic_acidosis(bicarbonate, measured_pco2=None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_winters_formula_metabolic_acidosis pattern
    """
    calculator = WintersFormulaMetabolicAcidosisCalculator()
    return calculator.calculate(bicarbonate, measured_pco2)