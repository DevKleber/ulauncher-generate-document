import random
import webbrowser
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

# Funções para gerar CPF e CNPJ válidos
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

# Extensão principal
class DocumentGeneratorExtension(Extension):

    def __init__(self):
        super(DocumentGeneratorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

# Exibe as opções na janela de query do Ulauncher
class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        # Obter argumento da query
        query = event.get_argument() or ""

        # Configuração se a janela deve permanecer aberta após copiar
        keep_app_open = extension.preferences["stay_open"] == "yes"

        items = []

        # Se o usuário digitar "cpf" ou "cnpj" como argumento, podemos mostrar apenas essa opção
        if "cpf" in query.lower():
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name='Gerar CPF',
                    description='Clique para gerar um CPF válido e copiar para a área de transferência',
                    on_enter=ExtensionCustomAction("cpf", keep_app_open=keep_app_open)
                )
            )
        elif "cnpj" in query.lower():
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name='Gerar CNPJ',
                    description='Clique para gerar um CNPJ válido e copiar para a área de transferência',
                    on_enter=ExtensionCustomAction("cnpj", keep_app_open=keep_app_open)
                )
            )
        else:
            # Sem argumento específico: mostra ambas as opções
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name='Gerar CPF',
                    description='Gera um CPF válido e copia para a área de transferência',
                    on_enter=ExtensionCustomAction("cpf", keep_app_open=keep_app_open)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name='Gerar CNPJ',
                    description='Gera um CNPJ válido e copia para a área de transferência',
                    on_enter=ExtensionCustomAction("cnpj", keep_app_open=keep_app_open)
                )
            )

        return RenderResultListAction(items)

# Ao selecionar uma opção, gera o documento e copia para a área de transferência
class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        acao = event.get_data()
        if acao == "cpf":
            doc = gerar_cpf(formatted=True)
        elif acao == "cnpj":
            doc = gerar_cnpj(formatted=True)
        else:
            doc = ""

        # Copia o documento gerado para a área de transferência
        return CopyToClipboardAction(doc)

if __name__ == '__main__':
    DocumentGeneratorExtension().run()
