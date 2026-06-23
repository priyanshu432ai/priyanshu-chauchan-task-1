import csv
import json
import os
import random
from datetime import datetime, timedelta

products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "USB Hub"]
regions = ["North", "South", "East", "West"]

def make_data(n=20):
    sales = []
    start = datetime(2026, 1, 1)
    for i in range(1, n+1):
        qty = random.randint(1, 50)
        price = round(random.uniform(100.0, 150000.0), 2)
        sales.append({
            "id": i,
            "date": (start + timedelta(days=random.randint(0, 149))).strftime("%d-%m-%Y"),
            "product": random.choice(products),
            "region": random.choice(regions),
            "qty": qty,
            "price": price,
            "total": round(qty * price, 2)
        })
    return sales

def get_stats(sales):
    total_rev = sum(s["total"] for s in sales)
    total_units = sum(s["qty"] for s in sales)
    avg = round(total_rev / len(sales), 2)

    by_product = {}
    by_region = {}
    for s in sales:
        by_product[s["product"]] = by_product.get(s["product"], 0) + s["total"]
        by_region[s["region"]] = by_region.get(s["region"], 0) + s["total"]

    best_product = max(by_product, key=by_product.get)
    best_region = max(by_region, key=by_region.get)

    return {
        "total_rev": round(total_rev, 2),
        "total_units": total_units,
        "avg": avg,
        "by_product": by_product,
        "by_region": by_region,
        "best_product": best_product,
        "best_region": best_region
    }

def rs(amount):
    # just a helper to format rupees nicely like Rs. 1,20,000.00
    # doing indian number formatting manually
    s = f"{amount:.2f}"
    rupees, paise = s.split(".")
    rupees = int(rupees)
    if rupees >= 1000:
        last3 = str(rupees)[-3:]
        rest = str(rupees)[:-3]
        groups = []
        while len(rest) > 2:
            groups.append(rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.append(rest)
        groups.reverse()
        formatted = ",".join(groups) + "," + last3
    else:
        formatted = str(rupees)
    return "Rs. " + formatted + "." + paise

def save_txt_report(sales, stats, folder):
    fname = os.path.join(folder, "sales_report.txt")
    now = datetime.now().strftime("%d %B %Y, %I:%M %p")

    with open(fname, "w", encoding="utf-8") as f:

        f.write("\n")
        f.write("        SALES REPORT\n")
        f.write("        Generated on: " + now + "\n")
        f.write("\n")
        f.write("------------------------------------------------\n")
        f.write("\n")

        f.write("OVERALL SUMMARY\n")
        f.write("\n")
        f.write("  Total Sales Revenue  :  " + rs(stats['total_rev']) + "\n")
        f.write("  Total Units Sold     :  " + str(stats['total_units']) + " units\n")
        f.write("  Average Order Value  :  " + rs(stats['avg']) + "\n")
        f.write("  Top Selling Product  :  " + stats['best_product'] + "\n")
        f.write("  Best Performing Region:  " + stats['best_region'] + "\n")
        f.write("\n")
        f.write("------------------------------------------------\n")
        f.write("\n")

        f.write("SALES BY PRODUCT\n")
        f.write("\n")
        sorted_products = sorted(stats["by_product"].items(), key=lambda x: x[1], reverse=True)
        rank = 1
        for p, rev in sorted_products:
            f.write("  " + str(rank) + ". " + p + "  -->  " + rs(rev) + "\n")
            rank += 1
        f.write("\n")
        f.write("------------------------------------------------\n")
        f.write("\n")

        f.write("SALES BY REGION\n")
        f.write("\n")
        sorted_regions = sorted(stats["by_region"].items(), key=lambda x: x[1], reverse=True)
        for r, rev in sorted_regions:
            pct = round(rev / stats["total_rev"] * 100, 1)
            f.write("  " + r + " Region  -->  " + rs(rev) + "  (" + str(pct) + "%)\n")
        f.write("\n")
        f.write("------------------------------------------------\n")
        f.write("\n")

        f.write("TRANSACTION DETAILS\n")
        f.write("\n")
        for s in sales:
            f.write("  Order #" + str(s['id']) + "\n")
            f.write("    Date     : " + s['date'] + "\n")
            f.write("    Product  : " + s['product'] + "\n")
            f.write("    Region   : " + s['region'] + "\n")
            f.write("    Qty      : " + str(s['qty']) + " units\n")
            f.write("    Price    : " + rs(s['price']) + " per unit\n")
            f.write("    Total    : " + rs(s['total']) + "\n")
            f.write("\n")

        f.write("------------------------------------------------\n")
        f.write("              END OF REPORT\n")
        f.write("------------------------------------------------\n")

    return fname

def save_csv(sales, folder):
    fname = os.path.join(folder, "sales_data.csv")
    with open(fname, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "product", "region", "qty", "price", "total"])
        writer.writeheader()
        writer.writerows(sales)
    return fname

def save_summary_csv(stats, folder):
    fname = os.path.join(folder, "sales_summary.csv")
    with open(fname, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Value"])
        w.writerow(["Total Revenue", rs(stats['total_rev'])])
        w.writerow(["Total Units", stats["total_units"]])
        w.writerow(["Avg Order Value", rs(stats['avg'])])
        w.writerow(["Best Product", stats["best_product"]])
        w.writerow(["Best Region", stats["best_region"]])
        w.writerow([])
        w.writerow(["Product", "Revenue"])
        for p, rev in sorted(stats["by_product"].items(), key=lambda x: x[1], reverse=True):
            w.writerow([p, rs(rev)])
        w.writerow([])
        w.writerow(["Region", "Revenue"])
        for r, rev in sorted(stats["by_region"].items(), key=lambda x: x[1], reverse=True):
            w.writerow([r, rs(rev)])
    return fname

def save_json(sales, stats, folder):
    fname = os.path.join(folder, "sales_report.json")
    with open(fname, "w") as f:
        json.dump({"generated": datetime.now().isoformat(), "stats": stats, "data": sales}, f, indent=4)
    return fname

def main():
    folder = "reports"
    os.makedirs(folder, exist_ok=True)

    print("Generating sales data...")
    sales = make_data(20)

    print("Calculating stats...")
    stats = get_stats(sales)

    print("Saving reports...")
    txt = save_txt_report(sales, stats, folder)
    csv1 = save_csv(sales, folder)
    csv2 = save_summary_csv(stats, folder)
    js = save_json(sales, stats, folder)

    print("\nAll files saved successfully!")
    print("  -> " + txt)
    print("  -> " + csv1)
    print("  -> " + csv2)
    print("  -> " + js)

    print("\n--- Quick Summary ---")
    print("Total Revenue  : " + rs(stats['total_rev']))
    print("Total Units    : " + str(stats['total_units']))
    print("Best Product   : " + stats['best_product'])
    print("Best Region    : " + stats['best_region'])

main()
