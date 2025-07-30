"""
Child-Pugh Score for Cirrhosis Mortality Calculator

Estimates severity of cirrhosis and prognosis in patients with chronic liver disease.
Originally developed to predict mortality during portacaval shunt surgery.

References:
1. Child CG, Turcotte JG. Surgery and portal hypertension. In: The liver and portal 
   hypertension. Edited by CG Child. Philadelphia: Saunders 1964:50-64.
2. Pugh RN, Murray-Lyon IM, Dawson JL, Pietroni MC, Williams R. Transection of the 
   oesophagus for bleeding oesophageal varices. Br J Surg. 1973 Aug;60(8):646-9.
3. Durand F, Valla D. Assessment of prognosis of cirrhosis. Semin Liver Dis. 2008 
   Feb;28(1):110-22.
"""

from typing import Dict, Any


class ChildPughScoreCalculator:
    """Calculator for Child-Pugh Score for Cirrhosis Mortality"""
    
    def __init__(self):
        # Clinical outcomes by Child-Pugh grade
        self.grade_outcomes = {
            "A": {
                "one_year_survival": 100,
                "two_year_survival": 85,
                "operative_risk": "Excellent",
                "surgical_recommendation": "Suitable for major surgery and liver resection"
            },
            "B": {
                "one_year_survival": 80,
                "two_year_survival": 60,
                "operative_risk": "Good",
                "surgical_recommendation": "Consider surgery with caution; may need transplant evaluation"
            },
            "C": {
                "one_year_survival": 45,
                "two_year_survival": 35,
                "operative_risk": "Poor",
                "surgical_recommendation": "High surgical mortality; priority for liver transplantation"
            }
        }
    
    def calculate(
        self,
        total_bilirubin: float,
        serum_albumin: float,
        inr: float,
        ascites: str,
        encephalopathy: str
    ) -> Dict[str, Any]:
        """
        Calculates Child-Pugh score for cirrhosis severity assessment
        
        Args:
            total_bilirubin: Serum total bilirubin level (mg/dL)
            serum_albumin: Serum albumin level (g/dL)
            inr: International Normalized Ratio
            ascites: Ascites severity (absent/slight/moderate)
            encephalopathy: Encephalopathy grade (none/grade_1_2/grade_3_4)
            
        Returns:
            Dict with Child-Pugh score, grade, and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(total_bilirubin, serum_albumin, inr, ascites, encephalopathy)
        
        # Calculate individual component scores
        bilirubin_points = self._score_bilirubin(total_bilirubin)
        albumin_points = self._score_albumin(serum_albumin)
        inr_points = self._score_inr(inr)
        ascites_points = self._score_ascites(ascites)
        encephalopathy_points = self._score_encephalopathy(encephalopathy)
        
        # Calculate total score
        total_score = bilirubin_points + albumin_points + inr_points + ascites_points + encephalopathy_points
        
        # Determine grade and interpretation
        grade_assessment = self._get_grade_assessment(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            total_bilirubin, bilirubin_points, serum_albumin, albumin_points,
            inr, inr_points, ascites, ascites_points, encephalopathy, encephalopathy_points
        )
        
        return {
            "result": {
                "total_score": total_score,
                "grade": grade_assessment["grade"],
                "one_year_survival": grade_assessment["one_year_survival"],
                "two_year_survival": grade_assessment["two_year_survival"],
                "operative_risk": grade_assessment["operative_risk"],
                "surgical_recommendation": grade_assessment["surgical_recommendation"],
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": grade_assessment["interpretation"],
            "stage": f"Child-Pugh {grade_assessment['grade']}",
            "stage_description": grade_assessment["description"]
        }
    
    def _validate_inputs(self, bilirubin, albumin, inr, ascites, encephalopathy):
        """Validates input parameters"""
        
        # Validate bilirubin
        if not isinstance(bilirubin, (int, float)) or bilirubin < 0.1 or bilirubin > 50.0:
            raise ValueError("Total bilirubin must be between 0.1 and 50.0 mg/dL")
        
        # Validate albumin
        if not isinstance(albumin, (int, float)) or albumin < 1.0 or albumin > 5.0:
            raise ValueError("Serum albumin must be between 1.0 and 5.0 g/dL")
        
        # Validate INR
        if not isinstance(inr, (int, float)) or inr < 0.8 or inr > 10.0:
            raise ValueError("INR must be between 0.8 and 10.0")
        
        # Validate ascites
        if ascites not in ["absent", "slight", "moderate"]:
            raise ValueError("Ascites must be 'absent', 'slight', or 'moderate'")
        
        # Validate encephalopathy
        if encephalopathy not in ["none", "grade_1_2", "grade_3_4"]:
            raise ValueError("Encephalopathy must be 'none', 'grade_1_2', or 'grade_3_4'")
    
    def _score_bilirubin(self, bilirubin: float) -> int:
        """Scores total bilirubin level"""
        
        if bilirubin < 2.0:
            return 1
        elif bilirubin <= 3.0:
            return 2
        else:  # > 3.0
            return 3
    
    def _score_albumin(self, albumin: float) -> int:
        """Scores serum albumin level"""
        
        if albumin > 3.5:
            return 1
        elif albumin >= 2.8:
            return 2
        else:  # < 2.8
            return 3
    
    def _score_inr(self, inr: float) -> int:
        """Scores INR value"""
        
        if inr < 1.7:
            return 1
        elif inr <= 2.3:
            return 2
        else:  # > 2.3
            return 3
    
    def _score_ascites(self, ascites: str) -> int:
        """Scores ascites severity"""
        
        ascites_scores = {
            "absent": 1,
            "slight": 2,
            "moderate": 3
        }
        return ascites_scores[ascites]
    
    def _score_encephalopathy(self, encephalopathy: str) -> int:
        """Scores encephalopathy grade"""
        
        encephalopathy_scores = {
            "none": 1,
            "grade_1_2": 2,
            "grade_3_4": 3
        }
        return encephalopathy_scores[encephalopathy]
    
    def _get_grade_assessment(self, score: int) -> Dict[str, Any]:
        """
        Determines Child-Pugh grade and clinical assessment based on total score
        
        Args:
            score: Total Child-Pugh score (5-15)
            
        Returns:
            Dict with grade and clinical outcomes
        """
        
        if score <= 6:  # Grade A: 5-6 points
            grade = "A"
            description = "Well-compensated disease"
            interpretation = f"Child-Pugh Grade A (Score {score}): Well-compensated cirrhosis. Excellent operative risk with one-year survival ~100% and two-year survival ~85%. Suitable for major surgery and liver resection."
        elif score <= 9:  # Grade B: 7-9 points
            grade = "B"
            description = "Significant functional compromise"
            interpretation = f"Child-Pugh Grade B (Score {score}): Significant functional compromise. Good operative risk with one-year survival ~80% and two-year survival ~60%. Consider surgery with caution; may require liver transplant evaluation."
        else:  # Grade C: 10-15 points
            grade = "C"
            description = "Decompensated disease"
            interpretation = f"Child-Pugh Grade C (Score {score}): Decompensated cirrhosis. Poor operative risk with one-year survival ~45% and two-year survival ~35%. High surgical mortality; priority candidate for liver transplantation."
        
        outcomes = self.grade_outcomes[grade]
        
        return {
            "grade": grade,
            "description": description,
            "interpretation": interpretation,
            "one_year_survival": outcomes["one_year_survival"],
            "two_year_survival": outcomes["two_year_survival"],
            "operative_risk": outcomes["operative_risk"],
            "surgical_recommendation": outcomes["surgical_recommendation"]
        }
    
    def _get_scoring_breakdown(self, bilirubin, bil_pts, albumin, alb_pts, inr, inr_pts, ascites, asc_pts, enceph, enc_pts):
        """Provides detailed scoring breakdown"""
        
        # Bilirubin category
        if bilirubin < 2.0:
            bil_category = f"{bilirubin} mg/dL (<2.0)"
        elif bilirubin <= 3.0:
            bil_category = f"{bilirubin} mg/dL (2.0-3.0)"
        else:
            bil_category = f"{bilirubin} mg/dL (>3.0)"
        
        # Albumin category
        if albumin > 3.5:
            alb_category = f"{albumin} g/dL (>3.5)"
        elif albumin >= 2.8:
            alb_category = f"{albumin} g/dL (2.8-3.5)"
        else:
            alb_category = f"{albumin} g/dL (<2.8)"
        
        # INR category
        if inr < 1.7:
            inr_category = f"{inr} (<1.7)"
        elif inr <= 2.3:
            inr_category = f"{inr} (1.7-2.3)"
        else:
            inr_category = f"{inr} (>2.3)"
        
        # Ascites mapping
        ascites_mapping = {
            "absent": "Absent",
            "slight": "Slight",
            "moderate": "Moderate"
        }
        
        # Encephalopathy mapping
        enceph_mapping = {
            "none": "None",
            "grade_1_2": "Grade 1-2",
            "grade_3_4": "Grade 3-4"
        }
        
        breakdown = {
            "component_scores": {
                "total_bilirubin": {
                    "value": bilirubin,
                    "unit": "mg/dL",
                    "category": bil_category,
                    "points": bil_pts,
                    "description": "Total serum bilirubin level"
                },
                "serum_albumin": {
                    "value": albumin,
                    "unit": "g/dL", 
                    "category": alb_category,
                    "points": alb_pts,
                    "description": "Serum albumin level"
                },
                "inr": {
                    "value": inr,
                    "unit": "",
                    "category": inr_category,
                    "points": inr_pts,
                    "description": "International Normalized Ratio"
                },
                "ascites": {
                    "value": ascites_mapping[ascites],
                    "category": ascites_mapping[ascites],
                    "points": asc_pts,
                    "description": "Presence and severity of ascites"
                },
                "encephalopathy": {
                    "value": enceph_mapping[enceph],
                    "category": enceph_mapping[enceph],
                    "points": enc_pts,
                    "description": "Hepatic encephalopathy grade"
                }
            },
            "scoring_criteria": {
                "bilirubin_mg_dl": {
                    "1_point": "<2.0",
                    "2_points": "2.0-3.0",
                    "3_points": ">3.0"
                },
                "albumin_g_dl": {
                    "1_point": ">3.5",
                    "2_points": "2.8-3.5",
                    "3_points": "<2.8"
                },
                "inr": {
                    "1_point": "<1.7",
                    "2_points": "1.7-2.3",
                    "3_points": ">2.3"
                },
                "ascites": {
                    "1_point": "Absent",
                    "2_points": "Slight",
                    "3_points": "Moderate"
                },
                "encephalopathy": {
                    "1_point": "None",
                    "2_points": "Grade 1-2",
                    "3_points": "Grade 3-4"
                }
            },
            "clinical_context": {
                "development": "Originally developed for portal hypertension surgery risk assessment",
                "current_use": "Widely used for cirrhosis prognosis and surgical risk stratification",
                "limitations": "MELD and MELD-Na scores now preferred for liver transplant allocation",
                "reassessment": "Should be reassessed if patient's clinical condition changes"
            }
        }
        
        return breakdown


def calculate_child_pugh_score(
    total_bilirubin: float,
    serum_albumin: float,
    inr: float,
    ascites: str,
    encephalopathy: str
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ChildPughScoreCalculator()
    return calculator.calculate(
        total_bilirubin=total_bilirubin,
        serum_albumin=serum_albumin,
        inr=inr,
        ascites=ascites,
        encephalopathy=encephalopathy
    )