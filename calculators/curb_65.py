"""
CURB-65 Score Calculator

Avalia a gravidade da pneumonia adquirida na comunidade para determinar 
necessidade de internação hospitalar.
Referência: Lim WS et al. Thorax. 2003;58(5):377-82.
"""

from typing import Dict, Any


class Curb65Calculator:
    """Calculadora para CURB-65 Score"""
    
    def __init__(self):
        # Riscos de mortalidade por pontuação
        self.mortality_risk = {
            0: 1.5,
            1: 1.5,
            2: 9.2,
            3: 22.0,
            4: 22.0,
            5: 22.0
        }
    
    def calculate(self, confusion: bool, urea: float, respiratory_rate: int,
                 systolic_bp: int, diastolic_bp: int, age: int) -> Dict[str, Any]:
        """
        Calcula o CURB-65 score
        
        Args:
            confusion: Confusão mental de início recente
            urea: Ureia sérica em mg/dL
            respiratory_rate: Frequência respiratória (respirações/min)
            systolic_bp: Pressão arterial sistólica (mmHg)
            diastolic_bp: Pressão arterial diastólica (mmHg)
            age: Idade em anos
            
        Returns:
            Dict com resultado, interpretação e risco de mortalidade
        """
        
        # Validações
        self._validate_inputs(confusion, urea, respiratory_rate, systolic_bp, diastolic_bp, age)
        
        # Calcular pontuação
        score = 0
        
        # C - Confusion (1 ponto se presente)
        if confusion:
            score += 1
        
        # U - Urea > 19 mg/dL (1 ponto)
        if urea > 19.0:
            score += 1
        
        # R - Respiratory rate ≥ 30/min (1 ponto)
        if respiratory_rate >= 30:
            score += 1
        
        # B - Blood pressure: PAS < 90 mmHg OU PAD ≤ 60 mmHg (1 ponto)
        if systolic_bp < 90 or diastolic_bp <= 60:
            score += 1
        
        # 65 - Age ≥ 65 anos (1 ponto)
        if age >= 65:
            score += 1
        
        # Obter interpretação
        interpretation = self._get_interpretation(score)
        mortality_risk = self.mortality_risk.get(score, 22.0)
        
        return {
            "result": score,
            "unit": "pontos",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "mortality_risk": f"{mortality_risk}%",
            "components": {
                "confusion": 1 if confusion else 0,
                "urea": 1 if urea > 19.0 else 0,
                "respiratory_rate": 1 if respiratory_rate >= 30 else 0,
                "blood_pressure": 1 if (systolic_bp < 90 or diastolic_bp <= 60) else 0,
                "age": 1 if age >= 65 else 0
            }
        }
    
    def _validate_inputs(self, confusion: bool, urea: float, respiratory_rate: int,
                        systolic_bp: int, diastolic_bp: int, age: int):
        """Valida os parâmetros de entrada"""
        
        if not isinstance(confusion, bool):
            raise ValueError("Confusão deve ser um valor booleano (True/False)")
        
        if not isinstance(urea, (int, float)) or urea < 0 or urea > 200:
            raise ValueError("Ureia deve ser um número entre 0 e 200 mg/dL")
        
        if not isinstance(respiratory_rate, int) or respiratory_rate < 0 or respiratory_rate > 60:
            raise ValueError("Frequência respiratória deve ser um inteiro entre 0 e 60")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 0 or systolic_bp > 300:
            raise ValueError("Pressão sistólica deve ser um inteiro entre 0 e 300 mmHg")
        
        if not isinstance(diastolic_bp, int) or diastolic_bp < 0 or diastolic_bp > 200:
            raise ValueError("Pressão diastólica deve ser um inteiro entre 0 e 200 mmHg")
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Idade deve ser um inteiro entre 0 e 120 anos")
        
        # Validação lógica adicional
        if systolic_bp < diastolic_bp:
            raise ValueError("Pressão sistólica não pode ser menor que a diastólica")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determina a interpretação baseada no score
        
        Args:
            score: CURB-65 score calculado
            
        Returns:
            Dict com interpretação clínica
        """
        
        if score <= 1:
            return {
                "stage": "Baixo Risco",
                "description": "Mortalidade: 1.5%",
                "interpretation": "Tratamento ambulatorial. Considerar antibioticoterapia oral e acompanhamento em 48-72 horas."
            }
        
        elif score == 2:
            return {
                "stage": "Risco Intermediário",
                "description": "Mortalidade: 9.2%",
                "interpretation": "Considerar internação hospitalar vs. observação. Avaliar individualmente fatores sociais, comorbidades e resposta ao tratamento inicial."
            }
        
        else:  # score >= 3
            return {
                "stage": "Alto Risco",
                "description": "Mortalidade: 22%",
                "interpretation": "Internação hospitalar mandatória. Considerar admissão em UTI, especialmente se CURB-65 ≥ 4. Iniciar antibioticoterapia endovenosa imediatamente."
            }


def calculate_curb_65(confusion: bool, urea: float, respiratory_rate: int,
                     systolic_bp: int, diastolic_bp: int, age: int) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_curb_65
    """
    calculator = Curb65Calculator()
    return calculator.calculate(confusion, urea, respiratory_rate,
                               systolic_bp, diastolic_bp, age)