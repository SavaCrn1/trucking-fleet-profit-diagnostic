from jinja2 import Environment, FileSystemLoader
from trucking_analysis import run_analysis

def main():
    # 1. Run your trucking data analysis
    data = run_analysis(r"C:\Users\savac\Downloads\trucking_sample_200_rows.xlsx")

    # 2. Setup Jinja environment to look inside your "templates" folder
    env = Environment(loader=FileSystemLoader("../templates"))

    # 3. Load your diagnostic report HTML template
    template = env.get_template("diagnostic.html")

    # 4. Prepare context dict with real analysis results for template rendering
    context = {
        "client_name": "ABC Trucking LLC",
        "period": "Last 30 Days",
        "ppm": data["overall"]["PPM"],
        "cpm": data["overall"]["Cost per Mile"],
        "total_profit": data["overall"]["Total Profit"],
        "revenue_per_week": data["overall"]["Revenue per Week"],
        "total_revenue": data["overall"]["Total Revenue"],
        "brokers": data["brokers"],
        "drivers": data["drivers"],
        "dispatchers": data["dispatchers"]
    }

    # 5. Render the template with your data
    html = template.render(context)

    # 6. Save the rendered HTML report to a file
    with open("../Output/diagnostic_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Report generated successfully!")

if __name__ == "__main__":
    main()
