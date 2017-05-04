from random import shuffle, randint

class Character(object):
    def __init__(self):
        self.name = ''
        self.size = ''
        self.race = ''
        self.class_one_level = ()  # tuple (class, level)
        self.hp = 0
        self.ability_scores = {}
        self.temporary_ablilty_modifiers = []
        self.base_saving_throws = {}
        self.misc_saving_throw_modifiers = []
        self.base_attack_bonus = []
        self.special_abilities = []
        self.feats = []
        self.weapons_list = []
        self.armour = {}
        self.shield = {}
        self.equipment = []
        self.dice_bag = {
            'd4': [i for i in range(1, 5)],
            'd6': [i for i in range(1, 7)],
            'd8': [i for i in range(1, 9)],
            'd10': [i for i in range(1, 11)],
            'd12': [i for i in range(1, 13)],
            'd20': [i for i in range(1, 21)]
        }


    def __dict__(self):
        data = {
            'name': self.name,
            'race': self.race,
            'class': self.class_one_level,
            'ability_scores': {
                'strength': self.ability_scores.get('strength'),
                'dexterity': self.ability_scores.get('dexterity'),
                'constitution': self.ability_scores.get('constitution'),
                'intelligence': self.ability_scores.get('intelligence'),
                'wisdom': self.ability_scores.get('wisdom'),
                'charisma': self.ability_scores.get('charisma')
            }
        }
        return data


    def roll_dice(self, dice):
        def roll(die):
            dice = self.dice_bag.get(die)
            shuffle(dice)
            return dice[randint(0, len(dice) - 1)]

        if dice == 'd100':
            tens = roll('d10')
            if tens == 10:
                tens = 00
            else:
                tens = tens * 10
            ones = roll('d10')
            if ones == 10: ones = 0
            if tens == 00 and ones == 0:
                return 100
            else:
                return tens + ones
        elif self.dice_bag.has_key(dice):
            result = roll(dice)
            return result


    def roll_ability_scores(self):
        roll_scores = []
        for i in range(7):
            rolls = [self.roll_dice('d6') for i in range(4)]
            rolls.sort()
            rolls.reverse()
            del rolls[3]
            total = 0
            for roll in rolls:
                total += roll
            roll_scores.append(total)
        roll_scores.sort()
        roll_scores.reverse()
        del roll_scores[6]
        return roll_scores


    def roll_hit_points(self):
        class_data, level = self.class_one_level
        hp = 0
        hitdice = class_data.get("hitdice")
        for i in range(level):
            hp += self.roll_dice(hitdice)
            hp += self.get_ability_modifier('constitution')
        return hp


    def get_class_data(self):
        class_data, level = self.class_one_level
        return class_data


    def get_level_data(self):
        class_data, level = self.class_one_level
        return class_data.get("levels").get(str(level))


    def get_ability_modifier(self, ability):
        ability_score = self.ability_scores.get(ability)
        # temporary_ability_modifiers = temporary_ability_modifiers.items()

        if ability_score == 1:
            return -5
        elif ability_score <= 3:
            return -4
        elif ability_score <= 5:
            return -3
        elif ability_score <= 7:
            return -2
        elif ability_score <= 9:
            return -1
        elif ability_score <= 11:
            return 0
        elif ability_score <= 13:
            return 1
        elif ability_score <= 15:
            return 2
        elif ability_score <= 17:
            return 3
        elif ability_score <= 19:
            return 4
        elif ability_score <= 21:
            return 5
        elif ability_score <= 23:
            return 6
        elif ability_score <= 25:
            return 7
        elif ability_score <= 27:
            return 8
        elif ability_score <= 29:
            return 9
        elif ability_score <= 31:
            return 10
        elif ability_score <= 33:
            return 11
        elif ability_score <= 35:
            return 12
        elif ability_score <= 37:
            return 13
        elif ability_score <= 39:
            return 14
        elif ability_score <= 41:
            return 15
        elif ability_score <= 43:
            return 16
        elif ability_score <= 45:
            return 17
        elif ability_score <= 47:
            return 18
        elif ability_score <= 49:
            return 19
        elif ability_score >= 50:
            return 20


    def get_initiative_modifier(self):
        # return dex_mod + misc_modifiers
        dex_mod = self.get_ability_modifier('dexterity')
        return dex_mod


    def get_save_modifier(self, save):
        # return base_save + ability_mod + magic_mod + misc_mod
        ability_relations = {
            'fortitude': 'constitution',
            'reflex': 'dexterity',
            'will': 'wisdom'
        }
        base_save = self.base_saving_throws.get(save)
        ability_modifier = self.get_ability_modifier(ability_relations.get(save))
        return base_save + ability_modifier


    def get_grapple_size_modifier(self):
        if self.size == 'colossal':
            return 16
        elif self.size == 'gargantuan':
            return 12
        elif self.size == 'huge':
            return 8
        elif self.size == 'large':
            return 4
        elif self.size == 'medium':
            return 0
        elif self.size == 'small':
            return -4
        elif self.size == 'tiny':
            return -8
        elif self.size == 'diminutive':
            return -12
        elif self.size == 'fine':
            return -16


    def get_grapple_modifier(self):
        # return base_attack_bonus + str_mod + grap_size_mod + misc
        base_attack = self.base_attack_bonus[0]
        str_mod = self.get_ability_modifier('strength')
        size_mod = self.get_grapple_size_modifier()
        return base_attack + str_mod + size_mod


    def get_size_modifier(self):
        if self.size == 'colossal':
            return -8
        elif self.size == 'gargantuan':
            return -4
        elif self.size == 'huge':
            return -2
        elif self.size == 'large':
            return -1
        elif self.size == 'medium':
            return 0
        elif self.size == 'small':
            return 1
        elif self.size == 'tiny':
            return 2
        elif self.size == 'diminutive':
            return 4
        elif self.size == 'fine':
            return 8


    def get_armour_class_dex_mod(self):
        dex_mod = self.get_ability_modifier('dexterity')
        if len(self.armour.items()) > 0 and self.armour.get('max_dex_bonus') is not None\
          and dex_mod >= self.armour.get('max_dex_bonus'):
                return self.armour.get('max_dex_bonus')
        elif len(self.shield.items()) > 0 and self.shield.get('max_dex_bonus') is not None\
          and (self.armour.get('max_dex_bonus') >= self.shield.get('max_dex_bonus') \
            or dex_mod >= self.shield.get('max_dex_bonus')):
                return self.shield.get('max_dex_bonus')
        else: return dex_mod
    
    
    def get_armour_class(self):
        armour_bonus = self.armour.get('ac_bonus', 0)
        shield_bonus = self.shield.get('ac_bonus', 0)
        dex_mod = self.get_armour_class_dex_mod()
        size_mod = self.get_size_modifier()
        return 10 + armour_bonus + shield_bonus + dex_mod + size_mod


    def get_touch_armour_class(self):
        dex_mod = self.get_armour_class_dex_mod()
        size_mod = self.get_size_modifier()
        return 10 + dex_mod + size_mod


    def get_flatfoot_armour_class(self):
        armour_bonus = self.armour.get('ac_bonus', 0)
        shield_bonus = self.shield.get('ac_bonus', 0)
        size_mod = self.get_size_modifier()
        return 10 + armour_bonus + shield_bonus + size_mod
    
    
    def get_protective_item_weight(self, item):
        if not item.get('weight'):
            return None
        elif self.size == 'small':
            return item.get('weight') / 2
        elif self.size == 'medium':
            return item.get('weight')
        elif self.size == 'large':
            return item.get('weight') * 2
        else:
            return None
    
    
    def check_protective_item_proficiency(self, item):
        class_data, level = self.class_one_level
        if item in class_data.get('armour_proficiency'): return True
        else: return False


    def check_weapon_proficiency(self, weapon):
        class_data, level = self.class_one_level
        if weapon.get('proficiency') in class_data.get('weapon_proficiency') \
            or weapon.get('name') in class_data.get('weapon_proficiency'): return True
        else: return False
    

    def get_attack_bonus(self, weapon):
        return [i + self.get_ability_modifier('strength') + self.get_size_modifier() \
                + (-4 if not self.check_weapon_proficiency(weapon) else 0) for i in self.base_attack_bonus]


    def get_max_class_skill_ranks(self):
        class_data, level = self.class_one_level
        int_mod = self.get_ability_modifier("intelligence")
        base_skill_ranks = class_data.get('base_skill_points')
        class_skill_ranks = (base_skill_ranks + int_mod) * 4
        for i in range(level - 1):
            class_skill_ranks += (base_skill_ranks + int_mod)
        return class_skill_ranks