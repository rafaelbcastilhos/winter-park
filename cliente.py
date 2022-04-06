from threading import Thread
from time import sleep
from random import randint
import init
from general import General


class Cliente(Thread):
    '''
        Os clientes (frequentadores do parque) realizam as seguintes ações:
        - Vestir os equipamentos de proteção (macacão, luvas, capacete)
        - Ir a uma das atrações:
            - Pista de patinação no gelo:
                - Pegar patins
                - Aguardar vaga na pista
                - Patinar
            - Teleférico:
                - Pagar uma cadeira livre
                - Subir a montanha
                - Ir para uma das pistas ou permanecer no teleférico
            - Pista de snowboad:
                - Pegar uma prancha
                - Aguardar vaga
                - Descer a montanha
                - Devolver equipamento, caso deixe a atração
            - Pista de esqui:
                - Pegar esquis
                - Aguardar vaga
                - Descer a montanha
                - Devolver equipamento, caso deixe a atração
            - Pistas de trenó (skeleton):
                - Pegar trenó
                - Aguardar pista livre
                - Descer a montanha
                - Devolver o equipamento
            - Pistas de bobsled:
                - Formar dupla
                - Pegar bobsled
                - Aguardar pista livre 
                - Descer a montanha
                - Devolver o equipamento
        - Decidir aleatoriamente se permanece, se vai para outra atração ou vai embora
        Cada uma dessas ações corresponde a um método do cliente. A sua responsabilidade 
        é desenvolver os comportamentos dentro dos métodos do cliente de modo que ele se
        comporte conforme a especificação contida no Moodle.
        Esses métodos são chamados no método run() da classe Cliente.
        Observação: Comente no código qual o objetivo de uma dada operação, 
        ou conjunto de operações, para facilitar a correção do trabalho.           
    '''
    # Construtor do nadador
    # Argumentos indicam o gênero e se é criança e aprendiz
    def __init__(self, id):
        self.id     = id
        self.alugar_bobsled = False

        super().__init__(name=("Cliente " + str(id)))

    # Função que imprime mensagens de log
    def log(self, mensagem):
        espacos = (16 - len(self.name)) * ' '
        print('['+ self.name + '] ' + espacos + mensagem + '\n', end='')

    # Representação do cliente nas mensagens de log
    def __repr__(self):
        return self.name

    # Comportamento do cliente
    def run(self):
        self.log("Entrou no Winter Park.")

        self.pegar_equip_protecao()

        while True:
            if randint(1, 3) == 1:
                # Vai para pista de patinação
                self.pegar_patins()
                self.aguardar_lugar_pista()
                while True:
                    self.patinar()
                    if randint(1, 3) == 1:
                        break
                self.devolver_patins()
            else:
                # Pega o teleférico para subir a montanha
                self.pegar_teleferico()
                self.aguardar_subida()
                if randint(1, 5) == 1:
                    # Desce de teleférico
                    self.aguardar_descida()
                    self.sair_teleferico()
                else:
                    self.sair_teleferico()
                    if randint(1, 2) == 1:
                        # Vai para o lado sul - esqui e snowboard
                        if randint(1, 2) == 1:
                            # Esquiar
                            self.pegar_esquis()
                            while True:
                                self.aguardar_lugar_montanha_sul()  
                                self.descer_esquiando()  
                                if randint(1, 2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()
                                else:
                                    self.devolver_esquis()
                                    break
                        else:
                            # Snowboard
                            self.pegar_snowboard()
                            while True:
                                self.aguardar_lugar_montanha_sul()  
                                self.descer_snowboard()   
                                if randint(1, 2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()
                                else:
                                    self.devolver_snowboard()
                                    break                                             
                    else:
                        # Vai para o lado norte - trenó e bobsled
                        if randint(1, 3) == 1:
                            # Bobsled
                            self.formar_dupla()
                            self.pegar_bobsled()
                            while True:
                                self.aguardar_pista_bobsled()  
                                self.descer_bobsled()  
                                self.devolver_bobsled()
                                if randint(1, 2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()
                                else:
                                    break                        
                        else:
                            # Trenó   
                            self.pegar_treno()
                            while True:
                                self.aguardar_pista_treno()  
                                self.descer_treno()  
                                self.devolver_treno()
                                if randint(1, 2) == 1:
                                    self.pegar_teleferico()
                                    self.aguardar_subida()
                                    self.sair_teleferico()
                                else:
                                    break                   

            if randint(1, 5) == 1:
                # Devolve o kit de equipamentos de proteção
                self.devolver_equip_protecao()
                # Vai embora
                self.log("Saiu do Winter Park.")
                return

    # Simula o tempo de uso de uma atração
    def tempo_atracao(self):
        sleep(randint(init.tempo_atracao_min, init.tempo_atracao_max) * init.unidade_de_tempo)
        
    # Cliente pega um kit com os equipamentos de proteção
    def pegar_equip_protecao(self):
        '''
            O cliente pega um kit com os equipamentos de proteção.
        '''
        General().get_funcionario("equip. proteção").entrega_equipamento()
        self.log("Pegou um kit com equipamentos de proteção.")
        
    # Cliente devolve um kit com os equipamentos de proteção
    def devolver_equip_protecao(self):
        '''
            O cliente devolve um kit com os equipamentos de proteção.
        '''
        self.log("Devolveu um kit com equipamentos de proteção.")
        General().get_funcionario("equip. proteção").recebe_equipamento()
        
    # Cliente pega um par de patins para usar a pista de patinação
    def pegar_patins(self):
        '''
            O cliente pega um par de patins para patinar no gelo.
        '''
        General().get_funcionario("patins").entrega_equipamento()
        self.log("Pegou um par de patins.")

    # Cliente aguarda um lugar na pista de patinação
    def patinar(self):
        self.log("Está patinando.")
        self.tempo_atracao()

    # Cliente devolver os patins que estava usando
    def devolver_patins(self):
        '''
            O cliente devolve os patins que usou na pista de patinação.
        '''
        General().get_atracao("pista de patinação").sair_atracao()
        self.log("Devolveu um par de patins.")
        General().get_funcionario("patins").recebe_equipamento()

    # Cliente aguarda que haja lugar na pista de patinação         
    def aguardar_lugar_pista(self):
        '''
            O cliente deve aguardar que haja uma vaga para entrar na pista de patinação.
        '''
        General().get_atracao("pista de patinação").entrar_atracao()
        self.log("Entrou na pista de patinação.")

    # Cliente aguarda um lugar no teleférico
    def pegar_teleferico(self):
        '''
            O cliente deve aguardar que haja uma cadeira vaga para andar no teleférico.
        '''
        General().get_atracao("teleférico").entrar_atracao()
        self.log("Pegou cadeira no teleférico.")

    # Cliente deve aguardar a subida do teleférico
    def aguardar_subida(self):
        self.tempo_atracao() 
        self.log("Chegou ao topo da montanha de teleférico.")

    # Cliente deve aguardar a descida do teleférico 
    def aguardar_descida(self):
        self.tempo_atracao()     
        self.log("Desceu a montanha de teleférico.")

    # Cliente libera seu lugar no teleférico
    def sair_teleferico(self):
        '''
            O cliente libera a cadeira que usou para andar no teleférico.
        '''
        General().get_atracao("teleférico").sair_atracao()
        self.log("Liberou uma cadeira no teleférico.")
        
    # Cliente pega esquis
    def pegar_esquis(self):
        '''
            O cliente pega um par de esquis para usar.
        '''        
        General().get_funcionario("esquis").entrega_equipamento()
        self.log("Pegou esquis.")

    # Cliente aguarda para poder esquiar na montanha
    def aguardar_lugar_montanha_sul(self):
        '''
            Aguardar que haja uma vaga para esquiar.
        '''
        General().get_atracao("pista esqui e snowboard").entrar_atracao()
        self.log("Conseguiu lugar na montanha sul.")

    # Cliente desce a montanha esquiando
    def descer_esquiando(self):
        self.log("Começa a descer a montanha esquiando.")
        self.tempo_atracao()
        self.log("Terminou de descer a montanha esquiando.")
        General().get_atracao("pista esqui e snowboard").sair_atracao()

    # Cliente devolve os esquis
    def devolver_esquis(self):
        '''
            O cliente pega um par de esquis para usar.
        '''        
        self.log("Devolveu os esquis.")
        General().get_funcionario("esquis").recebe_equipamento()
        
    # Cliente pega uma prancha de snowboard
    def pegar_snowboard(self):
        '''
            O cliente pega uma prancha de snowboard.
        '''
        General().get_funcionario("snowboard").entrega_equipamento()
        self.log("Pegou um snowboard.")
        
    # Cliente desce a montanha com uma prancha de snowboard
    def descer_snowboard(self):
        self.log("Começou a descer a pista de snowboard.")       
        self.tempo_atracao()
        self.log("Desceu a pista de snowboard.")
        General().get_atracao("pista esqui e snowboard").sair_atracao()

    # Cliente devolve uma prancha de snowboard
    def devolver_snowboard(self):
        '''
            O cliente devolve uma prancha de snowboard.
        '''
        self.log("Devolveu um snowboard.")    
        General().get_funcionario("snowboard").recebe_equipamento()

    # Cliente aguarda formação da dupla
    def formar_dupla(self):
        '''
            O cliente aguarda que outro cliente forme uma dupla com ele.
            Acontece timeout se ele esperou demais.
        '''
        self.alugar_bobsled = False
        self.dupla_index = False

        General().lock_dupla.acquire()

        # Entra na ultima criada ou cria dupla se não existirem duplas ou ainda dupla cheia
        General().entrar_dupla(self.id)

        # Ultima duplas criada e index
        ultima_dupla = General().duplas[-1]
        self.dupla_index = len(General().duplas) - 1

        # É o cliente que criou a dupla
        if len(ultima_dupla) < 3:
            self.log("Esperando encontrar dupla")
            if not General().condition_dupla.wait(30):
                self.log("Cansou de esperar e deixou a fila de formação de duplas")
                General().desfazer_dupla()
                self.alugar_bobsled = False
                self.dupla_index = False
            else:
                self.log("Formou uma dupla para descer a montanha no bobsled.")
                self.alugar_bobsled = True

        # É o cliente que falta para completar a dupla
        else:
            self.alugar_bobsled = False
            General().condition_dupla.notify()
            self.log("Formou uma dupla para descer a montanha no bobsled.")

        General().lock_dupla.release()
        
    # Cliente aguarda um bobsled livre para descer a montanha
    def pegar_bobsled(self):
        '''
            O cliente aguarda que haja um bobsled livre para descer a montanha.
        '''
        if self.alugar_bobsled:
            General().get_funcionario("bobsled").entrega_equipamento()
            self.log("Pegou um bobsled.")

    # Cliente aguarda uma pista de bobsled livre para descer a montanha
    def aguardar_pista_bobsled(self):
        if self.dupla_index is not False:
            self.log("Aguarda por uma pista de bobsled.")
            '''
                O cliente aguarda que haja uma pista de bobsled livre para descer a montanha.
            '''
            General().get_atracao("pistas bobsled e trenó").entrar_atracao()
            self.log("Conseguiu uma pista de bobsled.")

    # Cliente desce a montanha de bobsled
    def descer_bobsled(self):
        if self.dupla_index is not False:
            General().lock_espera_descer.acquire()

            # Mais um da dupla esperando pra descer
            General().duplas[self.dupla_index][0] += 1

            # Espera pela dupla
            if General().duplas[self.dupla_index][0] < 2:
                General().condition_espera_descer.wait()
            
            # Descem juntos
            else:
                General().condition_espera_descer.notify()
            
            self.dupla_index = False
            General().lock_espera_descer.release()

            self.log("Começou a descer a pista de bobsled.")
            self.tempo_atracao()
            self.log("Terminou de descer a pista de bobsled.")
            General().get_atracao("pistas bobsled e trenó").sair_atracao()

    # Cliente devolve o bobsled que usou para descer a montanha
    def devolver_bobsled(self):
        '''
            O cliente devolveu o bobsled usado para descer a montanha.
        '''
        if self.alugar_bobsled:
            General().get_funcionario("bobsled").recebe_equipamento()
            self.log("Devolveu um bobsled.")
            self.alugar_bobsled = False

    # Cliente aguarda um trenó livre para descer a montanha
    def pegar_treno(self):
        '''
            O cliente aguarda que haja um trenó livre para descer a montanha.
        '''
        General().get_funcionario("trenó").entrega_equipamento()
        self.log("Pegou um trenó.")

    # Cliente aguarda uma pista de trenó livre para descer a montanha
    def aguardar_pista_treno(self):
        self.log("Aguarda por uma pista de trenó.")
        '''
            O cliente aguarda que haja uma pista de trenó livre para descer a montanha.
        '''
        General().get_atracao("pistas bobsled e trenó").entrar_atracao()
        self.log("Conseguiu uma pista de trenó.")

    # Cliente desce a montanha de trenó
    def descer_treno(self):
        self.log("Começou a descer a pista de trenó.")
        self.tempo_atracao()
        self.log("Terminou de descer a pista de trenó.")
        General().get_atracao("pistas bobsled e trenó").sair_atracao() 

    # Cliente devolve o trenó que usou para descer a montanha
    def devolver_treno(self):
        '''
            O cliente devolveu o trenó usado para descer a montanha.
        '''
        self.log("Devolveu um trenó.")
        General().get_funcionario("trenó").recebe_equipamento()
