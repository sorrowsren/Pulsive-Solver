from flask import Flask, request, jsonify
import json
from solver.funCaptchaChallenge import funCaptchaChallenge
from time import time
import asyncio
import string
import secrets

app = Flask(__name__)

deduction_amount = 0.0009

with open('data/keys.json', 'r') as f:
    keys_data = json.load(f)

def save_keys():
    with open('data/keys.json', 'w') as f:
        json.dump(keys_data, f, indent=4)

@app.route('/check_balance', methods=['POST'])
async def check_balance():
    json_data = request.get_json()

    if 'key' in json_data:
        for key_obj in keys_data:
            if key_obj["key"] == json_data["key"]:
                return jsonify({"balance": f"${key_obj['balance']}"})
        return jsonify({"response": "Invalid key."})
    else:
        return jsonify({"response": "Invalid key."})

@app.route('/solve', methods=['POST'])
async def solve():
    json_data = request.get_json()

    if 'key' in json_data:
        for key_obj in keys_data:
            if key_obj["key"] == json_data["key"]:
                if key_obj["balance"] > 0:
                    key_obj["balance"] -= deduction_amount
                    save_keys()
                    try:
                        key = json_data["key"]
                        challenge_info = json_data["challengeInfo"]
                        browser_info = json_data["browserInfo"]
                        proxy = json_data["proxy"]
                    except:
                        return jsonify({"success": False, "reason": "You haven't entered the required parameters"})
                    
                    challenge_info_keys = [
                        "publicKey", "site", "surl", "capiMode", "styleTheme",
                        "languageEnabled", "jsfEnabled", "ancestorOrigins", "treeIndex",
                        "treeStructure", "locationHref"
                    ]

                    browser_info_keys = [
                        "User-Agent", "Sec-Ch-Ua"
                    ]

                    challenge_info_keys_exist = all(key in challenge_info for key in challenge_info_keys)
                    browser_info_keys_exist = all(key in browser_info for key in browser_info_keys)

                    if not challenge_info_keys_exist:
                        return jsonify({"success": False, "reason": "You haven't entered the required challengeInfo parameters"})
                    
                    if not browser_info_keys_exist:
                        return jsonify({"success": False, "reason": "You haven't entered the required browserInfo parameters"})
                    
                    try:
                        solver = funCaptchaChallenge(challenge_info, browser_info, proxy)

                        start_time = time()
                        solution = solver.solve()["solution"]
                        end_time = round(time() - start_time, 2)

                        if "sup=1" in solution:
                            return jsonify({"success": True, "solution": solution, "gameInfo": {"variant": "silent_pass", "waves": 0, "gameType": 4, "solveTime": end_time}})
                        else:
                            interactor = solver.interactor
                            variant, waves, gameType = interactor.variant, interactor.waves, interactor.gameType

                            if solution == "Failed to solve the captcha.":
                                key_obj["balance"] += deduction_amount
                                save_keys()
                                return jsonify({"success": False, "reason": "Failed to solve the captcha, your balance has been refunded."})
                            else:
                                return jsonify({"success": True, "solution": solution, "gameInfo": {"variant": variant, "waves": waves, "gameType": gameType, "solveTime": end_time}})
                    
                    except ValueError as e:
                        return jsonify({"success": False, "reason": str(e)})
                    
                    except Exception:
                        return jsonify({"success": False, "reason": "Proxy failed to make request"})
                else:
                    return jsonify({"response": "Your balance has run out, please charge more to continue using."})
        return jsonify({"response": "Invalid key."})
    else:
        return jsonify({"response": "Invalid key."})

@app.route('/admin', methods=['POST'])
async def admin():
    json_data = request.get_json()

    if 'admin_key' in json_data and 'action' in json_data and json_data['admin_key'] == 'Pulsive@123':
        action = json_data['action']
        key = json_data.get('key')
        balance = json_data.get('balance')

        if action == 'gen_key' and balance is not None:
            def generate_secure_string(length=32):
                alphabet = string.ascii_uppercase + string.digits
                return ''.join(secrets.choice(alphabet) for _ in range(length))
            
            key = "PULSIVE-" + generate_secure_string()

            keys_data.append({"key": key, "balance": balance})
            save_keys()
            return jsonify({"response": "Key generated successfully.", "key": key})
        
        elif action == 'add_key' and key and balance is not None:
            keys_data.append({"key": key, "balance": balance})
            save_keys()
            return jsonify({"response": "Key added successfully.", "key": key})
        
        elif action == 'remove_key' and key:
            for key_obj in keys_data:
                if key_obj["key"] == key:
                    keys_data.remove(key_obj)
                    save_keys()
                    return jsonify({"response": "Key removed successfully."})
            return jsonify({"response": "Key not found."})
        
        elif action == 'set_balance' and key and balance is not None:
            for key_obj in keys_data:
                if key_obj["key"] == key:
                    key_obj["balance"] = balance
                    save_keys()
                    return jsonify({"response": "Balance set successfully."})
            return jsonify({"response": "Key not found."})

        elif action == 'increase_balance' and key and balance is not None:
            for key_obj in keys_data:
                if key_obj["key"] == key:
                    key_obj["balance"] += balance
                    save_keys()
                    return jsonify({"response": "Balance increased successfully."})
            return jsonify({"response": "Key not found."})

        elif action == 'decrease_balance' and key and balance is not None:
            for key_obj in keys_data:
                if key_obj["key"] == key:
                    if key_obj["balance"] >= balance:
                        key_obj["balance"] -= balance
                        save_keys()
                        return jsonify({"response": "Balance decreased successfully."})
                    else:
                        return jsonify({"response": "Insufficient balance to decrease."})
            return jsonify({"response": "Key not found."})

        return jsonify({"response": "Invalid action or parameters."})
    
    return jsonify({"response": "Invalid admin key or missing parameters."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)