from threading import Semaphore
from general import General


class Equipamentos:
    '''
        Equipamentos representa um conjunto de equipamentos de um determinado tipo. 
        Você deve implementar os métodos que controlam a entrega e devolução de
        equipamentos, respeitando as restrições impostas no enunciado do trabalho.
    '''

    # Construtor da classe que representa um conjunto de equipamentos
    def __init__(self, nome_equipamento, quant_equipamentos):
        self.nome = nome_equipamento
        self.quantidade = quant_equipamentos
        self.semaforo_oferta_demanda = Semaphore(quant_equipamentos)

    def pegar_equipamento(self):
        # Retira/espera equipamento
        General().get_equipamento(self.nome).semaforo_oferta_demanda.acquire()

    def devolver_equipamento(self):
        # Sem release, pq o equipamento deve ser limpo antes de ser usado
        # Sinaliza para limpar
        with General().lock_higienizar:
            General().adicionar_higienizar(self.nome)
