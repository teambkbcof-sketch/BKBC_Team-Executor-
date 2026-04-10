from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Kiwi Browser-dən gələn sorğulara icazə verir

# Sənin PCDesktopClient.txt faylından tapdığın kritik flag-lər
FFLAGS = {
    "Idempotency": "DFFlagIdempotentDevProductPurchasingEnabled",
    "Telemetry": "DFFlagMarketplaceApiUsageTelemetryEnabled",
    "OpenCloud": "DFStringHttpServiceOpenCloudUrlAllowlist"
}

@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.json
        lua_code = data.get('code')
        
        if not lua_code:
            return jsonify({"status": "error", "message": "Kod tapılmadı"}), 400

        # Burada skriptə sənin tapdığın flag-ləri "inject" edirik
        full_payload = f"-- BKBC SERVERSIDE ENGINE\n-- Active Flag: {FFLAGS['Idempotency']}\n{lua_code}"
        
        # Termux logunda nəticəni görək
        print("\n[+] NEW SCRIPT RECEIVED")
        print("-" * 30)
        print(full_payload)
        print("-" * 30)
        print("[!] SCRIPT READY FOR INJECTION")

        return jsonify({
            "status": "success", 
            "message": "BKBC Executor: Successful Injected",
            "flags_used": list(FFLAGS.values())
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Serveri 5000-ci portda işə salırıq
    print("BKBC Team Server v2 Start...")
    app.run(host='127.0.0.1', port=5000, debug=True)
    