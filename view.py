import Tkinter as tk
from Tkinter import N, S, E, SW, W, NW, LEFT, RIGHT, Y, BOTH


class CharacterSheetView(tk.Toplevel):
    def __init__(self, master, control):
        tk.Toplevel.__init__(self, master)
        self.geometry("+000+000")
        self.title("D&D 3.5 Character generator")
        self.race_class_level = RaceClassLevel(self)
        self.race_class_level.frame.grid(row=0, column=0, columnspan=2, sticky=W)
        self.ability_scores = AbilityScores(self)
        self.ability_scores.frame.grid(row=1, column=0, sticky=W)
        self.saving_throws = SavingThrows(self, self.ability_scores)
        self.saving_throws.frame.grid(row=2, column=0, columnspan=2, sticky=W)
        self.base_attack_bonus = BaseAttackBonus(self)
        self.base_attack_bonus.frame.grid(row=3, column=0, columnspan=2, sticky=W)
        self.grapple = Grapple(self, self.ability_scores)
        self.grapple.frame.grid(row=4, column=0, columnspan=2, sticky=W)

        self.attack = tk.Frame(self, bd=2)
        self.attack.grid(row=6, column=0, columnspan=2, sticky=W)

        self.weapons_list = []
        for i in range(3):
            weapon = Weapon(self.attack)
            weapon.frame.grid(row=i, column=0)
            self.weapons_list.append(weapon)

        self.group_frame = tk.Frame(self, bd=2)
        self.group_frame.grid(row=1, column=1, rowspan=3, sticky=NW)
        self.hit_points = HitPoints(self.group_frame)
        self.speed = Speed(self.group_frame)
        self.armour_class = ArmourClass(self.group_frame)
        self.touch_armour_class = TouchArmourClass(self.group_frame)
        self.flatfooted_armour_class = FlatfootedArmourClass(self.group_frame)
        self.initiative = Initiative(self.group_frame, self.ability_scores)
        self.initiative.frame.grid(row=8, column=0, columnspan=4)
        self.skills = Skills(self, control)
        self.skills.frame.grid(row=2, column=2, rowspan=5, pady=(4,0), sticky=NW)

        self.protection = tk.Frame(self, bd=2)
        self.protection.grid(row=1, column=2, sticky=W)
        self.armour = Armour(self.protection)
        self.armour.frame.grid(row=1, column=0)
        self.shield = Shield(self.protection)
        self.shield.frame.grid(row=2, column=0)

        self.next_phase_btn = NextPhaseButton(self.race_class_level.frame)
        self.next_phase_btn.button.grid(row=1, column=3)


class NextPhaseButton:
    def __init__(self, parent):
        self.button = tk.Button(parent, text="Next", font=("", 12), bd=2)

class RaceClassLevel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2)
        class_options = []
        race_options = []
        self.class_var = tk.StringVar()
        self.race_var = tk.StringVar()

        tk.Label(self.frame, text="CLASS AND LEVEL", font=("", 8)).grid(row=0, column=0, columnspan=2, sticky=SW, pady=0, padx=(7,0))
        tk.Label(self.frame, text="RACE", font=("", 8)).grid(row=0, column=2, sticky=SW, pady=0, padx=(7,0))

        self.class_choices = tk.OptionMenu(self.frame, self.class_var, class_options)
        self.class_choices.config(font=("", 10), width=12)
        self.class_choices.grid(row=1, column=0, pady=0)

        self.class_level = tk.Spinbox(self.frame, from_=1, to=20, width=2, validate="all")
        self.class_level.config(font=("", 10))
        self.class_level.grid(row=1, column=1, pady=0)

        self.race_choices = tk.OptionMenu(self.frame, self.race_var, race_options)
        self.race_choices.config(font=("", 10), width=10)
        self.race_choices.grid(row=1, column=2, pady=0)

    def not_editable(self):
        self.class_choices.grid_remove()
        self.class_level.grid_remove()
        self.race_choices.grid_remove()

        tk.Label(self.frame, text=self.class_var.get(), font=("", 12)).grid(row=1, column=0, sticky=W, pady=0, padx=(7,0))
        tk.Label(self.frame, text=("lvl " + self.class_level.get()), font=("", 12)).grid(row=1, column=1, sticky=W, pady=0)
        tk.Label(self.frame, text=self.race_var.get(), font=("", 12)).grid(row=1, column=2, sticky=W, pady=0, padx=(7,0))

class AbilityScores:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2)

        self.str_score_var = tk.StringVar()
        self.str_mod_var = tk.StringVar()
        self.dex_score_var = tk.StringVar()
        self.dex_mod_var = tk.StringVar()
        self.con_score_var = tk.StringVar()
        self.con_mod_var = tk.StringVar()
        self.int_score_var = tk.StringVar()
        self.int_mod_var = tk.StringVar()
        self.wis_score_var = tk.StringVar()
        self.wis_mod_var = tk.StringVar()
        self.cha_score_var = tk.StringVar()
        self.cha_mod_var = tk.StringVar()

        tk.Label(self.frame, text="ABILITY NAME", font=("", 6)).grid(row=0, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="ABILITY\nSCORE", font=("", 6)).grid(row=0, column=1, sticky=S, pady=0)
        tk.Label(self.frame, text="ABILITY\nMODIFIER", font=("", 6)).grid(row=0, column=2, sticky=S, pady=0)

        # strength
        tk.Label(self.frame, text="STR", font=("", 10, 'bold'), bd=0, width=8).grid(row=1, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="STRENGTH", font=("", 6), bd=0).grid(row=2, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.str_score_var, font=("", 12), width=5).grid(row=1, column=1, rowspan=2)
        tk.Label(self.frame, textvariable=self.str_mod_var, font=("", 14), width=3).grid(row=1, column=2, rowspan=2)

        # dexterity
        tk.Label(self.frame, text="DEX", font=("", 10, 'bold'), bd=0).grid(row=3, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="DEXTERITY", font=("", 6), bd=0).grid(row=4, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.dex_score_var, font=("", 12)).grid(row=3, column=1, rowspan=2)
        tk.Label(self.frame, textvariable=self.dex_mod_var, font=("", 14)).grid(row=3, column=2, rowspan=2)

        # constitution
        tk.Label(self.frame, text="CON", font=("", 10, 'bold'), bd=0).grid(row=5, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="CONSTITUTION", font=("", 6), bd=0).grid(row=6, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.con_score_var, font=("", 12)).grid(row=5, column=1, rowspan=2)
        tk.Label(self.frame, textvariable=self.con_mod_var, font=("", 14)).grid(row=5, column=2, rowspan=2)

        # intelligence
        tk.Label(self.frame, text="INT", font=("", 10, 'bold'), bd=0).grid(row=7, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="INTELLIGENCE", font=("", 6), bd=0).grid(row=8, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.int_score_var, font=("", 12)).grid(row=7, column=1, rowspan=2)
        tk.Label(self.frame, textvariable=self.int_mod_var, font=("", 14)).grid(row=7, column=2, rowspan=2)

        # wisdom
        tk.Label(self.frame, text="WIS", font=("", 10, 'bold'), bd=0).grid(row=9, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="WISDOM", font=("", 6), bd=0).grid(row=10, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.wis_score_var, font=("", 12)).grid(row=9, column=1, rowspan=2)
        tk.Label(self.frame, textvariable=self.wis_mod_var, font=("", 14)).grid(row=9, column=2, rowspan=2)

        # charisma
        tk.Label(self.frame, text="CHA", font=("", 10, 'bold'), bd=0).grid(row=11, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="CHARISMA", font=("", 6), bd=0).grid(row=12, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.cha_score_var, font=("", 12)).grid(row=11, column=1, rowspan=2)
        tk.Label(self.frame, textvariable=self.cha_mod_var, font=("", 14)).grid(row=11, column=2, rowspan=2)

        # ability switch frame -------------------------------------------------------------------
        self.ability_switch_frame = tk.Frame(self.frame, bd=2)
        self.ability_switch_frame.grid(row=1, column=3, rowspan=12)

        self.btn1 = tk.Button(self.ability_switch_frame, bd=0)
        self.btn1.grid(row=0, pady=0)
        self.btn2 = tk.Button(self.ability_switch_frame, bd=0)
        self.btn2.grid(row=1, pady=0)
        self.btn3 = tk.Button(self.ability_switch_frame, bd=0)
        self.btn3.grid(row=2, pady=0)
        self.btn4 = tk.Button(self.ability_switch_frame, bd=0)
        self.btn4.grid(row=3, pady=0)
        self.btn5 = tk.Button(self.ability_switch_frame, bd=0)
        self.btn5.grid(row=4, pady=0)

    def remove_switches(self):
        self.ability_switch_frame.grid_remove()

class SavingThrows:
    def __init__(self, parent, ability_scores):
        self.frame = tk.Frame(parent, bd=2)

        self.fort_save_total_var = tk.StringVar()
        self.fort_save_base_var = tk.StringVar()
        self.ref_save_total_var = tk.StringVar()
        self.ref_save_base_var = tk.StringVar()
        self.will_save_total_var = tk.StringVar()
        self.will_save_base_var = tk.StringVar()

        tk.Label(self.frame, text="SAVING THROWS", font=("", 8)).grid(row=0, column=0, sticky=SW)
        tk.Label(self.frame, text="TOTAL", font=("", 8)).grid(row=0, column=1, sticky=S)
        tk.Label(self.frame, text="BASE\nSAVE", font=("", 6)).grid(row=0, column=3, sticky=S)
        tk.Label(self.frame, text="ABILITY\nMODIFIER", font=("", 6)).grid(row=0, column=5, sticky=S)

        # fortitude save
        tk.Label(self.frame, text="FORTITUDE", font=("", 10, 'bold'), bd=0).grid(row=1, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="(CONSTITUTION)", font=("", 6), bd=0).grid(row=2, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.fort_save_total_var, font=("", 14), width=4).grid(row=1, column=1, rowspan=2)
        tk.Label(self.frame, text="=", font=("", 10), bd=0).grid(row=1, column=2, rowspan=2)
        tk.Label(self.frame, textvariable=self.fort_save_base_var, font=("", 12), width=4).grid(row=1, column=3, rowspan=2)
        tk.Label(self.frame, text="+", font=("", 10), bd=0).grid(row=1, column=4, rowspan=2)
        tk.Label(self.frame, textvariable=ability_scores.con_mod_var, font=("", 12)).grid(row=1, column=5, rowspan=2)

        # reflex save
        tk.Label(self.frame, text="REFLEX", font=("", 10, 'bold'), bd=0).grid(row=3, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="(DEXTERITY)", font=("", 6), bd=0).grid(row=4, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.ref_save_total_var, font=("", 14)).grid(row=3, column=1, rowspan=2)
        tk.Label(self.frame, text="=", font=("", 10), bd=0).grid(row=3, column=2, rowspan=2)
        tk.Label(self.frame, textvariable=self.ref_save_base_var, font=("", 12)).grid(row=3, column=3, rowspan=2)
        tk.Label(self.frame, text="+", font=("", 10), bd=0).grid(row=3, column=4, rowspan=2)
        tk.Label(self.frame, textvariable=ability_scores.dex_mod_var, font=("", 12)).grid(row=3, column=5, rowspan=2)

        # will save
        tk.Label(self.frame, text="WILL", font=("", 10, 'bold'), bd=0).grid(row=5, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="(WISDOM)", font=("", 6), bd=0).grid(row=6, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.will_save_total_var, font=("", 14)).grid(row=5, column=1, rowspan=2)
        tk.Label(self.frame, text="=", font=("", 10), bd=0).grid(row=5, column=2, rowspan=2)
        tk.Label(self.frame, textvariable=self.will_save_base_var, font=("", 12)).grid(row=5, column=3, rowspan=2)
        tk.Label(self.frame, text="+", font=("", 10), bd=0).grid(row=5, column=4, rowspan=2)
        tk.Label(self.frame, textvariable=ability_scores.wis_mod_var, font=("", 12)).grid(row=5, column=5, rowspan=2)


class BaseAttackBonus:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2)

        self.base_attack_bonus_var = tk.StringVar()

        tk.Label(self.frame, text="BASE ATTACK BONUS", font=("", 12, 'bold')).grid(row=0, column=0)

        tk.Label(self.frame, textvariable=self.base_attack_bonus_var, font=("", 14)).grid(row=0, column=1, padx=(8, 0))


class Grapple:
    def __init__(self,parent, ability_scores):
        self.frame = tk.Frame(parent, bd=2)

        self.grapple_total_var = tk.StringVar()
        self.grapple_base_attack_bonus_var = tk.StringVar()
        self.grapple_size_mod_var = tk.StringVar()

        tk.Label(self.frame, text="GRAPPLE", font=("", 12, 'bold'), bd=0).grid(row=0, column=0, sticky=S, padx=(2, 0), pady=0)
        tk.Label(self.frame, text="MODIFIER", font=("", 6), bd=0).grid(row=1, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.grapple_total_var, font=("", 14), width=4).grid(row=0, column=1, rowspan=2)
        tk.Label(self.frame, text="=", font=("", 10), bd=0).grid(row=0, column=2, rowspan=2)
        tk.Label(self.frame, textvariable=self.grapple_base_attack_bonus_var, font=("", 12)).grid(row=0, column=3, rowspan=2)
        tk.Label(self.frame, text="+", font=("", 10), bd=0).grid(row=0, column=4, rowspan=2)
        tk.Label(self.frame, textvariable=ability_scores.str_mod_var, font=("", 12)).grid(row=0, column=5, rowspan=2)
        tk.Label(self.frame, text="+", font=("", 10), bd=0).grid(row=0, column=6, rowspan=2)
        tk.Label(self.frame, textvariable=self.grapple_size_mod_var, font=("", 12)).grid(row=0, column=7, rowspan=2)

        tk.Label(self.frame, text="TOTAL", font=("", 8)).grid(row=2, column=1, sticky=N, pady=0)
        tk.Label(self.frame, text="BASE ATTACK\nBONUS", font=("", 6)).grid(row=2, column=3, sticky=N, pady=0)
        tk.Label(self.frame, text="STRENGTH\nMODIFIER", font=("", 6)).grid(row=2, column=5, sticky=N, pady=0)
        tk.Label(self.frame, text="SIZE\nMODIFIER", font=("", 6)).grid(row=2, column=7, sticky=N, pady=0)


class HitPoints:
    def __init__(self, parent):
        self.parent = parent

        self.hitdice_var = tk.StringVar()
        self.hp_total_var = tk.StringVar()
        self.current_hp_var = tk.StringVar()
        self.nonlethal_dmg_var = tk.StringVar()


        tk.Label(parent, text="HP", font=("", 12, 'bold'), bd=0).grid(row=1, column=0, sticky=S, pady=0)
        tk.Label(parent, text="HIT POINTS", font=("", 6), bd=0).grid(row=2, column=0, sticky=N, pady=0)
        self.hitdice_label = tk.Label(parent, text="HITDICE", font=("", 8))
        self.hitdice_label.grid(row=0, column=1, sticky=S, pady=0)

        self.hitdice = tk.Label(parent, textvariable=self.hitdice_var)
        self.hitdice.grid(row=1, column=1, rowspan=2, pady=0)


    def render_hitpoints(self):
        self.hitdice_label.grid_remove()
        self.hitdice.grid_remove()

        tk.Label(self.parent, text="TOTAL", font=("", 8)).grid(row=0, column=1, sticky=S, pady=0)
        tk.Label(self.parent, text="WOUNDS / CURRENT HP", font=("", 6)).grid(row=0, column=2, columnspan=3, sticky=S, pady=0)
        tk.Label(self.parent, text="NON-LETHAL\nDAMAGE", font=("", 6)).grid(row=0, column=5, columnspan=3, sticky=S, pady=0)

        tk.Label(self.parent, textvariable=self.hp_total_var, font=("", 14)).grid(row=1, column=1, rowspan=2, pady=0)
        tk.Label(self.parent, textvariable=self.current_hp_var, font=("", 12)).grid(row=1, column=2, rowspan=2, columnspan=2, pady=0)
        tk.Label(self.parent, textvariable=self.nonlethal_dmg_var, font=("", 12)).grid(row=1, column=5, rowspan=2, columnspan=3, pady=0)


class Speed:
    def __init__(self, parent):
        self.speed_var = tk.StringVar()

        tk.Label(parent, text="SPEED", font=("", 10, 'bold')).grid(row=0, column=8, columnspan=3, sticky=S, pady=0)

        tk.Label(parent, textvariable=self.speed_var, font=("", 14)).grid(row=1, column=8, rowspan=2, columnspan=3)


class ArmourClass:
    def __init__(self, parent):
        self.ac_total_var = tk.StringVar()
        self.ac_armour_bonus_var = tk.StringVar()
        self.ac_shield_bonus_var = tk.StringVar()
        self.ac_dex_mod_var = tk.StringVar()
        self.ac_size_mod_var = tk.StringVar()

        tk.Label(parent, text="AC", font=("", 12, 'bold'), bd=0).grid(row=3, column=0, sticky=S, pady=0)
        tk.Label(parent, text="ARMOUR CLASS", font=("", 6), bd=0).grid(row=4, column=0, sticky=N, pady=0)

        tk.Label(parent, textvariable=self.ac_total_var, font=("", 14)).grid(row=3, column=1, rowspan=2, pady=0)
        tk.Label(parent, text="=", font=("", 10), bd=0).grid(row=3, column=2, rowspan=2)
        tk.Label(parent, text="10+", font=("", 12)).grid(row=3, column=3, rowspan=2, pady=0, padx=(3, 0))
        tk.Label(parent, textvariable=self.ac_armour_bonus_var, font=("", 12)).grid(row=3, column=4, rowspan=2)
        tk.Label(parent, text="+", font=("", 10), bd=0).grid(row=3, column=5, rowspan=2)
        tk.Label(parent, textvariable=self.ac_shield_bonus_var, font=("", 12)).grid(row=3, column=6, rowspan=2)
        tk.Label(parent, text="+", font=("", 10), bd=0).grid(row=3, column=7, rowspan=2)
        tk.Label(parent, textvariable=self.ac_dex_mod_var, font=("", 12)).grid(row=3, column=8, rowspan=2)
        tk.Label(parent, text="+", font=("", 10), bd=0).grid(row=3, column=9, rowspan=2)
        tk.Label(parent, textvariable=self.ac_size_mod_var, font=("", 12)).grid(row=3, column=10, rowspan=2)

        tk.Label(parent, text="TOTAL", font=("", 8)).grid(row=5, column=1, sticky=N, pady=0)
        tk.Label(parent, text="ARMOUR\nBONUS", font=("", 6)).grid(row=5, column=4, sticky=N, pady=0)
        tk.Label(parent, text="SHIELD\nBONUS", font=("", 6)).grid(row=5, column=6, sticky=N, pady=0)
        tk.Label(parent, text="DEX\nMODIFIER", font=("", 6)).grid(row=5, column=8, sticky=N, pady=0)
        tk.Label(parent, text="SIZE\nMODIFIER", font=("", 6)).grid(row=5, column=10, sticky=N, pady=0)

class TouchArmourClass:
    def __init__(self, parent):
        self.touch_ac_var = tk.StringVar()

        tk.Label(parent, text="TOUCH", font=("", 10, 'bold'), bd=0).grid(row=6, column=0, sticky=S, pady=(3, 0))
        tk.Label(parent, text="ARMOUR CLASS", font=("", 6), bd=0).grid(row=7, column=0, sticky=N, pady=0)

        tk.Label(parent, textvariable=self.touch_ac_var, font=("", 14)).grid(row=6, column=1, rowspan=2, pady=(3, 0))


class FlatfootedArmourClass:
    def __init__(self, parent):
        self.flat_footed_ac_var = tk.StringVar()

        tk.Label(parent, text="FLAT-FOOTED", font=("", 10, 'bold'), bd=0).grid(row=6, column=2, columnspan=3, sticky=S, pady=(3, 0))
        tk.Label(parent, text="ARMOUR CLASS", font=("", 6), bd=0).grid(row=7, column=2, columnspan=3, sticky=N, pady=0)

        tk.Label(parent, textvariable=self.flat_footed_ac_var, font=("", 14)).grid(row=6, column=6, rowspan=2, pady=(3, 0))


class Initiative:
    def __init__(self, parent, ability_scores):
        self.frame = tk.Frame(parent)
        self.initiative_var = tk.StringVar()

        tk.Label(self.frame, text="INITIATIVE", font=("", 12, 'bold'), bd=0).grid(row=0, column=0, sticky=S, pady=0)
        tk.Label(self.frame, text="MODIFIER", font=("", 6), bd=0).grid(row=1, column=0, sticky=N, pady=0)

        tk.Label(self.frame, textvariable=self.initiative_var, font=("", 14), width=4).grid(row=0, column=1, rowspan=2)
        tk.Label(self.frame, text="=", font=("", 10), bd=0).grid(row=0, column=2, rowspan=2)
        tk.Label(self.frame, textvariable=ability_scores.dex_mod_var, font=("", 12)).grid(row=0, column=3, rowspan=2)

        tk.Label(self.frame, text="TOTAL", font=("", 8)).grid(row=2, column=1, sticky=N, pady=0)
        tk.Label(self.frame, text="DEX\nMODIFIER", font=("", 6)).grid(row=2, column=3, sticky=N, pady=0)


class Armour:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.armour_var = tk.StringVar()
        self.armour_category_var = tk.StringVar()
        self.armour_ac_bonus_var = tk.StringVar()
        self.armour_max_dex_var = tk.StringVar()
        self.armour_check_penalty_var = tk.StringVar()
        self.armour_spell_failure_var = tk.StringVar()
        self.armour_weight_var = tk.StringVar()

        tk.Label(self.frame, text="ARMOUR", font=("", 10, 'bold'), bd=0).grid(row=0, column=0, sticky=SW, padx=(7, 0), pady=0)
        tk.Label(self.frame, text="CATEGORY", font=("", 6), bd=0).grid(row=0, column=1, sticky=SW, padx=(7, 0), pady=0)

        options_var = []
        categories_var = []

        self.armour_choices = tk.OptionMenu(self.frame, self.armour_var, tuple(options_var))
        self.armour_choices.config(width=20, font=("", 10))
        self.armour_choices.grid(row=1, column=0, pady=0)

        self.armour_categories = tk.OptionMenu(self.frame, self.armour_category_var, tuple(categories_var))
        self.armour_categories.config(width=10, font=("", 10))
        self.armour_categories.grid(row=1, column=1, pady=0)

        armour_variable_frame = tk.Frame(self.frame)
        armour_variable_frame.grid(row=2, column=0, columnspan=2, sticky=W, padx=(7, 0))

        tk.Label(armour_variable_frame, textvariable=self.armour_ac_bonus_var, font=("", 12), width=6).grid(row=0, column=0)
        tk.Label(armour_variable_frame, textvariable=self.armour_max_dex_var, font=("", 12), width=6).grid(row=0, column=1)
        tk.Label(armour_variable_frame, textvariable=self.armour_check_penalty_var, font=("", 12), width=6).grid(row=0, column=2)
        tk.Label(armour_variable_frame, textvariable=self.armour_spell_failure_var, font=("", 12), width=6).grid(row=0, column=3)
        tk.Label(armour_variable_frame, textvariable=self.armour_weight_var, font=("", 12), width=6).grid(row=0, column=4)

        tk.Label(armour_variable_frame, text="AC BONUS", font=("", 6), bd=0).grid(row=1, column=0, sticky=N, pady=0)
        tk.Label(armour_variable_frame, text="MAX DEX", font=("", 6), bd=0).grid(row=1, column=1, sticky=N, pady=0)
        tk.Label(armour_variable_frame, text="CHECK\nPENALTY", font=("", 6), bd=0).grid(row=1, column=2, sticky=N, pady=0)
        tk.Label(armour_variable_frame, text="SPELL\nFAILURE", font=("", 6), bd=0).grid(row=1, column=3, sticky=N, pady=0)
        tk.Label(armour_variable_frame, text="WEIGHT", font=("", 6), bd=0).grid(row=1, column=4, sticky=N, pady=0)


class Shield:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.shield_var = tk.StringVar()
        self.shield_category_var = tk.StringVar()
        self.shield_ac_bonus_var = tk.StringVar()
        self.shield_max_dex_var = tk.StringVar()
        self.shield_check_penalty_var = tk.StringVar()
        self.shield_spell_failure_var = tk.StringVar()
        self.shield_weight_var = tk.StringVar()

        tk.Label(self.frame, text="SHIELD", font=("", 10, 'bold'), bd=0).grid(row=0, column=0, sticky=SW, padx=(7, 0), pady=0)
        tk.Label(self.frame, text="CATEGORY", font=("", 6), bd=0).grid(row=0, column=1, sticky=SW, padx=(7, 0), pady=0)

        options_var = []
        categories_var = []

        self.shield_choices = tk.OptionMenu(self.frame, self.shield_var, tuple(options_var))
        self.shield_choices.config(width=20, font=("", 10))
        self.shield_choices.grid(row=1, column=0, pady=0)

        self.shield_categories = tk.OptionMenu(self.frame, self.shield_category_var, tuple(categories_var))
        self.shield_categories.config(width=10, font=("", 10))
        self.shield_categories.grid(row=1, column=1, pady=0)

        shield_variable_frame = tk.Frame(self.frame)
        shield_variable_frame.grid(row=2, column=0, columnspan=2, sticky=W, padx=(7, 0))

        tk.Label(shield_variable_frame, textvariable=self.shield_ac_bonus_var, font=("", 12), width=6).grid(row=0, column=0)
        tk.Label(shield_variable_frame, textvariable=self.shield_max_dex_var, font=("", 12), width=6).grid(row=0, column=1)
        tk.Label(shield_variable_frame, textvariable=self.shield_check_penalty_var, font=("", 12), width=6).grid(row=0, column=2)
        tk.Label(shield_variable_frame, textvariable=self.shield_spell_failure_var, font=("", 12), width=6).grid(row=0, column=3)
        tk.Label(shield_variable_frame, textvariable=self.shield_weight_var, font=("", 12), width=6).grid(row=0, column=4)

        tk.Label(shield_variable_frame, text="AC BONUS", font=("", 6), bd=0).grid(row=1, column=0, sticky=N, pady=0)
        tk.Label(shield_variable_frame, text="MAX DEX", font=("", 6), bd=0).grid(row=1, column=1, sticky=N, pady=0)
        tk.Label(shield_variable_frame, text="CHECK\nPENALTY", font=("", 6), bd=0).grid(row=1, column=2, sticky=N, pady=0)
        tk.Label(shield_variable_frame, text="SPELL\nFAILURE", font=("", 6), bd=0).grid(row=1, column=3, sticky=N, pady=0)
        tk.Label(shield_variable_frame, text="WEIGHT", font=("", 6), bd=0).grid(row=1, column=4, sticky=N, pady=0)


class Weapon:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2)

        self.weapon_var = tk.StringVar()
        self.weapon_category_var = tk.StringVar()
        self.weapon_proficiency_var = tk.StringVar()
        self.weapon_attack_bonus_var = tk.StringVar()
        self.weapon_damage_var = tk.StringVar()
        self.weapon_critical_var = tk.StringVar()
        self.weapon_range_var = tk.StringVar()
        self.weapon_weight_var = tk.StringVar()

        tk.Label(self.frame, text="WEAPON", font=("", 10, 'bold'), bd=0).grid(row=0, column=0, sticky=SW, padx=(7, 0), pady=0)
        tk.Label(self.frame, text="CATEGORY", font=("", 6), bd=0).grid(row=0, column=1, sticky=SW, padx=(7, 0), pady=0)
        tk.Label(self.frame, text="PROFICIENCY", font=("", 6), bd=0).grid(row=0, column=2, sticky=SW, padx=(7, 0), pady=0)

        options_var = []
        categories_var = []
        proficiencies_var = []

        self.weapon_choices = tk.OptionMenu(self.frame, self.weapon_var, tuple(options_var))
        self.weapon_choices.config(width=21, font=("", 10))
        self.weapon_choices.grid(row=1, column=0, pady=0)

        self.weapon_categories = tk.OptionMenu(self.frame, self.weapon_category_var, tuple(categories_var))
        self.weapon_categories.config(width=17, font=("", 10))
        self.weapon_categories.grid(row=1, column=1, pady=0)

        self.weapon_proficiencies = tk.OptionMenu(self.frame, self.weapon_proficiency_var, tuple(proficiencies_var))
        self.weapon_proficiencies.config(width=9, font=("", 10))
        self.weapon_proficiencies.grid(row=1, column=2, pady=0)

        weapon_variable_frame = tk.Frame(self.frame)
        weapon_variable_frame.grid(row=2, column=0, columnspan=3, stick=W, padx=(7, 0))

        tk.Label(weapon_variable_frame, textvariable=self.weapon_attack_bonus_var, font=("", 12), anchor=W, width=12).grid(row=0, column=0, sticky=W)
        tk.Label(weapon_variable_frame, textvariable=self.weapon_damage_var, font=("", 12), width=7).grid(row=0, column=1)
        tk.Label(weapon_variable_frame, textvariable=self.weapon_critical_var, font=("", 12), width=8).grid(row=0, column=2)
        tk.Label(weapon_variable_frame, textvariable=self.weapon_range_var, font=("", 12), width=6).grid(row=0, column=3)
        tk.Label(weapon_variable_frame, textvariable=self.weapon_weight_var, font=("", 12), width=6).grid(row=0, column=4)

        tk.Label(weapon_variable_frame, text="ATTACK BONUS", font=("", 6), bd=0).grid(row=1, column=0, sticky=NW, pady=0)
        tk.Label(weapon_variable_frame, text="DAMAGE", font=("", 6), bd=0).grid(row=1, column=1, sticky=N, pady=0)
        tk.Label(weapon_variable_frame, text="CRITICAL", font=("", 6), bd=0).grid(row=1, column=2, sticky=N, pady=0)
        tk.Label(weapon_variable_frame, text="RANGE\nINCREMENT", font=("", 6), bd=0).grid(row=1, column=3, sticky=N, pady=0)
        tk.Label(weapon_variable_frame, text="WEIGHT", font=("", 6), bd=0).grid(row=1, column=4, sticky=N, pady=0)

class Skills:
    def __init__(self, parent, control):
        self.frame = tk.Frame(parent, bd=2)

        self.skills_list = []

        tk.Label(self.frame, text="SKILL NAME", font=("", 10, "bold"), width=11, anchor=W).grid(row=0, column=0, sticky=SW)
        tk.Label(self.frame, text="KEY\nABILITY", font=("", 6), width=5).grid(row=0, column=1, sticky=S)
        tk.Label(self.frame, text="SKILL\nMODIFIER", font=("", 6), width=7).grid(row=0, column=2, sticky=S)
        tk.Label(self.frame, text="ABILITY\nMODIFIER", font=("", 6), width=6).grid(row=0, column=3, sticky=S)
        tk.Label(self.frame, text="RANKS", font=("", 6), width=5).grid(row=0, column=4, sticky=S)

        frame = tk.Frame(self.frame)
        frame.grid(row=1, columnspan=6, sticky=W, pady=(2,0))

        canvas = tk.Canvas(frame)
        f = tk.Frame(canvas)

        yscrollbar = tk.Scrollbar(frame)
        yscrollbar.pack(side=RIGHT, fill=Y)
        yscrollbar.config(command=canvas.yview)

        for i, v in enumerate(control.SKILLS_LIST):
            skill = Skill(f, i)
            skill.skill_name.set("%s" % v)
            skill.key_ability.set("%s" % control.SKILLS.get(v).get('key_ability'))
            self.skills_list.append(skill)

        canvas.create_window(0, 0, window=f, anchor='nw')
        canvas.config(yscrollcommand=yscrollbar.set)
        canvas.config(width=260, height=385)
        canvas.pack(side=LEFT, expand=True, fill=BOTH)

        self.frame.update()
        canvas.config(scrollregion=canvas.bbox("all"))



class Skill:
    def __init__(self, parent, r):
        self.skill_name = tk.StringVar()
        self.key_ability = tk.StringVar()
        self.skill_mod_var = tk.StringVar()
        self.ability_mod_var = tk.StringVar()
        self.ranks_var = tk.StringVar()

        tk.Label(parent, textvariable=self.skill_name, font=("", 10), width=14, anchor=W).grid(row=r, column=0)
        tk.Label(parent, textvariable=self.key_ability, font=("", 8), width=3).grid(row=r, column=1)
        tk.Label(parent, textvariable=self.skill_mod_var, font=("", 14), width=7).grid(row=r, column=2)
        tk.Label(parent, textvariable=self.ability_mod_var, font=("", 12), width=2).grid(row=r, column=3)