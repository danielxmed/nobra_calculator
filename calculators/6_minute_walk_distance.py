"""
6 Minute Walk Distance Calculator

Calcula valores de referência para distância caminhada como medida de status funcional.
Referência: Enright PL, Sherrill DL. Am J Respir Crit Care Med. 1998;158(5):1384-7.
"""

from typing import Dict, Any, Optional


class SixMinuteWalkDistanceCalculator:
    """Calculadora para 6 Minute Walk Distance"""
    
    def __init__(self):
        # Constantes das equações de Enright-Sherrill
        self.MALE_HEIGHT_COEFF = 7.57
        self.MALE_AGE_COEFF = -5.02
        self.MALE_WEIGHT_COEFF = -1.76
        self.MALE_CONSTANT = -309
        
        self.FEMALE_HEIGHT_COEFF = 2.11
        self.FEMALE_AGE_COEFF = -5.78
        self.FEMALE_WEIGHT_COEFF = -2.29
        self.FEMALE_CONSTANT = 667
        
        # Limite inferior da normalidade
        self.LOWER_LIMIT_NORMAL = 153
    
    def calculate(self, age: int, sex: str, height: float, weight: float, 
                 observed_distance: Optional[float] = None) -> Dict[str, Any]:
        """
        Calcula a distância predita para caminhada de 6 minutos
        
        Args:
            age: Idade em anos
            sex: "masculino" ou "feminino"
            height: Altura em centímetros
            weight: Peso em quilogramas
            observed_distance: Distância observada (opcional)
            
        Returns:
            Dict com resultado predito, interpretação e comparação
        """
        
        # Validações
        self._validate_inputs(age, sex, height, weight, observed_distance)
        
        # Calcular distância predita
        predicted_distance = self._calculate_predicted_distance(age, sex, height, weight)
        
        # Calcular limite inferior da normalidade
        lower_limit = predicted_distance - self.LOWER_LIMIT_NORMAL
        
        # Resultados base
        result = {
            "result": round(predicted_distance, 1),
            "unit": "metros",
            "lower_limit_normal": round(lower_limit, 1),
            "interpretation": f"Distância predita de {predicted_distance:.1f} metros para paciente {sex} de {age} anos, {height} cm e {weight} kg. Limite inferior da normalidade: {lower_limit:.1f} metros.",
            "stage": "Predito",
            "stage_description": "Valor de referência calculado"
        }
        
        # Se distância observada foi fornecida, adicionar análise comparativa
        if observed_distance is not None:
            percentage_predicted = (observed_distance / predicted_distance) * 100
            interpretation_observed = self._get_interpretation_observed(percentage_predicted, observed_distance, lower_limit)
            
            result.update({
                "observed_distance": observed_distance,
                "percentage_predicted": round(percentage_predicted, 1),
                "interpretation": interpretation_observed["interpretation"],
                "stage": interpretation_observed["stage"],
                "stage_description": interpretation_observed["description"]
            })
        
        return result
    
    def _validate_inputs(self, age: int, sex: str, height: float, weight: float, 
                        observed_distance: Optional[float]):
        """Valida os parâmetros de entrada"""
        
        if not isinstance(age, int) or age < 18 or age > 100:
            raise ValueError("Idade deve ser um inteiro entre 18 e 100 anos")
        
        if sex not in ["masculino", "feminino"]:
            raise ValueError("Sexo deve ser 'masculino' ou 'feminino'")
        
        if not isinstance(height, (int, float)) or height < 120.0 or height > 220.0:
            raise ValueError("Altura deve estar entre 120.0 e 220.0 cm")
        
        if not isinstance(weight, (int, float)) or weight < 30.0 or weight > 200.0:
            raise ValueError("Peso deve estar entre 30.0 e 200.0 kg")
        
        if observed_distance is not None:
            if not isinstance(observed_distance, (int, float)) or observed_distance < 0.0 or observed_distance > 1000.0:
                raise ValueError("Distância observada deve estar entre 0.0 e 1000.0 metros")
    
    def _calculate_predicted_distance(self, age: int, sex: str, height: float, weight: float) -> float:
        """Calcula a distância predita usando equações de Enright-Sherrill"""
        
        if sex == "masculino":
            # Equação para homens: 6MWD = (7.57 × altura) - (5.02 × idade) - (1.76 × peso) - 309
            predicted = (self.MALE_HEIGHT_COEFF * height + 
                        self.MALE_AGE_COEFF * age + 
                        self.MALE_WEIGHT_COEFF * weight + 
                        self.MALE_CONSTANT)
        else:
            # Equação para mulheres: 6MWD = (2.11 × altura) - (2.29 × peso) - (5.78 × idade) + 667
            predicted = (self.FEMALE_HEIGHT_COEFF * height + 
                        self.FEMALE_WEIGHT_COEFF * weight + 
                        self.FEMALE_AGE_COEFF * age + 
                        self.FEMALE_CONSTANT)
        
        # Garantir que não seja negativo
        return max(predicted, 0.0)
    
    def _get_interpretation_observed(self, percentage_predicted: float, 
                                   observed_distance: float, lower_limit: float) -> Dict[str, str]:
        """
        Interpreta a distância observada comparada com a predita
        
        Args:
            percentage_predicted: Porcentagem do valor predito
            observed_distance: Distância observada
            lower_limit: Limite inferior da normalidade
            
        Returns:
            Dict com interpretação
        """
        
        # Classificação baseada na porcentagem do predito e limite inferior
        if observed_distance < lower_limit or percentage_predicted < 50:
            return {
                "stage": "Severamente Reduzido",
                "description": "Capacidade funcional severamente reduzida",
                "interpretation": f"Distância observada de {observed_distance:.1f}m representa {percentage_predicted:.1f}% do predito. Valor muito abaixo do esperado, indicando limitação funcional grave que requer investigação e tratamento intensivos."
            }
        elif percentage_predicted < 75:
            return {
                "stage": "Moderadamente Reduzido",
                "description": "Capacidade funcional moderadamente reduzida",
                "interpretation": f"Distância observada de {observed_distance:.1f}m representa {percentage_predicted:.1f}% do predito. Valor abaixo do esperado, sugerindo limitação funcional moderada que pode se beneficiar de reabilitação."
            }
        elif percentage_predicted < 90:
            return {
                "stage": "Levemente Reduzido",
                "description": "Capacidade funcional levemente reduzida",
                "interpretation": f"Distância observada de {observed_distance:.1f}m representa {percentage_predicted:.1f}% do predito. Valor ligeiramente abaixo do esperado, podendo indicar limitação funcional leve ou início de declínio."
            }
        else:
            return {
                "stage": "Normal",
                "description": "Capacidade funcional normal",
                "interpretation": f"Distância observada de {observed_distance:.1f}m representa {percentage_predicted:.1f}% do predito. Valor dentro dos limites esperados, indicando capacidade funcional preservada."
            }


def calculate_6_minute_walk_distance(age: int, sex: str, height: float, weight: float, 
                                   observed_distance: Optional[float] = None) -> Dict[str, Any]:
    """
    Função de conveniência para o sistema de carregamento dinâmico
    
    IMPORTANTE: Esta função deve seguir o padrão calculate_{score_id}
    """
    calculator = SixMinuteWalkDistanceCalculator()
    return calculator.calculate(age, sex, height, weight, observed_distance)