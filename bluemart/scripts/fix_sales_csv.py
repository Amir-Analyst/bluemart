"""
Fix duplicate headers in sales CSV file
"""
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def fix_sales_csv():
    print("Fixing duplicate headers in sales CSV...")
    
    input_file = str(config.FILE_SALES)
    temp_file = input_file + ".tmp"
    
    header_line = "date,store_id,sku_id,customer_id,quantity,unit_price,total_value,channel,discount_pct,transaction_id"
    
    with open(input_file, 'r') as infile, open(temp_file, 'w') as outfile:
        # Write header once
        outfile.write(header_line + '\n')
        
        # Skip first line (original header)
        next(infile)
        
        lines_written = 0
        for line in infile:
            # Skip any duplicate headers
            if line.strip() == header_line:
                print(f"   Skipped duplicate header at line {lines_written + 2}")
                continue
            outfile.write(line)
            lines_written += 1
            
            if lines_written % 1000000 == 0:
                print(f"   Processed {lines_written:,} lines...")
    
    # Replace original with fixed file
    import shutil
    shutil.move(temp_file, input_file)
    
    print(f"Fixed! Total data lines: {lines_written:,}")

if __name__ == "__main__":
    fix_sales_csv()
