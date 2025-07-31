"""
Glasgow-Blatchford Bleeding Score (GBS) Calculator

The Glasgow-Blatchford Bleeding Score is a clinical scoring system used to assess 
the risk of upper gastrointestinal bleeding and identify patients who may need 
medical intervention such as blood transfusion or endoscopic intervention. It helps 
stratify patients for safe outpatient management versus hospital admission and is 
particularly valuable for identifying low-risk patients who can be managed as 
outpatients, reducing healthcare costs and hospital burden.

References (Vancouver style):
1. Blatchford O, Murray WR, Blatchford M. A risk score to predict need for treatment 
   for upper-gastrointestinal haemorrhage. Lancet. 2000;356(9238):1318-1321. 
   doi: 10.1016/S0140-6736(00)02816-6.
2. Stanley AJ, Ashley D, Dalton HR, et al. Outpatient management of patients with 
   low-risk upper-gastrointestinal haemorrhage: multicentre validation and prospective 
   evaluation. Lancet. 2009;373(9657):42-47. doi: 10.1016/S0140-6736(08)61769-9.
3. Saltzman JR, Tabak YP, Hyett BH, Sun X, Travis AC, Johannes RS. A simple risk 
   score accurately predicts in-hospital mortality, length of stay, and cost in 
   acute upper GI bleeding. Gastrointest Endosc. 2011;74(6):1215-1224. 
   doi: 10.1016/j.gie.2011.06.024.
"""

from typing import Dict, Any


class GlasgowBlatchfordBleedingScoreCalculator:
    """Calculator for Glasgow-Blatchford Bleeding Score (GBS)"""
    
    def __init__(self):
        # BUN scoring thresholds (mg/dL)
        self.BUN_THRESHOLDS = [
            (18.2, 0),   # <18.2 mg/dL = 0 points
            (22.3, 2),   # 18.2-22.3 mg/dL = 2 points
            (28.0, 3),   # 22.4-28.0 mg/dL = 3 points
            (70.0, 4),   # 28.1-70.0 mg/dL = 4 points
            (float('inf'), 6)  # >70.0 mg/dL = 6 points
        ]
        
        # Hemoglobin scoring thresholds by gender (g/dL)
        self.HEMOGLOBIN_MALE_THRESHOLDS = [
            (13.0, 0),   # >13.0 g/dL = 0 points
            (12.0, 1),   # 12.0-13.0 g/dL = 1 point
            (10.0, 3),   # 10.0-12.0 g/dL = 3 points
            (0.0, 6)     # <10.0 g/dL = 6 points
        ]
        
        self.HEMOGLOBIN_FEMALE_THRESHOLDS = [
            (12.0, 0),   # >12.0 g/dL = 0 points
            (10.0, 1),   # 10.0-12.0 g/dL = 1 point
            (0.0, 6)     # <10.0 g/dL = 6 points
        ]
        
        # Systolic BP scoring thresholds (mmHg)
        self.SYSTOLIC_BP_THRESHOLDS = [
            (110, 0),    # ≥110 mmHg = 0 points
            (100, 1),    # 100-109 mmHg = 1 point
            (90, 2),     # 90-99 mmHg = 2 points
            (0, 3)       # <90 mmHg = 3 points
        ]
        
        # Heart rate threshold
        self.HEART_RATE_THRESHOLD = 100  # ≥100 bpm = 1 point
        
        # Additional clinical factors (2 points each except melena = 1 point)
        self.CLINICAL_FACTORS = {
            'melena': 1,
            'syncope': 2,
            'liver_disease': 2,
            'heart_failure': 2
        }
    
    def calculate(self, bun: float, hemoglobin: float, gender: str, systolic_bp: int,
                 heart_rate: int, melena: str, syncope: str, liver_disease: str,
                 heart_failure: str) -> Dict[str, Any]:
        """
        Calculates Glasgow-Blatchford Bleeding Score using clinical parameters
        
        Args:
            bun (float): Blood urea nitrogen in mg/dL
            hemoglobin (float): Hemoglobin in g/dL
            gender (str): Patient gender ("male" or "female")
            systolic_bp (int): Systolic blood pressure in mmHg
            heart_rate (int): Heart rate in bpm
            melena (str): Presence of melena ("yes" or "no")
            syncope (str): History of syncope ("yes" or "no")
            liver_disease (str): History of liver disease ("yes" or "no")
            heart_failure (str): History of heart failure ("yes" or "no")
            
        Returns:
            Dict with the total GBS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(bun, hemoglobin, gender, systolic_bp, heart_rate,
                            melena, syncope, liver_disease, heart_failure)
        
        # Calculate component scores
        bun_score = self._calculate_bun_score(bun)
        hemoglobin_score = self._calculate_hemoglobin_score(hemoglobin, gender)
        bp_score = self._calculate_bp_score(systolic_bp)
        hr_score = self._calculate_heart_rate_score(heart_rate)
        
        # Calculate clinical factor scores
        melena_score = self.CLINICAL_FACTORS['melena'] if melena == "yes" else 0
        syncope_score = self.CLINICAL_FACTORS['syncope'] if syncope == "yes" else 0
        liver_score = self.CLINICAL_FACTORS['liver_disease'] if liver_disease == "yes" else 0
        heart_score = self.CLINICAL_FACTORS['heart_failure'] if heart_failure == "yes" else 0
        
        # Calculate total score
        total_score = (bun_score + hemoglobin_score + bp_score + hr_score + 
                      melena_score + syncope_score + liver_score + heart_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(
            total_score, bun, hemoglobin, gender, systolic_bp, heart_rate,
            melena, syncope, liver_disease, heart_failure,
            bun_score, hemoglobin_score, bp_score, hr_score,
            melena_score, syncope_score, liver_score, heart_score
        )
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bun: float, hemoglobin: float, gender: str, systolic_bp: int,
                        heart_rate: int, melena: str, syncope: str, liver_disease: str,
                        heart_failure: str):
        """Validates input parameters"""
        
        if not isinstance(bun, (int, float)) or bun < 5 or bun > 200:
            raise ValueError("BUN must be a number between 5 and 200 mg/dL")
        
        if not isinstance(hemoglobin, (int, float)) or hemoglobin < 3.0 or hemoglobin > 20.0:
            raise ValueError("Hemoglobin must be a number between 3.0 and 20.0 g/dL")
        
        if gender not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 50 or systolic_bp > 250:
            raise ValueError("Systolic BP must be an integer between 50 and 250 mmHg")
        
        if not isinstance(heart_rate, int) or heart_rate < 30 or heart_rate > 200:
            raise ValueError("Heart rate must be an integer between 30 and 200 bpm")
        
        for param, name in [(melena, "melena"), (syncope, "syncope"), 
                           (liver_disease, "liver_disease"), (heart_failure, "heart_failure")]:
            if param not in ["yes", "no"]:
                raise ValueError(f"{name} must be 'yes' or 'no'")
    
    def _calculate_bun_score(self, bun: float) -> int:
        """Calculates BUN component score"""
        if bun < 18.2:
            return 0
        elif bun <= 22.3:
            return 2
        elif bun <= 28.0:
            return 3
        elif bun <= 70.0:
            return 4
        else:
            return 6
    
    def _calculate_hemoglobin_score(self, hemoglobin: float, gender: str) -> int:
        """Calculates hemoglobin component score based on gender"""
        if gender == "male":
            if hemoglobin > 13.0:
                return 0
            elif hemoglobin >= 12.0:
                return 1
            elif hemoglobin >= 10.0:
                return 3
            else:
                return 6
        else:  # female
            if hemoglobin > 12.0:
                return 0
            elif hemoglobin >= 10.0:
                return 1
            else:
                return 6
    
    def _calculate_bp_score(self, systolic_bp: int) -> int:
        """Calculates systolic blood pressure component score"""
        if systolic_bp >= 110:
            return 0
        elif systolic_bp >= 100:
            return 1
        elif systolic_bp >= 90:
            return 2
        else:
            return 3
    
    def _calculate_heart_rate_score(self, heart_rate: int) -> int:
        """Calculates heart rate component score"""
        return 1 if heart_rate >= self.HEART_RATE_THRESHOLD else 0
    
    def _get_interpretation(self, total_score: int, bun: float, hemoglobin: float,
                          gender: str, systolic_bp: int, heart_rate: int, melena: str,
                          syncope: str, liver_disease: str, heart_failure: str,
                          bun_score: int, hemoglobin_score: int, bp_score: int,
                          hr_score: int, melena_score: int, syncope_score: int,
                          liver_score: int, heart_score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on the GBS score
        
        Returns:
            Dict with interpretation details
        """
        
        # Build component summary
        component_details = [
            f"BUN: {bun:.1f} mg/dL ({bun_score} points)",
            f"Hemoglobin: {hemoglobin:.1f} g/dL ({hemoglobin_score} points)",
            f"Systolic BP: {systolic_bp} mmHg ({bp_score} points)",
            f"Heart rate: {heart_rate} bpm ({hr_score} points)"
        ]
        
        clinical_factors = []
        if melena_score > 0:
            clinical_factors.append(f"Melena present ({melena_score} points)")
        if syncope_score > 0:
            clinical_factors.append(f"Syncope ({syncope_score} points)")
        if liver_score > 0:
            clinical_factors.append(f"Liver disease ({liver_score} points)")
        if heart_score > 0:
            clinical_factors.append(f"Heart failure ({heart_score} points)")
        
        if clinical_factors:
            component_details.extend(clinical_factors)
        
        component_summary = "; ".join(component_details)
        
        # Determine risk level and management recommendations
        if total_score == 0:
            return {
                "stage": "Low Risk",
                "description": "Very low risk - Safe for outpatient management",
                "interpretation": (
                    f"Glasgow-Blatchford Bleeding Score: {total_score}/23. [{component_summary}]. "
                    f"Very low risk for needing medical intervention in upper GI bleeding. "
                    f"Patient can be safely managed as outpatient with appropriate follow-up. "
                    f"No immediate need for blood transfusion or endoscopic intervention. "
                    f"Arrange outpatient gastroenterology follow-up within 7-14 days. "
                    f"Provide clear return precautions for worsening symptoms such as "
                    f"increased bleeding, dizziness, weakness, or abdominal pain. "
                    f"Consider proton pump inhibitor therapy and H. pylori testing if indicated."
                )
            }
        elif total_score <= 5:
            return {
                "stage": "Low-Moderate Risk",
                "description": "Low to moderate risk requiring clinical assessment",
                "interpretation": (
                    f"Glasgow-Blatchford Bleeding Score: {total_score}/23. [{component_summary}]. "
                    f"Low to moderate risk for intervention in upper GI bleeding. "
                    f"Consider hospital admission for clinical observation and assessment. "
                    f"Risk for blood transfusion or endoscopic intervention is present but "
                    f"relatively low. Monitor vital signs, complete blood count, and clinical "
                    f"status closely. Consider early gastroenterology consultation if symptoms "
                    f"worsen or score increases. Initiate proton pump inhibitor therapy. "
                    f"Ensure adequate IV access and type and screen blood products."
                )
            }
        elif total_score <= 11:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk requiring hospital admission",
                "interpretation": (
                    f"Glasgow-Blatchford Bleeding Score: {total_score}/23. [{component_summary}]. "
                    f"Moderate risk for needing medical intervention in upper GI bleeding. "
                    f"Hospital admission recommended with close monitoring in appropriate "
                    f"clinical setting. Significant risk for blood transfusion or endoscopic "
                    f"intervention. Gastroenterology consultation should be obtained promptly. "
                    f"Begin high-dose proton pump inhibitor therapy. Ensure adequate IV access, "
                    f"type and crossmatch blood products, and monitor hemoglobin levels closely. "
                    f"Consider early endoscopy within 24 hours if clinical condition permits."
                )
            }
        else:  # total_score >= 12
            return {
                "stage": "High Risk",
                "description": "High risk requiring immediate intervention",
                "interpretation": (
                    f"Glasgow-Blatchford Bleeding Score: {total_score}/23. [{component_summary}]. "
                    f"High risk for needing immediate medical intervention in upper GI bleeding. "
                    f"Urgent hospital admission required with intensive monitoring. High "
                    f"likelihood of requiring blood transfusion and/or emergency endoscopic "
                    f"intervention. Immediate gastroenterology consultation and consideration "
                    f"for ICU admission. Begin immediate resuscitation with IV fluids and "
                    f"blood products as needed. High-dose proton pump inhibitor therapy. "
                    f"Urgent endoscopy should be considered within 12-24 hours or emergently "
                    f"if hemodynamically unstable. Monitor closely for signs of rebleeding."
                )
            }


def calculate_glasgow_blatchford_bleeding_score(bun: float, hemoglobin: float, gender: str,
                                               systolic_bp: int, heart_rate: int, melena: str,
                                               syncope: str, liver_disease: str,
                                               heart_failure: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glasgow_blatchford_bleeding_score pattern
    """
    calculator = GlasgowBlatchfordBleedingScoreCalculator()
    return calculator.calculate(bun, hemoglobin, gender, systolic_bp, heart_rate,
                               melena, syncope, liver_disease, heart_failure)