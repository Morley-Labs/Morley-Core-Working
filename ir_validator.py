# morley_compiler/ir_validator.py
import json


def debug_log(message):
    print(f"[IR Validator] {message}")


def validate_ir(ir):
    # If the input is a string, parse it into a dictionary
    if isinstance(ir, str):
        ir = json.loads(ir)

    # Required keys for IR structure
    required_keys = [
        "instructions",
        "logical_operations",
        "arithmetic_operations",
        "timers",
        "counters",
        "math_operations",
        "comparators",
        "set_reset_latches",
        "jump_instructions",
        "function_blocks",
        "selection_functions",
        "scan_cycle",
    ]

    # Check for missing keys
    for key in required_keys:
        if key not in ir:
            debug_log(f"[Validation Failed] Missing key: {key}")
            return False

    # Check if all values are of the expected type
    for key, value in ir.items():
        if key in ["timers", "counters", "function_blocks"]:
            if not isinstance(value, dict):
                debug_log(f"[Validation Failed] {key} should be a dictionary.")
                return False
        else:
            if not isinstance(value, list):
                debug_log(f"[Validation Failed] {key} should be a list.")
                return False

    debug_log("[Validation Passed] IR Structure is valid.")
    return True


if __name__ == "__main__":
    # Sample IR for testing
    sample_ir = {
        "instructions": [{"type": "LL_XIC", "args": ["A"]}],
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
    print(validate_ir(sample_ir))
