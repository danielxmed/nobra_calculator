"""
Denver HIV Risk Score Calculator

Predicts probability of undiagnosed HIV infection in patients aged 13 and older 
using demographic and behavioral risk factors.

References:
- Haukoos JS, et al. Am J Epidemiol. 2012;175(8):838-846.
- Hsieh YH, et al. Acad Emerg Med. 2014;21(7):757-767.
- CDC. JAMA. 2019;321(23):2326-2336.
"""

from typing import Dict, Any, Optional


class DenverHivRiskScoreCalculator:
    """Calculator for Denver HIV Risk Score"""
    
    def __init__(self):
        # Denver HIV Risk Score component weights
        self.SCORE_COMPONENTS = {
            "age_group": {
                "under_22": 2,
                "22_25": 4,
                "26_32": 6,
                "33_46": 12,
                "47_54": 8,
                "55_60": 3,
                "over_60": 0
            },
            "gender": {
                "male": 21,
                "female": 0
            },
            "sexual_practices": {
                "sex_with_male": 22,
                "receptive_anal_intercourse": 8,
                "vaginal_intercourse": -10,
                "none": 0
            },
            "injection_drug_use": {
                "yes": 9,
                "no": 0
            },
            "past_hiv_testing": {
                "yes": -4,
                "no": 0
            },
            "race_ethnicity": {
                "black": 9,
                "hispanic": 3,
                "white": 0,
                "asian": 0,
                "other": 1
            }
        }
        
        # Risk categories and prevalence data
        self.RISK_CATEGORIES = {
            "very_low": {
                "score_range": (-14, 19),
                "label": "Very Low Risk",
                "description": "Very low probability of undiagnosed HIV infection",
                "hiv_prevalence": "0.31%",
                "prevalence_numeric": 0.31,
                "recommendation": "Consider routine screening per guidelines"
            },
            "low": {
                "score_range": (20, 29),
                "label": "Low Risk",
                "description": "Low probability of undiagnosed HIV infection",
                "hiv_prevalence": "0.41%",
                "prevalence_numeric": 0.41,
                "recommendation": "Offer HIV testing and prevention counseling"
            },
            "moderate": {
                "score_range": (30, 39),
                "label": "Moderate Risk",
                "description": "Moderate probability of undiagnosed HIV infection",
                "hiv_prevalence": "0.99%",
                "prevalence_numeric": 0.99,
                "recommendation": "Strongly recommend HIV testing"
            },
            "high": {
                "score_range": (40, 49),
                "label": "High Risk",
                "description": "High probability of undiagnosed HIV infection",
                "hiv_prevalence": "1.59%",
                "prevalence_numeric": 1.59,
                "recommendation": "Urgent HIV testing recommended"
            },
            "very_high": {
                "score_range": (50, 81),
                "label": "Very High Risk",
                "description": "Very high probability of undiagnosed HIV infection",
                "hiv_prevalence": "3.59%",
                "prevalence_numeric": 3.59,
                "recommendation": "Immediate HIV testing essential"
            }
        }
        
        # Screening recommendations by risk level
        self.SCREENING_RECOMMENDATIONS = {
            "very_low": [
                "Consider routine screening per CDC guidelines",
                "Provide general HIV prevention education",
                "Document risk assessment in medical record",
                "Follow standard screening intervals if no risk factors"
            ],
            "low": [
                "Offer HIV testing with informed consent",
                "Provide risk reduction counseling",
                "Consider annual screening if ongoing low-level risk",
                "Educate about HIV transmission and prevention"
            ],
            "moderate": [
                "Strongly recommend HIV testing",
                "Provide comprehensive prevention counseling",
                "Consider more frequent screening (every 3-6 months)",
                "Discuss risk reduction strategies and safer practices",
                "Consider PrEP evaluation if appropriate"
            ],
            "high": [
                "Urgent HIV testing with expedited results",
                "Comprehensive risk assessment and counseling",
                "Frequent screening (every 3 months) if negative",
                "Strong consideration for PrEP evaluation",
                "Linkage to HIV prevention services"
            ],
            "very_high": [
                "Immediate HIV testing with same-day results if possible",
                "Comprehensive prevention services engagement",
                "Frequent screening (monthly to quarterly) if negative",
                "Prioritize for PrEP evaluation and initiation",
                "Intensive case management and support services"
            ]
        }
    
    def calculate(self, age_group: str, gender: str, sexual_practices: str,
                  injection_drug_use: str, past_hiv_testing: str,
                  race_ethnicity: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates Denver HIV Risk Score for HIV infection probability
        
        Args:
            age_group (str): Patient age group category
            gender (str): Patient gender
            sexual_practices (str): Sexual behavior risk factors
            injection_drug_use (str): History of injection drug use
            past_hiv_testing (str): History of previous HIV testing
            race_ethnicity (str, optional): Race/ethnicity for additional stratification
            
        Returns:
            Dict with Denver HIV Risk Score, risk category, and screening recommendations
        """
        
        # Validations
        self._validate_inputs(age_group, gender, sexual_practices, injection_drug_use,
                            past_hiv_testing, race_ethnicity)
        
        # Calculate Denver HIV Risk Score
        hiv_risk_score = self._calculate_hiv_risk_score(age_group, gender, sexual_practices,
                                                      injection_drug_use, past_hiv_testing, race_ethnicity)
        
        # Determine risk category
        risk_category = self._determine_risk_category(hiv_risk_score)
        
        # Get risk details
        risk_details = self.RISK_CATEGORIES[risk_category]
        
        # Generate clinical assessment
        clinical_assessment = self._get_clinical_assessment(
            age_group, gender, sexual_practices, injection_drug_use, past_hiv_testing,
            race_ethnicity, hiv_risk_score, risk_category)
        
        # Get screening recommendations
        screening_recommendations = self._get_screening_recommendations(
            risk_category, hiv_risk_score)
        
        # Generate interpretation
        interpretation = self._get_interpretation(risk_category, hiv_risk_score, risk_details)
        
        # Get prevention guidance
        prevention_guidance = self._get_prevention_guidance(risk_category, sexual_practices, injection_drug_use)
        
        return {
            "result": hiv_risk_score,
            "unit": "Denver HIV Risk Score",
            "interpretation": interpretation,
            "stage": risk_details["label"],
            "stage_description": risk_details["description"],
            "hiv_risk_score": hiv_risk_score,
            "risk_category": risk_category,
            "hiv_prevalence": risk_details["hiv_prevalence"],
            "prevalence_numeric": risk_details["prevalence_numeric"],
            "recommendation": risk_details["recommendation"],
            "clinical_assessment": clinical_assessment,
            "screening_recommendations": screening_recommendations,
            "prevention_guidance": prevention_guidance,
            "score_components": self._get_score_breakdown(
                age_group, gender, sexual_practices, injection_drug_use, past_hiv_testing, race_ethnicity),
            "testing_guidance": self._get_testing_guidance(risk_category),
            "follow_up_recommendations": self._get_follow_up_recommendations(risk_category),
            "prep_considerations": self._get_prep_considerations(risk_category, sexual_practices, injection_drug_use)
        }
    
    def _validate_inputs(self, age_group, gender, sexual_practices, injection_drug_use,
                        past_hiv_testing, race_ethnicity):
        """Validates input parameters"""
        
        # Validate age group
        valid_age_groups = ["under_22", "22_25", "26_32", "33_46", "47_54", "55_60", "over_60"]
        if age_group not in valid_age_groups:
            raise ValueError(f"age_group must be one of: {valid_age_groups}")
        
        # Validate gender
        if gender not in ["male", "female"]:
            raise ValueError("gender must be 'male' or 'female'")
        
        # Validate sexual practices
        valid_practices = ["sex_with_male", "receptive_anal_intercourse", "vaginal_intercourse", "none"]
        if sexual_practices not in valid_practices:
            raise ValueError(f"sexual_practices must be one of: {valid_practices}")
        
        # Validate injection drug use
        if injection_drug_use not in ["yes", "no"]:
            raise ValueError("injection_drug_use must be 'yes' or 'no'")
        
        # Validate past HIV testing
        if past_hiv_testing not in ["yes", "no"]:
            raise ValueError("past_hiv_testing must be 'yes' or 'no'")
        
        # Validate race/ethnicity if provided
        if race_ethnicity is not None:
            valid_race_ethnicity = ["black", "hispanic", "white", "asian", "other"]
            if race_ethnicity not in valid_race_ethnicity:
                raise ValueError(f"race_ethnicity must be one of: {valid_race_ethnicity}")
    
    def _calculate_hiv_risk_score(self, age_group, gender, sexual_practices,
                                 injection_drug_use, past_hiv_testing, race_ethnicity):
        """Calculates the Denver HIV Risk Score using component weights"""
        
        score = 0
        
        # Age group component (0-12 points)
        score += self.SCORE_COMPONENTS["age_group"][age_group]
        
        # Gender component (0-21 points)
        score += self.SCORE_COMPONENTS["gender"][gender]
        
        # Sexual practices component (-10 to 22 points)
        score += self.SCORE_COMPONENTS["sexual_practices"][sexual_practices]
        
        # Injection drug use component (0-9 points)
        score += self.SCORE_COMPONENTS["injection_drug_use"][injection_drug_use]
        
        # Past HIV testing component (-4 to 0 points)
        score += self.SCORE_COMPONENTS["past_hiv_testing"][past_hiv_testing]
        
        # Race/ethnicity component (0-9 points, optional)
        if race_ethnicity is not None:
            score += self.SCORE_COMPONENTS["race_ethnicity"][race_ethnicity]
        
        return score
    
    def _determine_risk_category(self, hiv_risk_score):
        """Determines risk category based on Denver HIV Risk Score"""
        
        for category, details in self.RISK_CATEGORIES.items():
            score_min, score_max = details["score_range"]
            if score_min <= hiv_risk_score <= score_max:
                return category
        
        # Handle edge cases
        if hiv_risk_score < -14:
            return "very_low"
        else:
            return "very_high"
    
    def _get_clinical_assessment(self, age_group, gender, sexual_practices,
                               injection_drug_use, past_hiv_testing, race_ethnicity,
                               hiv_risk_score, risk_category):
        """Generate clinical assessment based on parameters"""
        
        assessment = {
            "hiv_risk_score": hiv_risk_score,
            "risk_category": risk_category,
            "score_components": [],
            "risk_factors": [],
            "protective_factors": [],
            "clinical_considerations": []
        }
        
        # Document score components
        age_descriptions = {
            "under_22": "Age <22 years (2 points)",
            "22_25": "Age 22-25 years (4 points)",
            "26_32": "Age 26-32 years (6 points)",
            "33_46": "Age 33-46 years (12 points)",
            "47_54": "Age 47-54 years (8 points)",
            "55_60": "Age 55-60 years (3 points)",
            "over_60": "Age >60 years (0 points)"
        }
        assessment["score_components"].append(age_descriptions[age_group])
        
        gender_points = self.SCORE_COMPONENTS["gender"][gender]
        assessment["score_components"].append(f"{gender.title()} gender ({gender_points} points)")
        
        practice_descriptions = {
            "sex_with_male": "Sex with male partner (22 points)",
            "receptive_anal_intercourse": "Receptive anal intercourse (8 points)",
            "vaginal_intercourse": "Vaginal intercourse (-10 points)",
            "none": "No specified sexual practices (0 points)"
        }
        assessment["score_components"].append(practice_descriptions[sexual_practices])
        
        idu_points = self.SCORE_COMPONENTS["injection_drug_use"][injection_drug_use]
        assessment["score_components"].append(f"Injection drug use: {injection_drug_use} ({idu_points} points)")
        
        testing_points = self.SCORE_COMPONENTS["past_hiv_testing"][past_hiv_testing]
        assessment["score_components"].append(f"Past HIV testing: {past_hiv_testing} ({testing_points} points)")
        
        if race_ethnicity is not None:
            race_points = self.SCORE_COMPONENTS["race_ethnicity"][race_ethnicity]
            assessment["score_components"].append(f"Race/ethnicity: {race_ethnicity} ({race_points} points)")
        
        # Risk factors
        if gender == "male":
            assessment["risk_factors"].append("Male gender associated with higher HIV acquisition risk")
        
        if sexual_practices == "sex_with_male":
            assessment["risk_factors"].append("Sex with male partners increases HIV transmission risk")
        
        if sexual_practices == "receptive_anal_intercourse":
            assessment["risk_factors"].append("Receptive anal intercourse carries highest per-act transmission risk")
        
        if injection_drug_use == "yes":
            assessment["risk_factors"].append("Injection drug use increases HIV transmission through shared equipment")
        
        # Protective factors
        if past_hiv_testing == "yes":
            assessment["protective_factors"].append("Previous HIV testing indicates health-seeking behavior and awareness")
        
        if sexual_practices == "vaginal_intercourse":
            assessment["protective_factors"].append("Vaginal intercourse carries lower transmission risk than anal intercourse")
        
        # Clinical considerations
        assessment["clinical_considerations"] = [
            f"Patient assessed with Denver HIV Risk Score of {hiv_risk_score}",
            f"Risk category: {risk_category} with {self.RISK_CATEGORIES[risk_category]['hiv_prevalence']} estimated prevalence",
            f"Screening approach: {self.RISK_CATEGORIES[risk_category]['recommendation'].lower()}"
        ]
        
        return assessment
    
    def _get_screening_recommendations(self, risk_category, hiv_risk_score):
        """Get screening recommendations based on risk assessment"""
        
        base_recommendations = self.SCREENING_RECOMMENDATIONS[risk_category].copy()
        specific_recommendations = []
        
        # Score-specific considerations
        if hiv_risk_score >= 50:
            specific_recommendations.append("Very high score warrants immediate testing with expedited results")
        elif hiv_risk_score >= 40:
            specific_recommendations.append("High score indicates urgent need for HIV testing")
        elif hiv_risk_score >= 30:
            specific_recommendations.append("Moderate to high score supports targeted screening approach")
        
        # Additional considerations
        if risk_category in ["moderate", "high", "very_high"]:
            specific_recommendations.append("Consider linkage to HIV prevention services regardless of test result")
            specific_recommendations.append("Provide comprehensive risk reduction counseling")
        
        return {
            "primary_recommendations": base_recommendations,
            "specific_considerations": specific_recommendations,
            "testing_frequency": self._get_testing_frequency(risk_category),
            "counseling_requirements": self._get_counseling_requirements(risk_category)
        }
    
    def _get_testing_frequency(self, risk_category):
        """Get recommended testing frequency based on risk level"""
        
        frequency_map = {
            "very_low": "Follow standard CDC guidelines (typically annual if sexually active)",
            "low": "Annual testing if ongoing risk factors present",
            "moderate": "Every 3-6 months if ongoing risk factors",
            "high": "Every 3 months if negative and ongoing risk",
            "very_high": "Monthly to quarterly if negative and ongoing high-risk behavior"
        }
        
        return frequency_map[risk_category]
    
    def _get_counseling_requirements(self, risk_category):
        """Get counseling requirements based on risk level"""
        
        if risk_category in ["very_low", "low"]:
            return [
                "Basic HIV prevention education",
                "Information about transmission routes",
                "Safe sex practices discussion"
            ]
        else:
            return [
                "Comprehensive risk assessment and counseling",
                "Detailed prevention strategy development",
                "Risk reduction goal setting",
                "Referral to specialized prevention services"
            ]
    
    def _get_prevention_guidance(self, risk_category, sexual_practices, injection_drug_use):
        """Get prevention guidance based on risk factors"""
        
        guidance = {
            "general_prevention": [],
            "specific_interventions": [],
            "harm_reduction": [],
            "prep_considerations": []
        }
        
        # General prevention
        guidance["general_prevention"] = [
            "Consistent condom use during sexual activity",
            "Limiting number of sexual partners",
            "Regular STD screening and treatment",
            "Open communication with partners about HIV status"
        ]
        
        # Specific interventions based on risk factors
        if sexual_practices in ["sex_with_male", "receptive_anal_intercourse"]:
            guidance["specific_interventions"].extend([
                "Consider pre-exposure prophylaxis (PrEP) evaluation",
                "Use of appropriate lubrication during anal intercourse",
                "Post-exposure prophylaxis (PEP) awareness for high-risk exposures"
            ])
        
        if injection_drug_use == "yes":
            guidance["harm_reduction"].extend([
                "Access to clean needle and syringe programs",
                "Substance use treatment referrals",
                "Safe injection practices education",
                "Overdose prevention and naloxone training"
            ])
        
        # PrEP considerations
        if risk_category in ["moderate", "high", "very_high"]:
            guidance["prep_considerations"] = [
                "Evaluate for PrEP candidacy based on ongoing risk",
                "Discuss benefits and risks of daily oral PrEP",
                "Consider long-acting injectable PrEP options",
                "Ensure comprehensive monitoring if PrEP initiated"
            ]
        
        return guidance
    
    def _get_testing_guidance(self, risk_category):
        """Get specific testing guidance based on risk level"""
        
        guidance = {
            "test_types": [],
            "timing": "",
            "result_management": []
        }
        
        if risk_category in ["very_low", "low"]:
            guidance["test_types"] = ["Standard HIV testing (laboratory-based or rapid)"]
            guidance["timing"] = "Routine testing schedule"
            guidance["result_management"] = [
                "Standard result notification procedures",
                "Basic prevention counseling with results"
            ]
        else:
            guidance["test_types"] = [
                "Rapid HIV testing preferred for immediate results",
                "Consider 4th generation HIV testing for improved sensitivity"
            ]
            guidance["timing"] = "Expedited testing with same-day results when possible"
            guidance["result_management"] = [
                "Immediate result notification and counseling",
                "Expedited linkage to care if positive",
                "Comprehensive prevention services if negative"
            ]
        
        return guidance
    
    def _get_follow_up_recommendations(self, risk_category):
        """Get follow-up recommendations based on risk level"""
        
        if risk_category in ["very_low", "low"]:
            return {
                "timing": "Annual or per standard guidelines",
                "components": [
                    "Risk reassessment",
                    "Repeat testing if indicated",
                    "General prevention education"
                ]
            }
        elif risk_category == "moderate":
            return {
                "timing": "3-6 months",
                "components": [
                    "Comprehensive risk reassessment",
                    "PrEP evaluation if appropriate",
                    "STD screening",
                    "Prevention counseling reinforcement"
                ]
            }
        else:  # high or very_high
            return {
                "timing": "1-3 months",
                "components": [
                    "Intensive risk assessment and monitoring",
                    "PrEP initiation or monitoring",
                    "Comprehensive STD screening",
                    "Linkage to prevention services",
                    "Case management if needed"
                ]
            }
    
    def _get_prep_considerations(self, risk_category, sexual_practices, injection_drug_use):
        """Get PrEP considerations based on risk assessment"""
        
        considerations = {
            "candidacy": "",
            "evaluation_needed": False,
            "specific_factors": []
        }
        
        if risk_category in ["moderate", "high", "very_high"]:
            considerations["candidacy"] = "Strong candidate for PrEP evaluation"
            considerations["evaluation_needed"] = True
            
            if sexual_practices in ["sex_with_male", "receptive_anal_intercourse"]:
                considerations["specific_factors"].append("High-risk sexual behavior supports PrEP indication")
            
            if injection_drug_use == "yes":
                considerations["specific_factors"].append("Injection drug use is indication for PrEP")
        
        elif risk_category == "low":
            considerations["candidacy"] = "Consider PrEP evaluation based on individual circumstances"
            considerations["evaluation_needed"] = False
        
        else:  # very_low
            considerations["candidacy"] = "PrEP generally not indicated based on current risk assessment"
            considerations["evaluation_needed"] = False
        
        return considerations
    
    def _get_score_breakdown(self, age_group, gender, sexual_practices,
                           injection_drug_use, past_hiv_testing, race_ethnicity):
        """Get detailed breakdown of score components"""
        
        components = []
        
        age_points = self.SCORE_COMPONENTS["age_group"][age_group]
        components.append({
            "component": "Age Group",
            "value": age_group,
            "points": age_points,
            "description": f"Age group risk factor"
        })
        
        gender_points = self.SCORE_COMPONENTS["gender"][gender]
        components.append({
            "component": "Gender",
            "value": gender,
            "points": gender_points,
            "description": f"Gender-based risk factor"
        })
        
        practice_points = self.SCORE_COMPONENTS["sexual_practices"][sexual_practices]
        components.append({
            "component": "Sexual Practices",
            "value": sexual_practices,
            "points": practice_points,
            "description": f"Sexual behavior risk factor"
        })
        
        idu_points = self.SCORE_COMPONENTS["injection_drug_use"][injection_drug_use]
        components.append({
            "component": "Injection Drug Use",
            "value": injection_drug_use,
            "points": idu_points,
            "description": f"Substance use risk factor"
        })
        
        testing_points = self.SCORE_COMPONENTS["past_hiv_testing"][past_hiv_testing]
        components.append({
            "component": "Past HIV Testing",
            "value": past_hiv_testing,
            "points": testing_points,
            "description": f"Previous testing history"
        })
        
        if race_ethnicity is not None:
            race_points = self.SCORE_COMPONENTS["race_ethnicity"][race_ethnicity]
            components.append({
                "component": "Race/Ethnicity",
                "value": race_ethnicity,
                "points": race_points,
                "description": f"Demographic risk factor"
            })
        
        return components
    
    def _get_interpretation(self, risk_category, hiv_risk_score, risk_details):
        """Get comprehensive interpretation of HIV risk assessment"""
        
        base_interpretation = (f"Denver HIV Risk Score of {hiv_risk_score} indicates {risk_details['label']} "
                             f"with approximately {risk_details['hiv_prevalence']} HIV prevalence in similar populations.")
        
        if risk_category == "very_low":
            return (f"{base_interpretation} Routine screening may be considered based on clinical "
                   f"judgment and standard guidelines. Focus on general prevention education.")
        
        elif risk_category == "low":
            return (f"{base_interpretation} Offer HIV testing and basic prevention counseling. "
                   f"Consider periodic rescreening based on ongoing risk factors.")
        
        elif risk_category == "moderate":
            return (f"{base_interpretation} Strongly recommend HIV testing with comprehensive "
                   f"prevention counseling. Consider PrEP evaluation and frequent rescreening.")
        
        elif risk_category == "high":
            return (f"{base_interpretation} Urgent HIV testing recommended with expedited results. "
                   f"Provide comprehensive prevention services and strong PrEP consideration.")
        
        else:  # very_high
            return (f"{base_interpretation} Immediate HIV testing essential with same-day results "
                   f"when possible. Prioritize for comprehensive prevention services and PrEP initiation.")


def calculate_denver_hiv_risk_score(age_group: str, gender: str, sexual_practices: str,
                                   injection_drug_use: str, past_hiv_testing: str,
                                   race_ethnicity: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DenverHivRiskScoreCalculator()
    return calculator.calculate(age_group, gender, sexual_practices, injection_drug_use,
                              past_hiv_testing, race_ethnicity)