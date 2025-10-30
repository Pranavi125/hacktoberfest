#!/usr/bin/env python3
"""
Alice in Wonderland — tiny interactive Python adventure
Run: python alice_adventure.py
"""

import sys
import random
import textwrap

WRAP = 70

def wprint(text=""):
    print("\n".join(textwrap.wrap(text, WRAP)))

def prompt(options):
    """Show numbered options and return chosen index (0-based)."""
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        choice = input("Choose a number: ").strip()
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(options):
                return n - 1
        print("Please enter a valid number.")

class Game:
    def __init__(self):
        self.inventory = set()
        self.curiouser = 0  # curiosity meter, affects outcomes

    def start(self):
        wprint("You are Alice. You wake on a sunny bank and notice a curious rabbit wearing a waistcoat.")
        wprint("Something shiny glints from the rabbit's pocket. You can follow the rabbit or explore the bank.")
        idx = prompt(["Follow the White Rabbit", "Explore the bank / have a nap"])
        if idx == 0:
            self.follow_rabbit()
        else:
            self.bank_path()

    def follow_rabbit(self):
        self.curiouser += 1
        wprint("You follow the rabbit down a hole — it's deeper than it looks! You tumble through a corridor of floating clocks.")
        wprint("At the bottom there's a corridor with three doors and a small cake labelled 'EAT ME'.")
        idx = prompt(["Open the big blue door", "Try the tiny keyhole", "Eat the 'EAT ME' cake"])
        if idx == 0:
            self.big_blue_door()
        elif idx == 1:
            self.tiny_keyhole()
        else:
            self.eat_cake()

    def bank_path(self):
        wprint("You wander around, daydreaming. A Caterpillar appears on a mushroom and asks you a riddle.")
        riddle = random.choice([
            ("Why is a raven like a writing desk?", "Because it can produce a few notes, though they are very flat; and it is nevar put with the wrong end in front."),
            ("What goes on four legs in the morning...", "Man (a classical riddle)"),
        ])
        wprint("Caterpillar asks: " + riddle[0])
        idx = prompt(["Answer the riddle", "Ignore and walk on"])
        if idx == 0:
            wprint("You give a thoughtful answer. The Caterpillar grants you a magic mushroom slice.")
            self.inventory.add("mushroom-slice")
            self.curiouser += 1
            self.follow_rabbit()
        else:
            wprint("You yawn and keep walking. Suddenly, everything goes a little sideways... you feel smaller.")
            self.inventory.add("shrunk")
            self.curiouser -= 1
            self.follow_rabbit()

    def big_blue_door(self):
        wprint("The big blue door swings open to a grand garden — the Queen's gardeners are painting roses red.")
        idx = prompt(["Sneak past the gardeners", "Talk to the gardeners", "Pick a rose and run"])
        if idx == 0:
            self.sneak_garden()
        elif idx == 1:
            self.talk_gardeners()
        else:
            self.pick_rose()

    def tiny_keyhole(self):
        wprint("You peer through the tiny keyhole and see a teapot on a table. It's just the size for a mouse.")
        if "mushroom-slice" in self.inventory:
            wprint("You remember the mushroom slice. Eat a bit to shrink and slip through?")
            idx = prompt(["Eat mushroom slice", "Don't eat it"])
            if idx == 0:
                self.inventory.discard("mushroom-slice")
                self.inventory.add("small")
                wprint("You shrink down to mouse-size and squeeze through the keyhole into a cosy tea room.")
                self.teaparty()
                return
        wprint("You cannot fit, but a mouse offers to help if you find some biscuit crumbs.")
        idx = prompt(["Search nearby for crumbs", "Give up and go back"])
        if idx == 0:
            if random.random() < 0.6:
                wprint("You find crumbs! The mouse helps you inside.")
                self.inventory.add("small")
                self.teaparty()
            else:
                wprint("No crumbs today. You head back, empty-handed.")
                self.follow_rabbit()
        else:
            self.follow_rabbit()

    def eat_cake(self):
        wprint("You nibble the cake. You feel odd... taller. Very tall.")
        self.inventory.add("tall")
        self.curiouser += 1
        wprint("From your height you can see a croquet ground. The Queen is nearby. She doesn't like tall newcomers.")
        idx = prompt(["Hide behind a hedge", "Approach the Queen politely"])
        if idx == 0:
            self.hide_hedge()
        else:
            self.approach_queen()

    def teaparty(self):
        wprint("You join a mad tea party with the Hatter and March Hare. They serve riddles and nonsensical tea.")
        idx = prompt(["Join the riddles", "Steal a cup and run", "Offer a riddle of your own"])
        if idx == 0:
            self.riddle_session()
        elif idx == 1:
            wprint("You dash off with a steaming cup. The Hatter shrieks but the March Hare laughs.")
            self.curiouser += 1
            self.big_blue_door()
        else:
            self.offer_riddle()

    def riddle_session(self):
        wprint("Their riddles make you laugh so hard that you learn a secret: a door behind a portrait opens with music.")
        self.inventory.add("music-note")
        self.curiouser += 1
        self.big_blue_door()

    def offer_riddle(self):
        wprint("You offer a clever riddle. They applaud so loudly the Dormouse wakes and points you toward the Queen's garden.")
        self.big_blue_door()

    def sneak_garden(self):
        wprint("You creep past the gardeners. A card soldier spots you and challenges you to a silly game.")
        idx = prompt(["Play along", "Refuse and run"])
        if idx == 0:
            if self.curiouser > 0 or "music-note" in self.inventory:
                wprint("You play the game cleverly and earn a tiny painted rose (they call you 'creative').")
                self.inventory.add("painted-rose")
                self.win_game()
            else:
                wprint("You fumble the rules and the card soldier reports you. The Queen shouts 'Off with their head!'")
                self.ending_bad()
        else:
            self.follow_rabbit()

    def talk_gardeners(self):
        wprint("You talk politely. They reveal they're painting roses because the Queen can't be bothered to grow them red.")
        self.inventory.add("garden-secret")
        self.big_blue_door()

    def pick_rose(self):
        wprint("You pick a rose. The gardener gasps — the Queen notices and chases after you.")
        if "small" in self.inventory:
            wprint("You slip into a rabbit hole and escape. Safe... for now.")
            self.win_game()
        else:
            self.ending_bad()

    def hide_hedge(self):
        wprint("Hidden in the hedge you overhear a conspiracy: the Knave is being accused of stealing tarts.")
        idx = prompt(["Help the Knave prove innocence", "Stay hidden — it's risky"])
        if idx == 0:
            self.prove_knave()
        else:
            self.follow_rabbit()

    def approach_queen(self):
        wprint("You approach. The Queen looks at you with suspicion. 'Why are you so tall?' she asks.")
        if "mushroom-slice" in self.inventory or "small" in self.inventory:
            wprint("Your size confuses her less. She laughs and invites you to croquet. You play and impress her.")
            self.win_game()
        else:
            wprint("The Queen is not impressed. Guards appear, and you tumble away.")
            self.ending_bad()

    def prove_knave(self):
        wprint("You gather evidence: crumbs, the painted-rose, and the garden-secret. The court listens.")
        if "painted-rose" in self.inventory or "music-note" in self.inventory:
            wprint("Your evidence is convincing. The Knave is freed and thanks you warmly. The Queen reluctantly applauds.")
            self.win_game()
        else:
            wprint("Your evidence is thin. The Queen is unconvinced. You're sent to fetch more clues.")
            self.follow_rabbit()

    def win_game(self):
        endings = [
            "The Queen, in a rare good mood, grants you a curious medal saying 'For Very Curious Behavior'.",
            "You find yourself back on the bank, holding a painted rose — was it all a dream?",
            "A Cheshire Cat appears, grins, and says 'You're quite all right.' You wake up smiling."
        ]
        wprint(random.choice(endings))
        self.end(True)

    def ending_bad(self):
        endings = [
            "The Queen shouts and you are chased — you tumble, awake, and realise it was the sun on your face.",
            "Guards escort you away; you manage a narrow escape but lose some belongings.",
            "You wake up in a teapot. The Dormouse scowls. You decide to be more careful next time."
        ]
        wprint(random.choice(endings))
        self.end(False)

    def end(self, won):
        print("\n" + ("🎉 You finished the adventure — a good ending!" if won else "😅 That was rough — try again!"))
        print("Inventory:", ", ".join(sorted(self.inventory)) if self.inventory else "empty")
        again = prompt(["Play again", "Quit"])
        if again == 0:
            self.__init__()
            self.start()
        else:
            wprint("Goodbye — may your curiosity never end!")
            sys.exit(0)

if __name__ == "__main__":
    Game().start()
