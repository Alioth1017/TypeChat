import asyncio
import json
import sys
from dotenv import dotenv_values
import schema as math
from typechat import Failure, create_language_model, process_requests
from program import TypeChatProgramTranslator, TypeChatProgramValidator, JsonProgram, evaluate_json_program  # type: ignore

vals = dotenv_values()
model = create_language_model(vals)
validator = TypeChatProgramValidator(JsonProgram)
translator = TypeChatProgramTranslator(model, validator, math.MathAPI)


async def apply_operations(func: str, args: list[int | float]) -> int | float:
    print(f"{func}({json.dumps(args)}) ")
    match func:
        case "add":
            return args[0] + args[1]
        case "sub":
            return args[0] - args[1]
        case "mul":
            return args[0] * args[1]
        case "div":
            return args[0] / args[1]
        case "neg":
            return -1 * args[0]
        case "id":
            return args[0]
        case _:
            raise ValueError(f'Unexpected function name {func}')


async def request_handler(message: str):
    result = await translator.translate(message)
    if isinstance(result, Failure):
        print(result.message)
    else:
        result = result.value
        print(json.dumps(result, indent=2))
        math_result = await evaluate_json_program(result, apply_operations)  # type: ignore
        print(f"Math Result: {math_result}")


async def main():
    file_path = sys.argv[1] if len(sys.argv) == 2 else None
    await process_requests("🧮> ", file_path, request_handler)


if __name__ == "__main__":
    asyncio.run(main())
