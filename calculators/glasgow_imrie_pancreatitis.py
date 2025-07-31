"""
Glasgow-Imrie Criteria for Severity of Acute Pancreatitis Calculator

The Glasgow-Imrie Criteria is a clinical scoring system used to assess the severity 
of acute pancreatitis using 8 laboratory and clinical parameters. Originally developed 
as a modification of Ranson's criteria, it helps predict mortality risk and guide 
management decisions including ICU admission and treatment intensity. The criteria 
use the PANCREAS mnemonic (PaO2, Age, Neutrophils, Calcium, Renal function, 
Enzymes, Albumin, Sugar) for easy clinical recall.

References (Vancouver style):
1. Imrie CW, Benjamin IS, Ferguson JC, et al. A single-centre double-blind trial of 
   Trasylol therapy in primary acute pancreatitis. Br J Surg. 1978;65(5):337-341.
2. Blamey SL, Imrie CW, O'Neill J, Gilmour WH, Carter DC. Prognostic factors in 
   acute pancreatitis. Gut. 1984;25(12):1340-1346. doi: 10.1136/gut.25.12.1340.
3. Ranson JH, Rifkind KM, Roses DF, Fink SD, Eng K, Spencer FC. Prognostic signs 
   and the role of operative management in acute pancreatitis. Surg Gynecol Obstet. 
   1974;139(1):69-81.
4. Banks PA, Bollen TL, Dervenis C, et al. Classification of acute pancreatitis--2012: 
   revision of the Atlanta classification and definitions by international consensus. 
   Gut. 2013;62(1):102-111. doi: 10.1136/gutjnl-2012-302779.
"""

from typing import Dict, Any


class GlasgowImriePancreatitisCalculator:
    """Calculator for Glasgow-Imrie Criteria for Severity of Acute Pancreatitis"""
    
    def __init__(self):
        # PANCREAS mnemonic thresholds
        self.PAO2_THRESHOLD = 59.3  # mmHg (<59.3 = 1 point)
        self.AGE_THRESHOLD = 55  # years (>55 = 1 point)
        self.WBC_THRESHOLD = 15.0  # ×10⁹/L (>15 = 1 point)
        self.CALCIUM_THRESHOLD = 8.0  # mg/dL (<8 = 1 point)
        self.UREA_THRESHOLD = 44.8  # mg/dL (>44.8 = 1 point)
        self.LDH_THRESHOLD = 600  # IU/L (>600 = 1 point)
        self.ALBUMIN_THRESHOLD = 3.2  # g/dL (<3.2 = 1 point)
        self.GLUCOSE_THRESHOLD = 180  # mg/dL (>180 = 1 point)
        
        # Criteria descriptions for PANCREAS mnemonic
        self.CRITERIA_DESCRIPTIONS = {
            'pao2': 'P - PaO2 <59.3 mmHg',
            'age': 'A - Age >55 years',
            'wbc': 'N - Neutrophils (WBC) >15×10⁹/L',
            'calcium': 'C - Calcium <8 mg/dL',
            'urea': 'R - Renal function (Urea) >44.8 mg/dL',
            'ldh': 'E - Enzymes (LDH) >600 IU/L',
            'albumin': 'A - Albumin <3.2 g/dL',
            'glucose': 'S - Sugar (Glucose) >180 mg/dL'
        }
    
    def calculate(self, pao2: float, age: int, wbc: float, calcium: float,
                 urea: float, ldh: int, albumin: float, glucose: float) -> Dict[str, Any]:
        """
        Calculates Glasgow-Imrie score using the PANCREAS criteria
        
        Args:
            pao2 (float): Partial pressure of oxygen in mmHg
            age (int): Patient age in years
            wbc (float): White blood cell count in ×10⁹/L
            calcium (float): Serum calcium in mg/dL
            urea (float): Blood urea nitrogen in mg/dL
            ldh (int): Lactate dehydrogenase in IU/L
            albumin (float): Serum albumin in g/dL
            glucose (float): Blood glucose in mg/dL
            
        Returns:
            Dict with the Glasgow-Imrie score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pao2, age, wbc, calcium, urea, ldh, albumin, glucose)
        
        # Calculate individual criteria scores
        criteria_scores = self._calculate_criteria_scores(
            pao2, age, wbc, calcium, urea, ldh, albumin, glucose
        )
        
        # Calculate total score
        total_score = sum(criteria_scores.values())
        
        # Get interpretation
        interpretation = self._get_interpretation(
            total_score, pao2, age, wbc, calcium, urea, ldh, albumin, glucose, criteria_scores
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, pao2: float, age: int, wbc: float, calcium: float,
                        urea: float, ldh: int, albumin: float, glucose: float):
        """Validates input parameters"""
        
        if not isinstance(pao2, (int, float)) or pao2 < 30 or pao2 > 150:
            raise ValueError("PaO2 must be a number between 30 and 150 mmHg")
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if not isinstance(wbc, (int, float)) or wbc < 1.0 or wbc > 50.0:
            raise ValueError("WBC must be a number between 1.0 and 50.0 ×10⁹/L")
        
        if not isinstance(calcium, (int, float)) or calcium < 4.0 or calcium > 15.0:
            raise ValueError("Calcium must be a number between 4.0 and 15.0 mg/dL")
        
        if not isinstance(urea, (int, float)) or urea < 5 or urea > 200:
            raise ValueError("Urea must be a number between 5 and 200 mg/dL")
        
        if not isinstance(ldh, int) or ldh < 100 or ldh > 5000:
            raise ValueError("LDH must be an integer between 100 and 5000 IU/L")
        
        if not isinstance(albumin, (int, float)) or albumin < 1.0 or albumin > 6.0:
            raise ValueError("Albumin must be a number between 1.0 and 6.0 g/dL")
        
        if not isinstance(glucose, (int, float)) or glucose < 50 or glucose > 800:
            raise ValueError("Glucose must be a number between 50 and 800 mg/dL")
    
    def _calculate_criteria_scores(self, pao2: float, age: int, wbc: float, calcium: float,
                                  urea: float, ldh: int, albumin: float, glucose: float) -> Dict[str, int]:
        """Calculates individual criteria scores based on PANCREAS mnemonic"""
        
        return {
            'pao2': 1 if pao2 < self.PAO2_THRESHOLD else 0,
            'age': 1 if age > self.AGE_THRESHOLD else 0,
            'wbc': 1 if wbc > self.WBC_THRESHOLD else 0,
            'calcium': 1 if calcium < self.CALCIUM_THRESHOLD else 0,
            'urea': 1 if urea > self.UREA_THRESHOLD else 0,
            'ldh': 1 if ldh > self.LDH_THRESHOLD else 0,
            'albumin': 1 if albumin < self.ALBUMIN_THRESHOLD else 0,
            'glucose': 1 if glucose > self.GLUCOSE_THRESHOLD else 0
        }
    
    def _get_interpretation(self, total_score: int, pao2: float, age: int, wbc: float,
                          calcium: float, urea: float, ldh: int, albumin: float,
                          glucose: float, criteria_scores: Dict[str, int]) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the Glasgow-Imrie score
        
        Returns:
            Dict with interpretation details
        """
        
        # Build positive criteria summary
        positive_criteria = []
        lab_values = {
            'pao2': f"PaO2: {pao2:.1f} mmHg",
            'age': f"Age: {age} years",
            'wbc': f"WBC: {wbc:.1f}×10⁹/L",
            'calcium': f"Calcium: {calcium:.1f} mg/dL",
            'urea': f"Urea: {urea:.1f} mg/dL",
            'ldh': f"LDH: {ldh} IU/L",
            'albumin': f"Albumin: {albumin:.1f} g/dL",
            'glucose': f"Glucose: {glucose:.1f} mg/dL"
        }
        
        for criterion, score in criteria_scores.items():
            if score == 1:
                positive_criteria.append(f"{self.CRITERIA_DESCRIPTIONS[criterion]} ✓")
        
        all_values = "; ".join(lab_values.values())
        positive_summary = "; ".join(positive_criteria) if positive_criteria else "None"
        
        # Determine severity level and management recommendations
        if total_score <= 2:
            return {
                "stage": "Mild Pancreatitis",
                "description": "Low risk for severe pancreatitis",
                "interpretation": (
                    f"Glasgow-Imrie Score: {total_score}/8. [{all_values}]. "
                    f"Positive criteria: {positive_summary}. "
                    f"Low risk for severe pancreatitis (7-16% risk of severe disease). "
                    f"Patient can typically be managed with conservative treatment on "
                    f"general medical ward. Continue supportive care with IV fluids, "
                    f"pain management, and monitoring for clinical deterioration. "
                    f"Consider oral feeding when bowel sounds return and abdominal "
                    f"pain improves. Serial monitoring of laboratory parameters and "
                    f"clinical status. Early mobilization when tolerated. Discharge "
                    f"planning when clinically stable with appropriate follow-up."
                )
            }
        elif total_score <= 4:
            return {
                "stage": "Moderate Pancreatitis",
                "description": "Moderate risk for severe pancreatitis",
                "interpretation": (
                    f"Glasgow-Imrie Score: {total_score}/8. [{all_values}]. "
                    f"Positive criteria: {positive_summary}. "
                    f"Moderate risk for severe pancreatitis (20-61% risk of severe disease). "
                    f"Consider ICU monitoring or admission to high-dependency unit for "
                    f"close observation. Implement aggressive fluid resuscitation, "
                    f"optimal pain management, and frequent monitoring for complications. "
                    f"Monitor for signs of organ failure, local complications, and "
                    f"systemic inflammatory response. Consider early ERCP if biliary "
                    f"pancreatitis is suspected. Nutritional support may be required. "
                    f"Multidisciplinary team involvement including gastroenterology."
                )
            }
        else:  # total_score >= 5
            return {
                "stage": "Severe Pancreatitis",
                "description": "High risk for severe pancreatitis",
                "interpretation": (
                    f"Glasgow-Imrie Score: {total_score}/8. [{all_values}]. "
                    f"Positive criteria: {positive_summary}. "
                    f"High risk for severe pancreatitis (55-100% risk of severe disease). "
                    f"ICU admission typically required for intensive monitoring and "
                    f"organ support. Implement aggressive supportive care including "
                    f"hemodynamic support, respiratory monitoring, and renal function "
                    f"assessment. Monitor closely for multi-organ failure, pancreatic "
                    f"necrosis, and systemic complications. Consider early imaging "
                    f"(contrast-enhanced CT) to assess for necrosis. May require "
                    f"surgical consultation for potential necrosectomy or drainage "
                    f"procedures. Nutritional support essential. Multidisciplinary "
                    f"approach with critical care, gastroenterology, and surgery."
                )
            }


def calculate_glasgow_imrie_pancreatitis(pao2: float, age: int, wbc: float, calcium: float,
                                       urea: float, ldh: int, albumin: float,
                                       glucose: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glasgow_imrie_pancreatitis pattern
    """
    calculator = GlasgowImriePancreatitisCalculator()
    return calculator.calculate(pao2, age, wbc, calcium, urea, ldh, albumin, glucose)