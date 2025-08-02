"""
Intrauterine RBC Transfusion Dosage Calculator

Estimates volume of donor RBCs needed for intrauterine transfusion (IUT) in fetal anemia cases.
Used primarily for severe fetal anemia in hemolytic disease of the fetus and newborn (HDFN) when 
maternal RBC alloantibodies threaten fetal health.

References:
1. Mandelbrot L, Daffos F, Forestier F, MacAleese J, Descamps P. Assessment of fetal blood volume for computer-assisted management of in utero transfusion. Fetal Ther. 1988;3(1-2):60-6.
2. Liley AW. Intrauterine transfusion of foetus in haemolytic disease. Br Med J. 1963;2(5365):1107-9.
3. Society for Maternal-Fetal Medicine (SMFM). Management of alloimmunization during pregnancy. Am J Obstet Gynecol. 2018;218(2):B7-B18.
4. Van Kamp IL, et al. Complications of intrauterine intravascular transfusion for fetal anemia. Am J Obstet Gynecol. 2005;192(1):171-7.
"""

import math
from typing import Dict, Any


class IntrauterineRbcTransfusionDosageCalculator:
    """Calculator for Intrauterine RBC Transfusion Dosage"""
    
    def __init__(self):
        # Fetoplacental volume coefficient (mL/g of fetal weight)
        self.FETOPLACENTAL_VOLUME_COEFFICIENT = 0.14
    
    def calculate(self, fetal_weight_g: float, initial_hematocrit: float, 
                 goal_hematocrit: float, transfused_hematocrit: float) -> Dict[str, Any]:
        """
        Calculates intrauterine RBC transfusion volume
        
        Args:
            fetal_weight_g (float): Estimated fetal weight in grams
            initial_hematocrit (float): Current fetal hematocrit percentage
            goal_hematocrit (float): Target fetal hematocrit percentage
            transfused_hematocrit (float): Hematocrit of donor RBC unit
            
        Returns:
            Dict with transfusion volume and interpretation
        """
        
        # Validations
        self._validate_inputs(fetal_weight_g, initial_hematocrit, goal_hematocrit, transfused_hematocrit)
        
        # Calculate transfusion volume
        transfusion_volume = self._calculate_transfusion_volume(
            fetal_weight_g, initial_hematocrit, goal_hematocrit, transfused_hematocrit
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(transfusion_volume, fetal_weight_g)
        
        return {
            "result": round(transfusion_volume, 1),
            "unit": "mL",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, fetal_weight_g: float, initial_hematocrit: float, 
                        goal_hematocrit: float, transfused_hematocrit: float):
        """Validates input parameters"""
        
        if not isinstance(fetal_weight_g, (int, float)) or fetal_weight_g < 200 or fetal_weight_g > 5000:
            raise ValueError("fetal_weight_g must be a number between 200 and 5000 grams")
        
        if not isinstance(initial_hematocrit, (int, float)) or initial_hematocrit < 5 or initial_hematocrit > 60:
            raise ValueError("initial_hematocrit must be a number between 5 and 60%")
        
        if not isinstance(goal_hematocrit, (int, float)) or goal_hematocrit < 25 or goal_hematocrit > 60:
            raise ValueError("goal_hematocrit must be a number between 25 and 60%")
        
        if not isinstance(transfused_hematocrit, (int, float)) or transfused_hematocrit < 60 or transfused_hematocrit > 90:
            raise ValueError("transfused_hematocrit must be a number between 60 and 90%")
        
        if goal_hematocrit <= initial_hematocrit:
            raise ValueError("goal_hematocrit must be greater than initial_hematocrit")
    
    def _calculate_transfusion_volume(self, fetal_weight_g: float, initial_hematocrit: float, 
                                    goal_hematocrit: float, transfused_hematocrit: float) -> float:
        """
        Calculates the required transfusion volume using the standard formula
        
        Args:
            fetal_weight_g (float): Fetal weight in grams
            initial_hematocrit (float): Initial hematocrit percentage
            goal_hematocrit (float): Goal hematocrit percentage
            transfused_hematocrit (float): Transfused RBC hematocrit percentage
            
        Returns:
            float: Transfusion volume in mL
        """
        
        # Calculate fetoplacental volume (mL)
        fetoplacental_volume = fetal_weight_g * self.FETOPLACENTAL_VOLUME_COEFFICIENT
        
        # Calculate hematocrit difference needed
        hematocrit_difference = goal_hematocrit - initial_hematocrit
        
        # Calculate transfusion volume using the standard formula
        # Volume = Fetoplacental volume × [Hct(goal) - Hct(initial)] / Hct(transfused)
        transfusion_volume = fetoplacental_volume * (hematocrit_difference / transfused_hematocrit)
        
        return transfusion_volume
    
    def _get_interpretation(self, transfusion_volume: float, fetal_weight_g: float) -> Dict[str, str]:
        """
        Gets clinical interpretation based on transfusion volume
        
        Args:
            transfusion_volume (float): Calculated transfusion volume in mL
            fetal_weight_g (float): Fetal weight in grams
            
        Returns:
            Dict with interpretation details
        """
        
        if transfusion_volume < 20:
            return {
                "stage": "Small Volume",
                "description": "Small transfusion volume",
                "interpretation": f"Small volume transfusion ({transfusion_volume:.1f} mL) appropriate for early gestational age or mild anemia. This volume represents a conservative approach that minimizes risk of circulatory overload. Monitor fetal heart rate closely during and after transfusion. Ensure adequate venous access and consider pre-medication to prevent fetal bradycardia. Post-transfusion hematocrit should be checked to confirm adequate response."
            }
        elif transfusion_volume < 60:
            return {
                "stage": "Moderate Volume",
                "description": "Moderate transfusion volume",
                "interpretation": f"Moderate volume transfusion ({transfusion_volume:.1f} mL) typical for established fetal anemia in fetuses weighing approximately {fetal_weight_g:.0f}g. Standard monitoring protocols apply including continuous fetal heart rate monitoring, ultrasound guidance, and post-procedure assessment. Donor blood should be CMV-negative, irradiated, and crossmatched with maternal serum. Consider pancuronium for fetal immobilization during the procedure."
            }
        else:
            return {
                "stage": "Large Volume",
                "description": "Large transfusion volume",
                "interpretation": f"Large volume transfusion ({transfusion_volume:.1f} mL) for severe anemia or larger fetus (weight: {fetal_weight_g:.0f}g). This significant volume requires careful monitoring for circulatory overload and may necessitate staged transfusions or slower infusion rates. Consider dividing into multiple smaller transfusions if volume exceeds fetal circulatory capacity. Enhanced monitoring includes arterial Doppler studies, amniotic fluid assessment, and extended post-procedure observation. Coordinate with neonatal team for potential early delivery if complications arise."
            }


def calculate_intrauterine_rbc_transfusion_dosage(fetal_weight_g: float, initial_hematocrit: float, 
                                                goal_hematocrit: float, transfused_hematocrit: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_intrauterine_rbc_transfusion_dosage pattern
    """
    calculator = IntrauterineRbcTransfusionDosageCalculator()
    return calculator.calculate(fetal_weight_g, initial_hematocrit, goal_hematocrit, transfused_hematocrit)