# Ulauncher Generate Document

This project is an extension for [Ulauncher](https://ulauncher.io/) that generates **valid CPF and CNPJ numbers** and automatically copies them to the clipboard.

## Table of Contents

- [Overview](#overview)
- [Demo](#demo)
- [Files and Structure](#files-and-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This extension allows you to quickly generate CPF and CNPJ numbers (Brazilian identification documents) with correct check digits directly through Ulauncher. When triggered by the configured keyword (default is `doc`), you can choose to:

- **Generate CPF**  
- **Generate CNPJ**

The generated number is then automatically copied to your clipboard.

**Note**: This project is provided for testing and educational purposes only. Do not use it for illegal or malicious activities.

---

## Demo

In the `images/` folder, there is a **demo.gif** showing how the extension works in Ulauncher:
- **demo.gif**: Demonstrates the extension, from opening Ulauncher to generating and copying the CPF/CNPJ.

---

## Files and Structure

```plaintext
.
├── images
│   ├── cnpj.webp
│   ├── cpf.webp
│   ├── cpfcnpj.webp
│   └── demo.gif
├── main.py
├── manifest.json
├── README.md
├── tmp.py
├── versions.json
└── ...
