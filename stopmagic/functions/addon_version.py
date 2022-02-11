from typing import Any


def addon_version(info: "dict[str, Any]") -> str:
    """Gets the string form of the addon version"""

    result = ""
    i = 0
    length = len(info["version"])
    while i < length:
        result += str(info["version"][i])
        if i + 1 != length:
            result += "."
        i += 1
    if "warning" in info:
        result += "-" + info["warning"]
    return result
