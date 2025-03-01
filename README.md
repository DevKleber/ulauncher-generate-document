# CPF and CNPJ Generator for Ulauncher

This extension for [Ulauncher](https://ulauncher.io/) quickly generates valid Brazilian CPF and CNPJ numbers and copies them directly to your clipboard.

---

## How It Works

- **Generation Functions:**  
  - `gerar_cpf()`: Creates a CPF by generating 9 random digits and calculating 2 check digits.  
  - `gerar_cnpj()`: Creates a CNPJ by generating 12 random digits and calculating 2 check digits.

- **Ulauncher Integration:**  
  The extension listens for keyword queries in Ulauncher. Depending on your input:
  - Typing `doc cpf` will display a CPF option.
  - Typing `doc cnpj` will display a CNPJ option.
  - If no filter is provided, both options appear.
  
  When you select an option, the generated number is automatically copied to your clipboard.

---

## How to Use

1. **Install the Extension:**
   - **Clone or Download:**  
     ```bash
     git clone https://github.com/YOUR_USERNAME/ulauncher-cpf-cnpj-generator.git
     ```
   - **Copy Files:**  
     Place the extension folder in your Ulauncher extensions directory, typically:
     ```
     ~/.local/share/ulauncher/extensions/cpf-cnpj-generator
     ```
   - **Restart Ulauncher:**  
     Restart or relaunch Ulauncher to load the extension.

2. **Generate a Document:**
   - **Activate Ulauncher:**  
     Press your Ulauncher shortcut (e.g., <kbd>Ctrl + Space</kbd>).
   - **Type the Keyword:**  
     Enter the keyword defined in `manifest.json` (default is `doc`).
   - **Filter (Optional):**  
     - Type `doc cpf` to generate and copy a CPF.
     - Type `doc cnpj` to generate and copy a CNPJ.
     - If no filter is used, both options will be displayed.
   - **Select an Option:**  
     Press <kbd>Enter</kbd> on the desired result. The generated CPF or CNPJ will be copied to your clipboard automatically.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
