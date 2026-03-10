from __future__ import annotations

import argparse
import importlib
import inspect
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CS_ROOT = Path(r"E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@dataclass(frozen=True)
class ModuleDef:
    name: str
    cs_files: tuple[Path, ...]
    py_prefixes: tuple[str, ...]
    py_files: tuple[Path, ...]


MODULES: tuple[ModuleDef, ...] = (
    ModuleDef(
        name="BaseInfo",
        cs_files=(
            CS_ROOT / "BaseInfo" / "BaseInfoController.cs",
            CS_ROOT / "BaseInfo" / "BasicConfigController.cs",
            CS_ROOT / "BaseInfo" / "CommodityController.cs",
        ),
        py_prefixes=("BaseInfo", "Commodity"),
        py_files=tuple((ROOT / "routers" / "eshang_api_main" / "base_info").glob("*.py")),
    ),
    ModuleDef(
        name="Merchants",
        cs_files=(CS_ROOT / "Merchants" / "MerchantsController.cs",),
        py_prefixes=("Merchants",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "merchants" / "merchants_router.py",),
    ),
    ModuleDef(
        name="Contract",
        cs_files=(
            CS_ROOT / "Contract" / "ContractController.cs",
            CS_ROOT / "Contract" / "BusinessProjectController.cs",
            CS_ROOT / "Contract" / "ExpensesController.cs",
            CS_ROOT / "Contract" / "ContractSynController.cs",
            CS_ROOT / "Contract" / "CONTRACT_SYNController.cs",
        ),
        py_prefixes=("Contract", "BusinessProject", "ContractSyn"),
        py_files=tuple((ROOT / "routers" / "eshang_api_main" / "contract").glob("*.py")),
    ),
    ModuleDef(
        name="Finance",
        cs_files=(
            CS_ROOT / "Finance" / "FinanceController.cs",
            CS_ROOT / "Finance" / "InvoiceController.cs",
            CS_ROOT / "Finance" / "BudgetProjectAHController.cs",
        ),
        py_prefixes=("Finance", "Invoice", "Budget", "Office"),
        py_files=tuple((ROOT / "routers" / "eshang_api_main" / "finance").glob("*.py")),
    ),
    ModuleDef(
        name="Revenue",
        cs_files=(CS_ROOT / "Revenue" / "RevenueController.cs",),
        py_prefixes=("Revenue",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "revenue" / "revenue_router.py",),
    ),
    ModuleDef(
        name="BigData",
        cs_files=(
            CS_ROOT / "BigData" / "BigDataController.cs",
            CS_ROOT / "BigData" / "CustomerController.cs",
        ),
        py_prefixes=("BigData", "Customer"),
        py_files=(ROOT / "routers" / "eshang_api_main" / "bigdata" / "bigdata_router.py",),
    ),
    ModuleDef(
        name="MobilePay",
        cs_files=(CS_ROOT / "MobilePay" / "MobilePayController.cs",),
        py_prefixes=("MobilePay",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part1.py",),
    ),
    ModuleDef(
        name="Audit",
        cs_files=(CS_ROOT / "Audit" / "AuditController.cs",),
        py_prefixes=("Audit",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part1.py",),
    ),
    ModuleDef(
        name="Analysis",
        cs_files=(CS_ROOT / "Analysis" / "AnalysisController.cs",),
        py_prefixes=("Analysis",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part2.py",),
    ),
    ModuleDef(
        name="BusinessMan",
        cs_files=(CS_ROOT / "BusinessMan" / "BusinessManController.cs",),
        py_prefixes=("BusinessMan", "Merchants"),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part2.py",),
    ),
    ModuleDef(
        name="Supplier",
        cs_files=(CS_ROOT / "BusinessMan" / "SupplierController.cs",),
        py_prefixes=("Supplier",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part2.py",),
    ),
    ModuleDef(
        name="Verification",
        cs_files=(CS_ROOT / "DataVerification" / "VerificationController.cs",),
        py_prefixes=("Verification",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part2.py",),
    ),
    ModuleDef(
        name="Sales",
        cs_files=(CS_ROOT / "DataVerification" / "SalesController.cs",),
        py_prefixes=("Sales",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part2.py",),
    ),
    ModuleDef(
        name="Picture",
        cs_files=(CS_ROOT / "Picture" / "PictureController.cs",),
        py_prefixes=("Picture",),
        py_files=(ROOT / "routers" / "eshang_api_main" / "batch_modules" / "batch_router_part2.py",),
    ),
    ModuleDef(
        name="Video",
        cs_files=(CS_ROOT / "Video" / "ShopVideoController.cs",),
        py_prefixes=("ShopVideo",),
        py_files=(),
    ),
)


CS_ROUTE_RE = re.compile(r'\[Route\("(?P<route>[^"]+)"\)\]')
CS_ACCEPT_RE = re.compile(r'\[AcceptVerbs\((?P<verbs>[^\]]+)\)\]')
CS_METHOD_SIG_RE = re.compile(
    r"public\s+IHttpActionResult\s+(?P<method>\w+)\((?P<params>[^)]*)\)"
)


def normalize_path(path: Path | str | None) -> str:
    if not path:
        return ""
    try:
        return str(Path(path).resolve())
    except Exception:
        return str(path)


def clean_param_name(raw_name: str) -> str:
    name = raw_name.strip()
    name = re.sub(r"=.*$", "", name).strip()
    name = name.strip("[]")
    return name


def parse_cs_params(param_block: str) -> list[str]:
    param_block = param_block.strip()
    if not param_block:
        return []
    parts = [p.strip() for p in param_block.split(",") if p.strip()]
    params: list[str] = []
    for part in parts:
        name = clean_param_name(part.split()[-1])
        if name:
            params.append(name)
    return params


def parse_cs_routes(paths: Iterable[Path]) -> dict[str, dict]:
    routes: dict[str, dict] = {}
    for path in paths:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for index, line in enumerate(lines):
            route_match = CS_ROUTE_RE.search(line)
            if not route_match:
                continue

            route = route_match.group("route").lstrip("/")
            methods: set[str] = set()
            method_name = ""
            params: list[str] = []

            for offset in range(index, min(index + 12, len(lines))):
                accept_match = CS_ACCEPT_RE.search(lines[offset])
                if accept_match:
                    verbs = re.findall(r'"(GET|POST)"', accept_match.group("verbs"), flags=re.I)
                    methods.update(v.upper() for v in verbs)
                sig_match = CS_METHOD_SIG_RE.search(lines[offset])
                if sig_match:
                    method_name = sig_match.group("method")
                    params = parse_cs_params(sig_match.group("params"))
                    break

            if not methods:
                methods = {"POST"}

            routes[route] = {
                "route": route,
                "methods": sorted(methods),
                "params": params,
                "method_name": method_name,
                "source_file": normalize_path(path),
            }
    return routes


def wrapper_style(source: str) -> str:
    if '"code": 200' in source or "'code': 200" in source:
        return "code_message_data"
    if "Result.success" in source or "Result.fail" in source or "Result(" in source:
        return "Result_Code_Result_Desc_Result_Data"
    if '"Result_Code"' in source:
        return "Result_Code_Result_Desc_Result_Data"
    return "unknown"


def parse_py_routes() -> dict[str, dict]:
    app = importlib.import_module("main").app
    routes: dict[str, dict] = {}
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith("/EShangApiMain/"):
            continue
        rel = path[len("/EShangApiMain/"):]
        methods = sorted(m for m in getattr(route, "methods", set()) if m not in {"HEAD", "OPTIONS"})
        try:
            source = inspect.getsource(route.endpoint)
        except Exception:
            source = ""
        try:
            signature = inspect.signature(route.endpoint)
            params = [
                name
                for name, param in signature.parameters.items()
                if name not in {"db", "request"}
                and not str(param.default).startswith("Depends(")
            ]
        except Exception:
            params = []
        routes[rel] = {
            "route": rel,
            "methods": methods,
            "params": params,
            "endpoint_name": getattr(route.endpoint, "__name__", ""),
            "source_file": normalize_path(inspect.getsourcefile(route.endpoint)),
            "wrapper_style": wrapper_style(source),
        }
    return routes


def route_prefix(route: str) -> str:
    return route.split("/", 1)[0]


def belongs_to_module(route_info: dict, module: ModuleDef) -> bool:
    if route_prefix(route_info["route"]) not in module.py_prefixes:
        return False
    if not module.py_files:
        return False
    source_file = normalize_path(route_info.get("source_file"))
    module_files = {normalize_path(path) for path in module.py_files}
    return source_file in module_files


def module_completion(summary: dict) -> float:
    total = summary["csharp_unique_routes"]
    if not total:
        return 100.0
    return round(summary["matched_routes"] * 100.0 / total, 1)


def build_report() -> dict:
    py_routes = parse_py_routes()
    report = {
        "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "workspace": str(ROOT),
        "mode": "full_static_baseline",
        "note": "This is a machine baseline for full-route audit. It does not replace manual service/helper logic review.",
        "modules": [],
    }

    for module in MODULES:
        cs_routes = parse_cs_routes(module.cs_files)
        py_module_routes = {
            route: info
            for route, info in py_routes.items()
            if belongs_to_module(info, module)
        }

        route_names = sorted(set(cs_routes) | set(py_module_routes))
        route_items = []
        matched = 0
        python_only = 0
        csharp_only = 0
        method_mismatch = 0
        param_name_mismatch = 0
        wrapper_drift = 0

        for route_name in route_names:
            cs_info = cs_routes.get(route_name)
            py_info = py_module_routes.get(route_name)

            status = "matched"
            if cs_info and py_info:
                matched += 1
            elif cs_info:
                status = "missing_in_python"
                csharp_only += 1
            else:
                status = "python_only"
                python_only += 1

            cs_methods = cs_info["methods"] if cs_info else []
            py_methods = py_info["methods"] if py_info else []
            methods_equal = cs_methods == py_methods if cs_info and py_info else False
            if cs_info and py_info and not methods_equal:
                method_mismatch += 1

            cs_params = cs_info["params"] if cs_info else []
            py_params = py_info["params"] if py_info else []
            params_equal = cs_params == py_params if cs_info and py_info else False
            if cs_info and py_info and not params_equal:
                param_name_mismatch += 1

            wrapper = py_info["wrapper_style"] if py_info else ""
            if cs_info and py_info and wrapper == "code_message_data":
                wrapper_drift += 1

            route_items.append(
                {
                    "route": route_name,
                    "status": status,
                    "csharp": cs_info,
                    "python": py_info,
                    "method_match": methods_equal if cs_info and py_info else None,
                    "param_match": params_equal if cs_info and py_info else None,
                }
            )

        summary = {
            "module": module.name,
            "csharp_unique_routes": len(cs_routes),
            "python_runtime_routes": len(py_module_routes),
            "matched_routes": matched,
            "missing_in_python": csharp_only,
            "python_only_routes": python_only,
            "method_mismatch_routes": method_mismatch,
            "param_name_mismatch_routes": param_name_mismatch,
            "response_wrapper_drift_routes": wrapper_drift,
        }
        summary["completion_percent"] = module_completion(summary)

        report["modules"].append(
            {
                "summary": summary,
                "route_items": route_items,
            }
        )

    return report


def main() -> None:
    default_output = ROOT / "docs" / "full_audit_baseline_20260309.json"
    parser = argparse.ArgumentParser(description="Export full static audit baseline for migrated interfaces.")
    parser.add_argument("--output", type=Path, default=default_output, help="Output JSON path.")
    args = parser.parse_args()

    report = build_report()
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote baseline to: {args.output}")


if __name__ == "__main__":
    main()
