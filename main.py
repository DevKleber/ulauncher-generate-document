import os
import random
import datetime
import string
import logging

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from datafaker.first_names import first_names
from datafaker.last_names import last_names
from datafaker.streets import streets
from datafaker.municipalities import municipalities

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def get_icon(key, default='doc.png'):
    icon_path = os.path.join(IMAGES_DIR, f"{key}.png")
    if os.path.exists(icon_path):
        return icon_path
    else:
        return os.path.join(IMAGES_DIR, default)

def calculate_digit(numbers, weights):
    total = sum(int(n) * p for n, p in zip(numbers, weights))
    remainder = total % 11
    return '0' if remainder < 2 else str(11 - remainder)

def generate_random_number(count):
    return ''.join(random.choice(string.digits) for _ in range(count))


class DataGenerator:
    def __init__(self):
        self.first_names = first_names
        self.last_names = last_names
        self.streets = streets

    def generate_cpf(self, formatted=True) -> str:
        nine_digits = generate_random_number(9)
        first_weights = list(range(10, 1, -1))
        first_digit = calculate_digit(nine_digits, first_weights)
        second_weights = list(range(11, 1, -1))
        second_digit = calculate_digit(nine_digits + first_digit, second_weights)
        cpf = nine_digits + first_digit + second_digit
        if formatted:
            return "{}.{}.{}-{}".format(cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])
        return cpf

    def generate_cnpj(self, formatted=True) -> str:
        root = generate_random_number(8)
        suffix = "0001"
        numbers = root + suffix
        first_weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        first_digit = calculate_digit(numbers, first_weights)
        second_weights = [6] + first_weights
        second_digit = calculate_digit(numbers + first_digit, second_weights)
        cnpj = numbers + first_digit + second_digit
        if formatted:
            return "{}.{}.{}/{}-{}".format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
        return cnpj

    def generate_rg(self, formatted=False) -> str:
        rg = generate_random_number(9)
        if formatted:
            return "{}.{}.{}-{}".format(rg[:2], rg[2:5], rg[5:8], rg[8])
        return rg

    def generate_name(self) -> str:
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        return f"{first} {last}"

    def generate_address(self) -> str:
        street = random.choice(self.streets)
        number = random.randint(1, 2000)
        complement = random.choice([f"Apt {random.randint(1, 500)}", "", "House"])

        state = random.choice(list(municipalities.keys()))
        city = random.choice(municipalities[state])
        address = f"{street}, {number}"
        if complement:
            address += f", {complement}"
        address += f" - {city}/{state}"
        return address

    def generate_postal_code(self, with_dash=True) -> str:
        postal = generate_random_number(8)
        if with_dash:
            return f"{postal[:5]}-{postal[5:]}"
        return postal

    def generate_phone(self, with_ddd=True) -> str:
        ddd = generate_random_number(2) if with_ddd else ""
        if random.choice([True, False]):
            number = "9" + generate_random_number(8)
        else:
            number = generate_random_number(8)
        if ddd:
            if len(number) == 9:
                return f"({ddd}) {number[:5]}-{number[5:]}"
            else:
                return f"({ddd}) {number[:4]}-{number[4:]}"
        return number

    def generate_birth_date(self, start="1950-01-01", end="2010-12-31") -> str:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        birth_date = start_date + datetime.timedelta(days=random_days)
        return birth_date.strftime("%d/%m/%Y")

    def generate_email(self, name: str = None) -> str:
        if not name:
            name = self.generate_name()
        clean_name = ''.join(c for c in name if c.isalnum()).lower()
        domain = random.choice([
            "example.com", "test.com.br", "email.com",
            "gmail.com", "outlook.com", "yahoo.com", "hotmail.com"
        ])
        return f"{clean_name}@{domain}"

    def generate_full_data(self) -> dict:
        data = {
            "Name": self.generate_name(),
            "Birth Date": self.generate_birth_date(),
            "CPF": self.generate_cpf(),
            "RG": self.generate_rg(formatted=True),
            "CNPJ": self.generate_cnpj(),
            "Address": self.generate_address(),
            "Postal Code": self.generate_postal_code(),
            "Phone": self.generate_phone(),
            "Email": None
        }
        data["Email"] = self.generate_email(data["Name"])
        return data


GENERATORS = {
    "cpf": ("CPF", lambda gen: gen.generate_cpf()),
    "cnpj": ("CNPJ", lambda gen: gen.generate_cnpj()),
    "rg": ("RG", lambda gen: gen.generate_rg(formatted=True)),
    "name": ("Name", lambda gen: gen.generate_name()),
    "address": ("Address", lambda gen: gen.generate_address()),
    "postal": ("Postal Code", lambda gen: gen.generate_postal_code()),
    "phone": ("Phone", lambda gen: gen.generate_phone()),
    "birth": ("Birth Date", lambda gen: gen.generate_birth_date()),
    "email": ("Email", lambda gen: gen.generate_email()),
    "full": ("Full Data", lambda gen: "\n".join(
        f"{key}: {value}" for key, value in gen.generate_full_data().items()))
}


class EnglishDataExtension(Extension):
    def __init__(self):
        super(EnglishDataExtension, self).__init__()
        self.generator = DataGenerator()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener(self.generator))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener(self.generator))


class KeywordQueryEventListener(EventListener):
    def __init__(self, generator):
        self.generator = generator

    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower().strip()
        items = []

        if query in GENERATORS:
            friendly_name, gen_func = GENERATORS[query]
            items.append(
                ExtensionResultItem(
                    icon=get_icon(query, default='doc.png'),
                    name=friendly_name,
                    description=f"Generates {friendly_name} and copies it to clipboard",
                    highlightable=False,
                    on_enter=CopyToClipboardAction(gen_func(self.generator))
                )
            )
            return RenderResultListAction(items)

        for key, (friendly_name, _) in sorted(GENERATORS.items()):
            items.append(
                ExtensionSmallResultItem(
                    icon=get_icon(key, default='doc.png'),
                    name=friendly_name,
                    on_enter=ExtensionCustomAction(key, keep_app_open=True)
                )
            )
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def __init__(self, generator):
        self.generator = generator

    def on_event(self, event, extension):
        provider = event.get_data()
        if provider in GENERATORS:
            friendly_name, gen_func = GENERATORS[provider]
            value = gen_func(self.generator)
            return RenderResultListAction([
                ExtensionResultItem(
                    icon=get_icon(provider, default='doc.png'),
                    name=str(value),
                    description=f"{friendly_name} generated and copied to clipboard",
                    highlightable=False,
                    on_enter=CopyToClipboardAction(value)
                )
            ])
        else:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon=get_icon('icon', default='doc.png'),
                    name="Type not found",
                    highlightable=False,
                    on_enter=HideWindowAction()
                )
            ])


if __name__ == '__main__':
    EnglishDataExtension().run()
