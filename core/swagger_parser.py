import json

# Swagger dosyasını alıp, okuma modunda açıyor ve swagger adlı json değişkenine kaydediyor.
def load_swagger_file(file_like):
    try:
        if hasattr(file_like, "read"):  # Streamlit dosyası (BytesIO)
            return json.load(file_like)
        else:  # Dosya yolu (str)
            with open(file_like, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Hata: Swagger dosyası yüklenemedi: {e}")
        return None

# Swagger json daki endpointleri, metotları, özetleri ve parametre bilgilerini alıp geri döndürür.
def extract_endpoints(swagger_data):
    endpoints = []
    paths = swagger_data.get("paths", {})

    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue  # güvenlik için

        path_level_params = methods.get("parameters", [])  

        for method, details in methods.items():
            if method.lower() not in ["get", "post", "put", "delete", "patch", "head", "options"]:
                continue  

            if not isinstance(details, dict):
                continue  # details sözlük değilse atla

            summary = details.get("summary", "")
            method_params = details.get("parameters", [])
            consumes=details.get("consumes",[])
            all_parameters = path_level_params + method_params
            param_list = []

            for param in all_parameters:
                param_info = {
                    "name": param.get("name"),
                    "in": param.get("in"),
                    "required": param.get("required", False),
                    "type": param.get("schema", {}).get("type") if "schema" in param else param.get("type")
                }
                param_list.append(param_info)

            endpoints.append({
                "path": path,
                "method": method.upper(),
                "summary": summary,
                "consumes":consumes,
                "parameters": param_list
            })

    return endpoints

def get_base_url(swagger):
    scheme = swagger.get("schemes", ["https"])[0]
    host = swagger.get("host", "localhost")
    base_path = swagger.get("basePath", "")
    return f"{scheme}://{host}{base_path}"
