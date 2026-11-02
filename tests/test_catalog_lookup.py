from backend.services.catalog_service import (
    get_module,
    get_module_by_title,
    get_module_by_skill
)

print(
    get_module("M001")
)

print(
    get_module_by_title(
        "Microsoft Fabric Fundamentals"
    )
)

print(
    get_module_by_skill(
        "PySpark"
    )
)
