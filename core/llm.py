import ollama

OWASP_TOP_10 = """
OWASP API Security Top 10 2023:
1. Broken Object Level Authorization
2. Broken Authentication
3. Broken Object Property Level Authorization
4. Unrestricted Resource Consumption
5. Broken Function Level Authorization
6. Unrestricted Access to Sensitive Business Flows
7. Server Side Request Forgery (SSRF)
8. Security Misconfiguration
9. Improper Inventory Management
10. Unsafe Consumption of APIs
"""

def prompt_attack_cases(endpoint):
    method = endpoint["method"]
    path = endpoint["path"]
    summary = endpoint.get("summary", "")
    parameters = endpoint.get("parameters", [])

    param_str = ""
    for p in parameters:
        param_str += f"- {p['name']} ({p['in']}), required: {p['required']}, type: {p['type']}\n"

    prompt = f"""Bir API güvenlik uzmanı gibi davranmanı istiyorum.
    Aşağıdaki endpoint'i OWASP API Security Top 10 listesine göre analiz et:{OWASP_TOP_10}
    ### Endpoint Bilgileri:
    - METHOD: {method}
    - PATH: {path}
    - AÇIKLAMA: {summary}
    - PARAMETRELER:
    {param_str}
    
    ### Çıktı Formatı:
    1. Bu endpoint için risk taşıyan OWASP maddeleri hangileridir?
    2. Her OWASP açığı için kısa bir açıklama ve neden bu endpoint için geçerli olduğunu belirt.
    3. Her açıklık için:
    - En az bir pozitif test senaryosu (beklenen davranış)
    - En az bir negatif test senaryosu (hatalı giriş, yanlış tür vs.)
    - En az bir saldırı senaryosu örneği ver
    4. Bu endpoint'te oluşabilecek potansiyel *mantıksal kötüye kullanım (business logic abuse case)* senaryolarını açıkla.
    5. Her OWASP açığı için geliştiricilere yönelik net çözüm önerileri ver:
      - Alınabilecek savunma önlemleri nelerdir?
    Lütfen çıktını açık, numaralandırılmış ve detaylı ver.
    """

    response = ollama.chat(
        model="llama3.2",
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response["message"]["content"]