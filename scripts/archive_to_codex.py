import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    api_key = os.getenv("CODEX_API_KEY")
    if not api_key:
        raise ValueError("CODEX_API_KEY not found!")

    print(f"Archiving {args.source} with message: {args.message}")
    print(f"API key starts with: {api_key[:10]}...")

if __name__ == "__main__":
    main()
