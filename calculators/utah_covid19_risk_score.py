"""
Utah COVID-19 Risk Score Calculator

Identifies high-risk individuals appropriate for COVID-19 treatment and helps prioritize 
oral antiviral treatment during medication shortages.

References:
1. Utah Department of Health. COVID-19 Treatment Risk Score Calculator. Updated February 2022. 
   Available at: https://coronavirus.utah.gov/
2. Intermountain Healthcare. Utah COVID-19 Risk Assessment for Treatment Prioritization. 2022.
3. Centers for Disease Control and Prevention. Emergency Use Authorization for COVID-19 Treatments. 
   Updated 2022.
"""

from typing import Dict, Any


class UtahCovid19RiskScoreCalculator:
    """Calculator for Utah COVID-19 Risk Score"""
    
    def __init__(self):
        # Age points mapping
        self.AGE_POINTS = {
            (16, 20): 1.0,
            (21, 30): 1.5,
            (31, 40): 2.0,
            (41, 50): 2.5,
            (51, 60): 3.0,
            (61, 70): 3.5,
            (71, 80): 4.0,
            (81, 90): 4.5,
            (91, 100): 5.0,
            (101, 120): 5.5
        }
        
        # Highest risk comorbidities (2 points each)
        self.HIGHEST_RISK_CONDITIONS = {
            "diabetes_mellitus": 2.0,
            "obesity": 2.0
        }
        
        # Other high-risk comorbidities (1 point each)
        self.HIGH_RISK_CONDITIONS = {
            "active_cancer": 1.0,
            "immunosuppressive_therapies": 1.0,
            "hypertension": 1.0,
            "coronary_artery_disease": 1.0,
            "cardiac_arrhythmia": 1.0,
            "congestive_heart_failure": 1.0,
            "chronic_kidney_disease": 1.0,
            "chronic_pulmonary_disease": 1.0,
            "chronic_liver_disease": 1.0,
            "cerebrovascular_disease": 1.0,
            "chronic_neurologic_disease": 1.0
        }
        
        # Symptom risk factors
        self.SYMPTOM_POINTS = {
            "shortness_of_breath": 1.0
        }
        
        # Treatment thresholds based on vaccination status
        self.TREATMENT_THRESHOLDS = {
            "vaccinated": 8.0,
            "unvaccinated_not_pregnant": 6.0,
            "unvaccinated_pregnant": 4.0
        }
    
    def calculate(self, age: int, diabetes_mellitus: str, obesity: str, active_cancer: str,
                 immunosuppressive_therapies: str, hypertension: str, coronary_artery_disease: str,
                 cardiac_arrhythmia: str, congestive_heart_failure: str, chronic_kidney_disease: str,
                 chronic_pulmonary_disease: str, chronic_liver_disease: str, cerebrovascular_disease: str,
                 chronic_neurologic_disease: str, shortness_of_breath: str, vaccination_status: str) -> Dict[str, Any]:
        """
        Calculates Utah COVID-19 Risk Score and treatment eligibility
        
        Args:
            age (int): Patient age in years
            diabetes_mellitus (str): Diabetes mellitus present
            obesity (str): Obesity (BMI >30) present
            active_cancer (str): Active cancer present
            immunosuppressive_therapies (str): Immunosuppressive therapies present
            hypertension (str): Hypertension present
            coronary_artery_disease (str): Coronary artery disease present
            cardiac_arrhythmia (str): Cardiac arrhythmia present
            congestive_heart_failure (str): Congestive heart failure present
            chronic_kidney_disease (str): Chronic kidney disease present
            chronic_pulmonary_disease (str): Chronic pulmonary disease present
            chronic_liver_disease (str): Chronic liver disease present
            cerebrovascular_disease (str): Cerebrovascular disease present
            chronic_neurologic_disease (str): Chronic neurologic disease present
            shortness_of_breath (str): New shortness of breath present
            vaccination_status (str): COVID-19 vaccination status
            
        Returns:
            Dict with Utah COVID-19 Risk Score and treatment recommendation
        """
        
        # Validate inputs
        self._validate_inputs(age, diabetes_mellitus, obesity, active_cancer, immunosuppressive_therapies,
                            hypertension, coronary_artery_disease, cardiac_arrhythmia, congestive_heart_failure,
                            chronic_kidney_disease, chronic_pulmonary_disease, chronic_liver_disease,
                            cerebrovascular_disease, chronic_neurologic_disease, shortness_of_breath, vaccination_status)
        
        # Calculate age points
        age_points = self._calculate_age_points(age)
        
        # Calculate comorbidity points
        comorbidity_points = self._calculate_comorbidity_points(
            diabetes_mellitus, obesity, active_cancer, immunosuppressive_therapies, hypertension,
            coronary_artery_disease, cardiac_arrhythmia, congestive_heart_failure, chronic_kidney_disease,
            chronic_pulmonary_disease, chronic_liver_disease, cerebrovascular_disease, chronic_neurologic_disease
        )
        
        # Calculate symptom points
        symptom_points = self._calculate_symptom_points(shortness_of_breath)
        
        # Calculate total score
        total_score = age_points + comorbidity_points + symptom_points
        
        # Determine treatment eligibility
        treatment_recommendation = self._determine_treatment_eligibility(total_score, vaccination_status)
        
        # Generate interpretation
        interpretation = self._generate_interpretation(total_score, vaccination_status, treatment_recommendation)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": treatment_recommendation["stage"],
            "stage_description": treatment_recommendation["description"],
            "treatment_eligible": treatment_recommendation["eligible"],
            "threshold_score": self.TREATMENT_THRESHOLDS[vaccination_status],
            "vaccination_status": vaccination_status,
            "component_scores": {
                "age_points": age_points,
                "comorbidity_points": comorbidity_points,
                "symptom_points": symptom_points
            },
            "clinical_recommendations": interpretation["clinical_recommendations"],
            "important_considerations": interpretation["important_considerations"]
        }
    
    def _validate_inputs(self, age: int, *conditions):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 16 or age > 120:
            raise ValueError("Age must be between 16 and 120 years")
        
        valid_yes_no = ["yes", "no"]
        valid_vaccination = ["vaccinated", "unvaccinated_not_pregnant", "unvaccinated_pregnant"]
        
        # Check all yes/no conditions (all except vaccination_status)
        for condition in conditions[:-1]:  # All except last (vaccination_status)
            if condition not in valid_yes_no:
                raise ValueError(f"Condition values must be one of: {valid_yes_no}")
        
        # Check vaccination status
        vaccination_status = conditions[-1]
        if vaccination_status not in valid_vaccination:
            raise ValueError(f"Vaccination status must be one of: {valid_vaccination}")
    
    def _calculate_age_points(self, age: int) -> float:
        """Calculates points based on age"""
        
        for (min_age, max_age), points in self.AGE_POINTS.items():
            if min_age <= age <= max_age:
                return points
        
        # Default case (shouldn't reach here with proper validation)
        return 0.0
    
    def _calculate_comorbidity_points(self, diabetes_mellitus: str, obesity: str, active_cancer: str,
                                    immunosuppressive_therapies: str, hypertension: str, coronary_artery_disease: str,
                                    cardiac_arrhythmia: str, congestive_heart_failure: str, chronic_kidney_disease: str,
                                    chronic_pulmonary_disease: str, chronic_liver_disease: str, cerebrovascular_disease: str,
                                    chronic_neurologic_disease: str) -> float:
        """Calculates points for comorbidities"""
        
        total_points = 0.0
        
        # Highest risk conditions (2 points each)
        if diabetes_mellitus == "yes":
            total_points += self.HIGHEST_RISK_CONDITIONS["diabetes_mellitus"]
        if obesity == "yes":
            total_points += self.HIGHEST_RISK_CONDITIONS["obesity"]
        
        # Other high-risk conditions (1 point each)
        conditions = [
            active_cancer, immunosuppressive_therapies, hypertension, coronary_artery_disease,
            cardiac_arrhythmia, congestive_heart_failure, chronic_kidney_disease, chronic_pulmonary_disease,
            chronic_liver_disease, cerebrovascular_disease, chronic_neurologic_disease
        ]
        
        for condition in conditions:
            if condition == "yes":
                total_points += 1.0
        
        return total_points
    
    def _calculate_symptom_points(self, shortness_of_breath: str) -> float:
        """Calculates points for symptoms"""
        
        if shortness_of_breath == "yes":
            return self.SYMPTOM_POINTS["shortness_of_breath"]
        return 0.0
    
    def _determine_treatment_eligibility(self, total_score: float, vaccination_status: str) -> Dict[str, Any]:
        """Determines treatment eligibility based on score and vaccination status"""
        
        threshold = self.TREATMENT_THRESHOLDS[vaccination_status]
        
        if total_score >= threshold:
            return {
                "eligible": True,
                "stage": "Treatment Eligible",
                "description": "Qualifies for COVID-19 treatment"
            }
        else:
            return {
                "eligible": False,
                "stage": "Treatment Not Eligible",
                "description": "Does not meet treatment criteria"
            }
    
    def _generate_interpretation(self, total_score: float, vaccination_status: str, 
                               treatment_recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Generates clinical interpretation and recommendations"""
        
        threshold = self.TREATMENT_THRESHOLDS[vaccination_status]
        
        # Base interpretation
        if treatment_recommendation["eligible"]:
            interpretation = (f"Utah COVID-19 Risk Score: {total_score} points. Patient qualifies for "
                            f"COVID-19 antiviral treatment ({vaccination_status} threshold: ≥{threshold} points). "
                            f"Consider oral antivirals if within 10 days of symptom onset.")
            
            clinical_recommendations = {
                "immediate_actions": [
                    "Consider oral antiviral therapy (nirmatrelvir-ritonavir or molnupiravir)",
                    "Ensure treatment initiation within 10 days of symptom onset",
                    "Review contraindications and drug interactions",
                    "Monitor for treatment response and adverse effects"
                ],
                "treatment_options": [
                    "Nirmatrelvir-ritonavir (Paxlovid) - preferred if no contraindications",
                    "Molnupiravir - alternative option",
                    "Bebtelovimab - if oral antivirals contraindicated or unavailable"
                ],
                "monitoring": [
                    "Daily symptom assessment",
                    "Monitor for clinical deterioration",
                    "Follow up in 5-7 days or sooner if symptoms worsen",
                    "Complete isolation per current CDC guidelines"
                ]
            }
        else:
            interpretation = (f"Utah COVID-19 Risk Score: {total_score} points. Patient does not meet "
                            f"current criteria for COVID-19 antiviral treatment ({vaccination_status} threshold: "
                            f"≥{threshold} points). Continue supportive care and monitor for symptom progression.")
            
            clinical_recommendations = {
                "immediate_actions": [
                    "Continue supportive care (rest, hydration, symptom management)",
                    "Monitor for symptom progression or deterioration",
                    "Educate on warning signs requiring medical attention",
                    "Ensure appropriate isolation measures"
                ],
                "monitoring": [
                    "Daily symptom monitoring",
                    "Return if symptoms worsen (shortness of breath, chest pain, confusion)",
                    "Re-evaluate if new high-risk symptoms develop",
                    "Complete isolation per current CDC guidelines"
                ],
                "considerations": [
                    "Score may change if new symptoms or comorbidities develop",
                    "Individual clinical judgment may override score recommendations",
                    "Consider treatment if patient deteriorates despite supportive care"
                ]
            }
        
        # Important considerations
        important_considerations = {
            "timing": "Treatment must be initiated within 10 days of symptom onset for maximum effectiveness",
            "limitations": [
                "Calculator developed during COVID-19 crisis and not externally validated",
                "Should complement clinical judgment, not replace comprehensive evaluation",
                "Local resource availability may affect treatment thresholds"
            ],
            "contraindications": [
                "Check for drug interactions, especially with nirmatrelvir-ritonavir",
                "Consider renal and hepatic function for dosing adjustments",
                "Review patient allergies and previous adverse reactions"
            ],
            "special_populations": [
                "Pregnancy: unvaccinated pregnant patients have lower threshold (≥4 points)",
                "Immunocompromised: may need individualized assessment",
                "Elderly: often qualify based on age alone"
            ]
        }
        
        return {
            "interpretation": interpretation,
            "clinical_recommendations": clinical_recommendations,
            "important_considerations": important_considerations
        }


def calculate_utah_covid19_risk_score(age, diabetes_mellitus, obesity, active_cancer, immunosuppressive_therapies,
                                     hypertension, coronary_artery_disease, cardiac_arrhythmia, congestive_heart_failure,
                                     chronic_kidney_disease, chronic_pulmonary_disease, chronic_liver_disease,
                                     cerebrovascular_disease, chronic_neurologic_disease, shortness_of_breath,
                                     vaccination_status) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_utah_covid19_risk_score pattern
    """
    calculator = UtahCovid19RiskScoreCalculator()
    return calculator.calculate(age, diabetes_mellitus, obesity, active_cancer, immunosuppressive_therapies,
                              hypertension, coronary_artery_disease, cardiac_arrhythmia, congestive_heart_failure,
                              chronic_kidney_disease, chronic_pulmonary_disease, chronic_liver_disease,
                              cerebrovascular_disease, chronic_neurologic_disease, shortness_of_breath,
                              vaccination_status)