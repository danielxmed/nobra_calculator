"""
Rule of Nines Calculator

Calculates total body surface area (TBSA) affected by burns using standardized 
body segment percentages. This rapid assessment tool helps emergency providers 
estimate burn severity for fluid resuscitation, burn center transfer decisions, 
and initial treatment planning.

References (Vancouver style):
1. Pulaski EJ, Tennison CW. Burn therapy; a comparative study of various methods 
   of treatment; review of the literature and report of 300 cases. AMA Arch Surg. 
   1947 Dec;55(6):689-723. doi: 10.1001/archsurg.1947.01230180111007.
2. Wallace AB. The exposure treatment of burns. Lancet. 1951 Mar 17;1(6659):501-4. 
   doi: 10.1016/s0140-6736(51)91975-7.
3. Hettiaratchy S, Papini R. Initial management of a major burn: II--assessment 
   and resuscitation. BMJ. 2004 Jul 17;329(7458):101-3. doi: 10.1136/bmj.329.7458.101.
4. American Burn Association. Guidelines for the operation of burn centers. 
   J Burn Care Res. 2007 Jan-Feb;28(1):134-41. doi: 10.1097/BCR.0B013E318031AA21.
"""

from typing import Dict, Any


class RuleOfNinesCalculator:
    """Calculator for Rule of Nines burn surface area assessment"""
    
    def __init__(self):
        # Adult body surface area percentages
        self.ADULT_PERCENTAGES = {
            "head_neck": 9.0,
            "anterior_torso": 18.0,
            "posterior_torso": 18.0,
            "right_arm": 9.0,
            "left_arm": 9.0,
            "right_leg": 18.0,
            "left_leg": 18.0,
            "genitalia": 1.0
        }
        
        # Child body surface area percentages (age 1-14)
        self.CHILD_PERCENTAGES = {
            "head_neck": 18.0,
            "anterior_torso": 18.0,
            "posterior_torso": 18.0,
            "right_arm": 9.0,
            "left_arm": 9.0,
            "right_leg": 13.5,
            "left_leg": 13.5,
            "genitalia": 1.0
        }
        
        # Infant body surface area percentages (age <1)
        self.INFANT_PERCENTAGES = {
            "head_neck": 18.0,
            "anterior_torso": 18.0,
            "posterior_torso": 18.0,
            "right_arm": 9.0,
            "left_arm": 9.0,
            "right_leg": 13.5,
            "left_leg": 13.5,
            "genitalia": 1.0
        }
        
        # Clinical thresholds
        self.MINOR_BURN_THRESHOLD = 10.0        # <10% TBSA = minor burn
        self.MODERATE_BURN_THRESHOLD = 20.0     # 10-19% TBSA = moderate burn
        self.MAJOR_BURN_THRESHOLD = 30.0        # 20-29% TBSA = major burn
        # ≥30% TBSA = severe burn
        
        # Fluid resuscitation thresholds
        self.ADULT_FLUID_THRESHOLD = 10.0       # ≥10% TBSA adults need fluids
        self.PEDIATRIC_FLUID_THRESHOLD = 5.0    # ≥5% TBSA children need fluids
    
    def calculate(self, patient_age_group: str, head_neck_percentage: float,
                  anterior_torso_percentage: float, posterior_torso_percentage: float,
                  right_arm_percentage: float, left_arm_percentage: float,
                  right_leg_percentage: float, left_leg_percentage: float,
                  genitalia_percentage: float) -> Dict[str, Any]:
        """
        Calculates total body surface area burned using Rule of Nines
        
        The Rule of Nines divides the body into segments representing 9% (or multiples 
        of 9%) of total body surface area. Different percentages are used for adults 
        versus children due to varying body proportions.
        
        Args:
            patient_age_group (str): Age group ("adult", "child", or "infant")
            head_neck_percentage (float): % of head/neck area burned (0-100)
            anterior_torso_percentage (float): % of anterior torso burned (0-100)
            posterior_torso_percentage (float): % of posterior torso burned (0-100)
            right_arm_percentage (float): % of right arm burned (0-100)
            left_arm_percentage (float): % of left arm burned (0-100)
            right_leg_percentage (float): % of right leg burned (0-100)
            left_leg_percentage (float): % of left leg burned (0-100)
            genitalia_percentage (float): % of genitalia burned (0-100)
            
        Returns:
            Dict with the total body surface area burned and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(patient_age_group, head_neck_percentage, anterior_torso_percentage,
                             posterior_torso_percentage, right_arm_percentage, left_arm_percentage,
                             right_leg_percentage, left_leg_percentage, genitalia_percentage)
        
        # Calculate TBSA based on age group
        tbsa = self._calculate_tbsa(patient_age_group, head_neck_percentage, anterior_torso_percentage,
                                   posterior_torso_percentage, right_arm_percentage, left_arm_percentage,
                                   right_leg_percentage, left_leg_percentage, genitalia_percentage)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(tbsa, patient_age_group)
        
        return {
            "result": round(tbsa, 1),
            "unit": "%",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, patient_age_group: str, head_neck_percentage: float,
                        anterior_torso_percentage: float, posterior_torso_percentage: float,
                        right_arm_percentage: float, left_arm_percentage: float,
                        right_leg_percentage: float, left_leg_percentage: float,
                        genitalia_percentage: float):
        """Validates input parameters for Rule of Nines calculation"""
        
        # Age group validation
        if not isinstance(patient_age_group, str):
            raise ValueError("Patient age group must be a string")
        
        if patient_age_group.lower() not in ["adult", "child", "infant"]:
            raise ValueError("Patient age group must be 'adult', 'child', or 'infant'")
        
        # Percentage validations
        percentages = [
            ("Head/neck", head_neck_percentage),
            ("Anterior torso", anterior_torso_percentage),
            ("Posterior torso", posterior_torso_percentage),
            ("Right arm", right_arm_percentage),
            ("Left arm", left_arm_percentage),
            ("Right leg", right_leg_percentage),
            ("Left leg", left_leg_percentage),
            ("Genitalia", genitalia_percentage)
        ]
        
        for name, percentage in percentages:
            if not isinstance(percentage, (int, float)):
                raise ValueError(f"{name} percentage must be a number")
            
            if percentage < 0 or percentage > 100:
                raise ValueError(f"{name} percentage must be between 0% and 100%")
        
        # Clinical validity checks
        total_input = (head_neck_percentage + anterior_torso_percentage + posterior_torso_percentage +
                      right_arm_percentage + left_arm_percentage + right_leg_percentage +
                      left_leg_percentage + genitalia_percentage)
        
        if total_input > 800:  # Maximum possible if all regions 100% burned
            raise ValueError("Clinical concern: Total input percentages suggest error in assessment")
    
    def _calculate_tbsa(self, patient_age_group: str, head_neck_percentage: float,
                       anterior_torso_percentage: float, posterior_torso_percentage: float,
                       right_arm_percentage: float, left_arm_percentage: float,
                       right_leg_percentage: float, left_leg_percentage: float,
                       genitalia_percentage: float) -> float:
        """
        Calculates total body surface area burned based on age group
        
        Args:
            patient_age_group (str): Patient age category
            [body region percentages]: Percentage of each region burned
            
        Returns:
            float: Total body surface area burned (TBSA %)
        """
        
        # Select appropriate percentage table based on age group
        if patient_age_group.lower() == "adult":
            percentages = self.ADULT_PERCENTAGES
        else:  # child or infant use same percentages
            percentages = self.CHILD_PERCENTAGES
        
        # Calculate TBSA for each body region
        tbsa = 0.0
        
        # Head and neck
        tbsa += (head_neck_percentage / 100.0) * percentages["head_neck"]
        
        # Torso
        tbsa += (anterior_torso_percentage / 100.0) * percentages["anterior_torso"]
        tbsa += (posterior_torso_percentage / 100.0) * percentages["posterior_torso"]
        
        # Arms
        tbsa += (right_arm_percentage / 100.0) * percentages["right_arm"]
        tbsa += (left_arm_percentage / 100.0) * percentages["left_arm"]
        
        # Legs
        tbsa += (right_leg_percentage / 100.0) * percentages["right_leg"]
        tbsa += (left_leg_percentage / 100.0) * percentages["left_leg"]
        
        # Genitalia
        tbsa += (genitalia_percentage / 100.0) * percentages["genitalia"]
        
        return tbsa
    
    def _get_interpretation(self, tbsa: float, patient_age_group: str) -> Dict[str, str]:
        """
        Provides detailed clinical interpretation based on TBSA and age group
        
        Args:
            tbsa (float): Total body surface area burned
            patient_age_group (str): Patient age category
            
        Returns:
            Dict with stage, description, and detailed interpretation
        """
        
        # Determine fluid resuscitation threshold based on age
        fluid_threshold = (self.PEDIATRIC_FLUID_THRESHOLD if patient_age_group.lower() in ["child", "infant"] 
                          else self.ADULT_FLUID_THRESHOLD)
        
        # Generate age-appropriate recommendations
        age_specific_notes = ""
        if patient_age_group.lower() in ["child", "infant"]:
            age_specific_notes = (f" Pediatric patients require fluid resuscitation at ≥{fluid_threshold}% TBSA. "
                                f"Consider early burn center transfer for specialized pediatric burn care.")
        else:
            age_specific_notes = (f" Adult patients require fluid resuscitation at ≥{fluid_threshold}% TBSA. "
                                f"Calculate Parkland formula: 4 mL/kg/% TBSA over 24 hours.")
        
        if tbsa < self.MINOR_BURN_THRESHOLD:
            return {
                "stage": "Minor Burn",
                "description": "Outpatient management usually appropriate",
                "interpretation": (
                    f"Minor burn ({tbsa:.1f}% TBSA) typically manageable on outpatient basis with "
                    f"proper wound care and follow-up. Ensure adequate pain management, tetanus "
                    f"prophylaxis, and wound care education. Monitor for signs of infection and "
                    f"provide clear return precautions.{age_specific_notes} Consider referral to "
                    f"burn specialist for complex burns involving face, hands, feet, joints, or "
                    f"genitalia even if <10% TBSA."
                )
            }
        
        elif tbsa < self.MODERATE_BURN_THRESHOLD:
            return {
                "stage": "Moderate Burn",
                "description": "Consider hospital admission and burn center consultation",
                "interpretation": (
                    f"Moderate burn ({tbsa:.1f}% TBSA) requires careful assessment for hospital "
                    f"admission and burn center consultation. Initiate fluid resuscitation if "
                    f"≥{fluid_threshold}% TBSA.{age_specific_notes} Monitor urine output, vital signs, "
                    f"and pain control. Consider early burn center transfer for optimal care. "
                    f"Establish IV access and begin appropriate fluid management."
                )
            }
        
        elif tbsa < self.MAJOR_BURN_THRESHOLD:
            return {
                "stage": "Major Burn",
                "description": "Hospital admission and burn center transfer required",
                "interpretation": (
                    f"Major burn ({tbsa:.1f}% TBSA) requires immediate hospital admission and burn "
                    f"center transfer. Begin aggressive fluid resuscitation using Parkland formula "
                    f"({tbsa:.1f}% TBSA). Monitor for complications including compartment syndrome, "
                    f"respiratory compromise, and burn shock.{age_specific_notes} Establish central "
                    f"venous access, urinary catheter, and nasogastric tube as indicated. Early "
                    f"surgical consultation for escharotomy if circumferential burns present."
                )
            }
        
        else:  # tbsa >= 30%
            return {
                "stage": "Severe Burn",
                "description": "Life-threatening injury requiring immediate intensive care",
                "interpretation": (
                    f"Severe burn ({tbsa:.1f}% TBSA) represents life-threatening injury requiring "
                    f"immediate intensive care and burn center management. High mortality risk "
                    f"necessitating aggressive resuscitation, airway management, and multi-organ "
                    f"support.{age_specific_notes} Early intubation may be required for airway "
                    f"protection. Massive fluid resuscitation requirements with careful monitoring "
                    f"to avoid fluid overload. Early surgical intervention for escharotomy and "
                    f"burn excision. Nutritional support and infection prevention critical."
                )
            }


def calculate_rule_of_nines(patient_age_group: str, head_neck_percentage: float,
                           anterior_torso_percentage: float, posterior_torso_percentage: float,
                           right_arm_percentage: float, left_arm_percentage: float,
                           right_leg_percentage: float, left_leg_percentage: float,
                           genitalia_percentage: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    Calculates total body surface area burned using Rule of Nines.
    
    Args:
        patient_age_group (str): Age group ("adult", "child", or "infant")
        head_neck_percentage (float): % of head/neck area burned
        anterior_torso_percentage (float): % of anterior torso burned
        posterior_torso_percentage (float): % of posterior torso burned
        right_arm_percentage (float): % of right arm burned
        left_arm_percentage (float): % of left arm burned
        right_leg_percentage (float): % of right leg burned
        left_leg_percentage (float): % of left leg burned
        genitalia_percentage (float): % of genitalia burned
        
    Returns:
        Dict with total body surface area burned and clinical interpretation
    """
    calculator = RuleOfNinesCalculator()
    return calculator.calculate(patient_age_group, head_neck_percentage, anterior_torso_percentage,
                               posterior_torso_percentage, right_arm_percentage, left_arm_percentage,
                               right_leg_percentage, left_leg_percentage, genitalia_percentage)