from typing import Optional


def optional_value(value: Optional[str]) -> str:
    if "fd" in value:
        return value
    else:
        return "fd"


returned = optional_value("fdsfs")
optional_value(None)