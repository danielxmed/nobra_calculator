"""
Cytokine Release Syndrome (CRS) Grading Calculator

Assesses severity of cytokine release syndrome in immunotherapy patients,
particularly those receiving CAR-T cell therapy and other immune effector 
cell therapies.

References:
- Lee DW, Santomasso BD, Locke FL, et al. Biol Blood Marrow Transplant. 2019;25(4):625-638.
- Porter D, Frey N, Wood PA, et al. J Hematol Oncol. 2018;11(1):35.
- Neelapu SS, Tummala S, Kebriaei P, et al. Nat Rev Clin Oncol. 2018;15(1):47-62.
"""

from typing import Dict, Any, Optional


class CrsGradingCalculator:
    """Calculator for Cytokine Release Syndrome (CRS) Grading"""
    
    def __init__(self):
        # CRS grade definitions based on ASTCT criteria
        self.CRS_GRADES = {
            1: {
                "label": "Grade 1 - Mild",
                "description": "Mild symptoms",
                "severity": "mild",
                "intervention": "symptomatic"
            },
            2: {
                "label": "Grade 2 - Moderate", 
                "description": "Moderate intervention required",
                "severity": "moderate",
                "intervention": "supportive"
            },
            3: {
                "label": "Grade 3 - Severe",
                "description": "Aggressive intervention required",
                "severity": "severe", 
                "intervention": "aggressive"
            },
            4: {
                "label": "Grade 4 - Life-threatening",
                "description": "Life-threatening symptoms",
                "severity": "life_threatening",
                "intervention": "intensive"
            },
            5: {
                "label": "Grade 5 - Death",
                "description": "Death related to CRS",
                "severity": "fatal",
                "intervention": "none"
            }
        }
        
        # Treatment recommendations by grade
        self.TREATMENT_RECOMMENDATIONS = {
            1: [
                "Supportive care with symptomatic treatment",
                "Monitor vital signs and symptoms closely",
                "Adequate hydration and fever management",
                "No specific anti-cytokine therapy required"
            ],
            2: [
                "Vigilant supportive care with close monitoring",
                "Consider tocilizumab if extensive comorbidities present",
                "Fluid management and low-dose vasopressors if needed",
                "Monitor for progression to higher grades"
            ],
            3: [
                "Aggressive supportive care, often requiring ICU",
                "Tocilizumab ± corticosteroids recommended",
                "High-dose or multiple vasopressors as needed",
                "Consider corticosteroids if no improvement at 24 hours"
            ],
            4: [
                "Intensive care management mandatory",
                "Immediate tocilizumab and corticosteroids",
                "Mechanical ventilation and advanced organ support",
                "Multidisciplinary critical care approach"
            ],
            5: [
                "Palliative care and family support",
                "Documentation for research and quality improvement",
                "Root cause analysis of treatment course"
            ]
        }
    
    def calculate(self, fever_present: str, hypotension_status: str, oxygen_requirement: str,
                  organ_toxicity_grade: int, patient_age: Optional[int] = None,
                  comorbidities_present: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates CRS grade based on clinical parameters
        
        Args:
            fever_present (str): "yes" or "no" for fever ≥38°C or suppressed by therapy
            hypotension_status (str): Hypotension status and intervention needs
            oxygen_requirement (str): Oxygen support requirements
            organ_toxicity_grade (int): Highest CTCAE grade of organ toxicity (0-4)
            patient_age (int, optional): Patient age in years
            comorbidities_present (str, optional): "yes", "no", or "unknown"
            
        Returns:
            Dict with CRS grade, severity assessment, and management recommendations
        """
        
        # Validations
        self._validate_inputs(fever_present, hypotension_status, oxygen_requirement,
                            organ_toxicity_grade, patient_age, comorbidities_present)
        
        # Determine CRS grade using ASTCT criteria
        crs_grade = self._calculate_crs_grade(fever_present, hypotension_status,
                                            oxygen_requirement, organ_toxicity_grade)
        
        # Get grade details
        grade_details = self.CRS_GRADES[crs_grade]
        
        # Generate clinical assessment
        clinical_assessment = self._get_clinical_assessment(crs_grade, hypotension_status,
                                                          oxygen_requirement, organ_toxicity_grade)
        
        # Get management recommendations
        management = self._get_management_recommendations(crs_grade, patient_age,
                                                        comorbidities_present)
        
        # Generate interpretation
        interpretation = self._get_interpretation(crs_grade, clinical_assessment)
        
        # Get monitoring requirements
        monitoring = self._get_monitoring_requirements(crs_grade)
        
        return {
            "result": crs_grade,
            "unit": "CRS grade",
            "interpretation": interpretation,
            "stage": grade_details["label"],
            "stage_description": grade_details["description"],
            "crs_grade": crs_grade,
            "severity_level": grade_details["severity"],
            "intervention_type": grade_details["intervention"],
            "clinical_assessment": clinical_assessment,
            "management_recommendations": management,
            "monitoring_requirements": monitoring,
            "treatment_urgency": self._get_treatment_urgency(crs_grade),
            "prognosis": self._get_prognosis_assessment(crs_grade, organ_toxicity_grade),
            "care_setting": self._determine_care_setting(crs_grade)
        }
    
    def _validate_inputs(self, fever_present, hypotension_status, oxygen_requirement,
                        organ_toxicity_grade, patient_age, comorbidities_present):
        """Validates input parameters"""
        
        # Validate fever_present
        if fever_present not in ["yes", "no"]:
            raise ValueError("fever_present must be 'yes' or 'no'")
        
        # Validate hypotension_status
        valid_hypotension = ["none", "responsive_to_fluids", "low_dose_single_pressor",
                           "high_dose_multiple_pressors"]
        if hypotension_status not in valid_hypotension:
            raise ValueError(f"hypotension_status must be one of: {valid_hypotension}")
        
        # Validate oxygen_requirement
        valid_oxygen = ["none", "low_flow_oxygen", "high_flow_oxygen_40_plus",
                       "ventilator_required"]
        if oxygen_requirement not in valid_oxygen:
            raise ValueError(f"oxygen_requirement must be one of: {valid_oxygen}")
        
        # Validate organ_toxicity_grade
        if not isinstance(organ_toxicity_grade, int) or not 0 <= organ_toxicity_grade <= 4:
            raise ValueError("organ_toxicity_grade must be an integer between 0 and 4")
        
        # Validate optional parameters
        if patient_age is not None:
            if not isinstance(patient_age, int) or not 0 <= patient_age <= 120:
                raise ValueError("patient_age must be an integer between 0 and 120")
        
        if comorbidities_present is not None:
            if comorbidities_present not in ["yes", "no", "unknown"]:
                raise ValueError("comorbidities_present must be 'yes', 'no', or 'unknown'")
    
    def _calculate_crs_grade(self, fever_present, hypotension_status, oxygen_requirement,
                           organ_toxicity_grade):
        """Calculates CRS grade using ASTCT criteria"""
        
        # Grade 1 requires fever (unless suppressed by therapy)
        if fever_present == "no":
            # If no fever and no other symptoms, consider Grade 0 (not CRS)
            if (hypotension_status == "none" and oxygen_requirement == "none" and 
                organ_toxicity_grade == 0):
                return 1  # Return Grade 1 as minimum for this calculator
        
        # Determine grade based on severity indicators
        hypotension_grade = self._get_hypotension_grade(hypotension_status)
        oxygen_grade = self._get_oxygen_grade(oxygen_requirement)
        organ_grade = self._get_organ_toxicity_crs_grade(organ_toxicity_grade)
        
        # CRS grade is the maximum of all severity indicators
        max_grade = max(hypotension_grade, oxygen_grade, organ_grade)
        
        # Minimum grade is 1 if any symptoms present
        if fever_present == "yes" or max_grade > 0:
            return max(1, max_grade)
        
        return 1  # Default minimum grade
    
    def _get_hypotension_grade(self, hypotension_status):
        """Convert hypotension status to CRS grade component"""
        
        hypotension_grades = {
            "none": 0,
            "responsive_to_fluids": 2,
            "low_dose_single_pressor": 2,
            "high_dose_multiple_pressors": 3
        }
        
        return hypotension_grades.get(hypotension_status, 0)
    
    def _get_oxygen_grade(self, oxygen_requirement):
        """Convert oxygen requirement to CRS grade component"""
        
        oxygen_grades = {
            "none": 0,
            "low_flow_oxygen": 2,
            "high_flow_oxygen_40_plus": 3,
            "ventilator_required": 4
        }
        
        return oxygen_grades.get(oxygen_requirement, 0)
    
    def _get_organ_toxicity_crs_grade(self, organ_toxicity_grade):
        """Convert organ toxicity grade to CRS grade component"""
        
        # Grade 4 transaminitis is considered Grade 3 CRS per ASTCT criteria
        if organ_toxicity_grade == 4:
            # Assume this is transaminitis and map to Grade 3 CRS
            # In practice, this would need clinical context
            return 3
        elif organ_toxicity_grade == 3:
            return 3
        elif organ_toxicity_grade == 2:
            return 2
        else:
            return 0
    
    def _get_clinical_assessment(self, crs_grade, hypotension_status, oxygen_requirement,
                                organ_toxicity_grade):
        """Generate clinical assessment based on parameters"""
        
        assessment = {
            "crs_grade": crs_grade,
            "severity_indicators": [],
            "risk_factors": [],
            "clinical_features": []
        }
        
        # Document severity indicators
        if hypotension_status != "none":
            assessment["severity_indicators"].append(f"Hypotension: {hypotension_status}")
        
        if oxygen_requirement != "none":
            assessment["severity_indicators"].append(f"Oxygen requirement: {oxygen_requirement}")
        
        if organ_toxicity_grade > 0:
            assessment["severity_indicators"].append(f"Organ toxicity: Grade {organ_toxicity_grade}")
        
        # Clinical features by grade
        if crs_grade == 1:
            assessment["clinical_features"] = ["Fever", "Constitutional symptoms", "Mild discomfort"]
        elif crs_grade == 2:
            assessment["clinical_features"] = ["Moderate symptoms", "Cardiovascular involvement", "Respiratory involvement"]
        elif crs_grade >= 3:
            assessment["clinical_features"] = ["Severe systemic symptoms", "Multi-organ involvement", "Hemodynamic instability"]
        
        return assessment
    
    def _get_management_recommendations(self, crs_grade, patient_age, comorbidities_present):
        """Get management recommendations based on CRS grade and risk factors"""
        
        base_recommendations = self.TREATMENT_RECOMMENDATIONS.get(crs_grade, [])
        additional_recommendations = []
        
        # Age-based considerations
        if patient_age is not None:
            if patient_age < 18:
                additional_recommendations.append("Pediatric oncology consultation recommended")
            elif patient_age > 65:
                additional_recommendations.append("Consider increased monitoring due to advanced age")
        
        # Comorbidity considerations
        if comorbidities_present == "yes":
            if crs_grade >= 2:
                additional_recommendations.append("Lower threshold for tocilizumab due to comorbidities")
            additional_recommendations.append("Coordinate care with relevant specialists")
        
        # Specific medication recommendations
        if crs_grade >= 2:
            additional_recommendations.append("Consider tocilizumab 8 mg/kg IV (max 800 mg)")
        
        if crs_grade >= 3:
            additional_recommendations.append("Consider corticosteroids (methylprednisolone 1-2 mg/kg/day)")
        
        return {
            "primary_interventions": base_recommendations,
            "additional_considerations": additional_recommendations,
            "medication_options": self._get_medication_options(crs_grade),
            "monitoring_frequency": self._get_monitoring_frequency(crs_grade)
        }
    
    def _get_medication_options(self, crs_grade):
        """Get medication options by CRS grade"""
        
        if crs_grade == 1:
            return ["Acetaminophen/paracetamol for fever", "Adequate hydration", "Symptomatic care"]
        elif crs_grade == 2:
            return ["Tocilizumab (consider if comorbidities)", "IV fluids", "Low-dose vasopressors if needed"]
        elif crs_grade >= 3:
            return ["Tocilizumab 8 mg/kg IV", "Corticosteroids (methylprednisolone)", "High-dose vasopressors", "Advanced organ support"]
        
        return []
    
    def _get_monitoring_frequency(self, crs_grade):
        """Get monitoring frequency recommendations"""
        
        if crs_grade == 1:
            return "Every 4-8 hours"
        elif crs_grade == 2:
            return "Every 2-4 hours"
        elif crs_grade >= 3:
            return "Continuous monitoring in ICU setting"
        
        return "As clinically indicated"
    
    def _get_monitoring_requirements(self, crs_grade):
        """Get monitoring requirements by CRS grade"""
        
        base_monitoring = ["Vital signs", "Temperature", "Oxygen saturation", "Mental status"]
        
        if crs_grade >= 2:
            base_monitoring.extend(["Blood pressure", "Urine output", "Laboratory studies"])
        
        if crs_grade >= 3:
            base_monitoring.extend(["Cardiac monitoring", "Arterial blood gas", "Lactate levels",
                                  "Organ function tests", "Coagulation studies"])
        
        return {
            "parameters": base_monitoring,
            "frequency": self._get_monitoring_frequency(crs_grade),
            "laboratory_studies": self._get_laboratory_monitoring(crs_grade)
        }
    
    def _get_laboratory_monitoring(self, crs_grade):
        """Get laboratory monitoring recommendations"""
        
        if crs_grade == 1:
            return ["Basic metabolic panel", "Complete blood count"]
        elif crs_grade == 2:
            return ["Comprehensive metabolic panel", "Complete blood count", "Liver function tests",
                   "Inflammatory markers (CRP, IL-6 if available)"]
        elif crs_grade >= 3:
            return ["Comprehensive metabolic panel", "Complete blood count", "Liver function tests",
                   "Coagulation studies", "Arterial blood gas", "Lactate", "Troponin",
                   "Inflammatory markers", "Cultures if infection suspected"]
        
        return []
    
    def _get_treatment_urgency(self, crs_grade):
        """Determine treatment urgency based on CRS grade"""
        
        urgency_levels = {
            1: "Routine - symptomatic care",
            2: "Urgent - close monitoring required",
            3: "Emergent - immediate intervention needed",
            4: "Critical - life-threatening, immediate ICU care",
            5: "Terminal - comfort care"
        }
        
        return urgency_levels.get(crs_grade, "Unknown")
    
    def _get_prognosis_assessment(self, crs_grade, organ_toxicity_grade):
        """Assess prognosis based on CRS grade and organ involvement"""
        
        if crs_grade == 1:
            return {"outlook": "Excellent", "description": "Expected full recovery with supportive care"}
        elif crs_grade == 2:
            return {"outlook": "Good", "description": "Good prognosis with appropriate management"}
        elif crs_grade == 3:
            return {"outlook": "Guarded", "description": "Requires intensive management, variable outcome"}
        elif crs_grade == 4:
            return {"outlook": "Poor", "description": "Life-threatening condition with significant morbidity risk"}
        else:
            return {"outlook": "Terminal", "description": "Death attributable to CRS"}
    
    def _determine_care_setting(self, crs_grade):
        """Determine appropriate care setting based on CRS grade"""
        
        care_settings = {
            1: "Inpatient ward with oncology monitoring",
            2: "Inpatient ward with enhanced monitoring or step-down unit",
            3: "Intensive care unit (ICU)",
            4: "Intensive care unit (ICU) with advanced life support",
            5: "Comfort care setting"
        }
        
        return care_settings.get(crs_grade, "Appropriate clinical setting")
    
    def _get_interpretation(self, crs_grade, clinical_assessment):
        """Get comprehensive interpretation of CRS assessment"""
        
        grade_info = self.CRS_GRADES[crs_grade]
        
        base_interpretation = (f"CRS Grade {crs_grade} ({grade_info['label']}) indicates "
                             f"{grade_info['description'].lower()}.")
        
        if crs_grade == 1:
            return (f"{base_interpretation} Patient has mild constitutional symptoms requiring only "
                   f"symptomatic treatment. Prognosis is excellent with supportive care.")
        
        elif crs_grade == 2:
            return (f"{base_interpretation} Patient requires moderate intervention with close monitoring. "
                   f"Consider tocilizumab if comorbidities present. Good prognosis with appropriate management.")
        
        elif crs_grade == 3:
            return (f"{base_interpretation} Patient requires aggressive intervention, often in ICU setting. "
                   f"Tocilizumab and corticosteroids recommended. Prognosis is guarded and requires intensive management.")
        
        elif crs_grade == 4:
            return (f"{base_interpretation} Patient has life-threatening condition requiring immediate "
                   f"intensive care. Immediate tocilizumab, corticosteroids, and advanced organ support needed. "
                   f"Prognosis is poor with significant morbidity risk.")
        
        else:
            return (f"{base_interpretation} Death directly attributable to cytokine release syndrome "
                   f"despite all therapeutic interventions.")


def calculate_crs_grading(fever_present: str, hypotension_status: str, oxygen_requirement: str,
                         organ_toxicity_grade: int, patient_age: Optional[int] = None,
                         comorbidities_present: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CrsGradingCalculator()
    return calculator.calculate(fever_present, hypotension_status, oxygen_requirement,
                              organ_toxicity_grade, patient_age, comorbidities_present)