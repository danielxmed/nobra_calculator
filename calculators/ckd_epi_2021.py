"""
CKD-EPI 2021 Calculator

Implementa a equação CKD-EPI 2021 para estimar a taxa de filtração glomerular (TFGe)
baseada em creatinina sérica, idade e sexo.

Fórmula: eGFR = 142 × min(SCr/κ,1)^α × max(SCr/κ,1)^(-1.200) × 0.9938^Age × 1.012 [se feminino]

Onde:
- κ = 0.7 para mulheres, 0.9 para homens
- α = -0.241 para mulheres, -0.302 para homens
"""

import math
from typing import Dict, Any


class CKDEpi2021Calculator:
    """Calculadora para CKD-EPI 2021"""
    
    def __init__(self):
        # Constantes da fórmula
        self.KAPPA_FEMALE = 0.7
        self.KAPPA_MALE = 0.9
        self.ALPHA_FEMALE = -0.241
        self.ALPHA_MALE = -0.302
        self.BASE_MULTIPLIER = 142
        self.AGE_FACTOR = 0.9938
        self.FEMALE_MULTIPLIER = 1.012
        self.CREATININE_EXPONENT = -1.200
    
    def calculate(self, sex: str, age: int, serum_creatinine: float) -> Dict[str, Any]:
        """
        Calcula a TFGe usando a equação CKD-EPI 2021
        
        Args:
            sex (str): "masculino" ou "feminino"
            age (int): Idade em anos
            serum_creatinine (float): Creatinina sérica em mg/dL
            
        Returns:
            Dict com o resultado e interpretação
        """
        
        # Validações
        self._validate_inputs(sex, age, serum_creatinine)
        
        # Determinar constantes baseadas no sexo
        if sex.lower() == "feminino":
            kappa = self.KAPPA_FEMALE
            alpha = self.ALPHA_FEMALE
            sex_multiplier = self.FEMALE_MULTIPLIER
        else:
            kappa = self.KAPPA_MALE
            alpha = self.ALPHA_MALE
            sex_multiplier = 1.0
        
        # Calcular a razão creatinina/kappa
        scr_kappa_ratio = serum_creatinine / kappa
        
        # Aplicar as funções min e max
        min_term = min(scr_kappa_ratio, 1.0)
        max_term = max(scr_kappa_ratio, 1.0)
        
        # Calcular cada componente da fórmula
        min_component = math.pow(min_term, alpha)
        max_component = math.pow(max_term, self.CREATININE_EXPONENT)
        age_component = math.pow(self.AGE_FACTOR, age)
        
        # Calcular eGFR final
        egfr = (self.BASE_MULTIPLIER * 
                min_component * 
                max_component * 
                age_component * 
                sex_multiplier)
        
        # Arredondar para 1 casa decimal
        egfr = round(egfr, 1)
        
        # Obter interpretação
        interpretation = self._get_interpretation(egfr)
        
        return {
            "result": egfr,
            "unit": "mL/min/1.73 m²",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sex: str, age: int, serum_creatinine: float):
        """Valida os parâmetros de entrada"""
        
        if sex.lower() not in ["masculino", "feminino"]:
            raise ValueError("Sexo deve ser 'masculino' ou 'feminino'")
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Idade deve ser um número inteiro entre 18 e 120 anos")
        
        if not isinstance(serum_creatinine, (int, float)) or serum_creatinine <= 0:
            raise ValueError("Creatinina sérica deve ser um valor positivo")
        
        if serum_creatinine < 0.1 or serum_creatinine > 20.0:
            raise ValueError("Creatinina sérica deve estar entre 0.1 e 20.0 mg/dL")
    
    def _get_interpretation(self, egfr: float) -> Dict[str, str]:
        """
        Determina a interpretação baseada no valor da TFGe
        
        Args:
            egfr (float): Taxa de filtração glomerular estimada
            
        Returns:
            Dict com stage, description e interpretation
        """
        
        if egfr >= 90:
            return {
                "stage": "G1",
                "description": "Função renal normal ou elevada",
                "interpretation": "TFG normal ou elevada. Investigar presença de lesão renal para definir se há DRC."
            }
        elif egfr >= 60:
            return {
                "stage": "G2",
                "description": "Diminuição leve da TFG",
                "interpretation": "Diminuição leve da TFG. Investigar presença de lesão renal para definir se há DRC."
            }
        elif egfr >= 45:
            return {
                "stage": "G3a",
                "description": "Diminuição leve a moderada da TFG",
                "interpretation": "Estágio 3a de Doença Renal Crônica. Acompanhamento nefrológico recomendado."
            }
        elif egfr >= 30:
            return {
                "stage": "G3b",
                "description": "Diminuição moderada a grave da TFG",
                "interpretation": "Estágio 3b de Doença Renal Crônica. Encaminhamento ao nefrologista necessário."
            }
        elif egfr >= 15:
            return {
                "stage": "G4",
                "description": "Diminuição grave da TFG",
                "interpretation": "Estágio 4 de Doença Renal Crônica. Acompanhamento nefrológico especializado e preparação para terapia renal substitutiva."
            }
        else:
            return {
                "stage": "G5",
                "description": "Falência renal",
                "interpretation": "Estágio 5 de Doença Renal Crônica (falência renal). Necessária terapia renal substitutiva (diálise ou transplante)."
            }


def calculate_ckd_epi_2021(sex: str, age: int, serum_creatinine: float) -> Dict[str, Any]:
    """
    Função de conveniência para calcular CKD-EPI 2021
    
    Args:
        sex (str): "masculino" ou "feminino"
        age (int): Idade em anos
        serum_creatinine (float): Creatinina sérica em mg/dL
        
    Returns:
        Dict com o resultado e interpretação
    """
    calculator = CKDEpi2021Calculator()
    return calculator.calculate(sex, age, serum_creatinine)
