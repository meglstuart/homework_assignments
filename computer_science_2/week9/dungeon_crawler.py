"""
Multiple inheritance, MRO, the diamond problem, multilevel inheritance, and super()
===================================================================================

Built on top of the dungeon demo. Class hierarchy:

    LootableObject                 Character              (Chest is separate)
         |     \\                 /       \\                    |
       Weapon  Loot             Hero       Enemy                 |
         |                     /    \\        |                  |
    MagicWeapon             Mage  Warrior   Boss                 |
         |                     \\    /         \\                 |
    LegendaryWeapon          SpellKnight        +------ Mimic ---+
                                                (Chest + Enemy)

    Multilevel inheritance : LootableObject -> Weapon -> MagicWeapon -> LegendaryWeapon
                             Character -> Enemy -> Boss
    Multiple inheritance   : Mimic(Chest, Enemy)          (two unrelated parents)
    Diamond inheritance    : SpellKnight(Mage, Warrior)   (both inherit from Hero)

"""

# ---------------------------------------------------------------------------
# Tiny tracing helper so we can SEE which __init__ methods run, and how often.
# ---------------------------------------------------------------------------
init_trace = []


def trace(label):
    init_trace.append(label)


# ===========================================================================
# LOOTABLE OBJECTS  (multilevel inheritance: 4 levels deep)
# ===========================================================================
class LootableObject:
    """Base class for anything that can be found, carried, and valued."""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} (worth {self.value} gold)"


class Weapon(LootableObject):
    """A lootable object that can also deal damage."""

    def __init__(self, name, damage, value=0):
        super().__init__(name, value)
        self.damage = damage
        
    def __str__(self):
        return super().__str__() + f" (damage {self.damage})"


class MagicWeapon(Weapon):
    """Level 3: a weapon infused with an element."""

    def __init__(self, name, damage, element, value=0):
        super().__init__(name, damage, value)
        self.element = element

    def __str__(self):
        # super().__str__() runs Weapon.__str__, and we extend its result
        return super().__str__() + f" [{self.element} magic]"


class LegendaryWeapon(MagicWeapon):
    """Level 4: a magic weapon with a story attached."""

    def __init__(self, name, damage, element, lore, value=0):
        super().__init__(name, damage, element, value)
        self.lore = lore

    def __str__(self):
        return super().__str__() + f' -- "{self.lore}"'


class Loot(LootableObject):
    """Plain treasure. Everything it needs is inherited from LootableObject."""
    pass


# ===========================================================================
# CHEST  
# ===========================================================================
class Chest:
    def __init__(self, loot_items, **kwargs):
        trace("Chest.__init__")
        self.loot_items = loot_items
        # Pass any leftover keyword arguments to the NEXT class in the MRO.
        # If Chest is used alone, that next class is just `object`.
        super().__init__(**kwargs)

    def open(self):
        """Return all loot and leave the chest empty."""
        contents = self.loot_items
        self.loot_items = []
        return contents

    def __str__(self):
        string_rep = 'Chest Contents:\n'
        for loot in self.loot_items:
            string_rep += f'  {loot}\n'
        return string_rep


# ===========================================================================
# CHARACTERS
# ===========================================================================
class Character:
    """Base class for anything that can fight: has a name, health, and weapon."""

    def __init__(self, name, health, weapon, **kwargs):
        trace("Character.__init__")
        self.name = name
        self.health = health
        self.weapon = weapon
        super().__init__(**kwargs)   # next in the MRO (object, or a sibling)

    def is_alive(self):
        return self.health > 0

    def strike(self, weapon):
        """Called when this character is hit by a weapon."""
        self.health -= weapon.damage
        print(f"  {self.name} is hit by {weapon.name} for {weapon.damage}. "
              f"Health: {max(self.health, 0)}")

    def attack(self, target):
        """Attack another character with this character's weapon."""
        print(f"{self.name} attacks {target.name} with {self.weapon.name}!")
        target.strike(self.weapon)


class Hero(Character):
    """A character that can also collect loot."""

    def __init__(self, name, health, weapon, **kwargs):
        trace("Hero.__init__")
        super().__init__(name, health, weapon, **kwargs)
        self.loot = []

    def pick_up(self, loot_items):
        for item in loot_items:
            self.loot.append(item)
            print(f"  {self.name} picked up {item}")

    def total_loot_value(self):
        return sum(item.value for item in self.loot)


class Enemy(Character):
    """A hostile character. Fighting behavior is inherited from Character."""
    pass


# ---------------------------------------------------------------------------
# MULTILEVEL INHERITANCE:  Character -> Enemy -> Boss
# ---------------------------------------------------------------------------
class Boss(Enemy):
    """Level 3: a tougher enemy that becomes enraged at half health."""

    def __init__(self, name, health, weapon, **kwargs):
        trace("Boss.__init__")
        super().__init__(name, health, weapon, **kwargs)
        self.max_health = health
        self.enraged = False

    def strike(self, weapon):
        super().strike(weapon)   # Character.strike does the actual damage
        if self.is_alive() and not self.enraged and self.health < self.max_health / 2:
            self.enraged = True
            self.weapon.damage = int(self.weapon.damage * 1.5)
            print(f"  *** {self.name} is ENRAGED! Damage is now {self.weapon.damage} ***")


# ---------------------------------------------------------------------------
# MULTIPLE INHERITANCE:  Mimic is a Chest AND an Enemy
# ---------------------------------------------------------------------------
class Mimic(Chest, Enemy):
    """Looks like a Chest, fights like an Enemy. Chest and Enemy are unrelated."""

    def __init__(self, loot_items, name="Mimic", health=40, weapon=None):
        trace("Mimic.__init__")
        weapon = weapon or Weapon("Sharp Teeth", 10)
        # One super() call starts the chain: Mimic -> Chest -> Enemy -> Character
        super().__init__(loot_items=loot_items, name=name,
                         health=health, weapon=weapon)

    def open(self):
        print("  The Mimic's remains spill out its hoard...")
        return super().open()    # Chest.open


# ---------------------------------------------------------------------------
# THE DIAMOND:  SpellKnight(Mage, Warrior), both inherit from Hero
#
#                Hero
#               /    \
#            Mage    Warrior
#               \    /
#             SpellKnight
# ---------------------------------------------------------------------------
class Mage(Hero):
    def __init__(self, *, mana=50, **kwargs):
        trace("Mage.__init__")
        super().__init__(**kwargs)
        self.mana = mana

    def cast_fireball(self, target):
        if self.mana < 20:
            print(f"  {self.name} is out of mana!")
            return
        self.mana -= 20
        fireball = MagicWeapon("Fireball", 25, "fire")
        print(f"{self.name} casts Fireball at {target.name}! (mana left: {self.mana})")
        target.strike(fireball)

    def attack(self, target):
        self.mana += 5
        print(f"  [Mage] {self.name} draws in mana (+5 -> {self.mana})")
        super().attack(target)


class Warrior(Hero):
    def __init__(self, *, rage=0, **kwargs):
        trace("Warrior.__init__")
        super().__init__(**kwargs)
        self.rage = rage

    def attack(self, target):
        self.rage += 10
        print(f"  [Warrior] {self.name}'s rage builds (+10 -> {self.rage})")
        if self.rage >= 30:
            print(f"  [Warrior] {self.name} is ENRAGED!")
            old_damage = self.weapon.damage
            self.weapon.damage *= 2
            super().attack(target)
            self.weapon.damage = old_damage
            self.rage = 0
        else:
            super().attack(target)


class SpellKnight(Mage, Warrior):
    """Gets BOTH Mage and Warrior behavior. No code needed -- the MRO does it."""
    pass


# ===========================================================================
# DEMO HELPERS
# ===========================================================================
def banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def show_mro(cls):
    print(f"{cls.__name__}.__mro__:")
    print("  " + " -> ".join(c.__name__ for c in cls.__mro__))

# ===========================================================================
# DUNGEON
# ===========================================================================
class Dungeon:
    def __init__(self, hero, chests, enemies):
        self.hero = hero
        self.chests = chests
        self.enemies = enemies

    def fight(self, enemy):
        """Hero and enemy trade blows until one falls."""
        print(f"\n--- {self.hero.name} encounters {enemy.name}! ---")
        while self.hero.is_alive() and enemy.is_alive():
            # Mages like to open with a fireball
            if isinstance(self.hero, Mage) and self.hero.mana >= 20:
                self.hero.cast_fireball(enemy)
            else:
                self.hero.attack(enemy)
            if enemy.is_alive():
                enemy.attack(self.hero)
        if self.hero.is_alive():
            print(f"{enemy.name} has been defeated!")
        else:
            print(f"{self.hero.name} has fallen...")

    def explore(self):
        """Fight each enemy, then loot a chest after each victory."""
        print(f"{self.hero.name} enters the dungeon with "
              f"{self.hero.health} health, wielding {self.hero.weapon}.")

        chests = list(self.chests)
        for enemy in self.enemies:
            self.fight(enemy)
            if not self.hero.is_alive():
                break
            if chests:
                chest = chests.pop(0)
                print(f"\n{self.hero.name} approaches a chest...")
                # A Mimic IS a Chest, so it lives in the chest list --
                # but it is also an Enemy, so isinstance lets us catch it.
                if isinstance(chest, Enemy):
                    print("  It's a MIMIC!")
                    self.fight(chest)
                    if not self.hero.is_alive():
                        break
                print(f"{self.hero.name} opens the chest:")
                self.hero.pick_up(chest.open())

        self.report()

    def report(self):
        print("\n=== Dungeon report ===")
        if self.hero.is_alive():
            print(f"{self.hero.name} survived with {self.hero.health} health.")
        else:
            print(f"{self.hero.name} did not survive.")
        print(f"Loot collected: {len(self.hero.loot)} items, "
              f"worth {self.hero.total_loot_value()} gold")


def demo_dungeon():
    banner("Dungeon Destroyer")

    hero = SpellKnight(name="Aria", health=150,
                       weapon=LegendaryWeapon("Dawnbringer", 18, "light",
                                              "Forged from a fallen star", value=500),
                       mana=60)
    print(f"Hero class: {type(hero).__name__}  (MRO: "
          f"{' -> '.join(c.__name__ for c in type(hero).__mro__)})\n")

    enemies = [
        Enemy("Goblin", 30, Weapon("Rusty Dagger", 5)),
        Boss("Orc Warlord", 70, Weapon("War Axe", 12)),
    ]
    chests = [
        Chest([Loot("Silver Coin", 10), Loot("Ruby", 50)]),
        Mimic([Loot("Gold Goblet", 75),
               MagicWeapon("Frost Spear", 20, "ice", value=150)]),
    ]
    Dungeon(hero, chests, enemies).explore()


if __name__ == "__main__":
    demo_dungeon()