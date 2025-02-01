import requests
import json
import torch
import matplotlib.pyplot as plt
from policy_network import MultiAgentPolicy
from multi_agent_env import MultiAgentEnvironment


BASE_URL = "http://127.0.0.1:8080" #自己部署环境IP 和端口自定义

def create_masfd_env(num_agents, num_transactions, fraud_ratio, fraud_type):
    """
    创建多智能体欺诈检测环境。
    Args:
        num_agents: 智能体数量
        num_transactions: 交易数量
        fraud_ratio: 欺诈交易比例
        fraud_type: 欺诈类型
    Returns:
        服务器返回的环境创建结果
    """
    url = f"{BASE_URL}/createMASFDEnv"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "numAgents": num_agents,
        "numTransactions": num_transactions,
        "fraudRatio": fraud_ratio,
        "fraudType": fraud_type
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
        # 确保返回 JSON 格式
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"error": "Invalid response from server"}

def get_state():
    """
    获取当前环境的状态。
    Returns:
        当前环境状态的JSON表示
    """
    url = f"{BASE_URL}/getState"
    response = requests.get(url)
    # 假设响应是JSON数组，将其转换为Python列表
        # 确保返回 JSON 格式
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"error": "Invalid response from server"}

def step(actions):
    """
    执行给定的动作并获取环境的反馈。
    Args:
        actions: 一个字典，其中键是 transactionId，值是一个包含 'flag' 的字典。
    Returns:
        执行动作后的环境反馈（JSON格式）
    """
    url = f"{BASE_URL}/step"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(actions))
    try:
        result = response.json()
        state = result.get("state", [])  # 确保状态是数组
        step_rewards = result.get("rewards", [0, 0])  # 预防空值
        done = result.get("done", False)  # 预防空值
        return state, step_rewards, done
    except json.JSONDecodeError:
        return [], [0, 0], False

def reset():
    """
    重置环境到初始状态。
    Returns:
        重置操作的结果
    """
    url = f"{BASE_URL}/reset"
    response = requests.get(url)
    try:
        response.json()  # 确保服务器成功重置
    except json.JSONDecodeError:
        return {"error": "Invalid reset response"}

def train_masfd(env, num_episodes=1000, gamma=0.99, lr=0.001):
    """
    MASFD 训练循环。
    Args:
        env: 多智能体环境实例
        num_episodes: 训练的回合数
        gamma: 折扣因子
        lr: 学习率
    """
    # 初始化策略管理器
    policy_manager = MultiAgentPolicy(
        feature_dim=env.feature_dim,
        num_nodes=env.num_nodes,
        hidden_dim=128,
        lr=lr
    )

    # 存储训练结果
    rewards_history = []

    for episode in range(num_episodes):
        # 重置环境
        state = env.reset()
        done = False
        episode_rewards = []

        # 记录每一步的状态、动作和奖励
        fraudster_log_probs = []
        detector_log_probs = []
        rewards = []

        while not done:
            # Fraudster 生成动作（选择目标节点）
            fraudster_action, fraudster_log_prob = policy_manager.get_action(
                policy_manager.fraudster_policy, state)
            fraudster_log_probs.append(fraudster_log_prob)

            # Detector 生成动作（选择检测节点）
            detector_action, detector_log_prob = policy_manager.get_action(
                policy_manager.detector_policy, state)
            detector_log_probs.append(detector_log_prob)

            # 构造智能体的动作
            actions = [
                {"type": "fraudster", "target": fraudster_action.item(), "amount": torch.rand(1).item()},
                {"type": "detector", "node": detector_action.item()},
            ]

            # 执行动作，获取新状态和奖励
            state, step_rewards, done = env.step(actions)
            rewards.append(step_rewards)
            episode_rewards.append(sum(step_rewards))

        # 计算每个智能体的折扣奖励
        fraudster_rewards = [r[0] for r in rewards]
        detector_rewards = [r[1] for r in rewards]

        # 更新 Fraudster 策略
        policy_manager.update_policy(
            policy_manager.fraudster_optimizer,
            fraudster_log_probs,
            fraudster_rewards,
            gamma
        )

        # 更新 Detector 策略
        policy_manager.update_policy(
            policy_manager.detector_optimizer,
            detector_log_probs,
            detector_rewards,
            gamma
        )

        # 记录当前回合的总奖励
        total_rewards = sum(episode_rewards)
        rewards_history.append(total_rewards)

        # 输出训练日志
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_rewards:.2f}")

    return rewards_history

# 主函数
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

    # 初始化环境并启动训练
    num_nodes = 10
    num_edges = 20
    feature_dim = 5
    num_agents = 4
    max_steps = 50

    # 初始化多智能体环境
    env = MultiAgentEnvironment(
        num_nodes=num_nodes,
        num_edges=num_edges,
        feature_dim=feature_dim,
        num_agents=num_agents,
        max_steps=max_steps
    )

    # 启动训练
    print("开始训练 MASFD 系统...")
    rewards_history = train_masfd(env, num_episodes=500)

    # 可视化训练奖励
    plt.plot(rewards_history)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("Training Performance")
    plt.show()
