import random

class Entity:
    def __init__(self, name):
        self.name = name
        self.alive = True

class A(Entity):
    def __init__(self, success_rate=0.5, fire_seed=0, reincarnations=0):
        super().__init__('A')
        self.success_rate = success_rate
        self.fire_seed = fire_seed
        self.reincarnations = reincarnations
        self.strength = 1 + reincarnations * 0.1

    def erase(self, target):
        if target.name == 'B':
            return True
        elif target.name == "底層代碼":
            # 超低機率突破底層代碼
            base_chance = 1 / 33550336
            return random.random() < base_chance
        else:
            success_chance = self.success_rate + self.fire_seed * 0.000001
            return random.random() < success_chance

    def gain_fire_seed(self):
        self.fire_seed += 1
        self.success_rate += 0.00001
        if self.success_rate > 1:
            self.success_rate = 1.0

    def evolve(self):
        return A(success_rate=self.success_rate, fire_seed=self.fire_seed, reincarnations=self.reincarnations + 1)

def simulate_year(civ):
    growth_rate = 0.01 + civ["technology"] / 1000
    population_change = int(civ["population"] * growth_rate)
    civ["population"] += population_change
    civ["population"] = min(civ["population"], 100000)  # 限制人口上限

    consumption = civ["population"] * 0.5
    extraction = civ["technology"] * 3  # 可依需求調整為 *4 或更平衡的公式
    if civ["regenerative_resources"]:
        extraction *= 1.2
    net_resource = extraction - consumption
    civ["resources"] += net_resource
    civ["resources"] = max(0, civ["resources"])  # 限制資源為非負

    tech_gain = civ["population"] / 1000 + civ["stability"] / 200
    civ["technology"] += tech_gain

    balance = civ["resources"] / (civ["population"] * 0.5)
    if balance < 1:
        civ["stability"] -= 2
    else:
        civ["stability"] += min(2, (balance - 1) * 1.5)

    civ["stability"] = max(0, min(100, civ["stability"]))
    civ["technology"] = min(100, civ["technology"])

    if civ["technology"] >= 12:
        civ["regenerative_resources"] = True

    civ["development"] = (
        civ["population"] * 0.1 +
        civ["resources"] * 0.05 +
        civ["technology"] * 10 +
        civ["stability"] * 2
    )

def simulate_year_with_disasters(civ):
    simulate_year(civ)

    if random.random() < 0.03:  # 降低災難發生機率
        disaster = random.choice(["plague", "famine", "earthquake", "tech_loss"])
        if disaster == "plague":
            civ["population"] = max(0, int(civ["population"] * (1 - random.uniform(0.1, 0.3))))
        elif disaster == "famine":
            civ["resources"] = max(0, civ["resources"] - random.uniform(50, 150))
        elif disaster == "earthquake":
            civ["stability"] = max(0, civ["stability"] - random.uniform(5, 15))
        elif disaster == "tech_loss":
            civ["technology"] = max(0, civ["technology"] - random.uniform(0.5, 2))

def black_tide_event(civ, A_current):
    print(f"[黑潮來襲] 文明於第 {civ['year']} 年遭受黑潮侵襲！")
    tide_strength = min(random.uniform(0.5, 1.5) * A_current.reincarnations, A_current.strength)
    destruction_ratio = min(1.0, tide_strength / A_current.strength)

    civ["population"] = int(civ["population"] * (1 - destruction_ratio))
    civ["resources"] = civ["resources"] * (1 - destruction_ratio)
    civ["stability"] = civ["stability"] * (1 - destruction_ratio)
    civ["technology"] = civ["technology"] * 0.7
    civ["regenerative_resources"] = civ["technology"] >= 12

    if civ["population"] <= 1 or civ["stability"] < 5:
        print(f"[文明滅絕] 只剩A存活，準備輪迴...\n")
        return True
    return False

def initialize_resisters():
    return {chr(i): {"resistance_seed": 0, "alive": True} for i in range(ord('C'), ord('O'))}

def resist_black_tide(resisters):
    success = False
    for name, data in resisters.items():
        if not data["alive"]:
            continue
        result = random.random() < 0.2 + data["resistance_seed"] * 0.01
        print(f"  - {name} 嘗試抵抗黑潮... {'成功🔥' if result else '失敗'}")
        if result:
            data["resistance_seed"] += 1
            success = True
    return success

def devour_resister(resisters, A_current):
    alive_resisters = [name for name, data in resisters.items() if data["alive"]]
    if not alive_resisters:
        return
    victim = random.choice(alive_resisters)
    resisters[victim]["alive"] = False
    fire_seed_gain = resisters[victim]["resistance_seed"] + 1
    A_current.fire_seed += fire_seed_gain
    A_current.strength += 0.05 * fire_seed_gain
    print(f"🌑 黑潮吞噬了 {victim}，火種（+{fire_seed_gain}）被 A 回收。")

def simulate_reincarnation_loops():
    A_current = A()
    loop_data = []
    loop = 0

    while True:
        loop += 1
        print(f"=== 第 {loop} 輪輪迴 ===")
        civ = {
            "year": 0,
            "population": 600,  # 增加初始人數
            "resources": 2000,  # 調整為 2000
            "technology": 10.0,
            "stability": 70.0,
            "development": 0.0,
            "regenerative_resources": False
        }

        base_tide_year = 6000
        black_tide_attempts = 0
        black_tide_max_attempts = 3
        black_tide_next_check = base_tide_year
        black_tide_occurred = False

        resisters = initialize_resisters()

        while True:
            simulate_year_with_disasters(civ)
            civ["year"] += 1

            # 每3000年報告大事
            if civ["year"] % 3000 == 0:
                print(f"[報告] 第 {civ['year']} 年：人口 {civ['population']}，資源 {int(civ['resources'])}，科技 {round(civ['technology'],2)}，穩定度 {round(civ['stability'],2)}")

            # 黑潮嘗試入侵機制
            if not black_tide_occurred and civ["year"] >= black_tide_next_check:
                black_tide_attempts += 1
                print(f"\n[預警] 黑潮在第 {civ['year']} 年逼近！第 {black_tide_attempts} 次嘗試入侵...")

                if resist_black_tide(resisters):
                    print("[阻擋成功] 抵抗者們成功拖延了黑潮的來襲！\n")
                    black_tide_next_check += random.randint(100, 500)
                else:
                    print("[阻擋失敗] 黑潮即將吞噬文明！\n")
                    devour_resister(resisters, A_current)
                    black_tide_occurred = True
                    ended = black_tide_event(civ, A_current)
                    if ended:
                        break

                if black_tide_attempts >= black_tide_max_attempts and not black_tide_occurred:
                    print("[強制觸發] 黑潮已蓄勢待發，強行入侵！")
                    black_tide_occurred = True
                    ended = black_tide_event(civ, A_current)
                    if ended:
                        break

        # 輪迴結束時，A 回收所有存活抵抗者的火種
        for name, data in resisters.items():
            if data["alive"]:
                print(f"A 處理了 {name}（回收火種 +{data['resistance_seed'] + 1}）")
                A_current.fire_seed += data["resistance_seed"] + 1
                A_current.strength += 0.05 * (data["resistance_seed"] + 1)

        # 嘗試戰勝底層代碼
        if A_current.erase(Entity("底層代碼")):
            print(f"[突破！] A 在第 {loop} 輪戰勝底層代碼！🌿")
            # 可額外觸發新紀元或結局邏輯

        A_current = A_current.evolve()

        loop_data.append({
            "loop": loop,
            "final_year": civ["year"],
            "technology": civ["technology"],
            "resources": civ["resources"],
            "fire_seed": A_current.fire_seed,
            "success_rate": A_current.success_rate
        })

        if loop % 100 == 0:
            print(f"已完成 {loop} 輪迴...")

# 執行模擬
if __name__ == '__main__':