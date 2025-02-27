# morley_compiler/ir_to_plutus_compiler.py
import json
import os
from .ladder_logic_parser import parse_ladder_logic
from .ir_validator import validate_ir


def debug_log(message):
    print(f"[IR to Plutus Compiler] {message}")


# Load Plutus Mappings
def load_plutus_mappings(mapping_file):
    """
    Loads a JSON mapping file from the 'mappings/ir_to_plutus' directory.
    """
    mappings_dir = os.path.join(os.path.dirname(__file__), "mappings", "ir_to_plutus")
    file_path = os.path.join(mappings_dir, mapping_file)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[Error] Plutus Mapping file not found: {file_path}")
    with open(file_path, "r") as f:
        return json.load(f)


# Load All Required Plutus Mappings
plutus_arithmetic = load_plutus_mappings("ir_to_plutus_arithmetic.json")
plutus_logical = load_plutus_mappings("ir_to_plutus_logical.json")
plutus_timers = load_plutus_mappings("ir_to_plutus_timers.json")
plutus_counters = load_plutus_mappings("ir_to_plutus_counters.json")


# Main Compiler Function
def ir_to_plutus(ir):
    """
    Converts Intermediate Representation (IR) into Plutus Scripts.
    Utilizes mappings for accurate instruction translation.
    """
    if isinstance(ir, str):
        ir = json.loads(ir)

    # Validate IR before compilation
    if not validate_ir(ir):
        raise ValueError("[Validation Failed] Invalid IR Structure.")

    # Start building Morley-Plutus script
    plutus_script = []

    # Compile Morley-Plutus for Arithmetic Operations
    for math_op in ir["math_operations"]:
        operation = math_op["operation"]
        if operation in plutus_arithmetic:
            op_template = plutus_arithmetic[operation]["plutus_representation"]
            args = " ".join(math_op["args"])
            plutus_script.append(f"{op_template} {args}")
        else:
            plutus_script.append(f"-- Unsupported arithmetic operation: {operation}")

    # Compile Morley-Plutus for Logical Operations
    for logic_op in ir["logical_operations"]:
        operation = logic_op["type"]
        if operation in plutus_logical:
            op_template = plutus_logical[operation]["plutus_representation"]
            args = " ".join(logic_op["args"])
            plutus_script.append(f"{op_template} {args}")
        else:
            plutus_script.append(f"-- Unsupported logical operation: {operation}")

    # Compile Morley-Plutus for Timers
    for timer_name, timer_details in ir["timers"].items():
        timer_type = timer_details["type"]
        if timer_type in plutus_timers:
            op_template = plutus_timers[timer_type]["plutus_representation"]
            args = f"{timer_name} {timer_details['duration']}"
            plutus_script.append(f"{op_template} {args}")
        else:
            plutus_script.append(f"-- Unsupported timer type: {timer_type}")

    # Compile Morley-Plutus for Counters
    for counter_name, counter_details in ir["counters"].items():
        counter_type = counter_details["type"]
        if counter_type in plutus_counters:
            op_template = plutus_counters[counter_type]["plutus_representation"]
            args = counter_name
            if "args" in counter_details:
                args += " " + " ".join(counter_details["args"])
            plutus_script.append(f"{op_template} {args}")
        else:
            plutus_script.append(f"-- Unsupported counter type: {counter_type}")

    # Finalize Morley-Plutus Script
    compiled_script = "\n".join(plutus_script)

    debug_log(f"[Compilation Complete] Generated Plutus Script:\n{compiled_script}")
    return compiled_script


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
    ir = parse_ladder_logic(example_ladder)
    if validate_ir(ir):
        plutus_code = ir_to_plutus(ir)
        print(plutus_code)
