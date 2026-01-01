import json
import subprocess
import sys
import os

def run_process():
    # Read RawTX.json
    # It contains lines of raw transaction hex strings
    # The format in RawTX.json seems to be one hex string per line?
    # Let's verify file content if possible, but snippet showed lines starting with 0100...
    
    input_file = "RawTX.json"
    output_file = "signatures.json"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    params = []
    with open(input_file, 'r') as f:
        # The file doesn't look like a valid JSON list based on the snippet (it had multiple objects or strings?)
        # Snippet:
        # 1: 0100000001f2...
        # 2: 010000000706...
        # It looks like raw lines.
        lines = f.readlines()
        params = [line.strip() for line in lines if line.strip()]

    # Clear output file or append? getsign.sh appended using >>
    # But it also deleted it? getsign.sh:
    # cat RawTX.json > index.json
    # ...
    # python2 breakECDSA.py ... >> signatures.json
    
    # We will overwrite initially to start fresh for this run
    if os.path.exists(output_file):
        os.remove(output_file)

    print(f"Processing {len(params)} transactions...")
    
    for tx_hex in params:
        print(f"Processing: {tx_hex[:30]}...")
        try:
            # Call breakECDSA.py
            result = subprocess.run([sys.executable, "breakECDSA.py", tx_hex], capture_output=True, text=True, check=True)
            
            # Append output to signatures.json
            with open(output_file, "a") as outfile:
                outfile.write(result.stdout)
                
        except subprocess.CalledProcessError as e:
            print(f"Error processing {tx_hex[:30]}: {e}")
            print(e.stderr)

    print(f"Done! Results saved to {output_file}")

if __name__ == "__main__":
    run_process()
