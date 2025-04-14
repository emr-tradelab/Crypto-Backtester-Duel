"""
Minimal entry point for testing.
"""

def main() -> None:
    print("Hello from NautilusTradingBot - this is a simple test run.")

    from nautilus_trader import TEST_DATA_DIR
    print(TEST_DATA_DIR)  

if __name__ == "__main__":
    main()
