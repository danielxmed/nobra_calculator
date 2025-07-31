"""
Glucose Infusion Rate (GIR) Calculator

The Glucose Infusion Rate (GIR) is a critical calculation in neonatal and pediatric 
care that quantifies the rate at which glucose is administered intravenously. It is 
essential for maintaining appropriate blood glucose levels, preventing hypoglycemia, 
and optimizing nutritional support, particularly in preterm infants and critically 
ill children who cannot feed orally.

The GIR helps clinicians:
- Ensure adequate glucose delivery to prevent hypoglycemia
- Monitor and adjust parenteral nutrition
- Avoid excessive glucose administration that can lead to hyperglycemia
- Guide insulin therapy decisions when needed

References (Vancouver style):
1. Kalhan SC, Parimi PS. Gluconeogenesis in the fetus and neonate. Semin Perinatol. 
   2000;24(2):94-106. doi: 10.1053/sp.2000.6360.
2. Ditzenberger GR, Collins SD, Binder N. Continuous insulin infusion in the management 
   of hyperglycemia in the pediatric intensive care unit. Pediatr Crit Care Med. 
   2004;5(1):27-32. doi: 10.1097/01.PCC.0000102223.83245.02.
3. Sinclair JC, Bottino M, Cowett RM. Interventions for prevention of neonatal 
   hyperglycemia in very low birth weight infants. Cochrane Database Syst Rev. 
   2011;(10):CD007615. doi: 10.1002/14651858.CD007615.pub3.
4. Hay WW Jr, Raju TN, Higgins RD, Kalhan SC, Devaskar SU. Knowledge gaps and research 
   needs for understanding and treating neonatal hypoglycemia: workshop report from 
   Eunice Kennedy Shriver National Institute of Child Health and Human Development. 
   J Pediatr. 2009;155(5):612-617. doi: 10.1016/j.jpeds.2009.06.044.
"""

from typing import Dict, Any


class GlucoseInfusionRateCalculator:
    """Calculator for Glucose Infusion Rate (GIR)"""
    
    def __init__(self):
        # Clinical reference ranges (mg/kg/min)
        self.NORMAL_MIN = 4.0
        self.NORMAL_MAX = 8.0
        self.THERAPEUTIC_MIN = 8.1
        self.THERAPEUTIC_MAX = 12.0
        self.HIGH_THERAPEUTIC_MIN = 12.1
        self.HIGH_THERAPEUTIC_MAX = 18.0
        self.EXCESSIVE_THRESHOLD = 18.1
        
        # Common dextrose concentrations and their clinical uses
        self.DEXTROSE_CONCENTRATIONS = {
            2.5: "D2.5W - Very dilute, rarely used",
            5.0: "D5W - Standard maintenance fluid",
            7.5: "D7.5W - Intermediate concentration",
            10.0: "D10W - Common in neonatal care",
            12.5: "D12.5W - Higher concentration, often central line",
            15.0: "D15W - High concentration, central line required",
            20.0: "D20W - Very high concentration, central line required",
            25.0: "D25W - Maximum typical concentration"
        }
    
    def calculate(self, infusion_rate: float, dextrose_concentration: float, 
                 weight: float) -> Dict[str, Any]:
        """
        Calculates Glucose Infusion Rate (GIR) from IV parameters
        
        Args:
            infusion_rate (float): IV infusion rate in mL/hr
            dextrose_concentration (float): Dextrose concentration as percentage (e.g., 10.0 for D10W)
            weight (float): Patient weight in kg
            
        Returns:
            Dict with GIR value and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(infusion_rate, dextrose_concentration, weight)
        
        # Calculate GIR using standard formula
        gir = self._calculate_gir(infusion_rate, dextrose_concentration, weight)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(gir, infusion_rate, dextrose_concentration, weight)
        
        return {
            "result": round(gir, 2),
            "unit": "mg/kg/min",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, infusion_rate: float, dextrose_concentration: float, weight: float):
        """Validates input parameters"""
        
        if not isinstance(infusion_rate, (int, float)) or infusion_rate <= 0 or infusion_rate > 1000:
            raise ValueError("Infusion rate must be a positive number between 0.1 and 1000 mL/hr")
        
        if not isinstance(dextrose_concentration, (int, float)) or dextrose_concentration < 1 or dextrose_concentration > 50:
            raise ValueError("Dextrose concentration must be between 1% and 50%")
        
        if not isinstance(weight, (int, float)) or weight < 0.5 or weight > 200:
            raise ValueError("Weight must be between 0.5 and 200 kg")
    
    def _calculate_gir(self, infusion_rate: float, dextrose_concentration: float, weight: float) -> float:
        """
        Calculates GIR using the standard formula
        
        Formula: GIR (mg/kg/min) = [Infusion rate (mL/hr) × Dextrose concentration (%) × 10] / [Weight (kg) × 60]
        
        Derivation:
        - Dextrose concentration (%) × 10 = mg of dextrose per mL
        - Infusion rate × concentration gives mg/hr of dextrose
        - Divide by weight (kg) to get mg/kg/hr
        - Divide by 60 to convert to mg/kg/min
        """
        
        # Convert percentage to mg/mL (e.g., 10% = 100 mg/mL)
        dextrose_mg_per_ml = dextrose_concentration * 10
        
        # Calculate total glucose delivery in mg/hr
        glucose_per_hour = infusion_rate * dextrose_mg_per_ml
        
        # Convert to mg/kg/min
        gir = glucose_per_hour / (weight * 60)
        
        return gir
    
    def _get_interpretation(self, gir: float, infusion_rate: float, 
                          dextrose_concentration: float, weight: float) -> Dict[str, str]:
        """
        Provides clinical interpretation based on GIR value
        
        Returns:
            Dict with clinical interpretation and recommendations
        """
        
        # Calculate alternative simplified formula for comparison
        # GIR ≈ (D × DIR) / 6, where DIR is mL/kg/hr
        dir_per_kg = infusion_rate / weight
        simplified_gir = (dextrose_concentration * dir_per_kg) / 6
        
        # Build parameter summary
        parameter_summary = (
            f"Infusion parameters: {infusion_rate} mL/hr of D{dextrose_concentration}W "
            f"({dextrose_concentration}% dextrose) in {weight} kg patient. "
            f"Calculated GIR: {gir:.2f} mg/kg/min. "
            f"Verification (simplified formula): {simplified_gir:.2f} mg/kg/min."
        )
        
        # Determine clinical category and recommendations
        if gir < self.NORMAL_MIN:
            return {
                "stage": "Below Normal Range",
                "description": "Insufficient glucose delivery",
                "interpretation": (
                    f"{parameter_summary} GIR below {self.NORMAL_MIN} mg/kg/min may be "
                    f"insufficient to prevent hypoglycemia in neonates and infants not feeding "
                    f"orally. Risk of hypoglycemia, especially in preterm infants or those with "
                    f"increased metabolic demands. Recommendations: Consider increasing dextrose "
                    f"concentration (e.g., from D5W to D10W) or infusion rate. Monitor blood "
                    f"glucose closely every 2-4 hours. Ensure GIR ≥4 mg/kg/min as minimum. "
                    f"Evaluate for signs of hypoglycemia (jitteriness, lethargy, seizures). "
                    f"Consider enteral feeding if appropriate."
                )
            }
        elif gir <= self.NORMAL_MAX:
            return {
                "stage": "Normal/Physiologic Range",
                "description": "Appropriate glucose delivery",
                "interpretation": (
                    f"{parameter_summary} GIR {self.NORMAL_MIN}-{self.NORMAL_MAX} mg/kg/min "
                    f"represents normal glucose utilization rate. This range covers baseline "
                    f"glucose needs and is appropriate for maintaining euglycemia in most "
                    f"neonates and infants receiving IV fluids without enteral nutrition. "
                    f"Recommendations: Continue current regimen with routine glucose monitoring "
                    f"every 4-6 hours. Appropriate for maintenance therapy in stable patients. "
                    f"Monitor for clinical signs of hypo- or hyperglycemia. Consider advancing "
                    f"to enteral feeds when clinically appropriate."
                )
            }
        elif gir <= self.THERAPEUTIC_MAX:
            return {
                "stage": "Moderate/Therapeutic Range",
                "description": "Enhanced glucose delivery",
                "interpretation": (
                    f"{parameter_summary} GIR {self.THERAPEUTIC_MIN:.1f}-{self.THERAPEUTIC_MAX} "
                    f"mg/kg/min provides enhanced glucose delivery for growth and anabolism. "
                    f"Common in parenteral nutrition protocols for adequate caloric intake. "
                    f"Recommendations: Monitor blood glucose every 4-6 hours for hyperglycemia. "
                    f"May require Level 3 NICU care for close monitoring. Consider insulin "
                    f"therapy if blood glucose consistently >150-180 mg/dL. Ensure adequate "
                    f"protein and lipid intake to balance nutrition. Monitor for signs of "
                    f"glucose intolerance."
                )
            }
        elif gir <= self.HIGH_THERAPEUTIC_MAX:
            return {
                "stage": "High Therapeutic Range",
                "description": "High glucose delivery for nutrition",
                "interpretation": (
                    f"{parameter_summary} GIR {self.HIGH_THERAPEUTIC_MIN:.1f}-{self.HIGH_THERAPEUTIC_MAX} "
                    f"mg/kg/min represents high glucose delivery typically used in full parenteral "
                    f"nutrition. Optimal for growth in premature infants with high metabolic "
                    f"demands. Recommendations: Frequent glucose monitoring (every 2-4 hours). "
                    f"Likely requires insulin co-administration to prevent hyperglycemia. "
                    f"Monitor for signs of glucose intolerance, increased CO2 production, and "
                    f"respiratory burden. Consider central line access for safe administration "
                    f"of high-concentration dextrose. Balance with appropriate protein and lipid "
                    f"calories."
                )
            }
        else:  # gir > HIGH_THERAPEUTIC_MAX
            return {
                "stage": "Excessive Range",
                "description": "Risk of metabolic complications",
                "interpretation": (
                    f"{parameter_summary} GIR >{self.HIGH_THERAPEUTIC_MAX} mg/kg/min is "
                    f"excessive and increases risk of hyperglycemia, lipogenesis, fatty liver "
                    f"deposits, and increased CO2 production. Associated with respiratory burden "
                    f"and metabolic complications. Recommendations: IMMEDIATE reduction in glucose "
                    f"load by decreasing dextrose concentration or infusion rate. Implement "
                    f"insulin therapy if blood glucose >180 mg/dL. Increase lipid contribution "
                    f"to total calories (up to 3-4 g/kg/day). Monitor arterial blood gases for "
                    f"increased CO2. Assess liver function tests. Consider consultation with "
                    f"neonatal nutrition specialist. Target GIR reduction to <18 mg/kg/min."
                )
            }


def calculate_glucose_infusion_rate(infusion_rate: float, dextrose_concentration: float, 
                                  weight: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_glucose_infusion_rate pattern
    """
    calculator = GlucoseInfusionRateCalculator()
    return calculator.calculate(infusion_rate, dextrose_concentration, weight)