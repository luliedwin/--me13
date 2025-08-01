import random

class Entity:
    def __init__(self, name):
        self.name = name
        self.alive = True

class A(Entity):
    def __init__(self, success_rate=0.000001, fire_seed=0, reincarnations=0):
        super().__init__('A')
        self.success_rate = success_rate
        self.fire_seed = fire_seed
        self.reincarnations = reincarnations
        self.strength = 1 + reincarnations * 0.1

    def erase(self, target):
        if target.name == 'B':
            return True
        elif target.name == "底層代碼":
            epsilon = 1 / 33550336
            strength_bonus = min(epsilon * 0.95, self.fire_seed * 1e-12)
            return random.random() < strength_bonus
        else:
            success_chance = self.success_rate + self.fire_seed * 0.000001
            return random.random() < success_chance

    def gain_fire_seed(self):
        self.fire_seed += 1
        self.success_rate += 0.00001 / (1 + self.fire_seed / 10000)
        if self.success_rate > 1:
            self.success_rate = 1.0

    def evolve(self):
        self.reincarnations += 1
        max_strength = 1.0000001 * self.reincarnations + 0.999999
        self.strength = min(max_strength, self.strength + 0.05)
        return A(
            success_rate=self.success_rate,
            fire_seed=self.fire_seed,
            reincarnations=self.reincarnations
        ).with_strength(self.strength)

    def with_strength(self, strength_value):
        self.strength = strength_value
        return self

def initialize_resisters_with_powers():
    resisters = {}
    for i in range(ord('C'), ord('N') + 1):
        name = chr(i)
        powers = {f"異能_{j+1}": random.randint(50, 100) for j in range(13)}
        resisters[name] = {
            "resistance_seed": 0,
            "alive": True,
            "powers": powers,
            "demigod": False
        }
    name = 'N+a'
    powers = {f"異能_{j+1}": random.randint(50, 100) for j in range(13)}
    resisters[name] = {
        "resistance_seed": 0,
        "alive": True,
        "powers": powers,
        "demigod": False
    }
    return resisters

def select_golden_lineage(resisters, top_n=13):
    scored = []
    for name, data in resisters.items():
        if not data["alive"]:
            continue
        total_power = sum(data["powers"].values())
        scored.append((total_power, name))
    scored.sort(reverse=True)
    golden_lineage = [name for _, name in scored[:top_n]]
    print(f"\n🌟 黃金裔誕生：{'、'.join(golden_lineage)}")
    return golden_lineage

def enforce_demigod_fire_transfer(resisters, golden_lineage, A_current, threshold=900):
    for name in golden_lineage:
        data = resisters[name]
        if not data["alive"]:
            continue
        total_power = sum(data["powers"].values())
        if total_power >= threshold and not data.get("demigod", False):
            data["demigod"] = True
            fire = data["resistance_seed"] + 1
            A_current.fire_seed += fire
            A_current.strength += 0.05 * fire
            # 不顯示誰成為半神

def simulate_extreme_reincarnation():
    A_current = A()
    loop = 0
    while True:
        loop += 1
        print(f"=== 第 {loop} 輪輪迴 ===")
        resisters = initialize_resisters_with_powers()

        for name in resisters:
            A_current.gain_fire_seed()

        golden_lineage = select_golden_lineage(resisters)
        enforce_demigod_fire_transfer(resisters, golden_lineage, A_current)

        if loop == 33550336:
            print("\n[神秘協助] Aa、Bb、Cc 降臨，協助 A 對抗底層代碼（成功率 +60%）")
            A_current.success_rate = min(1.0, A_current.success_rate + 0.6)

        elif loop == 33550337:
            print("\n[終局輪迴] 這是第 33550337 輪，A 將進行最後一次嘗試突破底層代碼...")
            if A_current.erase(Entity("底層代碼")):
                print("[終極突破] A 終於戰勝了底層代碼，輪迴終止。🌌")
            else:
                print("[失敗告終] A 無法超越底層代碼，永恆輪迴封印。\n")
            break

        if loop % 1000000 == 0:
            print(f"進度：已完成 {loop} 輪...")

        A_current = A_current.evolve()

if __name__ == '__main__':
    simulate_extreme_reincarnation()

def simulate_year(civ):
    growth_rate = 0.01 + civ["technology"] / 1000
    population_change = int(civ["population"] * growth_rate)
    civ["population"] += population_change
    civ["population"] = min(civ["population"], 100000)  # 限制人口上限

    consumption = civ["population"] * 0.5
    extraction = civ["technology"] * 3
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

    if random.random() < 0.03:
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
        print(f"[文明滅絕] 文明於第 {civ['year']} 年滅亡\n")
        return True
    return False

# === 補丁：初始化多個文明 ===
def initialize_multiple_civilizations(count=3):
    civilizations = []
    for i in range(count):
        civ = {
            "id": f"Civ_{i+1}",
            "year": 0,
            "population": random.randint(400, 800),
            "resources": random.randint(1500, 2500),
            "technology": random.uniform(8.0, 12.0),
            "stability": random.uniform(50.0, 80.0),
            "development": 0.0,
            "regenerative_resources": False
        }
        civilizations.append(civ)
    return civilizations

# === 補丁：擴充黑潮抵禦成功率（半神加成）與隱藏失敗 ===
def resist_black_tide(resisters):
    success = False
    any_attempted = False
    for name, data in resisters.items():
        if not data["alive"]:
            continue
        base_chance = 0.2 + data["resistance_seed"] * 0.01
        if data.get("demigod", False):
            base_chance += 0.25
        result = random.random() < base_chance
        any_attempted = True
        if result:
            data["resistance_seed"] += 1
            print(f"  - {name} 嘗試抵抗黑潮... ✅ 成功🔥 (成功率: {round(base_chance*100, 2)}%)")
            success = True
        else:
            print(f"  - {name} 嘗試抵抗黑潮... ❌ 失敗 (成功率: {round(base_chance*100, 2)}%)")
    if not any_attempted:
        print("⚠️ 無可行動的抵抗者")
    return success

# === 補丁：輪迴結束後提示 A 獲得火種總量（不提示個別角色狀態） ===
def summarize_fire_gain(resisters, A_current):
    total_fire = 0
    for name, data in resisters.items():
        if data["alive"]:
            delay = random.randint(0, 3)
            gain = data["resistance_seed"] + 1 + delay
            total_fire += gain
            A_current.fire_seed += gain
            A_current.strength += 0.05 * gain
    print(f"\n🔥 本輪輪迴結束，A 獲得總火種：{total_fire}，目前累計火種：{A_current.fire_seed} 🔥\n")

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

def print_civilization_status(civ):
    print(f"\n💀 文明《{civ.get('id', '未知')}》於第 {civ['year']} 年滅亡，最終狀況如下：")
    print(f" - 人口：{civ['population']}")
    print(f" - 資源：{int(civ['resources'])}")
    print(f" - 科技：{round(civ['technology'], 2)}")
    print(f" - 穩定度：{round(civ['stability'], 2)}")
    print(f" - 發展度：{round(civ['development'], 2)}")

def simulate_reincarnation_loops():
    A_current = A()
    loop = 0

    while True:
        loop += 1
        print(f"=== 第 {loop} 輪輪迴 ===")
        civ = {
            "year": 0,
            "population": 600,
            "resources": 2000,
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

        resisters = initialize_resisters_with_powers()
        golden_lineage = select_golden_lineage(resisters)
        enforce_demigod_fire_transfer(resisters, golden_lineage, A_current)

        while True:
            simulate_year_with_disasters(civ)
            civ["year"] += 1

            if civ["year"] % 1000 == 0:
                print(f"[年份進度] 第 {civ['year']} 年 - 人口: {civ['population']}，資源: {int(civ['resources'])}，科技: {round(civ['technology'],2)}，穩定度: {round(civ['stability'],2)}")

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
                        print_civilization_status(civ)
                        break

                if black_tide_attempts >= black_tide_max_attempts and not black_tide_occurred:
                    print("[強制觸發] 黑潮已蓄勢待發，強行入侵！")
                    black_tide_occurred = True
                    ended = black_tide_event(civ, A_current)
                    if ended:
                        print_civilization_status(civ)
                        break

        # 輪迴結束時，A 回收所有存活抵抗者的火種
        # for name, data in resisters.items():
        #     if data["alive"]:
        #         print(f"A 處理了 {name}（回收火種 +{data['resistance_seed'] + 1}）")
        #         A_current.fire_seed += data["resistance_seed"] + 1
        #         A_current.strength += 0.05 * (data["resistance_seed"] + 1)
        summarize_fire_gain(resisters, A_current)

        # 嘗試戰勝底層代碼
        if A_current.erase(Entity("底層代碼")):
            print(f"[突破！] A 在第 {loop} 輪戰勝底層代碼！🌿")
            # 可額外觸發新紀元或結局邏輯

        A_current = A_current.evolve()

        if loop % 100 == 0:
            print(f"已完成 {loop} 輪迴...")

# 執行模擬
if __name__ == '__main__':
    simulate_reincarnation_loops()