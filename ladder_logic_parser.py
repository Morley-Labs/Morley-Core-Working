# morley_compiler/ladder_logic_parser.py
import json
import os
from .ir_validator import validate_ir  # Import IR Validator


def debug_log(message):
    print(f"[Ladder Logic Parser] {message}")


# Load Mappings Function
def load_mappings(mapping_file):
    """
    Loads a JSON mapping file from the 'mappings' directory.
    """
    mappings_dir = os.path.join(os.path.dirname(__file__), "mappings")
    file_path = os.path.join(mappings_dir, mapping_file)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[Error] Mapping file not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f)


# Parse Ladder Logic into Intermediate Representation (IR)
def parse_ladder_logic(ladder_logic):
    """
    Parses Ladder Logic and converts it into an Intermediate Representation (IR).
    Utilizes mappings for accurate instruction interpretation.
    """

    # Load Mappings
    ladder_logic_mappings = load_mappings("ladder_logic.json")
    instruction_set_mappings = load_mappings("instruction_set.json")
    structured_text_mappings = load_mappings("structured_text.json")

    ir_representation = {
        "instructions": [],
        "logical_operations": [],
        "arithmetic_operations": [],
        "timers": {},
        "counters": {},
        "math_operations": [],
        "comparators": [],
        "set_reset_latches": [],
        "jump_instructions": [],
        "function_blocks": {},
        "selection_functions": [],
        "scan_cycle": [],
    }

    # Tokenize Ladder Logic
    lines = ladder_logic.strip().splitlines()
    for line in lines:
        tokens = line.split()
        if not tokens:
            continue
        instruction = tokens[0]
        args = tokens[1:]

        # Basic Logic Operations (Contacts and Coils)
        if instruction in ladder_logic_mappings["contacts"]:
            ir_representation["instructions"].append(
                {
                    "type": f"IR_{ladder_logic_mappings['contacts'][instruction]['ir_representation']}",
                    "args": args,
                }
            )
        elif instruction in ladder_logic_mappings["coils"]:
            ir_representation["set_reset_latches"].append(
                {
                    "type": f"IR_{ladder_logic_mappings['coils'][instruction]['ir_representation']}",
                    "args": args,
                }
            )

        # Logical Operations
        elif instruction in ladder_logic_mappings["logical_operations"]:
            ir_representation["logical_operations"].append(
                {
                    "type": f"IR_{ladder_logic_mappings['logical_operations'][instruction]['ir_representation']}",
                    "args": args,
                }
            )

        # Math Operations
        elif instruction in ladder_logic_mappings["arithmetic"]:
            ir_representation["math_operations"].append(
                {
                    "operation": f"IR_{ladder_logic_mappings['arithmetic'][instruction]['ir_representation']}",
                    "args": args,
                }
            )

        # Timers and Counters
        elif instruction in ladder_logic_mappings["timers"]:
            ir_representation["timers"][args[0]] = {
                "type": f"IR_{ladder_logic_mappings['timers'][instruction]['ir_representation']}",
                "duration": args[1],
            }
        elif instruction in ladder_logic_mappings["counters"]:
            ir_representation["counters"][args[0]] = {
                "type": f"IR_{ladder_logic_mappings['counters'][instruction]['ir_representation']}"
            }

        # Comparators
        elif instruction in ladder_logic_mappings["comparison_operators"]:
            ir_representation["comparators"].append(
                {
                    "type": f"IR_{ladder_logic_mappings['comparison_operators'][instruction]['ir_representation']}",
                    "args": args,
                }
            )

        # Jump Instructions and Subroutines
        elif instruction in ladder_logic_mappings["jump_subroutine"]:
            ir_representation["jump_instructions"].append(
                {
                    "type": f"IR_{ladder_logic_mappings['jump_subroutine'][instruction]['ir_representation']}",
                    "args": args,
                }
            )

        # Function Blocks and Selection Functions
        elif instruction in ladder_logic_mappings["selection_functions"]:
            ir_representation["selection_functions"].append(
                {
                    "type": f"IR_{ladder_logic_mappings['selection_functions'][instruction]['ir_representation']}",
                    "args": args,
                }
            )

        # If nothing matches, consider it part of the scan cycle
        else:
            ir_representation["scan_cycle"].append(instruction)

    # Debugging and Logging
    debug_log(
        f"[IR Generation] Current IR Structure: {json.dumps(ir_representation, indent=2)}"
    )

    # Validate the IR before returning
    if validate_ir(ir_representation):
        debug_log("[Validation Passed] Generated IR is valid.")
    else:
        raise ValueError("[Validation Failed] Invalid IR structure.")

    return ir_representation


# For Local Testing
if __name__ == "__main__":
    example_ladder = """
    XIC A
    AND B
    OTE C
    ADD A B C
    TON T1 1000
    CTU C1 10 True
    """
    print(json.dumps(parse_ladder_logic(example_ladder), indent=2))
