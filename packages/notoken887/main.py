import argparse
import os
from notoken887.encryptor import TokenCryptor

def encrypt_code(code):
    cryptor = TokenCryptor()
    encrypted_lines = []
    for line in code.splitlines():
        if not line.strip().startswith(("import", "from")):
            encrypted_lines.append(cryptor.proccess(line))
    return '\n'.join(encrypted_lines)

def process_file(input_path, output_path, mode):
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    if mode == 'e':
        encrypted_code = encrypt_code(content)
        output_content = f"l = '''{encrypted_code.replace('\\n', ' ')}'''"
    else:
        decrypted_content = decrypt_code(content)
        output_content = decrypted_content.strip()
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(output_content)

    if mode == 'e':
        create_main_pyw(input_path, output_path)


def create_main_pyw(input_path, output_path):
    output_module = os.path.splitext(os.path.basename(output_path))[0]
    with open(input_path, 'r', encoding='utf-8') as infile:
        imports = [line for line in infile if line.strip().startswith(("import", "from"))]
    
    main_pyw_content = f"""from notoken887.encryptor import TokenCryptor
from {output_module} import l
{''.join(imports)}

cryptor = TokenCryptor()
decrypted_code = cryptor.process(l)
exec(decrypted_code)
#THIS PACKAGE WAS EMOJIFIED WITH NOTOKEN887 MADE BY RAYWZW"""

    with open('main.pyw', 'w', encoding='utf-8') as main_file:
        main_file.write(main_pyw_content)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt Python files using TokenCryptor.')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output file path')
    parser.add_argument('--mode', '-m', choices=['e', 'd'], required=True, help='Mode: e for encrypt, d for decrypt')
    args = parser.parse_args()
    process_file(args.input, args.output, args.mode)

if __name__ == "__main__":
    main()
