import pandas as pd

def generate_pricing_table():
    # 1. Cases for decision table
    # Conditions: Hour
    # Actions: Expected Rate
    
    data = {
        "Rule ID": ["DT-01", "DT-02", "DT-03", "DT-04"],
        "Description": [
            "Early Morning Discount", 
            "Standard Hours", 
            "Peak Evening Hours", 
            "Late Night (Invalid?)"
        ],
        "Condition: Hour (Input)": [8, 14, 19, 25],
        "Action: Multiplier": [0.8, 1.0, 1.5, "Error"],
        "Action: Expected Result": ["Discounted Price", "Base Price", "Increased Price", "ValueError"]
    }

    # Dataframe
    df = pd.DataFrame(data)

    # Output Types
    print("\n--- TERMİNAL Output ---")
    print(df.to_string(index=False))

    print("\n\n--- MARKDOWN Output ---")
    print(df.to_markdown(index=False))

    print("\n\n--- HTML Output ---")
    print(df.to_html(index=False))
    
    return df

if __name__ == "__main__":
    generate_pricing_table()