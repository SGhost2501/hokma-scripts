import argparse
import hashlib
import os
import zipfile


def main():
    parser = argparse.ArgumentParser(description='Hash and zip hokma corpus')
    parser.add_argument('--input', default='hokma_corpus_final.jsonl')
    args = parser.parse_args()

    with open(args.input, 'rb') as f:
        data = f.read()
    sha = hashlib.sha256(data).hexdigest()
    base = os.path.splitext(os.path.basename(args.input))[0]
    zip_name = f"{base}_{sha[:8]}.zip"

    with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(os.path.basename(args.input), data)
    print(f"SHA256: {sha}")
    print(f"Created {zip_name}")


if __name__ == '__main__':
    main()
