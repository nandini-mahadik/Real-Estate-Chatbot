def mock_summary(area, df_area):
    """
    Creates a simple natural-language summary without using an LLM.
    """
    if df_area is None or df_area.empty:
        return f"No data found for {area}."

    try:
        avg_price = df_area["Price"].mean()
        avg_demand = df_area["Demand"].mean()
    except Exception:
        avg_price = None
        avg_demand = None

    summary = [f"Real estate analysis for {area}:"]

    if avg_price is not None:
        summary.append(f"Average price is {avg_price:.2f}.")
    if avg_demand is not None:
        summary.append(f"Average demand is {avg_demand:.2f}.")

    # Simple trend detection
    if "Year" in df_area.columns and "Price" in df_area.columns:
        yearly = df_area.groupby("Year")["Price"].mean().sort_index()
        if len(yearly) >= 2:
            first = yearly.iloc[0]
            last = yearly.iloc[-1]

            if last > first:
                summary.append("Prices show an upward trend.")
            elif last < first:
                summary.append("Prices show a downward trend.")
            else:
                summary.append("Prices have remained stable.")

    return " ".join(summary)
