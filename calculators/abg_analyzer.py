"""
Arterial Blood Gas (ABG) Analyzer Calculator

Interprets arterial blood gas results to determine acid-base status, 
respiratory compensation, and metabolic derangements.

References:
- Seifter JL. Acid-base disorders. In: Harrison's Principles of Internal Medicine, 20e. McGraw Hill; 2018.
- Berend K, de Vries AP, Gans RO. Physiological approach to assessment of acid-base disturbances. N Engl J Med. 2014;371(15):1434-45.
- MDCalc. Arterial Blood Gas (ABG) Analyzer. Available at: https://www.mdcalc.com/calc/1741/arterial-blood-gas-abg-analyzer
"""

import math
from typing import Dict, Any, Optional


class AbgAnalyzerCalculator:
    """Calculator for Arterial Blood Gas (ABG) Analysis"""
    
    def __init__(self):
        # Normal ranges
        self.NORMAL_PH_MIN = 7.35
        self.NORMAL_PH_MAX = 7.45
        self.NORMAL_PCO2_MIN = 35
        self.NORMAL_PCO2_MAX = 45
        self.NORMAL_HCO3_MIN = 22
        self.NORMAL_HCO3_MAX = 26
        self.NORMAL_PO2_MIN = 80
        self.NORMAL_PO2_MAX = 100
    
    def calculate(self, ph: float, pco2: float, hco3: float, 
                 po2: Optional[float] = None, fio2: Optional[float] = None) -> Dict[str, Any]:
        """
        Analyzes arterial blood gas values
        
        Args:
            ph (float): Arterial blood pH value (6.8-7.8)
            pco2 (float): Partial pressure of CO2 in mmHg (10-100)
            hco3 (float): Bicarbonate concentration in mEq/L (5-50)
            po2 (Optional[float]): Partial pressure of O2 in mmHg (30-600)
            fio2 (Optional[float]): Fraction of inspired oxygen (0.21-1.0)
            
        Returns:
            Dict with the analysis result and interpretation
        """
        
        # Validations
        self._validate_inputs(ph, pco2, hco3, po2, fio2)
        
        # Perform ABG analysis
        analysis = self._analyze_abg(ph, pco2, hco3)
        
        # Add oxygenation assessment if available
        if po2 is not None:
            oxygenation = self._assess_oxygenation(po2, fio2)
            analysis["oxygenation"] = oxygenation
        
        # Generate complete interpretation
        interpretation = self._generate_interpretation(analysis)
        
        return {
            "result": analysis["primary_disorder"],
            "unit": "",
            "interpretation": interpretation,
            "stage": analysis["category"],
            "stage_description": analysis["description"],
            "detailed_analysis": analysis
        }
    
    def _validate_inputs(self, ph: float, pco2: float, hco3: float, 
                        po2: Optional[float], fio2: Optional[float]):
        """Validates input parameters"""
        
        if not isinstance(ph, (int, float)) or ph < 6.8 or ph > 7.8:
            raise ValueError("pH must be between 6.8 and 7.8")
        
        if not isinstance(pco2, (int, float)) or pco2 < 10 or pco2 > 100:
            raise ValueError("PCO2 must be between 10 and 100 mmHg")
        
        if not isinstance(hco3, (int, float)) or hco3 < 5 or hco3 > 50:
            raise ValueError("HCO3 must be between 5 and 50 mEq/L")
        
        if po2 is not None:
            if not isinstance(po2, (int, float)) or po2 < 30 or po2 > 600:
                raise ValueError("PO2 must be between 30 and 600 mmHg")
        
        if fio2 is not None:
            if not isinstance(fio2, (int, float)) or fio2 < 0.21 or fio2 > 1.0:
                raise ValueError("FiO2 must be between 0.21 and 1.0")
    
    def _analyze_abg(self, ph: float, pco2: float, hco3: float) -> Dict[str, Any]:
        """Performs the main ABG analysis"""
        
        analysis = {
            "ph": ph,
            "pco2": pco2,
            "hco3": hco3,
            "ph_status": self._assess_ph(ph),
            "primary_disorder": "",
            "compensation": "",
            "category": "",
            "description": ""
        }
        
        # Determine primary disorder
        if ph < self.NORMAL_PH_MIN:  # Acidemia
            if hco3 < self.NORMAL_HCO3_MIN:  # Low HCO3
                analysis["primary_disorder"] = "Metabolic Acidosis"
                analysis["category"] = "Metabolic Acidosis"
                analysis["description"] = "Primary metabolic acidosis"
                analysis["compensation"] = self._assess_respiratory_compensation_acidosis(pco2, hco3)
            elif pco2 > self.NORMAL_PCO2_MAX:  # High PCO2
                analysis["primary_disorder"] = "Respiratory Acidosis"
                analysis["category"] = "Respiratory Acidosis"
                analysis["description"] = "Primary respiratory acidosis"
                analysis["compensation"] = self._assess_metabolic_compensation_resp_acidosis(hco3, pco2)
            else:
                analysis["primary_disorder"] = "Mixed Acid-Base Disorder"
                analysis["category"] = "Mixed Disorder"
                analysis["description"] = "Complex acid-base disturbance"
                analysis["compensation"] = "Mixed disorder present"
                
        elif ph > self.NORMAL_PH_MAX:  # Alkalemia
            if hco3 > self.NORMAL_HCO3_MAX:  # High HCO3
                analysis["primary_disorder"] = "Metabolic Alkalosis"
                analysis["category"] = "Metabolic Alkalosis"
                analysis["description"] = "Primary metabolic alkalosis"
                analysis["compensation"] = self._assess_respiratory_compensation_alkalosis(pco2, hco3)
            elif pco2 < self.NORMAL_PCO2_MIN:  # Low PCO2
                analysis["primary_disorder"] = "Respiratory Alkalosis"
                analysis["category"] = "Respiratory Alkalosis"
                analysis["description"] = "Primary respiratory alkalosis"
                analysis["compensation"] = self._assess_metabolic_compensation_resp_alkalosis(hco3, pco2)
            else:
                analysis["primary_disorder"] = "Mixed Acid-Base Disorder"
                analysis["category"] = "Mixed Disorder"
                analysis["description"] = "Complex acid-base disturbance"
                analysis["compensation"] = "Mixed disorder present"
                
        else:  # Normal pH
            analysis["primary_disorder"] = "Normal pH"
            analysis["category"] = "Normal pH"
            analysis["description"] = "pH within normal range"
            
            # Check for compensated disorders
            if hco3 < self.NORMAL_HCO3_MIN and pco2 < self.NORMAL_PCO2_MIN:
                analysis["compensation"] = "Fully compensated metabolic acidosis"
            elif hco3 > self.NORMAL_HCO3_MAX and pco2 > self.NORMAL_PCO2_MAX:
                analysis["compensation"] = "Fully compensated metabolic alkalosis"
            elif hco3 < self.NORMAL_HCO3_MIN and pco2 > self.NORMAL_PCO2_MAX:
                analysis["compensation"] = "Fully compensated respiratory acidosis"
            elif hco3 > self.NORMAL_HCO3_MAX and pco2 < self.NORMAL_PCO2_MIN:
                analysis["compensation"] = "Fully compensated respiratory alkalosis"
            else:
                analysis["compensation"] = "No compensation needed"
        
        return analysis
    
    def _assess_ph(self, ph: float) -> str:
        """Determines pH status"""
        if ph < self.NORMAL_PH_MIN:
            return "Acidemia"
        elif ph > self.NORMAL_PH_MAX:
            return "Alkalemia"
        else:
            return "Normal"
    
    def _assess_respiratory_compensation_acidosis(self, pco2: float, hco3: float) -> str:
        """Assesses respiratory compensation for metabolic acidosis using Winter's formula"""
        # Winter's formula: Expected PCO2 = 1.5 × [HCO3] + 8 (±2)
        expected_pco2 = 1.5 * hco3 + 8
        lower_limit = expected_pco2 - 2
        upper_limit = expected_pco2 + 2
        
        if lower_limit <= pco2 <= upper_limit:
            return f"Appropriate respiratory compensation (PCO2 {pco2:.1f}, expected {expected_pco2:.1f}±2)"
        elif pco2 < lower_limit:
            return f"Overcompensation or mixed disorder (PCO2 {pco2:.1f}, expected {expected_pco2:.1f}±2)"
        else:
            return f"Inadequate respiratory compensation (PCO2 {pco2:.1f}, expected {expected_pco2:.1f}±2)"
    
    def _assess_respiratory_compensation_alkalosis(self, pco2: float, hco3: float) -> str:
        """Assesses respiratory compensation for metabolic alkalosis"""
        # Expected PCO2 increase: 0.7 mmHg per mEq/L increase in HCO3
        hco3_excess = hco3 - 24  # Normal HCO3 is ~24
        expected_pco2_increase = 0.7 * hco3_excess
        expected_pco2 = 40 + expected_pco2_increase  # Normal PCO2 is ~40
        
        if pco2 >= expected_pco2 - 5 and pco2 <= expected_pco2 + 5:
            return f"Appropriate respiratory compensation (PCO2 {pco2:.1f}, expected ~{expected_pco2:.1f})"
        elif pco2 < expected_pco2 - 5:
            return f"Inadequate respiratory compensation (PCO2 {pco2:.1f}, expected ~{expected_pco2:.1f})"
        else:
            return f"Overcompensation or mixed disorder (PCO2 {pco2:.1f}, expected ~{expected_pco2:.1f})"
    
    def _assess_metabolic_compensation_resp_acidosis(self, hco3: float, pco2: float) -> str:
        """Assesses metabolic compensation for respiratory acidosis"""
        # Acute: 1 mEq/L increase per 10 mmHg PCO2 increase
        # Chronic: 3.5 mEq/L increase per 10 mmHg PCO2 increase
        pco2_excess = pco2 - 40
        acute_expected_hco3 = 24 + (pco2_excess / 10) * 1
        chronic_expected_hco3 = 24 + (pco2_excess / 10) * 3.5
        
        if hco3 <= acute_expected_hco3 + 2:
            return f"Acute respiratory acidosis (HCO3 {hco3:.1f}, acute expected ~{acute_expected_hco3:.1f})"
        elif hco3 >= chronic_expected_hco3 - 2:
            return f"Chronic respiratory acidosis with compensation (HCO3 {hco3:.1f}, chronic expected ~{chronic_expected_hco3:.1f})"
        else:
            return f"Partial metabolic compensation (HCO3 {hco3:.1f})"
    
    def _assess_metabolic_compensation_resp_alkalosis(self, hco3: float, pco2: float) -> str:
        """Assesses metabolic compensation for respiratory alkalosis"""
        # Acute: 2 mEq/L decrease per 10 mmHg PCO2 decrease
        # Chronic: 5 mEq/L decrease per 10 mmHg PCO2 decrease
        pco2_deficit = 40 - pco2
        acute_expected_hco3 = 24 - (pco2_deficit / 10) * 2
        chronic_expected_hco3 = 24 - (pco2_deficit / 10) * 5
        
        if hco3 >= acute_expected_hco3 - 2:
            return f"Acute respiratory alkalosis (HCO3 {hco3:.1f}, acute expected ~{acute_expected_hco3:.1f})"
        elif hco3 <= chronic_expected_hco3 + 2:
            return f"Chronic respiratory alkalosis with compensation (HCO3 {hco3:.1f}, chronic expected ~{chronic_expected_hco3:.1f})"
        else:
            return f"Partial metabolic compensation (HCO3 {hco3:.1f})"
    
    def _assess_oxygenation(self, po2: float, fio2: Optional[float] = None) -> Dict[str, Any]:
        """Assesses oxygenation status"""
        
        oxygenation = {
            "po2": po2,
            "status": "Normal" if po2 >= self.NORMAL_PO2_MIN else "Hypoxemia"
        }
        
        if po2 < 60:
            oxygenation["severity"] = "Severe hypoxemia"
        elif po2 < 80:
            oxygenation["severity"] = "Mild to moderate hypoxemia"
        else:
            oxygenation["severity"] = "Normal oxygenation"
        
        # Calculate A-a gradient if FiO2 provided
        if fio2 is not None:
            # Simplified A-a gradient calculation (assumes normal conditions)
            # PAO2 = (FiO2 × (760 - 47)) - (PCO2 / 0.8)
            # A-a gradient = PAO2 - PaO2
            # Note: This is simplified and assumes standard conditions
            oxygenation["fio2"] = fio2
            oxygenation["note"] = f"On FiO2 {fio2:.2f}"
        
        return oxygenation
    
    def _generate_interpretation(self, analysis: Dict[str, Any]) -> str:
        """Generates complete clinical interpretation"""
        
        interpretation_parts = []
        
        # Main disorder
        interpretation_parts.append(f"Primary disorder: {analysis['primary_disorder']}")
        
        # pH status
        interpretation_parts.append(f"pH {analysis['ph']:.2f} indicates {analysis['ph_status'].lower()}")
        
        # Compensation
        if analysis['compensation']:
            interpretation_parts.append(f"Compensation: {analysis['compensation']}")
        
        # Values summary
        interpretation_parts.append(f"Values: pH {analysis['ph']:.2f}, PCO2 {analysis['pco2']:.1f} mmHg, HCO3 {analysis['hco3']:.1f} mEq/L")
        
        # Oxygenation if available
        if "oxygenation" in analysis:
            oxygenation = analysis["oxygenation"]
            interpretation_parts.append(f"Oxygenation: PO2 {oxygenation['po2']:.1f} mmHg - {oxygenation['severity']}")
        
        # Clinical recommendations
        if "Metabolic Acidosis" in analysis['primary_disorder']:
            interpretation_parts.append("Consider calculating anion gap and assessing for underlying causes")
        elif "Respiratory" in analysis['primary_disorder']:
            interpretation_parts.append("Assess respiratory function and underlying pulmonary/neuromuscular causes")
        
        return ". ".join(interpretation_parts) + "."


def calculate_abg_analyzer(ph: float, pco2: float, hco3: float, 
                          po2: Optional[float] = None, fio2: Optional[float] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_abg_analyzer pattern
    """
    calculator = AbgAnalyzerCalculator()
    return calculator.calculate(ph, pco2, hco3, po2, fio2)
