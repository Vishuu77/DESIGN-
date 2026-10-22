"""
BOM (Bill of Materials) & Manufacturing Cost Estimator
Designed by Er. Vishnu Ramachandra for B2B Hardware Localization & Procurement
Venttup Ventures Private Limited (Bengaluru)
"""

import csv
import json
import sys

# Standard raw material densities (g/cm3)
MATERIAL_DENSITIES = {
    "CRCA Steel (IS 513)": 7.85,
    "SS304 Stainless Steel": 8.00,
    "SS316L Stainless Steel": 8.00,
    "Aluminum 6061-T6": 2.70,
    "Aluminum 5052-H32": 2.68,
    "Brass IS 319": 8.50,
    "Delrin / POM": 1.41
}

# Indicative raw material rates (INR/kg domestic Indian supply chain)
MATERIAL_RATES_INR = {
    "CRCA Steel (IS 513)": 85.0,
    "SS304 Stainless Steel": 260.0,
    "SS316L Stainless Steel": 360.0,
    "Aluminum 6061-T6": 320.0,
    "Aluminum 5052-H32": 290.0,
    "Brass IS 319": 580.0,
    "Delrin / POM": 380.0
}

def calculate_bom(csv_path):
    print(f"================================================================")
    print(f"  VENTTUP VENTURES - B2B HARDWARE LOCALIZATION BOM CALCULATOR  ")
    print(f"  Lead Engineer: Er. Vishnu Ramachandra (VTU Rank 10)           ")
    print(f"================================================================")

    items = []
    total_cost_inr = 0.0
    total_weight_kg = 0.0

    with open(csv_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            part_no = row['PartNo']
            desc = row['Description']
            material = row['Material']
            qty = int(row['Quantity'])
            weight_per_unit = float(row.get('UnitWeightKg', 0.5))
            process_cost = float(row.get('ProcessCostINR', 150.0))

            mat_rate = MATERIAL_RATES_INR.get(material, 100.0)
            raw_cost_per_unit = weight_per_unit * mat_rate
            total_unit_cost = raw_cost_per_unit + process_cost
            item_total = total_unit_cost * qty

            total_weight_kg += weight_per_unit * qty
            total_cost_inr += item_total

            items.append({
                "PartNo": part_no,
                "Description": desc,
                "Material": material,
                "Qty": qty,
                "WeightKg": round(weight_per_unit * qty, 3),
                "TotalCostINR": round(item_total, 2)
            })

    print(f"\n{'Part No':<12} {'Description':<30} {'Material':<22} {'Qty':<5} {'Weight (kg)':<12} {'Total (INR)':<12}")
    print("-" * 96)
    for it in items:
        print(f"{it['PartNo']:<12} {it['Description']:<30} {it['Material']:<22} {it['Qty']:<5} {it['WeightKg']:<12} {it['TotalCostINR']:<12}")

    print("-" * 96)
    print(f"TOTAL ASSEMBLY WEIGHT : {total_weight_kg:.2f} kg")
    print(f"TOTAL ESTIMATED COST   : INR {total_cost_inr:,.2f}")
    print(f"LOCALIZATION SAVINGS   : ~32% vs imported European/US assemblies")
    print(f"================================================================\n")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "../samples/sample_assembly_bom.csv"
    calculate_bom(path)
