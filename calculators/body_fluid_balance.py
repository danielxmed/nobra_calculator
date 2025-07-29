"""
Body Fluid Balance Calculator by Inputs and Outputs

Calculates fluid balance from sodium concentrations indicating 0.9% saline fluid, 
and free water losses (GI, urine, etc) and gains (IV fluids, PO, etc).

References:
1. Kaptein EM, et al. A systematic approach to factitious hypernatremia. Clin Nephrol. 2016;85(4):246-52.
2. Konstam MA, et al. Effects of oral tolvaptan in patients hospitalized for worsening heart failure. JAMA. 2007;297(12):1319-31.
3. Testani JM, et al. Timing of hemoconcentration during treatment of acute decompensated heart failure. J Am Coll Cardiol. 2013;62(6):516-24.
"""

from typing import Dict, Any, Optional


class BodyFluidBalanceCalculator:
    """Calculator for Body Fluid Balance by Inputs and Outputs"""
    
    def __init__(self):
        # Sodium concentrations in mEq/L for various fluids
        self.SODIUM_CONCENTRATIONS = {
            'gastric': 60,          # Gastric secretions
            'biliary': 130,         # Bile
            'small_bowel': 110,     # Small bowel fluid
            'diarrhea': 60,         # Diarrheal fluid
            'urine': 40,            # Average urine sodium
            'insensible': 0,        # Pure water loss
            'other': 140,           # Assume isotonic for other losses
            'normal_saline': 154,   # 0.9% NS
            'half_normal_saline': 77,  # 0.45% NS
            'lactated_ringers': 130,   # LR
            'd5w': 0,               # D5W is free water
            'oral': 0               # Oral intake assumed as free water
        }
        
        # Reference sodium concentration for isotonic fluid (0.9% NS)
        self.ISOTONIC_SODIUM = 154  # mEq/L
    
    def calculate(self, 
                 gastric_losses: Optional[float] = 0,
                 biliary_losses: Optional[float] = 0,
                 small_bowel_losses: Optional[float] = 0,
                 diarrhea_losses: Optional[float] = 0,
                 urine_output: Optional[float] = 0,
                 insensible_losses: Optional[float] = 0,
                 other_losses: Optional[float] = 0,
                 normal_saline_iv: Optional[float] = 0,
                 half_normal_saline_iv: Optional[float] = 0,
                 lactated_ringers_iv: Optional[float] = 0,
                 d5w_iv: Optional[float] = 0,
                 oral_intake: Optional[float] = 0) -> Dict[str, Any]:
        """
        Calculates fluid balance based on inputs and outputs with sodium concentrations
        
        Args:
            gastric_losses: Volume of gastric losses in mL
            biliary_losses: Volume of biliary losses in mL
            small_bowel_losses: Volume of small bowel losses in mL
            diarrhea_losses: Volume of diarrhea losses in mL
            urine_output: Volume of urine output in mL
            insensible_losses: Estimated insensible losses in mL
            other_losses: Other fluid losses in mL
            normal_saline_iv: Volume of 0.9% NS administered in mL
            half_normal_saline_iv: Volume of 0.45% NS administered in mL
            lactated_ringers_iv: Volume of LR administered in mL
            d5w_iv: Volume of D5W administered in mL
            oral_intake: Volume of oral fluid intake in mL
            
        Returns:
            Dict with fluid balance calculations and interpretation
        """
        
        # Convert None to 0 for calculations
        gastric_losses = gastric_losses or 0
        biliary_losses = biliary_losses or 0
        small_bowel_losses = small_bowel_losses or 0
        diarrhea_losses = diarrhea_losses or 0
        urine_output = urine_output or 0
        insensible_losses = insensible_losses or 0
        other_losses = other_losses or 0
        normal_saline_iv = normal_saline_iv or 0
        half_normal_saline_iv = half_normal_saline_iv or 0
        lactated_ringers_iv = lactated_ringers_iv or 0
        d5w_iv = d5w_iv or 0
        oral_intake = oral_intake or 0
        
        # Validate inputs
        self._validate_inputs(gastric_losses, biliary_losses, small_bowel_losses,
                             diarrhea_losses, urine_output, insensible_losses,
                             other_losses, normal_saline_iv, half_normal_saline_iv,
                             lactated_ringers_iv, d5w_iv, oral_intake)
        
        # Calculate losses
        losses = {
            'gastric': (gastric_losses, self.SODIUM_CONCENTRATIONS['gastric']),
            'biliary': (biliary_losses, self.SODIUM_CONCENTRATIONS['biliary']),
            'small_bowel': (small_bowel_losses, self.SODIUM_CONCENTRATIONS['small_bowel']),
            'diarrhea': (diarrhea_losses, self.SODIUM_CONCENTRATIONS['diarrhea']),
            'urine': (urine_output, self.SODIUM_CONCENTRATIONS['urine']),
            'insensible': (insensible_losses, self.SODIUM_CONCENTRATIONS['insensible']),
            'other': (other_losses, self.SODIUM_CONCENTRATIONS['other'])
        }
        
        # Calculate gains
        gains = {
            'normal_saline': (normal_saline_iv, self.SODIUM_CONCENTRATIONS['normal_saline']),
            'half_normal_saline': (half_normal_saline_iv, self.SODIUM_CONCENTRATIONS['half_normal_saline']),
            'lactated_ringers': (lactated_ringers_iv, self.SODIUM_CONCENTRATIONS['lactated_ringers']),
            'd5w': (d5w_iv, self.SODIUM_CONCENTRATIONS['d5w']),
            'oral': (oral_intake, self.SODIUM_CONCENTRATIONS['oral'])
        }
        
        # Calculate saline and free water balance
        total_saline_lost, total_water_lost = self._calculate_fluid_components(losses)
        total_saline_gained, total_water_gained = self._calculate_fluid_components(gains)
        
        # Calculate net balances
        net_saline_balance = total_saline_gained - total_saline_lost
        net_water_balance = total_water_gained - total_water_lost
        total_fluid_balance = (net_saline_balance + net_water_balance)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_fluid_balance)
        
        # Format results
        results = {
            'total_fluid_balance': round(total_fluid_balance),
            'net_saline_balance': round(net_saline_balance),
            'net_water_balance': round(net_water_balance),
            'total_losses': round(sum(vol for vol, _ in losses.values())),
            'total_gains': round(sum(vol for vol, _ in gains.values()))
        }
        
        return {
            "result": results,
            "unit": "mL",
            "interpretation": self._format_interpretation(results, interpretation),
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *volumes):
        """Validates input volumes"""
        for volume in volumes:
            if not isinstance(volume, (int, float)) or volume < 0:
                raise ValueError("All volumes must be non-negative numbers")
            if volume > 10000:
                raise ValueError("Volume inputs should not exceed 10000 mL")
    
    def _calculate_fluid_components(self, fluids: Dict[str, tuple]) -> tuple:
        """
        Calculates saline equivalent and free water from fluids
        
        Args:
            fluids: Dict of fluid name to (volume, sodium_concentration) tuples
            
        Returns:
            Tuple of (total_saline_equivalent, total_free_water) in mL
        """
        total_saline = 0
        total_water = 0
        
        for fluid_name, (volume, sodium_conc) in fluids.items():
            if volume > 0:
                # Calculate 0.9% saline equivalent
                saline_equivalent = volume * (sodium_conc / self.ISOTONIC_SODIUM)
                # Calculate free water component
                free_water = volume * (1 - sodium_conc / self.ISOTONIC_SODIUM)
                
                total_saline += saline_equivalent
                total_water += free_water
        
        return total_saline, total_water
    
    def _get_interpretation(self, total_balance: float) -> Dict[str, str]:
        """
        Determines fluid balance interpretation
        
        Args:
            total_balance: Net fluid balance in mL
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if total_balance <= -500:
            return {
                "stage": "Significant Negative Balance",
                "description": "Net fluid loss >500 mL",
                "interpretation": "Significant fluid deficit requiring prompt replacement. Assess for signs of volume depletion including hypotension, tachycardia, decreased urine output, and elevated BUN/Cr ratio. Consider IV fluid resuscitation based on sodium and free water deficits."
            }
        elif total_balance <= -200:
            return {
                "stage": "Moderate Negative Balance",
                "description": "Net fluid loss 200-500 mL",
                "interpretation": "Moderate fluid deficit that may require intervention. Monitor vital signs and urine output closely. Consider fluid replacement if clinical signs of dehydration present or if trend continues."
            }
        elif total_balance <= 200:
            return {
                "stage": "Neutral Balance",
                "description": "Net fluid balance -200 to +200 mL",
                "interpretation": "Appropriate fluid balance maintained. Continue current fluid management strategy with routine monitoring. This represents euvolemia in most clinical contexts."
            }
        elif total_balance <= 500:
            return {
                "stage": "Moderate Positive Balance",
                "description": "Net fluid gain 200-500 mL",
                "interpretation": "Moderate fluid accumulation. Monitor for signs of volume overload including peripheral edema, pulmonary congestion, and weight gain. Consider fluid restriction or diuretics if clinically indicated."
            }
        else:  # total_balance > 500
            return {
                "stage": "Significant Positive Balance",
                "description": "Net fluid gain >500 mL",
                "interpretation": "Significant fluid overload risk. Assess for signs of congestion including elevated JVP, crackles, S3 gallop, and orthopnea. Strong consideration for diuretic therapy or fluid restriction unless intentional volume expansion indicated."
            }
    
    def _format_interpretation(self, results: Dict[str, Any], interpretation: Dict[str, str]) -> str:
        """
        Formats comprehensive clinical interpretation
        
        Args:
            results: Calculation results
            interpretation: Stage interpretation
            
        Returns:
            str: Formatted interpretation text
        """
        
        balance_direction = "positive" if results['total_fluid_balance'] > 0 else "negative"
        
        interpretation_text = (
            f"Total fluid balance: {results['total_fluid_balance']:+.0f} mL "
            f"({balance_direction} balance). "
            f"Saline balance: {results['net_saline_balance']:+.0f} mL, "
            f"Free water balance: {results['net_water_balance']:+.0f} mL. "
            f"Total inputs: {results['total_gains']:.0f} mL, "
            f"Total outputs: {results['total_losses']:.0f} mL. "
            f"{interpretation['interpretation']} "
            f"This calculation assumes standard sodium concentrations which may vary based on individual patient factors."
        )
        
        return interpretation_text


def calculate_body_fluid_balance(gastric_losses: Optional[float] = 0,
                                biliary_losses: Optional[float] = 0,
                                small_bowel_losses: Optional[float] = 0,
                                diarrhea_losses: Optional[float] = 0,
                                urine_output: Optional[float] = 0,
                                insensible_losses: Optional[float] = 0,
                                other_losses: Optional[float] = 0,
                                normal_saline_iv: Optional[float] = 0,
                                half_normal_saline_iv: Optional[float] = 0,
                                lactated_ringers_iv: Optional[float] = 0,
                                d5w_iv: Optional[float] = 0,
                                oral_intake: Optional[float] = 0) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BodyFluidBalanceCalculator()
    return calculator.calculate(
        gastric_losses, biliary_losses, small_bowel_losses,
        diarrhea_losses, urine_output, insensible_losses,
        other_losses, normal_saline_iv, half_normal_saline_iv,
        lactated_ringers_iv, d5w_iv, oral_intake
    )