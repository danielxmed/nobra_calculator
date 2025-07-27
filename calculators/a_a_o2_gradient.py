"""
A-a O₂ Gradient Calculator

Avalia grau de shunt e incompatibilidade V/Q através do gradiente alveolar-arterial de oxigênio.
Referência: Equação do gás alveolar e fisiologia respiratória
"""

from typing import Dict, Any, Optional


class AAO2GradientCalculator:
    """Calculadora para Gradiente A-a O₂"""
    
    def __init__(self):
        # Constantes fisiológicas
        self.DEFAULT_PATM = 760.0  # Pressão atmosférica ao nível do mar (mmHg)
        self.PH2O = 47.0  # Pressão de vapor d'água a 37°C (mmHg)
        self.DEFAULT_RQ = 0.8  # Quociente respiratório padrão
    
    def calculate(self, age: int, fio2: float, paco2: float, pao2: float,
                 patm: Optional[float] = None, respiratory_quotient: Optional[float] = None) -> Dict[str, Any]:
        """
        Calcula o gradiente alveolar-arterial de oxigênio
        
        Args:
            age: Idade em anos
            fio2: Fração inspirada de oxigênio (0.21 para ar ambiente)
            paco2: Pressão parcial de CO₂ arterial (mmHg)
            pao2: Pressão parcial de O₂ arterial (mmHg)
            patm: Pressão atmosférica (padrão: 760 mmHg)
            respiratory_quotient: Quociente respiratório (padrão: 0.8)
            
        Returns:
            Dict com resultado do gradiente e interpretação
        """
        
        # Usar valores padrão se não fornecidos
        if patm is None:
            patm = self.DEFAULT_PATM
        if respiratory_quotient is None:
            respiratory_quotient = self.DEFAULT_RQ
        
        # Validações
        self._validate_inputs(age, fio2, paco2, pao2, patm, respiratory_quotient)
        
        # Calcular PAO₂ (pressão alveolar de oxigênio) usando equação do gás alveolar
        pao2_alveolar = self._calculate_alveolar_oxygen(fio2, paco2, patm, respiratory_quotient)
        
        # Calcular gradiente A-a
        aa_gradient = pao2_alveolar - pao2
        
        # Calcular gradiente normal ajustado para idade
        normal_gradient_age_adjusted = (age / 4.0) + 4.0
        
        # Obter interpretação
        interpretation = self._get_interpretation(aa_gradient, age, normal_gradient_age_adjusted)
        
        return {
            "result": round(aa_gradient, 1),
            "unit": "mmHg",
            "pao2_alveolar": round(pao2_alveolar, 1),
            "normal_gradient_age_adjusted": round(normal_gradient_age_adjusted, 1),
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, fio2: float, paco2: float, pao2: float,
                        patm: float, respiratory_quotient: float):
        """Valida os parâmetros de entrada"""
        
        if not isinstance(age, int) or age < 1 or age > 120:
            raise ValueError("Idade deve ser um inteiro entre 1 e 120 anos")
        
        if not isinstance(fio2, (int, float)) or fio2 < 0.21 or fio2 > 1.0:
            raise ValueError("FiO₂ deve estar entre 0.21 e 1.0")
        
        if not isinstance(paco2, (int, float)) or paco2 < 10.0 or paco2 > 100.0:
            raise ValueError("PaCO₂ deve estar entre 10.0 e 100.0 mmHg")
        
        if not isinstance(pao2, (int, float)) or pao2 < 30.0 or pao2 > 600.0:
            raise ValueError("PaO₂ deve estar entre 30.0 e 600.0 mmHg")
        
        if not isinstance(patm, (int, float)) or patm < 500.0 or patm > 800.0:
            raise ValueError("Pressão atmosférica deve estar entre 500.0 e 800.0 mmHg")
        
        if not isinstance(respiratory_quotient, (int, float)) or respiratory_quotient < 0.7 or respiratory_quotient > 1.0:
            raise ValueError("Quociente respiratório deve estar entre 0.7 e 1.0")
    
    def _calculate_alveolar_oxygen(self, fio2: float, paco2: float, patm: float, rq: float) -> float:
        """
        Calcula a pressão alveolar de oxigênio usando a equação do gás alveolar
        
        PAO₂ = (Patm - PH₂O) × FiO₂ - PaCO₂/RQ
        
        Args:
            fio2: Fração inspirada de oxigênio
            paco2: Pressão parcial de CO₂ arterial
            patm: Pressão atmosférica
            rq: Quociente respiratório
            
        Returns:
            Pressão alveolar de oxigênio em mmHg
        """
        
        # Equação do gás alveolar
        pao2_alveolar = (patm - self.PH2O) * fio2 - (paco2 / rq)
        
        return max(pao2_alveolar, 0.0)  # Garantir valor não negativo
    
    def _get_interpretation(self, aa_gradient: float, age: int, 
                          normal_gradient_age_adjusted: float) -> Dict[str, str]:
        """
        Interpreta o gradiente A-a baseado no valor e idade
        
        Args:
            aa_gradient: Gradiente calculado
            age: Idade do paciente
            normal_gradient_age_adjusted: Gradiente normal ajustado para idade
            
        Returns:
            Dict com interpretação
        """
        
        # Determinar se está dentro do normal para a idade
        is_normal_for_age = aa_gradient <= normal_gradient_age_adjusted
        
        # Classificação baseada em faixas absolutas e ajuste por idade
        if aa_gradient <= 15 and is_normal_for_age:
            return {
                "stage": "Normal",
                "description": "Gradiente A-a normal",
                "interpretation": f"Gradiente A-a de {aa_gradient:.1f} mmHg está dentro do normal para idade de {age} anos (esperado ≤{normal_gradient_age_adjusted:.1f} mmHg). Função alveolar preservada."
            }
        elif aa_gradient <= 25 or (aa_gradient <= normal_gradient_age_adjusted * 1.5):
            return {
                "stage": "Levemente Elevado",
                "description": "Gradiente A-a levemente elevado",
                "interpretation": f"Gradiente A-a de {aa_gradient:.1f} mmHg está levemente elevado (normal para idade: ≤{normal_gradient_age_adjusted:.1f} mmHg). Sugere leve incompatibilidade V/Q ou shunt mínimo. Considerar atelectasia leve ou edema pulmonar inicial."
            }
        elif aa_gradient <= 50:
            return {
                "stage": "Moderadamente Elevado",
                "description": "Gradiente A-a moderadamente elevado",
                "interpretation": f"Gradiente A-a de {aa_gradient:.1f} mmHg está moderadamente elevado. Indica incompatibilidade V/Q moderada ou shunt. Sugere doença pulmonar significativa como pneumonia, edema pulmonar ou embolia pulmonar."
            }
        else:
            return {
                "stage": "Severamente Elevado",
                "description": "Gradiente A-a severamente elevado",
                "interpretation": f"Gradiente A-a de {aa_gradient:.1f} mmHg está severamente elevado. Indica incompatibilidade V/Q grave ou shunt significativo. Sugere doença pulmonar severa como SDRA, pneumonia extensa ou shunt intracardíaco."
            }


def calculate_a_a_o2_gradient(age: int, fio2: float, paco2: float, pao2: float,
                             patm: Optional[float] = None, 
                             respiratory_quotient: Optional[float] = None) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = AAO2GradientCalculator()
    return calculator.calculate(age, fio2, paco2, pao2, patm, respiratory_quotient)