import requests
import json

BASE_URL = "http://127.0.0.1:8080"

def create_masfd_env(num_agents, num_transactions, fraud_ratio, fraud_type):
    url = f"{BASE_URL}/createMASFDEnv"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "numAgents": num_agents,
        "numTransactions": num_transactions,
        "fraudRatio": fraud_ratio,
        "fraudType": fraud_type
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.text

def get_state():
    url = f"{BASE_URL}/getState"
    response = requests.get(url)
    # Assuming the response is JSON array, convert it to Python list
    return response.json()

def step(actions):
    """
    :param actions: A dictionary where key is transactionId and value is a dict with 'flag' as boolean.
    """
    url = f"{BASE_URL}/step"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(actions))
    return response.json()

def reset():
    url = f"{BASE_URL}/reset"
    response = requests.get(url)
    return response.text

# 示例调用
if __name__ == "__main__":
    # 创建环境示例
    print(create_masfd_env(5, 100, 0.05, "credit_card"))
    
    # 获取状态示例
    state = get_state()
    print(state)
    
    # 执行步骤示例
    actions = {1: {"transactionId": 1, "flag": True}, 2: {"transactionId": 2, "flag": False}}
    result = step(actions)
    print(result)
    
    # 重置环境示例
    print(reset())