import json
import Tkinter as tk
from model import Character
from view import CharacterSheetView

class CharacterSheetController(object):
    file_name = "players_handbook" + ".json"
    file = open(file_name, "r")
    buffer = file.read()
    data = json.loads(buffer)
    file.close()

    RACE_DEFAULT = data.get('race_default')
    RACES = data.get("races")
    RACE_OPTIONS = [str(i) for i in RACES.keys()]
    RACE_OPTIONS.sort()
    RACE_OPTIONS = ["human"] + RACE_OPTIONS

    CLASSES = data.get("classes")
    CLASS_OPTIONS = [str(i) for i in CLASSES.keys()]
    CLASS_OPTIONS.sort()

    ABILITIES = data.get('abilities')

    WEAPON_DEFAULT = data.get("weapon_default")
    WEAPON_LIST = data.get("weapon_list")
    WEAPON_PROFICIENCIES = data.get('weapon_proficiencies')
    WEAPON_CATEGORIES = data.get('weapon_categories')
    WEAPONS = data.get("weapons")
    weapon_options = [" -none- "]

    ARMOUR_DEFAULT = data.get("armour_default")
    ARMOUR_LIST = data.get("armour_list")
    ARMOUR_CATEGORIES = data.get("armour_categories")
    ARMOUR = data.get("armour")
    armour_options = [" -none- "]

    SHIELD_DEFAULT = data.get("shield_default")
    SHIELD_LIST = data.get("shield_list")
    SHIELD_CATEGORIES = data.get("shield_categories")
    SHIELDS = data.get("shields")
    shield_options = [" -none- "]

    SKILLS_LIST = data.get("skills_list")
    SKILLS = data.get("skills")
    
    def __init__(self, root):
        self.character = Character()
        self.ability_rolls = self.character.roll_ability_scores()
        self.view = CharacterSheetView(root, self)
        self.validate_lvl_cmd = (root.register(self.validate_level), "%P", "%s", "%S", "%W")
        self.class_cmd = self.combine_funcs(self.update_class_level, self.update_ability_scores,
                                                  self.update_saving_throws, self.update_base_attack_bonus,
                                                  self.update_grapple, self.update_hp, self.update_armour_class,
                                                  self.update_initiative, self.update_all_weapons, self.update_all_skills)
        self.class_level_cmd = self.combine_funcs(self.update_class_level, self.update_saving_throws,
                                                  self.update_base_attack_bonus, self.update_grapple,
                                                  self.update_all_weapons)

        #class field
        self.view.race_class_level.class_var.set(self.CLASS_OPTIONS[0])
        self.view.race_class_level.class_var.trace("w", self.class_cmd)
        menu = self.view.race_class_level.class_choices['menu']
        menu.delete(0, 'end')
        for c in self.CLASS_OPTIONS:
            menu.add_command(label=c, command=lambda c=c: self.view.race_class_level.class_var.set(c))
        # class level field
        self.view.race_class_level.class_level.config(command=self.class_level_cmd, validatecommand=self.validate_lvl_cmd)

        # race field
        self.view.race_class_level.race_var.set(self.RACE_OPTIONS[0])
        self.view.race_class_level.race_var.trace("w", self.combine_funcs(self.update_race, self.update_size, self.update_grapple, self.update_speed, self.update_armour_class))
        menu = self.view.race_class_level.race_choices['menu']
        menu.delete(0, 'end')
        for race in self.RACE_OPTIONS:
            menu.add_command(label=race, command=lambda r=race: self.view.race_class_level.race_var.set(r))

        self.view.next_phase_btn.button.config(command=self.next_phase_button)

        self.view.ability_scores.btn1.config(command=self.switch_str_dex_scores)
        self.view.ability_scores.btn2.config(command=self.switch_dex_con_scores)
        self.view.ability_scores.btn3.config(command=self.switch_con_int_scores)
        self.view.ability_scores.btn4.config(command=self.switch_int_wis_scores)
        self.view.ability_scores.btn5.config(command=self.switch_wis_cha_scores)

        self.view.armour.armour_var.set(self.armour_options[0])
        self.view.armour.armour_var.trace("w", self.combine_funcs(self.update_armour, self.update_armour_class))
        self.view.armour.armour_category_var.set(self.ARMOUR_CATEGORIES[0])
        self.view.armour.armour_category_var.trace("w", self.update_armour_category)
        menu = self.view.armour.armour_categories['menu']
        menu.delete(0, 'end')
        for armour_category in self.ARMOUR_CATEGORIES:
            menu.add_command(label=armour_category, command=lambda a=armour_category: self.view.armour.armour_category_var.set(a))

        self.view.shield.shield_var.set(self.shield_options[0])
        self.view.shield.shield_var.trace("w", self.combine_funcs(self.update_shield, self.update_armour_class))
        self.view.shield.shield_category_var.set(self.SHIELD_CATEGORIES[0])
        self.view.shield.shield_category_var.trace("w", self.update_shield_category)
        menu = self.view.shield.shield_categories['menu']
        menu.delete(0, 'end')
        for shield_category in self.SHIELD_CATEGORIES:
            menu.add_command(label=shield_category,
                             command=lambda s=shield_category: self.view.shield.shield_category_var.set(s))

        self.update_class_level()
        self.update_race()
        self.update_size()
        self.update_ability_scores()
        self.update_saving_throws()
        self.update_base_attack_bonus()
        self.update_grapple()
        self.update_hp()
        self.update_speed()
        self.update_armour_category()
        self.update_shield_category()
        self.update_armour_class()
        self.update_initiative()
        self.character.weapons_list = [{} for i in self.view.weapons_list]
        for weapon in self.view.weapons_list:
            weapon.weapon_var.set(self.weapon_options[0])
            weapon.weapon_var.trace("w", lambda a, b, c, w=weapon: self.update_weapon(w, [a, b, c]))
            weapon.weapon_category_var.set("unarmed")
            weapon.weapon_category_var.trace("w", lambda a, b, c, w=weapon: self.update_weapon_choices(w, [a, b, c]))
            menu = weapon.weapon_proficiencies['menu']
            menu.delete(0, 'end')
            for proficiency in self.WEAPON_PROFICIENCIES:
                menu.add_command(label=proficiency, command=lambda p=proficiency, w=weapon: w.weapon_proficiency_var.set(p))
            weapon.weapon_proficiency_var.set(self.WEAPON_PROFICIENCIES[0])
            weapon.weapon_proficiency_var.trace("w", lambda a, b, c, w=weapon: self.update_weapon_proficiency(w, [a, b, c]))
            self.update_weapon_proficiency(weapon)

        for skill in self.view.skills.skills_list:
            self.update_skill(skill)


    def next_phase_button(self):
        self.view.race_class_level.not_editable()
        self.view.ability_scores.remove_switches()
        self.character.hp = self.character.roll_hit_points()
        self.view.hit_points.render_hitpoints()
        self.update_hp()
        self.view.next_phase_btn.button.grid_remove()


    def validate_level(self, user_input, current_base, new_base, widget_name):
        valid = new_base == "" or new_base.isdigit()
        if valid:
            minval = int(self.view.race_class_level.frame.nametowidget(widget_name).config("from")[4])
            maxval = int(self.view.race_class_level.frame.nametowidget(widget_name).config("to")[4] + 1)
            if user_input and int(user_input) not in range(minval, maxval):
                valid = False
        return valid


    def update_class_level(self, *args):
        class_data = self.view.race_class_level.class_var.get()
        if self.view.race_class_level.class_level.get() == "": self.view.race_class_level.class_level.insert(0, 1)
        class_data, level = (self.CLASSES.get(class_data), int(self.view.race_class_level.class_level.get()))
        self.character.class_one_level = (class_data, level)


    def update_race(self, *args):
        race_data = self.view.race_class_level.race_var.get()
        if race_data == "human":
            self.character.race = self.RACE_DEFAULT.get(race_data)
        else:
            self.character.race = self.RACES.get(race_data)


    def update_size(self, *args):
        self.character.size = self.character.race.get("size")


    def update_saving_throws(self, *args):
        level_data = self.character.get_level_data()
        base_saving_throws = {
            "fortitude": level_data.get("fort_save"),
            "reflex": level_data.get("ref_save"),
            "will": level_data.get("will_save")
        }
        self.character.base_saving_throws = base_saving_throws
        self.view.saving_throws.fort_save_total_var.set(self.character.get_save_modifier("fortitude"))
        self.view.saving_throws.fort_save_base_var.set(base_saving_throws.get("fortitude"))
        self.view.saving_throws.ref_save_total_var.set(self.character.get_save_modifier("reflex"))
        self.view.saving_throws.ref_save_base_var.set(base_saving_throws.get("reflex"))
        self.view.saving_throws.will_save_total_var.set(self.character.get_save_modifier("will"))
        self.view.saving_throws.will_save_base_var.set(base_saving_throws.get("will"))


    def update_base_attack_bonus(self, *args):
        level_data = self.character.get_level_data()
        self.character.base_attack_bonus = level_data.get("base_attack_bonus")
        self.view.base_attack_bonus.base_attack_bonus_var.set(self.character.base_attack_bonus)


    def update_grapple(self, *args):
        self.view.grapple.grapple_total_var.set(self.character.get_grapple_modifier())
        self.view.grapple.grapple_base_attack_bonus_var.set(self.character.base_attack_bonus[0])
        self.view.grapple.grapple_size_mod_var.set(self.character.get_grapple_size_modifier())


    def update_hp(self, *args):
        self.view.hit_points.hitdice_var.set(self.character.get_class_data().get('hitdice'))
        self.view.hit_points.hp_total_var.set(self.character.hp)


    def update_speed(self, *args):
        self.view.speed.speed_var.set(str(self.character.race.get("land_speed")) + ' ft')


    def update_initiative(self, *args):
        self.view.initiative.initiative_var.set(self.character.get_initiative_modifier())


    def update_armour_class(self, *args):
        self.view.armour_class.ac_total_var.set(self.character.get_armour_class())
        self.view.armour_class.ac_armour_bonus_var.set(self.character.armour.get('ac_bonus', 0))
        self.view.armour_class.ac_shield_bonus_var.set(self.character.shield.get('ac_bonus', 0))
        self.view.armour_class.ac_dex_mod_var.set(self.character.get_armour_class_dex_mod())



        self.view.armour_class.ac_size_mod_var.set(self.character.get_size_modifier())
        self.view.touch_armour_class.touch_ac_var.set(self.character.get_touch_armour_class())
        self.view.flatfooted_armour_class.flat_footed_ac_var.set(self.character.get_flatfoot_armour_class())


    def update_armour(self, *args):
        armour_data = self.view.armour.armour_var.get()
        if armour_data == " -none- ":
            armour_data = self.ARMOUR_DEFAULT.get(" -none- ")
        else:
            armour_data = self.ARMOUR.get(armour_data)
        self.character.armour = armour_data

        self.view.armour.armour_ac_bonus_var.set(self.character.armour.get('ac_bonus'))
        self.view.armour.armour_max_dex_var.set(str(self.character.armour.get('max_dex_bonus')).lower())
        self.view.armour.armour_check_penalty_var.set(self.character.armour.get('check_penalty'))
        self.view.armour.armour_spell_failure_var.set(str(self.character.armour.get('spell_failure')) + ' %')
        self.view.armour.armour_weight_var.set(str(self.character.get_protective_item_weight(self.character.armour))\
                                               .lower() + "%s" % (" lb." if self.character.armour.get('weight') else ""))


    def update_armour_category(self, *args):
        category = self.view.armour.armour_category_var.get()
        armour_options = [" -none- "]
        for a in self.ARMOUR_LIST:
            armour = self.ARMOUR.get(a)
            if armour.get('category') == category: armour_options.append(a)
        self.view.armour.armour_var.set(armour_options[0])
        menu = self.view.armour.armour_choices['menu']
        menu.delete(0, 'end')
        for armour in armour_options:
            menu.add_command(label=armour, command=lambda a=armour: self.view.armour.armour_var.set(a))


    def update_shield(self, *args):
        shield_data = self.view.shield.shield_var.get()
        if shield_data == " -none- ":
            shield_data = self.SHIELD_DEFAULT.get(" -none- ")
        else:
            shield_data = self.SHIELDS.get(shield_data)
        self.character.shield = shield_data

        self.view.shield.shield_ac_bonus_var.set(self.character.shield.get('ac_bonus'))
        self.view.shield.shield_max_dex_var.set(str(self.character.shield.get('max_dex_bonus')).lower())
        self.view.shield.shield_check_penalty_var.set(self.character.shield.get('check_penalty'))
        self.view.shield.shield_spell_failure_var.set(str(self.character.shield.get('spell_failure')) + ' %')
        self.view.shield.shield_weight_var.set(
            str(self.character.get_protective_item_weight(self.character.shield)).lower() + "%s" % (" lb." if self.character.shield.get('weight') else ""))


    def update_shield_category(self, *args):
        category = self.view.shield.shield_category_var.get()
        shield_options = [" -none- "]
        for s in self.SHIELD_LIST:
            shield = self.SHIELDS.get(s)
            if shield.get('category') == category: shield_options.append(s)
            self.view.shield.shield_var.set(shield_options[0])
        menu = self.view.shield.shield_choices['menu']
        menu.delete(0, 'end')
        for shield in shield_options:
            menu.add_command(label=shield, command=lambda s=shield: self.view.shield.shield_var.set(s))


    def update_weapon(self, weapon, *args):
        weapon_data = weapon.weapon_var.get()
        if weapon_data in ["unarmed strike", " -none- "]:
            weapon_data = self.WEAPON_DEFAULT.get(weapon_data)
        else:
            weapon_data = self.WEAPONS.get(weapon_data)
        self.character.weapons_list[self.view.weapons_list.index(weapon)] = weapon_data
        model_weapon = self.character.weapons_list[self.view.weapons_list.index(weapon)]

        weapon.weapon_attack_bonus_var.set(self.character.get_attack_bonus(model_weapon))
        weapon.weapon_damage_var.set(model_weapon.get('dmg(m)'))
        weapon.weapon_critical_var.set(model_weapon.get('critical'))
        weapon.weapon_range_var.set(str(model_weapon.get('range')).lower() + "%s" % (" ft." if model_weapon.get('range') else ""))
        weapon.weapon_weight_var.set(str(model_weapon.get('weight')).lower() + "%s" % (" lb." if model_weapon.get('weight') else ""))


    def update_weapon_choices(self, weapon, *args):
        proficiency = weapon.weapon_proficiency_var.get()
        category = weapon.weapon_category_var.get()
        if proficiency == "simple" and category == "unarmed":
            weapon_options = ["unarmed strike"]
        else:
            weapon_options = [" -none- "]
        for w in self.WEAPON_LIST:
            weapon_data = self.WEAPONS.get(w)
            if weapon_data.get('proficiency') == proficiency and weapon_data.get('category') == category: weapon_options.append(w)
        weapon.weapon_var.set(weapon_options[0])
        menu = weapon.weapon_choices['menu']
        menu.delete(0, 'end')
        for weapon_data in weapon_options:
            menu.add_command(label=weapon_data, command=lambda w=weapon_data: weapon.weapon_var.set(w))


    def update_weapon_proficiency(self, weapon, *args):
        proficiency = weapon.weapon_proficiency_var.get()
        category = weapon.weapon_category_var.get()

        if proficiency == "simple":
            category_options = ["unarmed"] + self.WEAPON_CATEGORIES
        else:
            category_options = self.WEAPON_CATEGORIES
            if category == "unarmed": weapon.weapon_category_var.set(category_options[0])
        menu = weapon.weapon_categories['menu']
        menu.delete(0, 'end')
        for category in category_options:
            menu.add_command(label=category, command=lambda c=category: weapon.weapon_category_var.set(c))
        self.update_weapon_choices(weapon)


    def update_all_weapons(self, *args):
        for weapon in self.view.weapons_list:
            self.update_weapon(weapon)


    def update_skill(self, skill, *args):
        ability = self.ABILITIES.get(skill.key_ability.get())
        skill.skill_mod_var.set(self.character.get_ability_modifier(ability))
        skill.ability_mod_var.set(self.character.get_ability_modifier(ability))


    def update_all_skills(self, *args):
        for skill in self.view.skills.skills_list:
            self.update_skill(skill)


    def update_strength(self, *args):
        self.view.ability_scores.str_score_var.set(self.character.ability_scores['strength'])
        self.view.ability_scores.str_mod_var.set(self.character.get_ability_modifier('strength'))


    def update_dexterity(self, *args):
        self.view.ability_scores.dex_score_var.set(self.character.ability_scores['dexterity'])
        self.view.ability_scores.dex_mod_var.set(self.character.get_ability_modifier('dexterity'))


    def update_constitution(self, *args):
        self.view.ability_scores.con_score_var.set(self.character.ability_scores['constitution'])
        self.view.ability_scores.con_mod_var.set(self.character.get_ability_modifier('constitution'))


    def update_intelligence(self, *args):
        self.view.ability_scores.int_score_var.set(self.character.ability_scores['intelligence'])
        self.view.ability_scores.int_mod_var.set(self.character.get_ability_modifier('intelligence'))


    def update_wisdom(self, *args):
        self.view.ability_scores.wis_score_var.set(self.character.ability_scores['wisdom'])
        self.view.ability_scores.wis_mod_var.set(self.character.get_ability_modifier('wisdom'))


    def update_charisma(self, *args):
        self.view.ability_scores.cha_score_var.set(self.character.ability_scores['charisma'])
        self.view.ability_scores.cha_mod_var.set(self.character.get_ability_modifier('charisma'))


    def update_ability_scores(self, *args):
        class_data = self.character.get_class_data()
        i = 0
        for ability in class_data.get('abilities'):
            if ability == "str":
                self.character.ability_scores['strength'] = self.ability_rolls[i]
            elif ability == "dex":
                self.character.ability_scores['dexterity'] = self.ability_rolls[i]
            elif ability == "con":
                self.character.ability_scores['constitution'] = self.ability_rolls[i]
            elif ability == "int":
                self.character.ability_scores['intelligence'] = self.ability_rolls[i]
            elif ability == "wis":
                self.character.ability_scores['wisdom'] = self.ability_rolls[i]
            elif ability == "cha":
                self.character.ability_scores['charisma'] = self.ability_rolls[i]
            i += 1
        self.update_strength()
        self.update_dexterity()
        self.update_constitution()
        self.update_intelligence()
        self.update_wisdom()
        self.update_charisma()


    def switch_str_dex_scores(self):
        str = self.character.ability_scores['strength']
        dex = self.character.ability_scores['dexterity']
        self.character.ability_scores['strength'] = dex
        self.character.ability_scores['dexterity'] = str
        self.update_strength()
        self.update_dexterity()
        self.update_saving_throws()
        self.update_grapple()
        self.update_armour_class()
        self.update_initiative()
        for weapon in self.view.weapons_list:
            self.update_weapon(weapon)
        self.update_all_skills()


    def switch_dex_con_scores(self):
        dex = self.character.ability_scores['dexterity']
        con = self.character.ability_scores['constitution']
        self.character.ability_scores['dexterity'] = con
        self.character.ability_scores['constitution'] = dex
        self.update_dexterity()
        self.update_constitution()
        self.update_saving_throws()
        self.update_armour_class()
        self.update_initiative()
        self.update_all_skills()


    def switch_con_int_scores(self):
        con = self.character.ability_scores['constitution']
        int = self.character.ability_scores['intelligence']
        self.character.ability_scores['constitution'] = int
        self.character.ability_scores['intelligence'] = con
        self.update_constitution()
        self.update_intelligence()
        self.update_saving_throws()
        self.update_all_skills()


    def switch_int_wis_scores(self):
        int = self.character.ability_scores['intelligence']
        wis = self.character.ability_scores['wisdom']
        self.character.ability_scores['intelligence'] = wis
        self.character.ability_scores['wisdom'] = int
        self.update_intelligence()
        self.update_wisdom()
        self.update_saving_throws()
        self.update_all_skills()


    def switch_wis_cha_scores(self):
        wis = self.character.ability_scores['wisdom']
        cha = self.character.ability_scores['charisma']
        self.character.ability_scores['wisdom'] = cha
        self.character.ability_scores['charisma'] = wis
        self.update_wisdom()
        self.update_charisma()
        self.update_saving_throws()
        self.update_all_skills()


    def combine_funcs(self, *funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = CharacterSheetController(root)
    root.mainloop()