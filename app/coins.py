from pygame import image
from random import randint
import os

class Coin():
    def __init__(self, imgs, actual_money):
        self.imgs = imgs
        self.animation_count = 0
        self.actual_money = actual_money
        self.count_for_money = 0        # aby sa ti pripočitali peniaze na konci suboju
        self.v_h = 0            # vyhrate_money
        self.p_h = 0            # prehrate money
        self.coins_per_sec = 0.18
        self.upgrade_lvl = 0  # ukazuje na akom lvli je bana

    def get_width(self):
        return self.imgs[0].get_width()

    def get_height(self):
        return self.imgs[0].get_height()

    def animation_coin(self, count):
        coin_img = self.imgs[count // 4]
        count += 1
        if count >= len(self.imgs) * 4:
            count = 0

        return coin_img

    def vyhrate_money(self, health_hero, health_monster):   # vyhrate money po 1v1 suboji
        return randint(40, 90)

    def prehrate_money(self, health_hero, health_monster):  # vyhrate money po 1v1 suboji
        return randint(5, 10)

    def upgrade_mines(self):
        self.coins_per_sec = round(self.coins_per_sec * 1.13, 2)
        self.actual_money -= 250


coins = Coin([image.load(os.path.join("images", "minca1.png")), image.load(os.path.join("images", "minca2.png")), image.load(os.path.join("images", "minca3.png")), image.load(os.path.join("images", "minca_stred.png")), image.load(os.path.join("images", "minca4.png")), image.load(os.path.join("images", "minca5.png"))], 500)

coins_ohen = Coin([image.load(os.path.join("images", "ohen_minca1.png")), image.load(os.path.join("images", "ohen_minca2.png")), image.load(os.path.join("images", "ohen_minca3.png")), image.load(os.path.join("images", "ohen_minca_stred.png")), image.load(os.path.join("images", "ohen_minca4.png")), image.load(os.path.join("images", "ohen_minca5.png"))], 600)
coins_svetlo = Coin([image.load(os.path.join("images", "svetlo_minca1.png")), image.load(os.path.join("images", "svetlo_minca2.png")), image.load(os.path.join("images", "svetlo_minca3.png")), image.load(os.path.join("images", "svetlo_minca_stred.png")), image.load(os.path.join("images", "svetlo_minca4.png")), image.load(os.path.join("images", "svetlo_minca5.png"))], 600)
coins_zem = Coin([image.load(os.path.join("images", "zem_minca1.png")), image.load(os.path.join("images", "zem_minca2.png")), image.load(os.path.join("images", "zem_minca3.png")), image.load(os.path.join("images", "zem_minca_stred.png")), image.load(os.path.join("images", "zem_minca4.png")), image.load(os.path.join("images", "zem_minca5.png"))], 600)