import requests
import json
import os
import re

def get_model_fields():
    """从 models 及其子目录读取实体模型字段定义"""
    base_dir = r"E:\workfile\JAVA\NewAPI\models"
    models = {}
    
    # 递归查找所有模型文件
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 增强正则表达式：支持带或不带 Optional，支持各种空白
                    # 匹配格式: FIELD_NAME: Optional[Type] = None  # 注释
                    matches = re.findall(r"([A-Z0-9_]+):\s*(?:Optional\[)?\w+(?:\])?\s*=\s*None\s*#\s*(.*)", content)
                    if matches:
                        entity_name = filename.replace(".py", "").upper()
                        models[entity_name] = [{"name": m[0], "desc": m[1].strip()} for m in matches]
    return models

def resolve_schema(schema, components_schemas):
    """递归解析 OpenAPI 中的 schema 引用"""
    if not schema:
        return {}
    if "$ref" in schema:
        ref_name = schema["$ref"].split("/")[-1]
        return resolve_schema(components_schemas.get(ref_name, {}), components_schemas)
    for composite in ["anyOf", "allOf", "oneOf"]:
        if composite in schema:
            for sub_schema in schema[composite]:
                resolved = resolve_schema(sub_schema, components_schemas)
                if resolved and resolved.get("type") == "object":
                    return resolved
            return resolve_schema(schema[composite][0], components_schemas)
    return schema

def extract_entity_key(tag_name):
    """从标签名中提取实体 Key，例如 '业主单位管理 (OWNERUNIT)' -> 'OWNERUNIT'"""
    # 匹配括号内的内容
    match = re.search(r"\((.*?)\)", tag_name)
    if match:
        return match.group(1).upper()
    return tag_name.upper()

def gen_markdown():
    url = "http://localhost:8080/openapi.json"
    models_metadata = get_model_fields()
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed: {response.status_code}")
            return
        
        data = response.json()
        components_schemas = data.get('components', {}).get('schemas', {})
        
        md_content = "# EShang API (FastAPI) 迁移完成接口文档\n\n"
        md_content += f"> **基础地址**: `http://localhost:8080` (本地测试版)\n\n"
        
        tag_to_paths = {}
        for path, methods in data.get('paths', {}).items():
            for method, details in methods.items():
                p_tags = details.get('tags', ['Other'])
                for tag in p_tags:
                    if tag not in tag_to_paths: tag_to_paths[tag] = []
                    tag_to_paths[tag].append((path, method, details))
        
        for tag_name in sorted(tag_to_paths.keys()):
            md_content += f"## {tag_name}\n\n"
            entity_key = extract_entity_key(tag_name)
            entity_fields = models_metadata.get(entity_key, [])
            
            for path, method, details in tag_to_paths[tag_name]:
                md_content += f"### {method.upper()} {path}\n"
                md_content += f"**接口名称**: {details.get('summary', '')}\n\n"
                
                # Parameters (Query)
                params = details.get('parameters', [])
                if params:
                    md_content += "| 参数名 | 类型 | 必填 | 说明 |\n| --- | --- | --- | --- |\n"
                    for p in params:
                        md_content += f"| {p.get('name')} | {p.get('schema', {}).get('type', 'any')} | {'Y' if p.get('required') else 'N'} | {p.get('description', '')} |\n"
                    md_content += "\n"
                
                # Request Body
                request_body = details.get('requestBody', {})
                if request_body:
                    content = request_body.get('content', {})
                    if 'application/json' in content:
                        schema = content['application/json'].get('schema', {})
                        if "SearchModel" in str(schema):
                            md_content += "#### 📝 查询入参 (SearchModel)\n"
                            md_content += "| 核心字段 | 说明 |\n| --- | --- |\n"
                            md_content += "| PageIndex | 页码 (1...) |\n| PageSize | 条数 (0=全量) |\n"
                            md_content += "| SearchParameter | **详细过滤字段 (见下表)** |\n\n"
                            
                            if entity_fields:
                                md_content += f"**{entity_key} 过滤字段 (SearchParameter 内部):**\n\n"
                                md_content += "| 字段名 | 说明 |\n| --- | --- |\n"
                                for f in entity_fields[:10]: # 展示前10个常用字段
                                    md_content += f"| {f['name']} | {f['desc']} |\n"
                                md_content += "\n"
                                
                                example_param = {f['name']: ("string" if "名称" in f['desc'] or "说明" in f['desc'] else 0) for f in entity_fields[:3]}
                                example_json = {"PageIndex": 1, "PageSize": 20, "SearchParameter": example_param}
                                md_content += "**请求 JSON 示例**:\n```json\n" + json.dumps(example_json, indent=2, ensure_ascii=False) + "\n```\n"
                        
                        elif "Synchro" in path or entity_fields:
                            md_content += "#### 📝 同步入参 (Entity Body)\n"
                            if entity_fields:
                                md_content += "| 字段名 | 说明 |\n| --- | --- |\n"
                                for f in entity_fields:
                                    md_content += f"| {f['name']} | {f['desc']} |\n"
                                md_content += "\n"
                                example_sync = {f['name']: (0 if "内码" in f['desc'] or "状态" in f['desc'] else "string") for f in entity_fields[:5]}
                                md_content += "**同步 JSON 示例**:\n```json\n" + json.dumps(example_sync, indent=2, ensure_ascii=False) + "\n```\n"
                    md_content += "\n"
                md_content += "---\n\n"
        
        with open("迁移完成接口文档_FastAPI.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    gen_markdown()
