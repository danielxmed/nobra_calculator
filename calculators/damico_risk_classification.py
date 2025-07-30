"""
D'Amico Risk Classification for Prostate Cancer Calculator

Assesses 5-year risk of treatment failure in patients with localized prostate cancer 
based on clinical factors (PSA, Gleason score, clinical stage).

References:
- D'Amico AV, et al. JAMA. 1998;280(11):969-974.
- D'Amico AV, et al. J Clin Oncol. 2000;18(6):1164-1172.
- NCCN Clinical Practice Guidelines in Oncology: Prostate Cancer.
"""

from typing import Dict, Any, Optional


class DamicoRiskClassificationCalculator:
    """Calculator for D'Amico Risk Classification for Prostate Cancer"""
    
    def __init__(self):
        # Risk group definitions based on D'Amico criteria
        self.RISK_GROUPS = {
            "low": {
                "label": "Low Risk",
                "description": "Low risk of treatment failure",
                "criteria": "PSA ≤10 ng/mL AND Gleason score ≤6 AND clinical stage T1-T2a",
                "biochemical_recurrence_risk": "Low (5-15%)",
                "five_year_recurrence_rate": "5-15%"
            },
            "intermediate": {
                "label": "Intermediate Risk", 
                "description": "Intermediate risk of treatment failure",
                "criteria": "PSA 10-20 ng/mL OR Gleason score 7 OR clinical stage T2b",
                "biochemical_recurrence_risk": "Intermediate (15-45%)",
                "five_year_recurrence_rate": "15-45%"
            },
            "high": {
                "label": "High Risk",
                "description": "High risk of treatment failure", 
                "criteria": "PSA >20 ng/mL OR Gleason score ≥8 OR clinical stage ≥T2c",
                "biochemical_recurrence_risk": "High (45-65%)",
                "five_year_recurrence_rate": "45-65%"
            }
        }
        
        # Treatment recommendations by risk group
        self.TREATMENT_RECOMMENDATIONS = {
            "low": [
                "Active surveillance may be appropriate for select patients",
                "Radical prostatectomy offers excellent cure rates",
                "External beam radiation therapy provides equivalent outcomes",
                "Brachytherapy is an effective option for suitable candidates",
                "Regular PSA monitoring every 3-6 months if on active surveillance"
            ],
            "intermediate": [
                "Definitive local therapy typically recommended",
                "Radical prostatectomy with lymph node assessment",
                "External beam radiation with or without short-term androgen deprivation",
                "Consider brachytherapy boost in select cases",
                "Discuss risks and benefits of adjuvant therapy"
            ],
            "high": [
                "Multimodal therapy often recommended",
                "Radiation therapy with long-term androgen deprivation therapy (18-36 months)",
                "Radical prostatectomy with extended lymph node dissection", 
                "Consider neoadjuvant or adjuvant systemic therapy",
                "Close monitoring for local and distant recurrence"
            ]
        }
        
        # Prognostic factors by risk group
        self.PROGNOSTIC_FACTORS = {
            "low": {
                "prognosis": "Excellent",
                "disease_specific_survival": ">95% at 10 years",
                "biochemical_control": "85-95% at 5 years",
                "metastasis_risk": "Very low (<5%)"
            },
            "intermediate": {
                "prognosis": "Good to Very Good",
                "disease_specific_survival": "85-95% at 10 years", 
                "biochemical_control": "55-85% at 5 years",
                "metastasis_risk": "Low to moderate (5-15%)"
            },
            "high": {
                "prognosis": "Guarded to Good",
                "disease_specific_survival": "60-85% at 10 years",
                "biochemical_control": "35-55% at 5 years", 
                "metastasis_risk": "Moderate to high (15-35%)"
            }
        }
    
    def calculate(self, psa_level: float, gleason_score: int, clinical_stage: str,
                  patient_age: Optional[int] = None, treatment_planned: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates D'Amico risk classification based on clinical parameters
        
        Args:
            psa_level (float): Preoperative PSA level in ng/mL
            gleason_score (int): Biopsy Gleason score (2-10)
            clinical_stage (str): Clinical T stage
            patient_age (int, optional): Patient age in years
            treatment_planned (str, optional): Planned treatment modality
            
        Returns:
            Dict with risk classification, recommendations, and prognosis
        """
        
        # Validations
        self._validate_inputs(psa_level, gleason_score, clinical_stage, patient_age, treatment_planned)
        
        # Determine risk group using D'Amico criteria
        risk_group = self._calculate_risk_group(psa_level, gleason_score, clinical_stage)
        
        # Get risk group details
        risk_details = self.RISK_GROUPS[risk_group]
        
        # Generate clinical assessment
        clinical_assessment = self._get_clinical_assessment(psa_level, gleason_score, 
                                                          clinical_stage, risk_group)
        
        # Get treatment recommendations
        treatment_recommendations = self._get_treatment_recommendations(risk_group, patient_age,
                                                                      treatment_planned)
        
        # Generate interpretation
        interpretation = self._get_interpretation(risk_group, psa_level, gleason_score, clinical_stage)
        
        # Get prognostic information
        prognosis = self._get_prognosis_assessment(risk_group, patient_age)
        
        # Get monitoring recommendations
        monitoring = self._get_monitoring_recommendations(risk_group)
        
        return {
            "result": risk_group,
            "unit": "risk group",
            "interpretation": interpretation,
            "stage": risk_details["label"],
            "stage_description": risk_details["description"],
            "risk_group": risk_group,
            "risk_category": risk_details["label"],
            "criteria_met": risk_details["criteria"],
            "biochemical_recurrence_risk": risk_details["biochemical_recurrence_risk"],
            "five_year_recurrence_rate": risk_details["five_year_recurrence_rate"],
            "clinical_assessment": clinical_assessment,
            "treatment_recommendations": treatment_recommendations,
            "prognosis": prognosis,
            "monitoring_recommendations": monitoring,
            "risk_factors": self._identify_risk_factors(psa_level, gleason_score, clinical_stage),
            "counseling_points": self._get_counseling_points(risk_group)
        }
    
    def _validate_inputs(self, psa_level, gleason_score, clinical_stage, patient_age, treatment_planned):
        """Validates input parameters"""
        
        # Validate PSA level
        if not isinstance(psa_level, (int, float)) or psa_level < 0.1 or psa_level > 500:
            raise ValueError("PSA level must be a number between 0.1 and 500 ng/mL")
        
        # Validate Gleason score
        if not isinstance(gleason_score, int) or not 2 <= gleason_score <= 10:
            raise ValueError("Gleason score must be an integer between 2 and 10")
        
        # Validate clinical stage
        valid_stages = ["T1a", "T1b", "T1c", "T2a", "T2b", "T2c", "T3a", "T3b", "T4"]
        if clinical_stage not in valid_stages:
            raise ValueError(f"Clinical stage must be one of: {valid_stages}")
        
        # Validate optional parameters
        if patient_age is not None:
            if not isinstance(patient_age, int) or not 40 <= patient_age <= 100:
                raise ValueError("Patient age must be an integer between 40 and 100")
        
        if treatment_planned is not None:
            valid_treatments = ["radical_prostatectomy", "external_beam_radiation", 
                              "brachytherapy", "active_surveillance", "not_specified"]
            if treatment_planned not in valid_treatments:
                raise ValueError(f"Treatment planned must be one of: {valid_treatments}")
    
    def _calculate_risk_group(self, psa_level, gleason_score, clinical_stage):
        """Calculates D'Amico risk group using standard criteria"""
        
        # Check for high risk criteria (any one criterion makes it high risk)
        if (psa_level > 20 or 
            gleason_score >= 8 or 
            clinical_stage in ["T2c", "T3a", "T3b", "T4"]):
            return "high"
        
        # Check for intermediate risk criteria (any one criterion makes it intermediate risk)
        if (10 < psa_level <= 20 or 
            gleason_score == 7 or 
            clinical_stage == "T2b"):
            return "intermediate"
        
        # Low risk criteria (must meet all criteria)
        if (psa_level <= 10 and 
            gleason_score <= 6 and 
            clinical_stage in ["T1a", "T1b", "T1c", "T2a"]):
            return "low"
        
        # Default to intermediate if criteria don't clearly fit (edge cases)
        return "intermediate"
    
    def _get_clinical_assessment(self, psa_level, gleason_score, clinical_stage, risk_group):
        """Generate clinical assessment based on parameters"""
        
        assessment = {
            "psa_level": psa_level,
            "gleason_score": gleason_score,
            "clinical_stage": clinical_stage,
            "risk_group": risk_group,
            "primary_risk_factors": [],
            "disease_characteristics": []
        }
        
        # Identify primary risk factors
        if psa_level > 20:
            assessment["primary_risk_factors"].append(f"Elevated PSA: {psa_level} ng/mL (>20)")
        elif psa_level > 10:
            assessment["primary_risk_factors"].append(f"Intermediate PSA: {psa_level} ng/mL (10-20)")
        else:
            assessment["primary_risk_factors"].append(f"Low PSA: {psa_level} ng/mL (≤10)")
        
        if gleason_score >= 8:
            assessment["primary_risk_factors"].append(f"High-grade cancer: Gleason {gleason_score} (≥8)")
        elif gleason_score == 7:
            assessment["primary_risk_factors"].append(f"Intermediate-grade cancer: Gleason {gleason_score}")
        else:
            assessment["primary_risk_factors"].append(f"Low-grade cancer: Gleason {gleason_score} (≤6)")
        
        if clinical_stage in ["T2c", "T3a", "T3b", "T4"]:
            assessment["primary_risk_factors"].append(f"Advanced local stage: {clinical_stage} (≥T2c)")
        elif clinical_stage == "T2b":
            assessment["primary_risk_factors"].append(f"Intermediate local stage: {clinical_stage}")
        else:
            assessment["primary_risk_factors"].append(f"Early local stage: {clinical_stage} (T1-T2a)")
        
        # Disease characteristics
        assessment["disease_characteristics"] = [
            f"Clinically localized prostate cancer",
            f"Risk stratification based on D'Amico criteria",
            f"Classified as {risk_group} risk for biochemical recurrence"
        ]
        
        return assessment
    
    def _get_treatment_recommendations(self, risk_group, patient_age, treatment_planned):
        """Get treatment recommendations based on risk group and patient factors"""
        
        base_recommendations = self.TREATMENT_RECOMMENDATIONS[risk_group].copy()
        additional_recommendations = []
        
        # Age-based considerations
        if patient_age is not None:
            if patient_age < 55:
                additional_recommendations.append("Young age favors aggressive treatment for cure")
                if risk_group == "low":
                    additional_recommendations.append("Consider active surveillance with strict monitoring")
            elif patient_age > 75:
                additional_recommendations.append("Advanced age may favor less aggressive approaches")
                additional_recommendations.append("Consider life expectancy and comorbidities in treatment selection")
        
        # Treatment-specific considerations
        if treatment_planned:
            if treatment_planned == "active_surveillance":
                if risk_group != "low":
                    additional_recommendations.append("Active surveillance typically reserved for low-risk disease")
                else:
                    additional_recommendations.append("Excellent candidate for active surveillance protocol")
            elif treatment_planned == "radical_prostatectomy":
                additional_recommendations.append("Surgical approach offers excellent cancer control")
                if risk_group == "high":
                    additional_recommendations.append("Consider extended lymph node dissection")
            elif treatment_planned in ["external_beam_radiation", "brachytherapy"]:
                additional_recommendations.append("Radiation therapy provides equivalent outcomes to surgery")
                if risk_group != "low":
                    additional_recommendations.append("Consider androgen deprivation therapy")
        
        return {
            "primary_recommendations": base_recommendations,
            "additional_considerations": additional_recommendations,
            "multidisciplinary_approach": self._get_multidisciplinary_recommendations(risk_group),
            "follow_up_intensity": self._get_follow_up_recommendations(risk_group)
        }
    
    def _get_multidisciplinary_recommendations(self, risk_group):
        """Get multidisciplinary team recommendations"""
        
        if risk_group == "low":
            return [
                "Urologist for treatment planning and monitoring",
                "Consider radiation oncologist consultation for treatment options",
                "Patient education and support services"
            ]
        elif risk_group == "intermediate":
            return [
                "Urologist and radiation oncologist consultation recommended",
                "Medical oncologist if adjuvant therapy considered",
                "Pathology review for Gleason score confirmation",
                "Patient navigator for care coordination"
            ]
        else:  # high risk
            return [
                "Multidisciplinary tumor board review recommended",
                "Urologist, radiation oncologist, and medical oncologist consultation",
                "Pathology expert review for accurate grading",
                "Social work and palliative care if appropriate",
                "Clinical trial eligibility assessment"
            ]
    
    def _get_follow_up_recommendations(self, risk_group):
        """Get follow-up intensity recommendations"""
        
        if risk_group == "low":
            return "PSA every 6 months for 2 years, then annually if stable"
        elif risk_group == "intermediate":
            return "PSA every 3-6 months for 2 years, then every 6 months for 3 years, then annually"
        else:  # high risk
            return "PSA every 3 months for 2 years, then every 6 months for 3 years, then annually with imaging"
    
    def _get_prognosis_assessment(self, risk_group, patient_age):
        """Assess prognosis based on risk group and patient factors"""
        
        base_prognosis = self.PROGNOSTIC_FACTORS[risk_group].copy()
        
        # Age modifications
        if patient_age is not None:
            if patient_age < 60:
                base_prognosis["age_factor"] = "Young age associated with longer life expectancy and greater benefit from cure"
            elif patient_age > 75:
                base_prognosis["age_factor"] = "Advanced age may limit treatment options and life expectancy considerations"
            else:
                base_prognosis["age_factor"] = "Age appropriate for all standard treatment modalities"
        
        return base_prognosis
    
    def _get_monitoring_recommendations(self, risk_group):
        """Get monitoring recommendations by risk group"""
        
        base_monitoring = ["Serial PSA measurements", "Digital rectal examination", "Clinical assessment"]
        
        if risk_group == "low":
            additional_monitoring = [
                "Annual assessment if on active surveillance",
                "Consider repeat biopsy in 12-18 months if on active surveillance",
                "Monitor for PSA doubling time"
            ]
        elif risk_group == "intermediate":
            additional_monitoring = [
                "More frequent PSA monitoring in first 2 years",
                "Consider imaging if PSA rises after treatment",
                "Monitor for treatment-related side effects"
            ]
        else:  # high risk
            additional_monitoring = [
                "Intensive PSA monitoring",
                "Consider baseline and follow-up imaging",
                "Monitor for local and distant recurrence",
                "Assess for systemic therapy indications"
            ]
        
        return {
            "routine_monitoring": base_monitoring,
            "risk_specific_monitoring": additional_monitoring,
            "frequency": self._get_follow_up_recommendations(risk_group)
        }
    
    def _identify_risk_factors(self, psa_level, gleason_score, clinical_stage):
        """Identify specific risk factors present"""
        
        risk_factors = {
            "psa_risk": "low" if psa_level <= 10 else "intermediate" if psa_level <= 20 else "high",
            "gleason_risk": "low" if gleason_score <= 6 else "intermediate" if gleason_score == 7 else "high",
            "stage_risk": "low" if clinical_stage in ["T1a", "T1b", "T1c", "T2a"] else "intermediate" if clinical_stage == "T2b" else "high"
        }
        
        risk_factors["highest_risk_factor"] = max(risk_factors.values(), key=lambda x: ["low", "intermediate", "high"].index(x))
        
        return risk_factors
    
    def _get_counseling_points(self, risk_group):
        """Get key counseling points for patient discussion"""
        
        if risk_group == "low":
            return [
                "Excellent prognosis with low risk of cancer progression",
                "Multiple effective treatment options available",
                "Active surveillance is a reasonable option for many patients",
                "Treatment side effects may outweigh benefits in some cases",
                "Regular monitoring is essential regardless of treatment choice"
            ]
        elif risk_group == "intermediate":
            return [
                "Good prognosis with appropriate treatment",
                "Definitive treatment typically recommended",
                "Benefits of treatment generally outweigh risks",
                "Multiple treatment modalities offer similar cancer control",
                "Individual patient factors influence optimal treatment choice"
            ]
        else:  # high risk
            return [
                "Significant cancer that requires aggressive treatment",
                "Higher risk of progression without treatment",
                "Multimodal therapy often provides best outcomes",
                "Benefits of aggressive treatment typically outweigh risks",
                "Close monitoring and follow-up are essential"
            ]
    
    def _get_interpretation(self, risk_group, psa_level, gleason_score, clinical_stage):
        """Get comprehensive interpretation of risk assessment"""
        
        risk_details = self.RISK_GROUPS[risk_group]
        
        base_interpretation = (f"D'Amico {risk_details['label']} classification based on "
                             f"PSA {psa_level} ng/mL, Gleason score {gleason_score}, and "
                             f"clinical stage {clinical_stage}.")
        
        if risk_group == "low":
            return (f"{base_interpretation} Patient has excellent prognosis with {risk_details['five_year_recurrence_rate']} "
                   f"5-year biochemical recurrence risk. Active surveillance may be appropriate for select patients, "
                   f"though definitive treatment offers excellent cure rates.")
        
        elif risk_group == "intermediate":
            return (f"{base_interpretation} Patient has good prognosis with {risk_details['five_year_recurrence_rate']} "
                   f"5-year biochemical recurrence risk. Definitive local therapy is typically recommended with "
                   f"consideration of adjuvant therapy based on specific risk factors.")
        
        else:  # high risk
            return (f"{base_interpretation} Patient has significant cancer with {risk_details['five_year_recurrence_rate']} "
                   f"5-year biochemical recurrence risk. Multimodal therapy is often recommended, including radiation "
                   f"with androgen deprivation therapy or radical surgery with possible adjuvant treatment.")


def calculate_damico_risk_classification(psa_level: float, gleason_score: int, clinical_stage: str,
                                       patient_age: Optional[int] = None, 
                                       treatment_planned: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DamicoRiskClassificationCalculator()
    return calculator.calculate(psa_level, gleason_score, clinical_stage, patient_age, treatment_planned)