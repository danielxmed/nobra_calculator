"""
Common Terminology Criteria for Adverse Events (CTCAE) v5.0 Calculator

Grades severity of hematologic and lymphatic adverse events from cancer treatment 
according to standardized National Cancer Institute criteria.

References:
1. National Cancer Institute. Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0. 
   Published: November 27, 2017. U.S. Department of Health and Human Services, National Institutes 
   of Health, National Cancer Institute.
2. Freites-Martinez A, Santana N, Arias-Santiago S, Viera A. Using the Common Terminology Criteria 
   for Adverse Events (CTCAE - Version 5.0) to Evaluate the Severity of Adverse Events of Anticancer 
   Therapies. Actas Dermosifiliogr (Engl Ed). 2021 Feb;112(2):90-92.
3. Basch E, Reeve BB, Mitchell SA, et al. Development of the National Cancer Institute's patient-reported 
   outcomes version of the common terminology criteria for adverse events (PRO-CTCAE). J Natl Cancer Inst. 
   2014;106(9):dju244.
"""

from typing import Dict, Any, Optional


class CtcaeCalculator:
    """Calculator for Common Terminology Criteria for Adverse Events (CTCAE) v5.0"""
    
    def __init__(self):
        # Normal reference ranges by sex
        self.NORMAL_RANGES = {
            "hemoglobin": {
                "male": {"min": 14.0, "max": 18.0},      # g/dL
                "female": {"min": 12.0, "max": 16.0}     # g/dL
            },
            "neutrophil": {"min": 1500, "max": 8000},    # cells/mm³
            "platelet": {"min": 150000, "max": 450000},   # cells/mm³
            "wbc": {"min": 4000, "max": 11000},          # cells/mm³
            "lymphocyte": {"min": 1000, "max": 4000}     # cells/mm³
        }
        
        # CTCAE v5.0 Grading Criteria for Hematologic Adverse Events
        self.GRADING_CRITERIA = {
            "anemia": {
                "grade_1": {"male": {"min": 10.0, "max": 13.9}, "female": {"min": 10.0, "max": 11.9}},
                "grade_2": {"min": 8.0, "max": 9.9},
                "grade_3": {"min": 6.5, "max": 7.9, "requires_transfusion": True},
                "grade_4": {"max": 6.4}
            },
            "neutropenia": {
                "grade_1": {"min": 1000, "max": 1499},  # <LLN - 1500/mm³
                "grade_2": {"min": 500, "max": 999},    # <1500 - 1000/mm³  
                "grade_3": {"min": 200, "max": 499},    # <1.0 - 0.5 x 10⁹/L
                "grade_4": {"max": 199}                 # <0.5 x 10⁹/L
            },
            "thrombocytopenia": {
                "grade_1": {"min": 75000, "max": 149999},   # <LLN - 75,000/mm³
                "grade_2": {"min": 50000, "max": 74999},    # <75,000 - 50,000/mm³
                "grade_3": {"min": 25000, "max": 49999},    # <50,000 - 25,000/mm³
                "grade_4": {"max": 24999}                   # <25,000/mm³
            },
            "leukocytosis": {
                "grade_1": {"min": 11001, "max": 20000},    # >ULN - 20,000/mm³
                "grade_2": {"min": 20001, "max": 50000},    # >20,000 - 50,000/mm³
                "grade_3": {"min": 50001, "max": 100000},   # >50,000 - 100,000/mm³
                "grade_4": {"min": 100001}                  # >100,000/mm³
            },
            "lymphopenia": {
                "grade_1": {"min": 800, "max": 999},        # <LLN - 800/mm³
                "grade_2": {"min": 500, "max": 799},        # <800 - 500/mm³
                "grade_3": {"min": 200, "max": 499},        # <500 - 200/mm³
                "grade_4": {"max": 199}                     # <200/mm³
            }
        }
        
        # Febrile neutropenia criteria
        self.FEBRILE_NEUTROPENIA_CRITERIA = {
            "neutrophil_threshold": 1000,  # ANC <1.0 x 10⁹/L
            "temperature_threshold": 38.3,  # Temperature >38.3°C
            "sustained_temperature_threshold": 38.0,  # Or sustained ≥38°C for >1 hour
            "grade": 3  # Febrile neutropenia is always Grade 3
        }
    
    def calculate(
        self,
        adverse_event_type: str,
        patient_sex: str,
        hemoglobin: Optional[float] = None,
        neutrophil_count: Optional[float] = None,
        platelet_count: Optional[float] = None,
        wbc_count: Optional[float] = None,
        lymphocyte_count: Optional[float] = None,
        temperature: Optional[float] = None,
        transfusion_indicated: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Grades adverse events according to CTCAE v5.0 criteria
        
        Args:
            adverse_event_type: Type of adverse event to grade
            patient_sex: Patient biological sex (male/female)
            hemoglobin: Hemoglobin level in g/dL
            neutrophil_count: Absolute neutrophil count in cells/mm³
            platelet_count: Platelet count in cells/mm³
            wbc_count: White blood cell count in cells/mm³
            lymphocyte_count: Absolute lymphocyte count in cells/mm³
            temperature: Body temperature in Celsius
            transfusion_indicated: Whether transfusion is indicated (yes/no)
            
        Returns:
            Dict with CTCAE grade and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            adverse_event_type, patient_sex, hemoglobin, neutrophil_count,
            platelet_count, wbc_count, lymphocyte_count, temperature, transfusion_indicated
        )
        
        # Calculate grade based on adverse event type
        if adverse_event_type == "anemia":
            grade = self._grade_anemia(hemoglobin, patient_sex, transfusion_indicated)
            primary_value = hemoglobin
            unit = "g/dL"
            
        elif adverse_event_type == "neutropenia":
            grade = self._grade_neutropenia(neutrophil_count)
            primary_value = neutrophil_count
            unit = "cells/mm³"
            
        elif adverse_event_type == "thrombocytopenia":
            grade = self._grade_thrombocytopenia(platelet_count)
            primary_value = platelet_count
            unit = "cells/mm³"
            
        elif adverse_event_type == "febrile_neutropenia":
            grade = self._grade_febrile_neutropenia(neutrophil_count, temperature)
            primary_value = {"neutrophil_count": neutrophil_count, "temperature": temperature}
            unit = "composite"
            
        elif adverse_event_type == "leukocytosis":
            grade = self._grade_leukocytosis(wbc_count)
            primary_value = wbc_count
            unit = "cells/mm³"
            
        elif adverse_event_type == "lymphopenia":
            grade = self._grade_lymphopenia(lymphocyte_count)
            primary_value = lymphocyte_count
            unit = "cells/mm³"
            
        else:
            raise ValueError(f"Unsupported adverse event type: {adverse_event_type}")
        
        # Get interpretation
        interpretation = self._get_interpretation(grade, adverse_event_type, primary_value, unit)
        
        # Get clinical recommendations
        recommendations = self._get_clinical_recommendations(grade, adverse_event_type)
        
        return {
            "result": grade,
            "unit": "grade",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "clinical_details": {
                "adverse_event_type": adverse_event_type.replace("_", " ").title(),
                "primary_value": primary_value,
                "value_unit": unit,
                "grade_description": interpretation["grade_description"],
                "clinical_significance": interpretation["clinical_significance"],
                "monitoring_requirements": recommendations["monitoring"],
                "intervention_considerations": recommendations["interventions"],
                "dose_modification_guidance": recommendations["dose_modifications"]
            }
        }
    
    def _validate_inputs(self, adverse_event_type, patient_sex, hemoglobin, neutrophil_count,
                        platelet_count, wbc_count, lymphocyte_count, temperature, transfusion_indicated):
        """Validates input parameters"""
        
        # Validate adverse event type
        valid_types = ["anemia", "neutropenia", "thrombocytopenia", "febrile_neutropenia", 
                      "leukocytosis", "lymphopenia"]
        if adverse_event_type not in valid_types:
            raise ValueError(f"Invalid adverse event type. Must be one of: {valid_types}")
        
        # Validate patient sex
        if patient_sex not in ["male", "female"]:
            raise ValueError("Patient sex must be 'male' or 'female'")
        
        # Validate required parameters for each adverse event type
        if adverse_event_type == "anemia":
            if hemoglobin is None:
                raise ValueError("Hemoglobin level is required for anemia grading")
            if not (0.0 <= hemoglobin <= 25.0):
                raise ValueError("Hemoglobin must be between 0.0 and 25.0 g/dL")
                
        elif adverse_event_type == "neutropenia":
            if neutrophil_count is None:
                raise ValueError("Neutrophil count is required for neutropenia grading")
            if not (0.0 <= neutrophil_count <= 50000.0):
                raise ValueError("Neutrophil count must be between 0.0 and 50,000 cells/mm³")
                
        elif adverse_event_type == "thrombocytopenia":
            if platelet_count is None:
                raise ValueError("Platelet count is required for thrombocytopenia grading")
            if not (0.0 <= platelet_count <= 2000000.0):
                raise ValueError("Platelet count must be between 0.0 and 2,000,000 cells/mm³")
                
        elif adverse_event_type == "febrile_neutropenia":
            if neutrophil_count is None or temperature is None:
                raise ValueError("Both neutrophil count and temperature are required for febrile neutropenia grading")
            if not (0.0 <= neutrophil_count <= 50000.0):
                raise ValueError("Neutrophil count must be between 0.0 and 50,000 cells/mm³")
            if not (30.0 <= temperature <= 45.0):
                raise ValueError("Temperature must be between 30.0 and 45.0°C")
                
        elif adverse_event_type == "leukocytosis":
            if wbc_count is None:
                raise ValueError("WBC count is required for leukocytosis grading")
            if not (0.0 <= wbc_count <= 500000.0):
                raise ValueError("WBC count must be between 0.0 and 500,000 cells/mm³")
                
        elif adverse_event_type == "lymphopenia":
            if lymphocyte_count is None:
                raise ValueError("Lymphocyte count is required for lymphopenia grading")
            if not (0.0 <= lymphocyte_count <= 50000.0):
                raise ValueError("Lymphocyte count must be between 0.0 and 50,000 cells/mm³")
        
        # Validate transfusion indication if provided
        if transfusion_indicated is not None and transfusion_indicated not in ["yes", "no"]:
            raise ValueError("Transfusion indication must be 'yes' or 'no'")
    
    def _grade_anemia(self, hemoglobin: float, patient_sex: str, transfusion_indicated: Optional[str]) -> int:
        """Grades anemia according to CTCAE v5.0 criteria"""
        
        normal_range = self.NORMAL_RANGES["hemoglobin"][patient_sex]
        criteria = self.GRADING_CRITERIA["anemia"]
        
        # Check if within normal limits
        if hemoglobin >= normal_range["min"]:
            return 0
        
        # Grade 4: Life-threatening
        if hemoglobin <= criteria["grade_4"]["max"]:
            return 4
        
        # Grade 3: Severe (may require transfusion)
        if (criteria["grade_3"]["min"] <= hemoglobin <= criteria["grade_3"]["max"]):
            # Grade 3 can be assigned if transfusion is indicated
            if transfusion_indicated == "yes":
                return 3
            # Otherwise treat as Grade 2
            return 2
        
        # Grade 2: Moderate
        if criteria["grade_2"]["min"] <= hemoglobin <= criteria["grade_2"]["max"]:
            return 2
        
        # Grade 1: Mild
        grade_1_criteria = criteria["grade_1"][patient_sex]
        if grade_1_criteria["min"] <= hemoglobin <= grade_1_criteria["max"]:
            return 1
        
        # If hemoglobin is very low but not captured above, default to Grade 4
        return 4
    
    def _grade_neutropenia(self, neutrophil_count: float) -> int:
        """Grades neutropenia according to CTCAE v5.0 criteria"""
        
        criteria = self.GRADING_CRITERIA["neutropenia"]
        
        # Check if within normal limits
        if neutrophil_count >= self.NORMAL_RANGES["neutrophil"]["min"]:
            return 0
        
        # Grade 4: Life-threatening
        if neutrophil_count <= criteria["grade_4"]["max"]:
            return 4
        
        # Grade 3: Severe
        if criteria["grade_3"]["min"] <= neutrophil_count <= criteria["grade_3"]["max"]:
            return 3
        
        # Grade 2: Moderate
        if criteria["grade_2"]["min"] <= neutrophil_count <= criteria["grade_2"]["max"]:
            return 2
        
        # Grade 1: Mild
        if criteria["grade_1"]["min"] <= neutrophil_count <= criteria["grade_1"]["max"]:
            return 1
        
        return 0
    
    def _grade_thrombocytopenia(self, platelet_count: float) -> int:
        """Grades thrombocytopenia according to CTCAE v5.0 criteria"""
        
        criteria = self.GRADING_CRITERIA["thrombocytopenia"]
        
        # Check if within normal limits
        if platelet_count >= self.NORMAL_RANGES["platelet"]["min"]:
            return 0
        
        # Grade 4: Life-threatening
        if platelet_count <= criteria["grade_4"]["max"]:
            return 4
        
        # Grade 3: Severe
        if criteria["grade_3"]["min"] <= platelet_count <= criteria["grade_3"]["max"]:
            return 3
        
        # Grade 2: Moderate
        if criteria["grade_2"]["min"] <= platelet_count <= criteria["grade_2"]["max"]:
            return 2
        
        # Grade 1: Mild
        if criteria["grade_1"]["min"] <= platelet_count <= criteria["grade_1"]["max"]:
            return 1
        
        return 0
    
    def _grade_febrile_neutropenia(self, neutrophil_count: float, temperature: float) -> int:
        """Grades febrile neutropenia according to CTCAE v5.0 criteria"""
        
        criteria = self.FEBRILE_NEUTROPENIA_CRITERIA
        
        # Check neutropenia criteria (ANC <1.0 x 10⁹/L = <1000 cells/mm³)
        neutropenia_present = neutrophil_count < criteria["neutrophil_threshold"]
        
        # Check fever criteria (>38.3°C or sustained ≥38°C)
        fever_present = temperature > criteria["temperature_threshold"] or temperature >= criteria["sustained_temperature_threshold"]
        
        # Both criteria must be met for febrile neutropenia
        if neutropenia_present and fever_present:
            return criteria["grade"]  # Always Grade 3
        else:
            # If criteria not met, this is not febrile neutropenia
            return 0
    
    def _grade_leukocytosis(self, wbc_count: float) -> int:
        """Grades leukocytosis according to CTCAE v5.0 criteria"""
        
        criteria = self.GRADING_CRITERIA["leukocytosis"]
        
        # Check if within normal limits
        if wbc_count <= self.NORMAL_RANGES["wbc"]["max"]:
            return 0
        
        # Grade 4: Life-threatening
        if wbc_count >= criteria["grade_4"]["min"]:
            return 4
        
        # Grade 3: Severe
        if criteria["grade_3"]["min"] <= wbc_count <= criteria["grade_3"]["max"]:
            return 3
        
        # Grade 2: Moderate
        if criteria["grade_2"]["min"] <= wbc_count <= criteria["grade_2"]["max"]:
            return 2
        
        # Grade 1: Mild
        if criteria["grade_1"]["min"] <= wbc_count <= criteria["grade_1"]["max"]:
            return 1
        
        return 0
    
    def _grade_lymphopenia(self, lymphocyte_count: float) -> int:
        """Grades lymphopenia according to CTCAE v5.0 criteria"""
        
        criteria = self.GRADING_CRITERIA["lymphopenia"]
        
        # Check if within normal limits
        if lymphocyte_count >= self.NORMAL_RANGES["lymphocyte"]["min"]:
            return 0
        
        # Grade 4: Life-threatening
        if lymphocyte_count <= criteria["grade_4"]["max"]:
            return 4
        
        # Grade 3: Severe
        if criteria["grade_3"]["min"] <= lymphocyte_count <= criteria["grade_3"]["max"]:
            return 3
        
        # Grade 2: Moderate
        if criteria["grade_2"]["min"] <= lymphocyte_count <= criteria["grade_2"]["max"]:
            return 2
        
        # Grade 1: Mild
        if criteria["grade_1"]["min"] <= lymphocyte_count <= criteria["grade_1"]["max"]:
            return 1
        
        return 0
    
    def _get_interpretation(self, grade: int, adverse_event_type: str, primary_value, unit: str) -> Dict[str, str]:
        """Generates clinical interpretation of CTCAE grade"""
        
        grade_descriptions = {
            0: "Within normal limits",
            1: "Mild adverse event",
            2: "Moderate adverse event", 
            3: "Severe adverse event",
            4: "Life-threatening adverse event",
            5: "Death"
        }
        
        stage_descriptions = {
            0: "Grade 0",
            1: "Grade 1", 
            2: "Grade 2",
            3: "Grade 3",
            4: "Grade 4",
            5: "Grade 5"
        }
        
        clinical_significance = {
            0: "No intervention required; continue routine monitoring",
            1: "Asymptomatic or mild symptoms; clinical observation only; intervention not indicated",
            2: "Minimal intervention indicated; may limit age-appropriate activities of daily living",
            3: "Medically significant; hospitalization or prolongation may be indicated; disabling",
            4: "Life-threatening consequences; urgent intervention indicated",
            5: "Death related to adverse event"
        }
        
        # Generate detailed interpretation
        event_name = adverse_event_type.replace("_", " ").title()
        
        if grade == 0:
            interpretation = f"No {event_name.lower()} detected. Laboratory values within normal limits."
        else:
            if unit == "composite":
                interpretation = f"Grade {grade} {event_name} detected. {clinical_significance[grade]}"
            else:
                interpretation = f"Grade {grade} {event_name} detected with {primary_value} {unit}. {clinical_significance[grade]}"
        
        return {
            "stage": stage_descriptions[grade],
            "description": grade_descriptions[grade],
            "grade_description": grade_descriptions[grade],
            "interpretation": interpretation,
            "clinical_significance": clinical_significance[grade]
        }
    
    def _get_clinical_recommendations(self, grade: int, adverse_event_type: str) -> Dict[str, list]:
        """Generates clinical recommendations based on CTCAE grade"""
        
        recommendations = {
            "monitoring": [],
            "interventions": [],
            "dose_modifications": []
        }
        
        if grade == 0:
            recommendations["monitoring"] = ["Continue routine laboratory monitoring as per protocol"]
            recommendations["interventions"] = ["No specific interventions required"]
            recommendations["dose_modifications"] = ["No dose modifications indicated"]
            
        elif grade == 1:
            recommendations["monitoring"] = [
                "Increase monitoring frequency as clinically indicated",
                "Monitor for progression to higher grades"
            ]
            recommendations["interventions"] = [
                "Clinical observation and supportive care",
                "Patient education about signs and symptoms to report"
            ]
            recommendations["dose_modifications"] = ["Generally no dose modification required"]
            
        elif grade == 2:
            recommendations["monitoring"] = [
                "More frequent laboratory monitoring recommended",
                "Clinical assessment for symptoms and functional impact"
            ]
            recommendations["interventions"] = [
                "Supportive care measures as appropriate",
                "Consider prophylactic interventions if indicated"
            ]
            recommendations["dose_modifications"] = [
                "Consider dose delay until improvement to Grade 1 or baseline",
                "May require dose reduction per protocol guidelines"
            ]
            
        elif grade == 3:
            recommendations["monitoring"] = [
                "Intensive monitoring with frequent laboratory assessments",
                "Daily clinical evaluation until improvement"
            ]
            recommendations["interventions"] = [
                "Active medical management and supportive care",
                "Consider hospitalization if clinically indicated",
                "Implement appropriate treatment protocols"
            ]
            recommendations["dose_modifications"] = [
                "Hold treatment until improvement to Grade 1 or baseline",
                "Dose reduction required upon resumption",
                "Consider alternative treatment regimens"
            ]
            
        elif grade == 4:
            recommendations["monitoring"] = [
                "Continuous monitoring in appropriate care setting",
                "Immediate and frequent reassessment"
            ]
            recommendations["interventions"] = [
                "Urgent medical intervention required",
                "Intensive supportive care and treatment",
                "Consider emergency interventions as appropriate"
            ]
            recommendations["dose_modifications"] = [
                "Discontinue treatment permanently",
                "Consider alternative treatment options once stable",
                "Risk-benefit assessment required for any future therapy"
            ]
        
        # Add event-specific recommendations
        if adverse_event_type == "febrile_neutropenia" and grade >= 3:
            recommendations["interventions"].extend([
                "Empirical broad-spectrum antibiotics",
                "Blood cultures and infection workup",
                "Consider growth factor support (G-CSF)"
            ])
        
        if adverse_event_type == "thrombocytopenia" and grade >= 3:
            recommendations["interventions"].extend([
                "Bleeding precautions and assessment",
                "Consider platelet transfusion if bleeding or high risk",
                "Avoid procedures with bleeding risk"
            ])
        
        if adverse_event_type == "anemia" and grade >= 3:
            recommendations["interventions"].extend([
                "Evaluate for transfusion indication",
                "Iron studies and B12/folate assessment",
                "Consider erythropoiesis-stimulating agents if appropriate"
            ])
        
        return recommendations


def calculate_ctcae(
    adverse_event_type: str,
    patient_sex: str,
    hemoglobin: Optional[float] = None,
    neutrophil_count: Optional[float] = None,
    platelet_count: Optional[float] = None,
    wbc_count: Optional[float] = None,
    lymphocyte_count: Optional[float] = None,
    temperature: Optional[float] = None,
    transfusion_indicated: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CtcaeCalculator()
    return calculator.calculate(
        adverse_event_type=adverse_event_type,
        patient_sex=patient_sex,
        hemoglobin=hemoglobin,
        neutrophil_count=neutrophil_count,
        platelet_count=platelet_count,
        wbc_count=wbc_count,
        lymphocyte_count=lymphocyte_count,
        temperature=temperature,
        transfusion_indicated=transfusion_indicated
    )