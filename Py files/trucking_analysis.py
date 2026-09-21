import pandas as pd
url = r"C:\Users\savac\Downloads\trucking_sample_200_rows.xlsx"
def run_analysis(url):
    truck_df = pd.read_excel(url)
    print(truck_df.head(5))

    # DRIVER ANALYSIS
    drivers = truck_df["Driver Assigned"].unique()
    dh_avg = []
    cpm = []
    driver_revenue = []

    for driver in drivers:
        driver_data = truck_df[truck_df["Driver Assigned"] == driver]
        revenue = driver_data["Gross Revenue"].sum().astype(float)
        driver_revenue.append(round(revenue))

    deadhead_per_driver = truck_df.groupby("Driver Assigned")["Deadhead Miles"].mean()
    driver_cpm = truck_df.groupby("Driver Assigned")["Cost per Mile"].mean()

    for driver, avg_dh in deadhead_per_driver.items():
        dh_avg.append(round(avg_dh))
    for driver, cost in driver_cpm.items():
        cpm.append(round(cost, 2))

    driver_data = {
        "Avg DH": dh_avg,
        "Avg CPM": cpm,
        "Total Revenue": driver_revenue
    }
    dh_driver_analysis_df = pd.DataFrame(data=driver_data, index=drivers)
    dh_driver_analysis_df = dh_driver_analysis_df.sort_values(by="Total Revenue", ascending=False)

    # BROKER ANALYSIS
    loads = []
    avgs = []
    broker_rpm = []

    brokers = truck_df["Broker Name"].unique()
    loads_per_broker = truck_df.groupby("Broker Name")["Net Profit"].count()
    avg_profit_per_broker = truck_df.groupby("Broker Name")["Net Profit"].mean()
    rpm = truck_df.groupby("Broker Name")["Rate Per Mile"].mean()

    for broker, load_count in loads_per_broker.items():
        loads.append(load_count)
    for broker, avg in avg_profit_per_broker.items():
        avgs.append(round(avg))
    for broker, rate in rpm.items():
        broker_rpm.append(round(rate, 2))

    broker_data = {
        "Loads": loads,
        "Average Profit": avgs,
        "RPM": broker_rpm
    }
    broker_analysis_df = pd.DataFrame(data=broker_data, index=brokers)
    broker_analysis_df = broker_analysis_df.sort_values(by="Average Profit", ascending=False)

    # DISPATCHER ANALYSIS
    ppm = []
    rpm = []
    deadhead_percent = []

    dispatchers = truck_df["Dispatcher"].unique()
    for dispatcher in dispatchers:
        dispatcher_data = truck_df[truck_df["Dispatcher"] == dispatcher]
        total_profit = dispatcher_data["Net Profit"].sum()
        total_miles = dispatcher_data["Loaded Miles"].sum()
        total_deadhead = dispatcher_data["Deadhead Miles"].sum()
        ppm.append(round(total_profit / total_miles, 2))
        rpm.append(round(dispatcher_data["Rate Per Mile"].mean(), 2))
        deadhead_percent.append(round((total_deadhead / (total_deadhead + total_miles)) * 100, 2))

    dispatcher_data = {
        "Profit Per Mile": ppm,
        "Rate Per Mile": rpm,
        "Deadhead Percentage": deadhead_percent
    }
    dispatcher_analysis_df = pd.DataFrame(data=dispatcher_data, index=dispatchers)
    dispatcher_analysis_df = dispatcher_analysis_df.sort_values(by="Profit Per Mile", ascending=False)

    # OVERALL ANALYSIS
    prof_per_mile = round(truck_df["Net Profit"].sum() / truck_df["Loaded Miles"].sum(), 2)
    total_prof = round(truck_df["Net Profit"].sum())
    cost_per_mile = round(truck_df["Cost per Mile"].mean(), 2)
    revenue_per_week = round(truck_df["Gross Revenue"].sum() / 31 * 7)
    total_revenue = round(truck_df["Gross Revenue"].sum())

    overall_analysis = {
        "PPM": prof_per_mile,
        "Total Profit": total_prof,
        "Cost per Mile": cost_per_mile,
        "Revenue per Week": revenue_per_week,
        "Total Revenue": total_revenue
    }

    # Convert DataFrames to lists of dicts for JSON serialization & templating
    return {
        "overall": overall_analysis,
        "drivers": dh_driver_analysis_df.reset_index().rename(columns={"index": "Driver Assigned"}).to_dict(orient="records"),
        "brokers": broker_analysis_df.reset_index().rename(columns={"index": "Broker Name"}).to_dict(orient="records"),
        "dispatchers": dispatcher_analysis_df.reset_index().rename(columns={"index": "Dispatcher"}).to_dict(orient="records")
    }

# If you want to test run this file directly
if __name__ == "__main__":
    results = run_analysis(r"C:\Users\savac\Downloads\trucking_sample_200_rows.xlsx")
    print("Overall:", results["overall"])
    print("Drivers sample:", results["drivers"][:2])
    print("Brokers sample:", results["brokers"][:2])
    print("Dispatchers sample:", results["dispatchers"][:2])
