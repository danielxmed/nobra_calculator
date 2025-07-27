"""
CHA₂DS₂-VASc Score Calculator

Calcula o risco de AVC em pacientes com fibrilação atrial não-valvar.
Referência: Lip GY et al. Chest. 2010;137(2):263-72.
"""

from typing import Dict, Any


class Cha2ds2VascCalculator:
    """Calculadora para CHA₂DS₂-VASc Score"""
    
    def __init__(self):
        # Riscos anuais de AVC por pontuação
        self.stroke_risk = {
            0: 0.3,
            1: 0.9,
            2: 2.9,
            3: 4.6,
            4: 6.7,
            5: 10.0,
            6: 13.6,
            7: 15.7,
            8: 15.2,
            9: 17.4
        }
    
    def calculate(self, age: int, sex: str, congestive_heart_failure: bool,
                 hypertension: bool, stroke_tia_thromboembolism: bool,
                 vascular_disease: bool, diabetes: bool) -> Dict[str, Any]:
        """
        Calcula o CHA₂DS₂-VASc score
        
        Args:
            age: Idade em anos
            sex: "masculino" ou "feminino"
            congestive_heart_failure: História de ICC ou disfunção VE
            hypertension: História de hipertensão
            stroke_tia_thromboembolism: História de AVC/AIT/TE
            vascular_disease: Doença vascular prévia
            diabetes: História de diabetes
            
        Returns:
            Dict com resultado, interpretação e risco anual
        """
        
        # Validações
        self._validate_inputs(age, sex)
        
        # Calcular pontuação
        score = 0
        
        # C - Congestive heart failure (1 ponto)
        if congestive_heart_failure:
            score += 1
        
        # H - Hypertension (1 ponto)
        if hypertension:
            score += 1
        
        # A₂ - Age (0-2 pontos)
        if age >= 75:
            score += 2
        elif age >= 65:
            score += 1
        
        # D - Diabetes (1 ponto)
        if diabetes:
            score += 1
        
        # S₂ - Stroke/TIA/TE (2 pontos)
        if stroke_tia_thromboembolism:
            score += 2
        
        # V - Vascular disease (1 ponto)
        if vascular_disease:
            score += 1
        
        # Sc - Sex category (1 ponto se feminino)
        if sex.lower() == "feminino":
            score += 1
        
        # Obter interpretação
        interpretation = self._get_interpretation(score, sex)
        annual_risk = self.stroke_risk.get(score, 17.4)
        
        return {
            "result": score,
            "unit": "pontos",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "annual_stroke_risk": f"{annual_risk}%",
            "components": {
                "congestive_heart_failure": 1 if congestive_heart_failure else 0,
                "hypertension": 1 if hypertension else 0,
                "age_points": 2 if age >= 75 else (1 if age >= 65 else 0),
                "diabetes": 1 if diabetes else 0,
                "stroke_tia": 2 if stroke_tia_thromboembolism else 0,
                "vascular_disease": 1 if vascular_disease else 0,
                "sex_category": 1 if sex.lower() == "feminino" else 0
            }
        }
    
    def _validate_inputs(self, age: int, sex: str):
        """Valida os parâmetros de entrada"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Idade deve ser um inteiro entre 18 e 120 anos")
        
        if sex.lower() not in ["masculino", "feminino"]:
            raise ValueError("Sexo deve ser 'masculino' ou 'feminino'")
    
    def _get_interpretation(self, score: int, sex: str) -> Dict[str, str]:
        """
        Determina a interpretação baseada no score e sexo
        
        Args:
            score: CHA₂DS₂-VASc score calculado
            sex: Sexo do paciente
            
        Returns:
            Dict com interpretação clínica
        """
        
        is_male = sex.lower() == "masculino"
        annual_risk = self.stroke_risk.get(score, 17.4)
        
        if score == 0:
            return {
                "stage": "Muito Baixo Risco",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Pacientes masculinos com 0 pontos: anticoagulação não recomendada. Considerar aspirina ou nenhuma terapia antitrombótica."
            }
        
        elif score == 1:
            if is_male:
                return {
                    "stage": "Baixo Risco",
                    "description": f"Risco anual de AVC: {annual_risk}%",
                    "interpretation": "Homens com 1 ponto: anticoagulação pode ser considerada após discussão risco-benefício com o paciente."
                }
            else:
                return {
                    "stage": "Baixo Risco",
                    "description": f"Risco anual de AVC: {annual_risk}%",
                    "interpretation": "Mulheres com 1 ponto (apenas pelo sexo): anticoagulação não recomendada."
                }
        
        elif score == 2:
            return {
                "stage": "Risco Moderado",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Anticoagulação oral recomendada (warfarina com INR 2-3 ou DOAC). Benefício supera o risco de sangramento na maioria dos pacientes."
            }
        
        elif score == 3:
            return {
                "stage": "Risco Moderado-Alto",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Anticoagulação oral fortemente recomendada. Considerar DOACs como primeira escolha devido ao melhor perfil de segurança."
            }
        
        elif score == 4:
            return {
                "stage": "Alto Risco",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Anticoagulação oral essencial. Monitorar aderência e ajustar dose conforme função renal se usando DOACs."
            }
        
        elif score == 5:
            return {
                "stage": "Alto Risco",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Anticoagulação oral mandatória. Considerar estratégias para melhorar aderência e minimizar risco de sangramento."
            }
        
        elif score == 6:
            return {
                "stage": "Muito Alto Risco",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Anticoagulação oral imperativa. Avaliar e otimizar fatores de risco modificáveis. Monitoramento frequente."
            }
        
        else:  # score >= 7
            return {
                "stage": "Risco Extremo",
                "description": f"Risco anual de AVC: {annual_risk}%",
                "interpretation": "Anticoagulação oral crítica. Considerar oclusão de apêndice atrial esquerdo se contraindicação absoluta para anticoagulação."
            }


def calculate_cha2ds2_vasc(age: int, sex: str, congestive_heart_failure: bool,
                          hypertension: bool, stroke_tia_thromboembolism: bool,
                          vascular_disease: bool, diabetes: bool) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_cha2ds2_vasc
    """
    calculator = Cha2ds2VascCalculator()
    return calculator.calculate(age, sex, congestive_heart_failure,
                               hypertension, stroke_tia_thromboembolism,
                               vascular_disease, diabetes)