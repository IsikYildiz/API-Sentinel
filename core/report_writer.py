from llm import prompt_attack_cases, split_llm_output
from curl_generator import generate_curl_command

def write_markdown_report(endpoints, base_url, output_file="output/analysis_report.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# API Güvenlik Analiz Raporu\n\n")

        for endpoint in endpoints:
            method = endpoint["method"]
            path = endpoint["path"]
            summary = endpoint.get("summary", "-")
            parameters = endpoint.get("parameters", [])

            f.write(f"## 🔹 {method} {path}\n")
            f.write(f"**Açıklama:** {summary}\n\n")

            f.write("### Parametreler\n")
            if parameters:
                for p in parameters:
                    f.write(f"- `{p['name']}` ({p['in']}), type: `{p['type']}`, required: `{p['required']}`\n")
            else:
                f.write("- Parametre bulunamadı\n")
            f.write("\n")

            # curl_generator çıktısı
            curl_cmd = generate_curl_command(base_url, endpoint)
            f.write("### Curl Komutu:\n")
            f.write("```bash\n")
            f.write(curl_cmd + "\n")
            f.write("```\n\n")

            # LLM Test & Abuse Case Çıktısı
            llm_output = prompt_attack_cases(endpoint)
            sections = split_llm_output(llm_output)

            for title, content in sections.items():
                if "Curl" in title:  
                    continue
                f.write(f"### {title}\n")
                f.write(content.strip() + "\n\n")

            f.write("---\n\n")

    print(f"Rapor yazıldı: {output_file}")