'''
中英文翻译对比, 用于起函数变量名字, 本文没有参考, 待完善: https://bbs.mihoyo.com/ys/article/12861276
'''

'''
参考: https://bbs.mihoyo.com/ys/article/14495873

对于单次攻击的伤害，假设其触发暴击和增幅反应，其一般的公式为：
伤害 = 攻击力 * 伤害倍率 * (1+伤害加成) * (1+暴击伤害) * 防御减免 * 抗性减免 * 增幅反应总倍率

单次伤害乘区：
---
攻击区：
基础攻击力(白字) = 人物攻击力 + 武器攻击力
额外攻击力(绿字) = 基础攻击力 * %攻击力 + 固定攻击力(圣遗物提供的小攻击)
总攻击力 = 白字 + 绿字 = 基础攻击力 * (1+%攻击力) + 固定攻击力
---
倍率区：
伤害倍率 = 技能倍率
※ 伤害倍率 = 技能倍率 * (1+倍率提升) 【一些人物天赋或命之座提供额外倍率乘区的伤害提升, 比如行秋的第4命座】
---
基础 & 倍率区
【部分英雄防御力、生命值可转化为额外攻击力，比如 诺艾尔/钟离/阿贝多/心海/申鹤/云堇】
---
增伤区：
伤害加成系数 = 1+各伤害加成数值之和
※ 各伤害加成数值之和=元素/物理伤害加成 + 对元素影响下的敌人伤害提高 + 造成伤害提高 + 元素爆发/元素战技/普攻/重击伤害提高
---
暴击区：
暴击后倍率伤害 = 1+暴击伤害
※ 期望收益 = 1+(暴击率*暴击伤害) 【触发暴击才会有此乘区】
---
防御区：
对象承伤 = (人物等级+100) / ((人物等级+100) + (1-%穿防) * (1-%减防+%增防) * (怪物等级+100))
---
抗性区：
75% < 抗性, 对象承伤 = 1/(1+4*抗性)
0 <= 抗性 <= 75%, 对象承伤 = 1-抗性
抗性 < 0, 对象承伤 = 1-(抗性/2)
---
反应区：
增幅类元素反应 【蒸发、融化等, 提高单次伤害】【影响因素: 攻击力、暴击伤害、防御减免、抗性、伤害加成】
剧变类元素反应 【扩散、超载、超导、感电等, 造成额外一段伤害并有一些额外效果】【影响因素: 角色等级、元素精通、反应伤害提升、抗性】
---
单次增幅元素反应伤害：
增幅反应总倍率 = 反应基础倍率 * (1+精通提升+反应系数提升)
※ 反应基础倍率: 【蒸发(火水1.5 / 水火2.0)】【融合(火冰2.0 / 冰火1.5)】
※ 精通提升 = 2.78 * 精通 / (精通+1400)
※ 反应系数提升: 【实际为百分比, 一般出现在圣遗物4件套】
---
单次剧变元素反应伤害：
剧变伤害 = 等级系数 * 抗性承伤 * 反应基础倍率 * (1+精通提升+反应伤害提升)
※ 等级系数: 【常数, 90级为723, 80级为539】
※ 反应基础倍率: 【超导: 1 (40%物理减抗)】【扩散: 1.2】【碎冰: 3】【超载: 4】【感电: 2.4】
※ 精通提升 = (16*精通) / (精通+2000)
※ 反应系数提升: 【实际为百分比, 一般出现在圣遗物4件套】
'''

'''
抗性表参考: https://bbs.mihoyo.com/ys/article/20098257
'''

'''
attack [攻击区]
paras: 
    attack_character: 人物攻击力
    attack_arms: 武器攻击力
    attack_percentage_increase: %攻击力
    attack_fixed_power: 固定攻击力
'''
def get_attack(
    attack_character, 
    attack_arms, 
    attack_percentage_increase, 
    attack_fixed_power
):
    return (attack_character + attack_arms) * (1 + attack_percentage_increase) + attack_fixed_power

'''
damage_multipiler [倍率区]
paras:
    skill_multipiler: 技能倍率
    skill_multipiler_increase: 技能倍率提升, 默认 0
'''
def get_damage_multipiler(
    skill_multipiler, 
    skill_multipiler_increase=0
):
    return skill_multipiler * (1 + skill_multipiler_increase)

'''
skill_attack_fixed_power [原文'基础&倍率区', 本文修改为固定攻击力组成]
paras:
    convert_property: 转换为固定攻击力的属性
    convert_percentage: 转换为固定攻击力的百分比
'''
def get_skill_attack_fixed_power(
    convert_property, 
    convert_percentage
):
    return convert_property * convert_percentage

'''
damage_bonus [增伤区]
paras:
    increase_cause_harm: 造成伤害提升, 默认 0
    increase_damage_type: 元素/物理伤害提升, 默认 0
    increase_damage_mode: 元素爆发/元素战技/普攻/重击伤害提高, 默认 0
    increase_influence_by_elements: 元素影响下的敌人伤害提高, 默认 0
'''
def get_damage_bonus(
    increase_cause_harm=0, 
    increase_damage_type=0, 
    increase_damage_mode=0, 
    increase_influence_by_elements=0
):
    return 1 + increase_cause_harm + increase_damage_type + increase_damage_mode + increase_influence_by_elements

'''
critical_bracket [暴击区]
paras:
    critical_damage: 暴击伤害, 默认 0.5
'''
def get_critical_bracket(
    critical_bracket=0.5
):
    return 1 + critical_bracket
'''
critical_bracket_float [暴击浮动区, 考虑暴击未满爆情况]
paras:
    critical_rate: 暴击率, 默认 0.05
    critical_damage: 暴击伤害, 默认 0.5
'''
def get_critical_bracket_float(
    critical_rate=0.05, 
    critical_damage=0.5
):
    return 1 + critical_rate * critical_damage

'''
defense [防御区]
paras:
    level_character: 人物等级, 默认 90
    level_monster: 怪物等级, 默认 90
    defense_penetrate: 穿防, 默认 0
    defense_reduce: 减防, 默认 0
    defense_monster_increase: 怪物增防, 默认 0
'''
def get_defense(
    level_character=90, 
    level_monster=90, 
    defense_penetrate=0, 
    defense_reduce=0, 
    defense_monster_increase=0
):
    return (level_character + 100) / ((level_character + 100) + (1 - defense_penetrate) * (1 - defense_reduce + defense_monster_increase) * (level_monster + 100))

'''
resistance [抗性区]
paras:
    resistance_value: 怪物抗性, 参考 https://bbs.mihoyo.com/ys/article/20098257, 默认抗性 10%
todo:
# 读取 resistance.json 获取怪物对应的抗性数值
    type_monster: 需要计算的怪物类型
    type_resistance: 需要计算的抗性类型
'''
def get_resistance(
    resistance_value = 0.1
):
    if resistance_value > 0.75:
        return 1 / (1 + 4 * resistance_value)
    elif resistance_value >= 0:
        return 1 - resistance_value
    else:
        return 1 - resistance_value / 2

'''
elemental_reaction [反应区（增幅反应）] [待完善剧变反应]
paras:
    reaction_active_element: 触发反应的主动元素类型, 即角色攻击元素类型
    reaction_passive_element: 触发反应的被动元素类型, 即怪物头上的元素附着
    mastery: 角色精通
    raction_multipiler_increase: 反应系数提升, 一般出现在圣遗物的4件套中
notes:
    元素反应代码对应: 本实验暂时只考虑增幅反应
    无反应: 0; 增幅反应: 1;
    元素类型代码对应:
    冰: 1; 火: 2; 水: 3
todo:
# 读取 reaction_list.json 获取对应元素反应增幅
# 完善剧变反应测试
'''
def get_elemental_reaction(
    reaction_active_element,
    reaction_passive_element,
    mastery,
    reaction_multipiler_increase = 0,
):
    reaction_list = {
        "1": {
            "2": {
                "reaction_type": 1,
                "reaction_base_multipiler": 1.5
            }
        },
        "2": {
            "1": {
                "reaction_type": 1,
                "reaction_base_multipiler": 2
            },
            "3": {
                "reaction_type": 1,
                "reaction_base_multipiler": 1.5
            }
        },
        "3": {
            "2": {
                "reaction_type": 1,
                "reaction_base_multipiler": 2
            },
        }
    }
    if reaction_active_element in reaction_list.keys() and reaction_passive_element in reaction_list[reaction_active_element].keys():
        reaction_type = reaction_list[reaction_active_element][reaction_passive_element]['reaction_type']
        reaction_base_multipiler = reaction_list[reaction_active_element][reaction_passive_element]['reaction_base_multipiler']
    else:
        print('本代码暂时只支持查询增幅反应, 或者输入反应类型有问题或者不能发生反应')
        return 1
    mastery_increase = 2.78 * mastery / (mastery + 1400)
    return reaction_base_multipiler * (1 + mastery_increase + reaction_multipiler_increase)

'''
数据录入
角色属性: 人物等级, 基础攻击力
武器属性: 基础攻击力, 特效
圣遗物: 花, 羽毛, 沙, 杯, 头 

数据计算
攻击力 * 伤害倍率 * (1+伤害加成) * (1+暴击伤害) * 防御减免 * 抗性减免 * 增幅反应总倍率
'''
# 人物属性
character_attack_base = 334 # 人物角色基础攻击力，可以去米友社搜到
character_level = 90 # 人物角色等级
character_critical_rate = 0.05 # 人物基础暴击率
character_critical_damage = 0.5 + 0.384 # 人物基础爆伤
character_skill_multipiler = 6.22 # 技能倍率，可以从天赋看
# 怪物属性
monster_level = 88 # 被攻击怪物等级
monster_resistance = 0.1 # 怪物对应伤害抗性，可查表得知
# 羁绊属性
fetter_attack_percentage = 0 # 羁绊攻击百分比提升
# 武器属性
arms_attack_base = 510 # 武器基础攻击力
arms_attack_percentage = 0.413 # 武器攻击力百分比提升
# 圣遗物属性（6个数值来源: 圣遗物主词条或者2件套 花 羽毛 沙 杯 头）（5个数值来源: 花 羽毛 沙 杯 头）
artifacts_mastery = 80 + 0 + 33 + 0 + 44 + 37 # 圣遗物精通
artifacts_attack_percentage = 0.466 + 0.041 + 0 + 0 + 0 + 0.216 # 圣遗物攻击力百分比提升
artifacts_attack_fixed = 311 + 14 + 0 + 39 + 0 + 16 # 圣遗物固定攻击力
artifacts_critical_rate = 0.311 + 0.109 + 0.062 + 0.101 + 0.097 + 0 # 圣遗物暴击率
aritfacts_critical_damage = 0.21 + 0.202 + 0 + 0.14 + 0.078 # 圣遗物暴击伤害
artifacts_increase_damage_type = 0.466 # 圣遗物元素伤害提升（冰伤杯）
artifacts_increase_damage_mode = 0.35 # 圣遗物4件套效果重击提升
# 反应属性
# 元素类型代码对应: 冰: 1; 火: 2; 水: 3
reaction_active_element = '1'
reaction_passive_element = '2'


# 计算数据
attack = get_attack(character_attack_base, arms_attack_base, arms_attack_percentage + artifacts_attack_percentage + fetter_attack_percentage, artifacts_attack_fixed)
damage_multipiler = get_damage_multipiler(character_skill_multipiler)
damage_bonus = get_damage_bonus(increase_damage_type=artifacts_increase_damage_type, increase_damage_mode=artifacts_increase_damage_mode)
critical_bracket = get_critical_bracket(character_critical_damage + aritfacts_critical_damage)
defense = get_defense(level_character=character_level, level_monster=monster_level)
resistance = get_resistance()
elemental_reaction = get_elemental_reaction(reaction_active_element, reaction_passive_element, artifacts_mastery)

print('攻击力为：' + str(attack))
print('技能倍率为：' + str(damage_multipiler))
print('增伤为：' + str(damage_bonus))
print('暴击伤害为：' + str(critical_bracket))
print('防御区值为：' + str(defense))
print('抗性区值为：' + str(resistance))
print('反应区值为：' + str(elemental_reaction))

result = attack * damage_multipiler * damage_bonus * critical_bracket * defense * resistance * elemental_reaction
print('单次伤害为：' + str(round(result, 0)))