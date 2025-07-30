"""
CholeS Score for Duration of Laparoscopic Cholecystectomy Calculator

Predicts operative time duration for elective laparoscopic cholecystectomy procedures
to optimize theatre scheduling and resource allocation.

References:
1. Vohra RS, Pasquali S, Kirkham JJ, Marriott P, Johnstone M, Spreadborough P, et al. 
   The development and validation of a scoring tool to predict the operative duration 
   of elective laparoscopic cholecystectomy. Surg Endosc. 2018 Jul;32(7):3149-3157.
2. Griffiths EA, Hodson J, Vohra RS, Marriott P, Katbeh T, Zino S, et al. Utilisation 
   of an operative difficulty grading scale for laparoscopic cholecystectomy. Surg 
   Endosc. 2019 Jan;33(1):110-121.
3. Nassar AHM, Hodson J, Ng HJ, Vohra RS, Katbeh T, Zino S, et al. Predicting the 
   difficult laparoscopic cholecystectomy: development and validation of a pre-operative 
   risk score using an objective operative difficulty grading system. Surg Endosc. 
   2020 Oct;34(10):4549-4561.
"""

from typing import Dict, Any


class CholesScorecalculator:
    """Calculator for CholeS Score for Duration of Laparoscopic Cholecystectomy"""
    
    def __init__(self):
        # Point values based on original CholeS study
        self.scoring_criteria = {
            "age": {
                "under_40": 0,
                "40_or_over": 1.5
            },
            "gender": {
                "female": 0,
                "male": 1
            },
            "indication": {
                "pancreatitis": 0,
                "colic_dyskinesia_polyp": 0.5,
                "cbd_stone": 2,
                "acalculous_cholecystitis": 2.5
            },
            "bmi": {
                "under_25": 0,
                "25_to_35": 1,
                "over_35": 2
            },
            "cbd_diameter": {
                "normal": 0,
                "dilated": 2
            },
            "gallbladder_wall": {
                "normal": 0,
                "thick": 1.5
            },
            "preoperative_ct": {
                "no": 0,
                "yes": 1.5
            },
            "planned_cholangiogram": {
                "no": 0,
                "yes": 3
            },
            "previous_admissions": {
                "none": 0,
                "one_to_two": 1,
                "more_than_two": 2.5
            },
            "asa_grade": {
                "grade_1": 0,
                "grade_2": 1,
                "grade_3_or_higher": 2.5
            }
        }
        
        # Risk stratification thresholds
        self.risk_categories = {
            "low": {
                "threshold": 3.5,
                "probability": 5.1,
                "description": "Low likelihood of prolonged surgery",
                "scheduling": "3 cases per half-day list"
            },
            "intermediate": {
                "min_threshold": 4.0,
                "max_threshold": 8.0,
                "probability_range": "5.1-41.8",
                "description": "Moderate likelihood of prolonged surgery",
                "scheduling": "2-3 cases per half-day list"
            },
            "high": {
                "threshold": 8.5,
                "probability": 41.8,
                "description": "High likelihood of prolonged surgery",
                "scheduling": "Maximum 2 cases per half-day list"
            }
        }
    
    def calculate(
        self,
        age: int,
        gender: str,
        indication: str,
        bmi: float,
        cbd_diameter: str,
        gallbladder_wall: str,
        preoperative_ct: str,
        planned_cholangiogram: str,
        previous_admissions: int,
        asa_grade: int
    ) -> Dict[str, Any]:
        """
        Calculates CholeS score for operative duration prediction
        
        Args:
            age: Patient age in years
            gender: Patient gender (male/female)
            indication: Surgical indication
            bmi: Body Mass Index
            cbd_diameter: Common bile duct diameter (normal/dilated)
            gallbladder_wall: Gallbladder wall thickness (normal/thick)
            preoperative_ct: Pre-operative CT performed (yes/no)
            planned_cholangiogram: Planned intra-op cholangiogram (yes/no)
            previous_admissions: Number of previous surgical admissions
            asa_grade: ASA Physical Status Classification (1-5)
            
        Returns:
            Dict with CholeS score, risk category, and operative planning guidance
        """
        
        # Validate inputs
        self._validate_inputs(age, gender, indication, bmi, cbd_diameter, 
                            gallbladder_wall, preoperative_ct, planned_cholangiogram,
                            previous_admissions, asa_grade)
        
        # Calculate component scores
        age_points = self._score_age(age)
        gender_points = self._score_gender(gender)
        indication_points = self._score_indication(indication)
        bmi_points = self._score_bmi(bmi)
        cbd_points = self._score_cbd_diameter(cbd_diameter)
        gb_wall_points = self._score_gallbladder_wall(gallbladder_wall)
        ct_points = self._score_preoperative_ct(preoperative_ct)
        cholangiogram_points = self._score_planned_cholangiogram(planned_cholangiogram)
        admissions_points = self._score_previous_admissions(previous_admissions)
        asa_points = self._score_asa_grade(asa_grade)
        
        # Calculate total score
        total_score = (age_points + gender_points + indication_points + bmi_points + 
                      cbd_points + gb_wall_points + ct_points + cholangiogram_points + 
                      admissions_points + asa_points)
        
        # Get risk assessment
        risk_assessment = self._get_risk_assessment(total_score)
        
        # Get detailed scoring breakdown
        scoring_breakdown = self._get_scoring_breakdown(
            age, age_points, gender, gender_points, indication, indication_points,
            bmi, bmi_points, cbd_diameter, cbd_points, gallbladder_wall, gb_wall_points,
            preoperative_ct, ct_points, planned_cholangiogram, cholangiogram_points,
            previous_admissions, admissions_points, asa_grade, asa_points
        )
        
        return {
            "result": {
                "total_score": round(total_score, 1),
                "risk_category": risk_assessment["category"],
                "prolonged_surgery_probability": risk_assessment["probability"],
                "operative_planning": risk_assessment["planning"],
                "scheduling_recommendation": risk_assessment["scheduling"],
                "scoring_breakdown": scoring_breakdown
            },
            "unit": "points",
            "interpretation": risk_assessment["interpretation"],
            "stage": risk_assessment["category"],
            "stage_description": risk_assessment["description"]
        }
    
    def _validate_inputs(self, age, gender, indication, bmi, cbd_diameter,
                        gallbladder_wall, preoperative_ct, planned_cholangiogram,
                        previous_admissions, asa_grade):
        """Validates input parameters"""
        
        # Validate age
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120")
        
        # Validate gender
        if gender not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")
        
        # Validate indication
        valid_indications = ["pancreatitis", "colic_dyskinesia_polyp", "cbd_stone", "acalculous_cholecystitis"]
        if indication not in valid_indications:
            raise ValueError(f"Indication must be one of {valid_indications}")
        
        # Validate BMI
        if not isinstance(bmi, (int, float)) or bmi < 15.0 or bmi > 60.0:
            raise ValueError("BMI must be between 15.0 and 60.0")
        
        # Validate CBD diameter
        if cbd_diameter not in ["normal", "dilated"]:
            raise ValueError("CBD diameter must be 'normal' or 'dilated'")
        
        # Validate gallbladder wall
        if gallbladder_wall not in ["normal", "thick"]:
            raise ValueError("Gallbladder wall must be 'normal' or 'thick'")
        
        # Validate preoperative CT
        if preoperative_ct not in ["yes", "no"]:
            raise ValueError("Preoperative CT must be 'yes' or 'no'")
        
        # Validate planned cholangiogram
        if planned_cholangiogram not in ["yes", "no"]:
            raise ValueError("Planned cholangiogram must be 'yes' or 'no'")
        
        # Validate previous admissions
        if not isinstance(previous_admissions, int) or previous_admissions < 0 or previous_admissions > 20:
            raise ValueError("Previous admissions must be an integer between 0 and 20")
        
        # Validate ASA grade
        if not isinstance(asa_grade, int) or asa_grade < 1 or asa_grade > 5:
            raise ValueError("ASA grade must be an integer between 1 and 5")
    
    def _score_age(self, age: int) -> float:
        """Scores age component"""
        return self.scoring_criteria["age"]["40_or_over"] if age >= 40 else self.scoring_criteria["age"]["under_40"]
    
    def _score_gender(self, gender: str) -> float:
        """Scores gender component"""
        return self.scoring_criteria["gender"][gender]
    
    def _score_indication(self, indication: str) -> float:
        """Scores surgical indication component"""
        return self.scoring_criteria["indication"][indication]
    
    def _score_bmi(self, bmi: float) -> float:
        """Scores BMI component"""
        if bmi < 25:
            return self.scoring_criteria["bmi"]["under_25"]
        elif bmi <= 35:
            return self.scoring_criteria["bmi"]["25_to_35"]
        else:
            return self.scoring_criteria["bmi"]["over_35"]
    
    def _score_cbd_diameter(self, cbd_diameter: str) -> float:
        """Scores CBD diameter component"""
        return self.scoring_criteria["cbd_diameter"][cbd_diameter]
    
    def _score_gallbladder_wall(self, gallbladder_wall: str) -> float:
        """Scores gallbladder wall component"""
        return self.scoring_criteria["gallbladder_wall"][gallbladder_wall]
    
    def _score_preoperative_ct(self, preoperative_ct: str) -> float:
        """Scores preoperative CT component"""
        return self.scoring_criteria["preoperative_ct"][preoperative_ct]
    
    def _score_planned_cholangiogram(self, planned_cholangiogram: str) -> float:
        """Scores planned cholangiogram component"""
        return self.scoring_criteria["planned_cholangiogram"][planned_cholangiogram]
    
    def _score_previous_admissions(self, previous_admissions: int) -> float:
        """Scores previous admissions component"""
        if previous_admissions == 0:
            return self.scoring_criteria["previous_admissions"]["none"]
        elif previous_admissions <= 2:
            return self.scoring_criteria["previous_admissions"]["one_to_two"]
        else:
            return self.scoring_criteria["previous_admissions"]["more_than_two"]
    
    def _score_asa_grade(self, asa_grade: int) -> float:
        """Scores ASA grade component"""
        if asa_grade == 1:
            return self.scoring_criteria["asa_grade"]["grade_1"]
        elif asa_grade == 2:
            return self.scoring_criteria["asa_grade"]["grade_2"]
        else:
            return self.scoring_criteria["asa_grade"]["grade_3_or_higher"]
    
    def _get_risk_assessment(self, score: float) -> Dict[str, Any]:
        """
        Determines risk category and operative planning based on CholeS score
        
        Args:
            score: Total CholeS score
            
        Returns:
            Dict with risk assessment and planning guidance
        """
        
        if score <= 3.5:
            category = "Low Risk"
            probability = "5.1% chance of >90-minute surgery"
            description = "Low likelihood of prolonged surgery"
            planning = "Standard operative scheduling suitable"
            scheduling = "3 cases per half-day list recommended"
            interpretation = f"CholeS Score {score}: Low risk for prolonged surgery (5.1% chance >90 minutes). Standard scheduling with 3 cases per half-day list is appropriate."
            
        elif score <= 8.0:
            category = "Intermediate Risk"
            probability = "5.1-41.8% chance of >90-minute surgery"
            description = "Moderate likelihood of prolonged surgery"
            planning = "Consider operative complexity in scheduling"
            scheduling = "2-3 cases per half-day list based on total risk profile"
            interpretation = f"CholeS Score {score}: Intermediate risk for prolonged surgery (5.1-41.8% chance >90 minutes). Consider scheduling 2-3 cases per half-day list based on case complexity."
            
        else:  # score > 8.0
            category = "High Risk"
            probability = ">41.8% chance of >90-minute surgery"
            description = "High likelihood of prolonged surgery"
            planning = "Anticipate complex surgery with potential complications"
            scheduling = "Maximum 2 cases per half-day list to avoid overruns"
            interpretation = f"CholeS Score {score}: High risk for prolonged surgery (>41.8% chance >90 minutes). Schedule maximum 2 cases per half-day list to prevent theatre overruns."
        
        return {
            "category": category,
            "probability": probability,
            "description": description,
            "planning": planning,
            "scheduling": scheduling,
            "interpretation": interpretation
        }
    
    def _get_scoring_breakdown(self, age, age_pts, gender, gender_pts, indication, indication_pts,
                             bmi, bmi_pts, cbd_diameter, cbd_pts, gallbladder_wall, gb_wall_pts,
                             preoperative_ct, ct_pts, planned_cholangiogram, cholangiogram_pts,
                             admissions, admissions_pts, asa, asa_pts):
        """Provides detailed scoring breakdown"""
        
        # Format descriptions
        age_desc = f"Age {age} years ({'≥40' if age >= 40 else '<40'})"
        bmi_desc = f"BMI {bmi} kg/m² ({'<25' if bmi < 25 else '25-35' if bmi <= 35 else '>35'})"
        admissions_desc = f"{admissions} previous admissions ({'0' if admissions == 0 else '1-2' if admissions <= 2 else '>2'})"
        asa_desc = f"ASA Grade {asa} ({'1' if asa == 1 else '2' if asa == 2 else '≥3'})"
        
        indication_mapping = {
            "pancreatitis": "Pancreatitis",
            "colic_dyskinesia_polyp": "Colic/Dyskinesia/Polyp",
            "cbd_stone": "Common bile duct stone",
            "acalculous_cholecystitis": "Acalculous/Cholecystitis"
        }
        
        breakdown = {
            "component_scores": {
                "age": {
                    "value": age,
                    "category": age_desc,
                    "points": age_pts,
                    "description": "Patient age factor"
                },
                "gender": {
                    "value": gender.capitalize(),
                    "points": gender_pts,
                    "description": "Gender factor (male higher risk)"
                },
                "indication": {
                    "value": indication_mapping[indication],
                    "points": indication_pts,
                    "description": "Surgical indication complexity"
                },
                "bmi": {
                    "value": bmi,
                    "unit": "kg/m²",
                    "category": bmi_desc,
                    "points": bmi_pts,
                    "description": "Body Mass Index"
                },
                "cbd_diameter": {
                    "value": cbd_diameter.capitalize(),
                    "points": cbd_pts,
                    "description": "Common bile duct diameter"
                },
                "gallbladder_wall": {
                    "value": gallbladder_wall.capitalize(),
                    "points": gb_wall_pts,
                    "description": "Gallbladder wall thickness"
                },
                "preoperative_ct": {
                    "value": preoperative_ct.upper(),
                    "points": ct_pts,
                    "description": "Pre-operative CT scan performed"
                },
                "planned_cholangiogram": {
                    "value": planned_cholangiogram.upper(),
                    "points": cholangiogram_pts,
                    "description": "Planned intra-operative cholangiogram"
                },
                "previous_admissions": {
                    "value": admissions,
                    "category": admissions_desc,
                    "points": admissions_pts,
                    "description": "Number of previous surgical admissions"
                },
                "asa_grade": {
                    "value": asa,
                    "category": asa_desc,
                    "points": asa_pts,
                    "description": "ASA Physical Status Classification"
                }
            },
            "clinical_context": {
                "development": "Based on CholeS study (8,820 patients, 166 UK hospitals)",
                "validation": "Area under ROC curve: 0.708 for >90 minute prediction",
                "application": "Elective laparoscopic cholecystectomy only",
                "limitations": "Not validated for emergency or acute procedures",
                "score_range": "0.5-17.5 points (median 5.0)"
            },
            "operative_planning": {
                "purpose": "Optimize theatre scheduling and resource allocation",
                "low_risk": "≤3.5 points: 3 cases per half-day list",
                "intermediate_risk": "4-8 points: 2-3 cases per half-day list",
                "high_risk": ">8 points: Maximum 2 cases per half-day list",
                "considerations": "Does not include anesthesia time or theatre turnover"
            }
        }
        
        return breakdown


def calculate_choles_score(
    age: int,
    gender: str,
    indication: str,
    bmi: float,
    cbd_diameter: str,
    gallbladder_wall: str,
    preoperative_ct: str,
    planned_cholangiogram: str,
    previous_admissions: int,
    asa_grade: int
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CholesScorecalculator()
    return calculator.calculate(
        age=age,
        gender=gender,
        indication=indication,
        bmi=bmi,
        cbd_diameter=cbd_diameter,
        gallbladder_wall=gallbladder_wall,
        preoperative_ct=preoperative_ct,
        planned_cholangiogram=planned_cholangiogram,
        previous_admissions=previous_admissions,
        asa_grade=asa_grade
    )