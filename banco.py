menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Quanto você quer depositar? "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor inválido.")

    elif opcao == "2":
        valor = float(input("Quanto você quer sacar? "))
        if valor > saldo:
            print("Seu saldo é insuficiente.")
        elif valor > limite:
            print("Sua tentativa de saque excede o limite máximo.")
        elif numero_saques >= LIMITE_SAQUES:
            print("Você excedeu seu número máximo de saques diários.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        else:
            print("Valor inválido.")

    elif opcao == "3":
        print("\n=== EXTRATO ===")
        if not extrato:
            print("Nenhuma movimentação registrada hoje.")
        else:
            print(extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("================")

    elif opcao == "4":
        break

    else:
        print("Operação inválida.")
