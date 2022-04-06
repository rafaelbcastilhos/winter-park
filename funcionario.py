from threading import Thread, Lock
from time import sleep
import init
from general import General


class Funcionario(Thread):
    '''
        Funcionário deve realizar as seguintes ações:
        - Limpar os equipamentos.
        - Descansar.
        A sua responsabilidade é implementar os métodos com o comportamento do
        funcionário, respeitando as restrições impostas no enunciado do trabalho.
        Observação: Comente no código qual o objetivo de uma dada operação, 
        ou conjunto de operações, para facilitar a correção do trabalho.        
    '''

    # Construtor da classe Funcionario
    def __init__(self, id, equipamento):
        self.id = id
        self.trabalhando = False
        self.equipamento = equipamento
        self.lock = Lock()
        super().__init__(name=("Funcionario " + str(id)))

    # Imprime mensagem de log
    def log(self, mensagem):
        espacos = (16 - len(self.name)) * ' '
        print('[' + self.name + '] ' + espacos + mensagem + '\n', end='')

    # Comportamento do Funcionario
    def run(self):
        self.log("Iniciando o expediente. Gerenciando equipamento " + self.equipamento.nome)
        self.trabalhando = True

        cont_equip_limpos = 0
        while self.trabalhando:
            if self.limpar_equipamento():
                cont_equip_limpos += 1
            if cont_equip_limpos == init.num_equip_turno:
                self.descansar()
                cont_equip_limpos = 0

        self.log("Terminando o expediente")

    # Funcionário limpa os equipamentos.
    def limpar_equipamento(self):
        with General().lock_higienizar:
            if General().get_higienizar(self.equipamento.nome) != -1:
                # retira da lista de limpeza
                General().remover_higienizar(self.equipamento.nome)

                # tempo de limpeza
                sleep(init.tempo_limpeza_equipamento * init.unidade_de_tempo)
                self.log(f"Limpou {self.equipamento.nome}")

                # adiciona de volta aos eq
                General().get_equipamento(self.equipamento.nome).semaforo_oferta_demanda.release()

                return True
            return False

    # Funcionário entrega um equipamento para um cliente.
    def entrega_equipamento(self):
        # espera sair do descanso
        while self.lock.locked():
            pass
        
        General().get_equipamento(self.equipamento.nome).pegar_equipamento()
        self.log("Entregou " + self.equipamento.nome + " para um cliente.")

    # Funcionário recebe um equipamento.
    def recebe_equipamento(self):
        # espera sair do descanso
        while self.lock.locked():
            pass
        
        self.log("Recebeu " + self.equipamento.nome + " de um cliente.")
        General().get_equipamento(self.equipamento.nome).devolver_equipamento()

    # Funcionário descansa durante um tempo
    def descansar(self):
        self.log("Hora do intervalo de descanso.")
        with self.lock:
            sleep(init.tempo_descanso * init.unidade_de_tempo)
        self.log("Fim do intervalo de descanso.")
