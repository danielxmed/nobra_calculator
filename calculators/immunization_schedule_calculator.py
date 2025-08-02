"""
Immunization Schedule Calculator

Determines what immunizations/vaccinations are due based on patient's age according to CDC vaccination guidelines.
This clinical decision support tool helps healthcare providers identify appropriate vaccinations for pediatric 
and adult patients based on standardized immunization schedules.

References:
1. Centers for Disease Control and Prevention. Child and Adolescent Immunization Schedule by Age. Atlanta, GA: CDC; 2024.
2. Centers for Disease Control and Prevention. Adult Immunization Schedule by Age. Atlanta, GA: CDC; 2024.
3. Advisory Committee on Immunization Practices (ACIP). General recommendations on immunization. MMWR Recomm Rep. 2011;60(RR-2):1-64.
"""

from typing import Dict, Any, List


class ImmunizationScheduleCalculator:
    """Calculator for Immunization Schedule based on CDC guidelines"""
    
    def __init__(self):
        # Define vaccination schedules based on CDC guidelines
        self.infant_schedule = {
            0: ["Hepatitis B (1st dose)"],
            2: ["DTaP (1st dose)", "Hib (1st dose)", "IPV (1st dose)", "PCV13 (1st dose)", "RV (1st dose)"],
            4: ["DTaP (2nd dose)", "Hib (2nd dose)", "IPV (2nd dose)", "PCV13 (2nd dose)", "RV (2nd dose)"],
            6: ["DTaP (3rd dose)", "Hib (3rd dose)", "PCV13 (3rd dose)", "RV (3rd dose)", "Hepatitis B (2nd dose)", "Influenza (annual)"],
            12: ["MMR (1st dose)", "Varicella (1st dose)", "PCV13 (4th dose)", "Hib (4th dose)", "Hepatitis A (1st dose)"],
            15: ["DTaP (4th dose)"],
            18: ["Hepatitis A (2nd dose)", "Hepatitis B (3rd dose)"],
            19: ["Influenza (annual)"]
        }
        
        self.child_schedule = {
            (2, 3): ["Influenza (annual)"],
            (4, 6): ["DTaP (5th dose)", "IPV (4th dose)", "MMR (2nd dose)", "Varicella (2nd dose)", "Influenza (annual)"],
            (7, 10): ["Influenza (annual)", "Tdap catch-up if needed"],
            (11, 12): ["Tdap (1st dose)", "HPV (1st dose)", "Meningococcal ACWY (1st dose)", "Influenza (annual)"],
            (13, 15): ["HPV series completion", "Meningococcal ACWY booster", "Influenza (annual)"],
            (16, 18): ["Meningococcal B (consider)", "Influenza (annual)"]
        }
        
        self.adult_schedule = {
            (18, 26): ["Influenza (annual)", "Tdap/Td (every 10 years)", "HPV (if not previously vaccinated)", "Meningococcal (high risk)"],
            (27, 49): ["Influenza (annual)", "Tdap/Td (every 10 years)", "Zoster (if immunocompromised)"],
            (50, 64): ["Influenza (annual)", "Tdap/Td (every 10 years)", "Zoster (immunocompromised)"],
            (65, 120): ["Influenza (annual)", "Tdap/Td (every 10 years)", "Pneumococcal PCV15/PPSV23", "Zoster (Shingrix)"]
        }
    
    def calculate(self, age_group: str, age_months: int = None, age_years: int = None) -> Dict[str, Any]:
        """
        Determines vaccination recommendations based on patient age
        
        Args:
            age_group (str): Age group category ("under_2_years" or "2_years_and_over")
            age_months (int): Patient age in months (for under 2 years)
            age_years (int): Patient age in years (for 2 years and over)
            
        Returns:
            Dict with vaccination recommendations and guidance
        """
        
        # Validations
        self._validate_inputs(age_group, age_months, age_years)
        
        # Get vaccination recommendations
        recommendations = self._get_vaccination_recommendations(age_group, age_months, age_years)
        
        # Get interpretation
        interpretation = self._get_interpretation(age_group, age_months, age_years)
        
        return {
            "result": recommendations,
            "unit": None,
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_group: str, age_months: int = None, age_years: int = None):
        """Validates input parameters"""
        
        if age_group not in ["under_2_years", "2_years_and_over"]:
            raise ValueError("age_group must be 'under_2_years' or '2_years_and_over'")
        
        if age_group == "under_2_years":
            if age_months is None:
                raise ValueError("age_months is required when age_group is 'under_2_years'")
            if not isinstance(age_months, int) or age_months < 0 or age_months > 23:
                raise ValueError("age_months must be an integer between 0 and 23")
        
        if age_group == "2_years_and_over":
            if age_years is None:
                raise ValueError("age_years is required when age_group is '2_years_and_over'")
            if not isinstance(age_years, int) or age_years < 2 or age_years > 120:
                raise ValueError("age_years must be an integer between 2 and 120")
    
    def _get_vaccination_recommendations(self, age_group: str, age_months: int = None, age_years: int = None) -> str:
        """Gets vaccination recommendations based on age"""
        
        recommendations = []
        
        if age_group == "under_2_years":
            # Find closest vaccination schedule for infants
            recommendations = self._get_infant_recommendations(age_months)
        else:
            # Find appropriate schedule for children/adults
            if age_years < 18:
                recommendations = self._get_child_recommendations(age_years)
            else:
                recommendations = self._get_adult_recommendations(age_years)
        
        if not recommendations:
            recommendations = ["No specific vaccinations due at this age. Consult CDC guidelines for complete schedule."]
        
        # Add general guidance
        recommendations.append("Consider patient's vaccination history and any contraindications.")
        recommendations.append("Consult current CDC immunization schedules for most up-to-date recommendations.")
        
        return "; ".join(recommendations)
    
    def _get_infant_recommendations(self, age_months: int) -> List[str]:
        """Gets vaccination recommendations for infants under 2 years"""
        
        recommendations = []
        
        # Check exact month matches first
        if age_months in self.infant_schedule:
            recommendations.extend(self.infant_schedule[age_months])
        
        # For months not specifically listed, provide general guidance
        if not recommendations:
            if age_months < 2:
                recommendations = ["Hepatitis B series should be initiated"]
            elif age_months < 6:
                recommendations = ["Continue primary vaccination series (DTaP, Hib, IPV, PCV13, RV)"]
            elif age_months < 12:
                recommendations = ["Complete primary series and prepare for 12-month vaccinations"]
            else:
                recommendations = ["MMR, Varicella, and other 12+ month vaccinations should be considered"]
        
        # Always recommend annual influenza for 6+ months
        if age_months >= 6 and "Influenza (annual)" not in " ".join(recommendations):
            recommendations.append("Influenza (annual)")
        
        return recommendations
    
    def _get_child_recommendations(self, age_years: int) -> List[str]:
        """Gets vaccination recommendations for children 2-17 years"""
        
        recommendations = []
        
        for age_range, vaccines in self.child_schedule.items():
            if age_range[0] <= age_years <= age_range[1]:
                recommendations.extend(vaccines)
        
        return recommendations
    
    def _get_adult_recommendations(self, age_years: int) -> List[str]:
        """Gets vaccination recommendations for adults 18+ years"""
        
        recommendations = []
        
        for age_range, vaccines in self.adult_schedule.items():
            if age_range[0] <= age_years <= age_range[1]:
                recommendations.extend(vaccines)
        
        return recommendations
    
    def _get_interpretation(self, age_group: str, age_months: int = None, age_years: int = None) -> Dict[str, str]:
        """
        Gets clinical interpretation based on age
        
        Args:
            age_group (str): Age group category
            age_months (int): Age in months (for infants)
            age_years (int): Age in years (for children/adults)
            
        Returns:
            Dict with interpretation details
        """
        
        if age_group == "under_2_years":
            return {
                "stage": "Pediatric Schedule",
                "description": "Infant and toddler vaccination schedule",
                "interpretation": "Follow CDC pediatric immunization schedule with appropriate spacing between doses. Ensure primary vaccination series is completed on time. Consider patient's vaccination history and any contraindications. Live vaccines are contraindicated in immunocompromised patients."
            }
        
        age = age_years
        
        if age < 18:
            return {
                "stage": "Child/Adolescent Schedule", 
                "description": "Childhood and adolescent vaccination schedule",
                "interpretation": "Follow CDC child and adolescent immunization schedule. Ensure catch-up vaccinations as needed for any missed doses. Consider HPV series for adolescents 11-12 years. Assess for high-risk conditions requiring additional vaccines."
            }
        else:
            return {
                "stage": "Adult Schedule",
                "description": "Adult vaccination schedule", 
                "interpretation": "Follow CDC adult immunization schedule based on age, risk factors, and previous vaccination history. Ensure annual influenza vaccination. Consider pneumococcal vaccines for adults ≥65 years. Assess occupational and travel-related vaccination needs."
            }


def calculate_immunization_schedule_calculator(age_group: str, age_months: int = None, age_years: int = None) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_immunization_schedule_calculator pattern
    """
    calculator = ImmunizationScheduleCalculator()
    return calculator.calculate(age_group, age_months, age_years)