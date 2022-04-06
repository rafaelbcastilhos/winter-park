from threading import Lock, Condition


class General:
    _instance = None

    atracoes = []
    equipamentos = []
    funcionarios = []

    duplas = []
    lock_dupla = Lock()
    lock_espera_descer = Lock()
    condition_dupla = Condition(lock_dupla)
    condition_espera_descer = Condition(lock_espera_descer)

    higienizar = []
    lock_higienizar = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def adicionar_funcionario(self, funcionario):
        self.funcionarios.append(funcionario)

    def adicionar_equipamento(self, equipamento):
        self.equipamentos.append(equipamento)

    def adicionar_higienizar(self, equipamento):
        self.higienizar.append(equipamento)

    def remover_higienizar(self, equipamento):
        self.higienizar.remove(equipamento)

    def adicionar_atracao(self, atracao):
        self.atracoes.append(atracao)

    def adicionar_dupla(self, cliente):
        self.dupla.append(cliente)

    def entrar_dupla(self, cliente):
        # tenta entrar na ultima dupla formada,
        # se cheia, cria nova, se não existe duplas, cria uma
        try:
            if len(self.duplas[-1]) == 3:
                self.duplas.append([0, cliente])
            else:
                self.duplas[-1].append(cliente)
        except IndexError:
            self.duplas.append([0, cliente])

    def desfazer_dupla(self):
        self.duplas.pop()

    def get_funcionario(self, nome_equipamento):
        for funcionario in self.funcionarios:
            if funcionario.equipamento.nome == nome_equipamento:
                return funcionario

    def get_funcionario_indice(self, indice):
        return self.funcionarios[indice]

    def get_equipamento(self, nome_equipamento):
        for equipamento in self.equipamentos:
            if equipamento.nome == nome_equipamento:
                return equipamento

    def get_equipamento_indice(self, indice):
        return self.equipamentos[indice]

    def get_atracoes(self):
        return self.atracoes

    def get_atracao(self, nome_atracao):
        for atracao in self.atracoes:
            if atracao.nome == nome_atracao:
                return atracao

    def get_higienizar(self, nome_equipamento):
        try:
            return self.higienizar.index(nome_equipamento)
        except:
            return -1

    def limpar_dupla(self):
        self.dupla = []
