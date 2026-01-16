import sys
import os

# Add src to python path to allow imports if running from root
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.extract import extract_data
from src.transform import transform_data
from src.analyze import generate_insights

def main():
    print("=== Copper Intelligence Pipeline Started ===")
    
    # Step 1: Extract
    try:
        extract_data()
    except Exception as e:
        print(f"Extraction failed: {e}")
        return

    # Step 2: Transform
    try:
        transform_data()
    except Exception as e:
        print(f"Transformation failed: {e}")
        return

    # Step 3: Analyze
    try:
        insights = generate_insights()
        print("\n--- INSIGHTS ---")
        print(insights)
        print("----------------")
    except Exception as e:
        print(f"Analysis failed: {e}")
        return

    print("=== Pipeline Complete ===")

if __name__ == "__main__":
    main()
