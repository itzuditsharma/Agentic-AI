from misra.crew import Coder

assignment = (
    # Example: choose one
    # "Write a C program to compute factorial using recursion and follow MISRA rules."
    "Review this C++ code for MISRA violations:\nint main() { int x = 0; while(1) { x++; } }"
)

def run():
    coder_crew = Coder()
    relevant_rules = coder_crew.retrieve_misra_rules(assignment, k=7)

    inputs = {
        "assignment": assignment,
        "misra_rules": relevant_rules
    }

    result = coder_crew.crew().kickoff(inputs=inputs)
    print(result.raw)

if __name__ == "__main__":
    run()
