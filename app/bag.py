import pygame
from random import randint, uniform
from os import path

class Bag():
    def __init__(self, druh, img, txt):
        self.druh = druh
        self.img = pygame.image.load(path.join("images", f"{img}"))
        self.txt = txt
        self.pocet = 2

    def get_img(self):
        return self.img


def eat(pet, ovocie):
    if ovocie.druh == "ceresne" and pet.druh == "ohen":
            return randint(28, 35)

    if ovocie.druh == "banan" and pet.druh == "svetlo":
            return randint(28, 35)

    if ovocie.druh == "hruska" and pet.druh == "zem":
            return randint(28, 35)
    return randint(17, 23)

def rise_heal():
    return uniform(1.12, 1.22)  #1.60, 2.1

def rise_hp():
    return uniform(1.48, 1.73)

def rise_dmg():
    return uniform(1.12, 1.22)

def less_sleep():
    return uniform(0.16, 0.38)  # 0.65, 0.84

def less_food():
    return uniform(0.25, 0.49)

def more_coin():
    return uniform(0.75, 0.86)

def vacsia_vydrz():
    return uniform(0.7, 0.85)    # 0.7, 0.9

def lacnejsie_upgrady():
    return uniform(0.2, 0.5)

def vacsie_upgrade():
    return uniform(1.06, 1.14)



ceresne = Bag("ceresne", "ceresne.png", "")
banan = Bag("banan", "banan.png", "")
hruska = Bag("hruska", "hruska.png", "")

heal = Bag("heal", "heal.png", "12-22% increase in healing")
hp = Bag("hp", "hp.png", "12-17% increase in health")
dmg = Bag("dmg", "dmg.png", "12-22% increase in damage")
sleep = Bag("sleep", "sleep.png", "Less sleepy after fight")
food = Bag("food", "food.png", "Less hungry after fight ")
coin = Bag("coin", "coin.png", "14-25% more coins after won fight")
resistance = Bag("resistance", "resistance.png", "You will be stronger in fight")
sale = Bag("sale", "sale.png", "Lower prices for upgrade pets")
upgrade = Bag("upgrade", "upgrade.png", "Higher upgrades for pets")