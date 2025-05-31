import json

def generate_curl_command(base_url, endpoint, auth_token="demo_token"):
    method = endpoint["method"]
    path = endpoint["path"]
    params = endpoint.get("parameters", [])
    consumes = endpoint.get("consumes", ["application/json"])  # Swagger'dan gelen içerik türleri

    # 1. PATH parametrelerini doldurma
    for param in params:
        if param["in"] == "path":
            dummy_value = get_dummy_value(param["type"])
            path = path.replace("{" + param["name"] + "}", str(dummy_value))

    # 2. QUERY string oluşturma
    query_params = []
    for param in params:
        if param["in"] == "query":
            dummy_value = get_dummy_value(param["type"])
            query_params.append(f"{param['name']}={dummy_value}")

    query_string = "?" + "&".join(query_params) if query_params else ""
    full_url = base_url.rstrip("/") + path + query_string

    # 3. BODY içeriği hazırlama (varsa)
    body_data = {}
    content_type = consumes[0] if consumes else "application/json"
    is_body_present = False

    for param in params:
        if param["in"] == "body":
            is_body_present = True
            schema = param.get("schema", {})
            if "properties" in schema:
                for key, val in schema["properties"].items():
                    body_data[key] = get_dummy_value(val.get("type", "string"))
            else:
                body_data = get_dummy_value(schema.get("type", "string"))

    # 4. curl komutu oluşturma
    curl = f'curl -X {method} "{full_url}"'

    # 5. Authorization ekleme
    curl += f' -H "Authorization: Bearer {auth_token}"'

    # 6. Content-Type ve Body ekleme
    if is_body_present:
        if content_type == "application/json":
            json_data = json.dumps(body_data)
            curl += f' -H "Content-Type: application/json" -d \'{json_data}\''
        elif content_type == "application/x-www-form-urlencoded":
            form_data = "&".join([f"{k}={v}" for k, v in body_data.items()])
            curl += f' -H "Content-Type: application/x-www-form-urlencoded" -d "{form_data}"'
        elif content_type == "multipart/form-data":
            for k, v in body_data.items():
                curl += f' -F "{k}={v}"'

    return curl


def get_dummy_value(param_type):
    if param_type == "string":
        return "example"
    elif param_type == "integer":
        return 123
    elif param_type == "boolean":
        return "true"
    elif param_type == "number":
        return 12.34
    elif param_type == "array":
        return ["item1", "item2"]
    elif param_type == "object":
        return {"key": "value"}
    return "value"

def get_base_url(swagger):
    scheme = swagger.get("schemes", ["https"])[0]
    host = swagger.get("host", "localhost")
    base_path = swagger.get("basePath", "")
    return f"{scheme}://{host}{base_path}"