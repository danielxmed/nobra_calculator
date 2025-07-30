"""
Corrected QT Interval (QTc) Calculator

Corrects QT interval for heart rate extremes using multiple validated formulas.

References:
1. Bazett HC. An analysis of the time-relations of electrocardiograms. Heart. 1920;7:353-370.
2. Fridericia LS. Die Systolendauer im Elektrokardiogramm bei normalen Menschen und bei Herzkranken. 
   Acta Med Scand. 1920;53:469-486.
3. Sagie A, Larson MG, Goldberg RJ, Bengtson JR, Levy D. An improved method for adjusting the QT 
   interval for heart rate (the Framingham Heart Study). Am J Cardiol. 1992;70(7):797-801.
4. Hodges M, Salerno D, Erlien D. Bazett's QT correction reviewed. Evidence that a linear QT 
   correction for heart rate is better. J Am Coll Cardiol. 1983;1(2):694.
5. Rautaharju PM, Surawicz B, Gettes LS, et al. AHA/ACCF/HRS recommendations for the 
   standardization and interpretation of the electrocardiogram. J Am Coll Cardiol. 2009;53(11):982-991.
"""

import math
from typing import Dict, Any


class CorrectedQtIntervalCalculator:
    """Calculator for Corrected QT Interval (QTc) using multiple formulas"""
    
    def __init__(self):
        # Available correction formulas
        self.FORMULAS = {
            "bazett": "Bazett",
            "fridericia": "Fridericia", 
            "framingham": "Framingham",
            "hodges": "Hodges",
            "rautaharju": "Rautaharju"
        }
        
        # Clinical interpretation thresholds (in ms)
        self.THRESHOLDS = {
            "severely_short": 320,
            "short": 360,
            "normal_upper": 440,
            "borderline_male": 450,
            "prolonged_male": 460,
            "prolonged": 480,
            "significantly_prolonged": 500
        }
    
    def calculate(
        self,
        qt_interval: int,
        heart_rate: int,
        formula: str
    ) -> Dict[str, Any]:
        """
        Calculates the corrected QT interval using the specified formula
        
        Args:
            qt_interval: QT interval measured on ECG (ms)
            heart_rate: Heart rate measured on ECG (bpm)
            formula: QTc correction formula ("bazett", "fridericia", "framingham", "hodges", "rautaharju")
            
        Returns:
            Dict with QTc value and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(qt_interval, heart_rate, formula)
        
        # Calculate RR interval in seconds
        rr_interval = 60.0 / heart_rate
        
        # Calculate QTc using specified formula
        qtc_value = self._calculate_qtc(qt_interval, heart_rate, rr_interval, formula)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(qtc_value)
        
        # Get formula details
        formula_info = self._get_formula_info(formula, qt_interval, heart_rate, rr_interval)
        
        return {
            "result": round(qtc_value, 1),
            "unit": "ms",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "calculation_details": {
                "formula_used": self.FORMULAS[formula],
                "rr_interval": round(rr_interval, 3),
                "formula_equation": formula_info["equation"],
                "clinical_significance": interpretation["clinical_significance"],
                "risk_level": interpretation["risk_level"]
            }
        }
    
    def _validate_inputs(self, qt_interval: int, heart_rate: int, formula: str):
        """Validates input parameters"""
        
        # Validate QT interval
        if not isinstance(qt_interval, int) or qt_interval < 200 or qt_interval > 800:
            raise ValueError("QT interval must be an integer between 200 and 800 ms")
        
        # Validate heart rate
        if not isinstance(heart_rate, int) or heart_rate < 30 or heart_rate > 300:
            raise ValueError("Heart rate must be an integer between 30 and 300 bpm")
        
        # Validate formula
        if formula not in self.FORMULAS:
            raise ValueError(f"Formula must be one of: {list(self.FORMULAS.keys())}")
    
    def _calculate_qtc(self, qt: int, hr: int, rr: float, formula: str) -> float:
        """
        Calculates QTc using the specified formula
        
        Args:
            qt: QT interval in ms
            hr: Heart rate in bpm
            rr: RR interval in seconds
            formula: Formula name
            
        Returns:
            QTc value in ms
        """
        
        if formula == "bazett":
            # Bazett: QTc = QT / √RR
            return qt / math.sqrt(rr)
            
        elif formula == "fridericia":
            # Fridericia: QTc = QT / (RR)^(1/3)
            return qt / (rr ** (1/3))
            
        elif formula == "framingham":
            # Framingham: QTc = QT + 154 × (1 - RR)
            return qt + 154 * (1 - rr)
            
        elif formula == "hodges":
            # Hodges: QTc = QT + 1.75 × [(60/RR) - 60]
            return qt + 1.75 * ((60/rr) - 60)
            
        elif formula == "rautaharju":
            # Rautaharju: QTc = QT × (120 + HR) / 180
            return qt * (120 + hr) / 180
        
        else:
            raise ValueError(f"Unknown formula: {formula}")
    
    def _get_interpretation(self, qtc_value: float) -> Dict[str, Any]:
        """
        Determines the interpretation based on QTc value
        
        Args:
            qtc_value: Calculated QTc value in ms
            
        Returns:
            Dict with interpretation details
        """
        
        if qtc_value <= self.THRESHOLDS["severely_short"]:
            stage = "Severely Short QT"
            description = "Diagnostic for Short QT Syndrome"
            risk_level = "High"
            clinical_significance = "High risk of sudden cardiac death"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms is ≤320 ms, which is diagnostic for Short QT Syndrome "
                f"and associated with increased risk of sudden cardiac death. Immediate cardiology "
                f"evaluation recommended."
            )
            
        elif qtc_value <= self.THRESHOLDS["short"]:
            stage = "Short QT"
            description = "Suggestive of Short QT Syndrome"
            risk_level = "Moderate"
            clinical_significance = "May suggest Short QT Syndrome"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms (320-360 ms) may suggest Short QT Syndrome when "
                f"combined with additional clinical criteria. Consider genetic testing and "
                f"family history evaluation."
            )
            
        elif qtc_value <= self.THRESHOLDS["normal_upper"]:
            stage = "Normal"
            description = "Normal QTc interval"
            risk_level = "Low"
            clinical_significance = "Normal cardiac repolarization"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms is within normal limits for both men and women. "
                f"No specific cardiac monitoring required."
            )
            
        elif qtc_value <= self.THRESHOLDS["borderline_male"]:
            stage = "Borderline (Male)"
            description = "Borderline prolonged for males"
            risk_level = "Low-Moderate"
            clinical_significance = "Borderline prolongation in males"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms is borderline prolonged for males (440-450 ms). "
                f"Consider clinical context, medications, and monitoring."
            )
            
        elif qtc_value <= self.THRESHOLDS["prolonged_male"]:
            stage = "Prolonged (Male)"
            description = "Prolonged for males, borderline for females"
            risk_level = "Moderate"
            clinical_significance = "Mild prolongation"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms is prolonged for males and borderline for females "
                f"(450-460 ms). Clinical correlation and monitoring recommended."
            )
            
        elif qtc_value <= self.THRESHOLDS["prolonged"]:
            stage = "Prolonged"
            description = "Prolonged QTc interval"
            risk_level = "Moderate-High"
            clinical_significance = "Increased arrhythmic risk"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms is prolonged for both sexes (460-480 ms). "
                f"Increased risk of arrhythmias. Evaluate for reversible causes and consider "
                f"medication review."
            )
            
        elif qtc_value <= self.THRESHOLDS["significantly_prolonged"]:
            stage = "Significantly Prolonged"
            description = "Significantly prolonged QTc"
            risk_level = "High"
            clinical_significance = "Diagnostic for Long QT Syndrome"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms (≥480 ms) is diagnostic for Long QT Syndrome "
                f"regardless of symptoms. High arrhythmic risk requiring specialized evaluation "
                f"and management."
            )
            
        else:  # qtc_value > 500
            stage = "Severely Prolonged"
            description = "Severely prolonged QTc"
            risk_level = "Very High"
            clinical_significance = "Very high risk of torsades de pointes"
            interpretation = (
                f"QTc of {qtc_value:.1f} ms (>500 ms) indicates very high risk of torsades de "
                f"pointes and sudden cardiac death. Immediate cardiology consultation and "
                f"continuous cardiac monitoring recommended."
            )
        
        return {
            "stage": stage,
            "description": description,
            "interpretation": interpretation,
            "risk_level": risk_level,
            "clinical_significance": clinical_significance
        }
    
    def _get_formula_info(self, formula: str, qt: int, hr: int, rr: float) -> Dict[str, str]:
        """
        Provides formula-specific information and equations
        
        Args:
            formula: Formula name
            qt: QT interval
            hr: Heart rate
            rr: RR interval
            
        Returns:
            Dict with formula details
        """
        
        equations = {
            "bazett": f"QTc = {qt} / √{rr:.3f} = {qt} / {math.sqrt(rr):.3f}",
            "fridericia": f"QTc = {qt} / ({rr:.3f})^(1/3) = {qt} / {rr**(1/3):.3f}",
            "framingham": f"QTc = {qt} + 154 × (1 - {rr:.3f}) = {qt} + {154 * (1 - rr):.1f}",
            "hodges": f"QTc = {qt} + 1.75 × [({60}/{rr:.3f}) - 60] = {qt} + {1.75 * ((60/rr) - 60):.1f}",
            "rautaharju": f"QTc = {qt} × (120 + {hr}) / 180 = {qt} × {(120 + hr) / 180:.3f}"
        }
        
        return {
            "equation": equations[formula]
        }


def calculate_corrected_qt_interval(
    qt_interval: int,
    heart_rate: int,
    formula: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CorrectedQtIntervalCalculator()
    return calculator.calculate(
        qt_interval=qt_interval,
        heart_rate=heart_rate,
        formula=formula
    )