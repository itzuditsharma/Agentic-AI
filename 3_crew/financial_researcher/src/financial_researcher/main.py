import os
from financial_researcher.crew import FinancialResearcher
import logging
logging.basicConfig(level=logging.DEBUG)


# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the Financial research crew.
    """
    inputs = {
        'company': 'Tesla'
    }

    # Create and run the crew
    result = FinancialResearcher().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("Error occurred:", e)
