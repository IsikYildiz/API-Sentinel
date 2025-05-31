from swagger_parser import load_swagger_file, extract_endpoints, get_base_url
from report_writer import write_markdown_report

def main():
    swagger_file = "C:\\Users\\ACER\\Desktop\\api-example-swagger-v1.4.json"  
    output_file = "output/final_report.md"

    swagger = load_swagger_file(swagger_file)
    if not swagger:
        print("Swagger dosyası okunamadı.")
        return

    endpoints = extract_endpoints(swagger)
    base_url = get_base_url(swagger)

    print(f"🔍 {len(endpoints)} endpoint bulundu. Rapor hazırlanıyor...")
    write_markdown_report(endpoints, base_url, output_file)

if __name__ == "__main__":
    main()