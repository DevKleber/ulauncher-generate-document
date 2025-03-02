import random
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from faker import Faker

# Configura o Faker para o português do Brasil
fake = Faker('pt_BR')

# Função para gerar CPF válido
def gerar_cpf(formatted: bool = True) -> str:
    cpf = [random.randint(0, 9) for _ in range(9)]
    soma = sum((10 - i) * cpf[i] for i in range(9))
    resto = soma % 11
    cpf.append(0 if resto < 2 else 11 - resto)
    soma = sum((11 - i) * cpf[i] for i in range(10))
    resto = soma % 11
    cpf.append(0 if resto < 2 else 11 - resto)
    cpf_str = ''.join(map(str, cpf))
    if formatted:
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
    return cpf_str

# Função para gerar CNPJ válido
def gerar_cnpj(formatted: bool = True) -> str:
    cnpj = [random.randint(0, 9) for _ in range(12)]
    pesos_primeiro = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(cnpj[i] * pesos_primeiro[i] for i in range(12))
    resto = soma % 11
    cnpj.append(0 if resto < 2 else 11 - resto)
    pesos_segundo = [6] + pesos_primeiro
    soma = sum(cnpj[i] * pesos_segundo[i] for i in range(13))
    resto = soma % 11
    cnpj.append(0 if resto < 2 else 11 - resto)
    cnpj_str = ''.join(map(str, cnpj))
    if formatted:
        return f"{cnpj_str[:2]}.{cnpj_str[2:5]}.{cnpj_str[5:8]}/{cnpj_str[8:12]}-{cnpj_str[12:]}"
    return cnpj_str

# Função para gerar dados completos de pessoa
def gerar_dados_pessoa() -> dict:
    nome_completo = fake.name()
    data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=90)
    endereco = fake.address().replace("\n", ", ")
    cpf = gerar_cpf(formatted=True)
    telefone = fake.phone_number()
    return {
        "Nome": nome_completo,
        "Data de Nascimento": data_nascimento.strftime("%d/%m/%Y"),
        "Endereço": endereco,
        "CPF": cpf,
        "Telefone": telefone
    }

class DocumentGeneratorExtension(Extension):
    def __init__(self):
        super(DocumentGeneratorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower().strip()
        items = []
        
        if query == "cpf":
            cpf = gerar_cpf(formatted=True)
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name=cpf,
                    description='CPF válido gerado e copiado para a área de transferência',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cpf)
                )
            )
        elif query == "cnpj":
            cnpj = gerar_cnpj(formatted=True)
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name=cnpj,
                    description='CNPJ válido gerado e copiado para a área de transferência',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cnpj)
                )
            )
        elif query == "pessoa":
            pessoa = gerar_dados_pessoa()
            pessoa_str = (
                f"Nome: {pessoa['Nome']}\n"
                f"Data de Nascimento: {pessoa['Data de Nascimento']}\n"
                f"Endereço: {pessoa['Endereço']}\n"
                f"CPF: {pessoa['CPF']}\n"
                f"Telefone: {pessoa['Telefone']}"
            )
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name=pessoa['Nome'],
                    description='Dados completos da pessoa gerados e copiados para a área de transferência',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(pessoa_str)
                )
            )
        else:
            # Exibe todas as opções se o query estiver vazio ou não corresponder a nenhum dos casos acima
            cpf = gerar_cpf(formatted=True)
            cnpj = gerar_cnpj(formatted=True)
            pessoa = gerar_dados_pessoa()
            pessoa_str = (
                f"Nome: {pessoa['Nome']}\n"
                f"Data de Nascimento: {pessoa['Data de Nascimento']}\n"
                f"Endereço: {pessoa['Endereço']}\n"
                f"CPF: {pessoa['CPF']}\n"
                f"Telefone: {pessoa['Telefone']}"
            )
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name=cpf,
                    description='CPF válido gerado e copiado para a área de transferência',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cpf)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name=cnpj,
                    description='CNPJ válido gerado e copiado para a área de transferência',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cnpj)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name=pessoa['Nome'],
                    description='Dados completos da pessoa gerados e copiados para a área de transferência',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(pessoa_str)
                )
            )
        return RenderResultListAction(items)

if __name__ == '__main__':
    DocumentGeneratorExtension().run()
