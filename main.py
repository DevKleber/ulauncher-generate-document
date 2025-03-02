import random
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

# Functions to generate valid CPF and CNPJ
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

class DocumentGeneratorExtension(Extension):
    def __init__(self):
        super(DocumentGeneratorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower().strip()
        items = []
        
        # If the user types "cpf", show CPF only.
        if query == "cpf":
            cpf = gerar_cpf(formatted=True)
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name=cpf,
                    description='Valid CPF generated and copied to clipboard',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cpf)
                )
            )
        # If the user types "cnpj", show CNPJ only.
        elif query == "cnpj":
            cnpj = gerar_cnpj(formatted=True)
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name=cnpj,
                    description='Valid CNPJ generated and copied to clipboard',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cnpj)
                )
            )
        # Otherwise, show both options.
        else:
            cpf = gerar_cpf(formatted=True)
            cnpj = gerar_cnpj(formatted=True)
            items.append(
                ExtensionResultItem(
                    icon='images/cpf.png',
                    name=cpf,
                    description='Valid CPF generated and copied to clipboard',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cpf)
                )
            )
            items.append(
                ExtensionResultItem(
                    icon='images/cnpj.png',
                    name=cnpj,
                    description='Valid CNPJ generated and copied to clipboard',
                    highlightable=False,
                    on_enter=CopyToClipboardAction(cnpj)
                )
            )
        return RenderResultListAction(items)

if __name__ == '__main__':
    DocumentGeneratorExtension().run()
