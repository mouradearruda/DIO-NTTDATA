import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self.contas):
            raise StopIteration
        conta = self.contas[self._index]
        self._index += 1
        return f"Agência: {conta.agencia}, Número: {conta.numero}, Titular: {conta.cliente.nome}, Saldo: R$ {conta.saldo:.2f}"


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao('Saque', self.valor)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao('Depósito', self.valor)


class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self._transacoes.append({
            "tipo": tipo,
            "valor": valor,
            "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        })

    def gerar_relatorio(self):
        return self._transacoes

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        return [t for t in self._transacoes if datetime.strptime(t["data"], "%d-%m-%Y %H:%M:%S").date() == data_atual]


def log_transacao(func):
    def envolucro(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()} executado.")
        return resultado
    return envolucro


class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("Você excedeu o limite de transações diárias.")
        else:
            transacao.registrar(conta)


class Conta:
    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero
        self.saldo = 0
        self.historico = Historico()
        self.agencia = "0001"

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("Depósito realizado.")
            return True
        print("Valor inválido.")
        return False

    def sacar(self, valor):
        if valor <= self.saldo and valor > 0:
            self.saldo -= valor
            print("Saque realizado.")
            return True
        print("Saldo insuficiente.")
        return False


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        saques_hoje = len([t for t in self.historico.gerar_relatorio() if t['tipo'] == 'Saque'])
        if saques_hoje >= self.limite_saques:
            print("Você excedeu o limite de saques.")
            return False
        if valor > self.limite:
            print("Valor do saque excede o limite.")
            return False
        return super().sacar(valor)


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def criar_cliente(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")
        cliente = Cliente(nome, cpf, endereco)
        self.clientes.append(cliente)
        print("Cliente criado com sucesso.")

    def criar_conta(self):
        cpf = input("CPF: ")
        cliente = self.filtrar_cliente(cpf)
        if cliente:
            numero_conta = len(self.contas) + 1
            nova_conta = ContaCorrente(cliente, numero_conta)
            cliente.adicionar_conta(nova_conta)
            self.contas.append(nova_conta)
            print("Conta criada com sucesso.")
        else:
            print("Cliente não encontrado.")

    def filtrar_cliente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def listar_contas(self):
        for conta in ContasIterador(self.contas):
            print(conta)

    @log_transacao
    def depositar(self):
        cpf = input("CPF: ")
        cliente = self.filtrar_cliente(cpf)
        if cliente:
            valor = float(input("Valor: "))
            transacao = Deposito(valor)
            conta = cliente.contas[0] 
            cliente.realizar_transacao(conta, transacao)
        else:
            print("Cliente não encontrado.")

    @log_transacao
    def sacar(self):
        cpf = input("CPF: ")
        cliente = self.filtrar_cliente(cpf)
        if cliente:
            valor = float(input("Valor: "))
            transacao = Saque(valor)
            conta = cliente.contas[0] 
            cliente.realizar_transacao(conta, transacao)
        else:
            print("Cliente não encontrado.")

    @log_transacao
    def exibir_extrato(self):
        cpf = input("CPF: ")
        cliente = self.filtrar_cliente(cpf)
        if cliente:
            conta = cliente.contas[0] 
            print("\n=== EXTRATO ===")
            for transacao in conta.historico.gerar_relatorio():
                print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
        else:
            print("Cliente não encontrado.")


def menu():
    banco = Banco()
    while True:
        opcao = input("\n[d] Depositar\n[s] Sacar\n[e] Extrato\n[nc] Nova Conta\n[lc] Listar Contas\n[q] Sair\nEscolha: ")
        if opcao == 'd':
            banco.depositar()
        elif opcao == 's':
            banco.sacar()
        elif opcao == 'e':
            banco.exibir_extrato()
        elif opcao == 'nc':
            banco.criar_conta()
        elif opcao == 'lc':
            banco.listar_contas()
        elif opcao == 'q':
            break
        else:
            print("Opção inválida.")


menu()
