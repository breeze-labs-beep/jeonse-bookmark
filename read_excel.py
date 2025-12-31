
import openpyxl
import json

try:
    wb = openpyxl.load_workbook('links_metadata_classified.xlsx')
    sheet = wb.active
    
    data = []
    headers = [cell.value for cell in sheet[1]]
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = {}
        has_data = False
        for i, value in enumerate(row):
            if i < len(headers):
                # Map Korean headers or keep original? 
                # Let's keep original keys but also add English aliases if useful.
                # Actually, let's just dump it as is, but maybe map specific fields for the frontend.
                key = headers[i]
                row_data[key] = value
                if value:
                    has_data = True
        
        if has_data:
            # Create a clean record for the app
            record = {
                "url": row_data.get("final_url") or row_data.get("original_url"),
                "title": row_data.get("title"),
                "category": row_data.get("분류"),
                "domain": row_data.get("domain"),
                "original_data": row_data
            }
            data.append(record)
            
    with open('metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully saved {len(data)} items to metadata.json")

except Exception as e:
    print(f"Error reading excel: {e}")
