import textwrap
from datetime import datetime


def menu():
    menu = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [lu]\tListar Usuários
    [h]\tHistórico de Transações
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"Depósito:\tR$ {valor:.2f} - {timestamp}\n"
        print("\n==== Depósito realizado com sucesso! ====")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"Saque:\t\tR$ {valor:.2f} - {timestamp}\n"
        numero_saques += 1
        print("\n==== Saque realizado com sucesso! ====")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n" + "=" * 50)
    print(" " * 18 + "EXTRATO")
    print("=" * 50)
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print("-" * 50)
    print(f"Saldo atual:\t\tR$ {saldo:.2f}")
    print("=" * 50)


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return usuarios

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("\n==== Usuário criado com sucesso! ====")
    return usuarios


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n==== Conta criada com sucesso! ====")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    print("\n" + "=" * 60)
    print(" " * 20 + "LISTA DE CONTAS")
    print("=" * 60)

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            CPF:\t\t{conta['usuario']['cpf']}
        """
        print(textwrap.dedent(linha))
        print("-" * 60)


def listar_usuarios(usuarios):
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! @@@")
        return

    print("\n" + "=" * 60)
    print(" " * 20 + "LISTA DE USUÁRIOS")
    print("=" * 60)

    for usuario in usuarios:
        linha = f"""\
            Nome:\t\t{usuario['nome']}
            CPF:\t\t{usuario['cpf']}
            Data Nasc.:\t{usuario['data_nascimento']}
            Endereço:\t{usuario['endereco']}
        """
        print(textwrap.dedent(linha))
        print("-" * 60)


def historico_transacoes(extrato):
    print("\n" + "=" * 60)
    print(" " * 18 + "HISTÓRICO DE TRANSAÇÕES")
    print("=" * 60)
    if not extrato:
        print("Nenhuma transação realizada.")
    else:
        print(extrato)
    print("=" * 60)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    print("=" * 50)
    print(" " * 15 + "BANCO PYTHON")
    print(" " * 10 + "Sistema Bancário Digital")
    print("=" * 50)

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            usuarios = criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "h":
            historico_transacoes(extrato)

        elif opcao == "q":
            print("\n==== Obrigado por usar o Banco Python! ====")
            print("==== Tenha um ótimo dia! ====")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()