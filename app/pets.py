import pygame
from random import randint
from math import sqrt, floor
from coins import *
from os import path

working_path_pets = os.getcwd() + "\images"
class Pet(Coin):
    def __init__(self, img, health, damage1, damage2, reg1, reg2, name, druh, utok, druh_coin, super_pow):
        self.img = pygame.image.load(path.join("images", f"{img}"))
        self.health = health
        self.damage1 = damage1
        self.damage2 = damage2
        self.reg1 = reg1
        self.reg2 = reg2
        self.name = name
        self.druh = druh
        self.utok = utok
        self.druh_coin = druh_coin
        self.super_pow = super_pow
        self.sleep = 100
        self.cas_od_kedy_spi = None
        self.less_sleep = 1     # je to premenna ktora sa podiela na vypocte sleep (teda koklo sa ti po suboji ubere) a tuto premennu meni elixir --> less_sleep, premenna udava percento o kolko menej budu pets ospale
        self.less_food = 1
        self.more_coin = 1
        self.resistance = 1     # budes odolnjsi v subojoch teda ze ti bude monster uberat menej
        self.sale = 1           # budu lacnejsie upgrady
        self.more_upgrade = 1   # za rovnaku cenu vacsi upgrade
        self.food = 100
        self.lvl = 1
        self.elixir = None      # ak nebude mat nijaky elixir tak moze mat 1, ak uz ma sa mu bude zobrazovat v lavom rohu lebo ja do tejto premennej vlozit objekt Bag a ten ma atribut img
        self.elixir_duration = 2
        self.elixir_ucinok = None


    def get_img(self):
        return self.img

    def get_health(self):
        return int(self.health)

    def get_damage(self):
        return randint(int(self.damage1 * sqrt(self.sleep *.01 * self.food * .01)), int(self.damage2 * sqrt(self.sleep *.01 * self.food * .01)))

    def get_super_damage(self):
        return randint(int(self.damage1 * 1.86 * sqrt(self.sleep *.01 * self.food * .01)), int(self.damage2 * 1.86 * sqrt(self.sleep *.01 * self.food * .01)))

    def get_regeneration(self):
        return randint(int(self.reg1 * sqrt(self.sleep *.01 * self.food * .01)), int(self.reg2 * sqrt(self.sleep *.01 * self.food * .01)))

    def get_reg(self):
        return "{} - {}".format(int(self.reg1), int(self.reg2))

    def get_dmg(self):
        return "{} - {}".format(int(self.damage1), int(self.damage2))

    def get_sleep(self):
        return int(self.sleep)

    def get_food(self):
        return int(self.food)

    def get_name(self):
        return self.name

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def get_cena(self):
        return int(self.health * 3)

    def get_trieda(self):
        return self.druh

    def get_tired(self):
        return randint(1, 5)

    def get_hunger(self):
        return randint(2, 6)


    def cena_upgrade(self):
        return int((sqrt(self.health) * 2 + round((self.damage1 + self.damage2) / 3 * 1.04)) * self.sale)


    def upgrade(self):
        self.health = round(self.health * 1.07 * self.more_upgrade)

        self.reg1 = round(self.reg1 * 1.07 * self.more_upgrade)
        self.reg2 = round(self.reg2 * 1.07 * self.more_upgrade)

        self.damage1 = round(self.damage1 * 1.07 * self.more_upgrade)
        self.damage2 = round(self.damage2 * 1.07 * self.more_upgrade)



class Monster(Pet):
    def __init__(self, img):
        super(Monster, self).__init__(img, None, None, None, None, None, None, None, None, None, None)

    def set_health_1v1(self, pet):
        self.health = randint(int(pet.health * 1.85), int(pet.health * 2.45))

        return self.health

    def set_health_until_die(self, health):
        self.health = randint(health // 4, health // 2.1)
        return self.health

    def set_health_boos(self, pets):      # nastavi HP Bossovi do win_fight_boss
        self.health = 0
        for pet in pets:
            self.health += pet.health
        self.health = randint(int(self.health * 2.05), int(self.health * 2.7))
        return self.health

    def get_damage_1v1(self, hp, pet):
        rozpatie_utoku = (self.health // pet.damage1, self.health // pet.damage2)
        utok1 = hp // rozpatie_utoku[0]
        utok2 = hp // rozpatie_utoku[1]

        return randint(int(utok1 * 1.2), int(utok2 * 1.2))

    def get_damage_until_die(self, pet):
        return randint(pet.damage1 // 4, pet.damage2 // 2.1)

    def get_damage_boss(self, boss_hp, pet_hp, pet):
        damage_pets = boss_hp // 4      # kolko musi ubrat kazdy z pets aby zabili bossa
        vydrz1 = damage_pets // pet.damage1 # kolko utokov od bossa musi vydrzat pet aby ubral ten damage_pets
        vydrz2 = damage_pets // pet.damage2
        return randint(int((pet_hp // vydrz1) * 1.55) if int((pet_hp // vydrz1) * 1.55) > 1 else pet_hp // 8, int((pet_hp // vydrz2) * 1.55) if int((pet_hp // vydrz2) * 1.55) > 1 else pet_hp // 7)



svetlo = [pygame.image.load(path.join(working_path_pets, "svetlo0.png")), pygame.image.load(path.join(working_path_pets, "svetlo1.png")), pygame.image.load(path.join(working_path_pets, "svetlo2.png")), pygame.image.load(path.join(working_path_pets, "svetlo3.png")), pygame.image.load(path.join(working_path_pets, "svetlo4.png"))]
ohen = [pygame.image.load(path.join(working_path_pets, "ohen0.png")), pygame.image.load(path.join(working_path_pets, "ohen1.png")), pygame.image.load(path.join(working_path_pets, "ohen2.png")), pygame.image.load(path.join(working_path_pets, "ohen3.png")), pygame.image.load(path.join(working_path_pets, "ohen4.png")), pygame.image.load(path.join(working_path_pets, "ohen5.png")), pygame.image.load(path.join(working_path_pets, "ohen6.png")), pygame.image.load(path.join("images", "ohen7.png"))]
zem = [pygame.image.load(path.join(working_path_pets, "zem0.png")), pygame.image.load(path.join(working_path_pets, "zem1.png")), pygame.image.load(path.join(working_path_pets, "zem2.png")), pygame.image.load(path.join(working_path_pets, "zem3.png")), pygame.image.load(path.join(working_path_pets, "zem4.png"))]

healing = [pygame.image.load(path.join(working_path_pets, "healing0.png")), pygame.image.load(path.join(working_path_pets, "healing1.png")), pygame.image.load(path.join(working_path_pets, "healing2.png")), pygame.image.load(path.join(working_path_pets, "healing3.png")), pygame.image.load(path.join(working_path_pets, "healing4.png")), pygame.image.load(path.join(working_path_pets, "healing5.png")), pygame.image.load(path.join(working_path_pets, "healing6.png"))]

tien = [pygame.image.load(path.join(working_path_pets, "tien0.png")), pygame.image.load(path.join(working_path_pets, "tien1.png")), pygame.image.load(path.join(working_path_pets, "tien2.png")), pygame.image.load(path.join(working_path_pets, "tien3.png")), pygame.image.load(path.join(working_path_pets, "tien4.png")), pygame.image.load(path.join(working_path_pets, "tien5.png")), pygame.image.load(path.join(working_path_pets, "tien6.png")), pygame.image.load(path.join("images", "tien7.png"))]


SuperUtok_svetlo = [pygame.image.load(path.join(working_path_pets, "super_svetlo0.png")), pygame.image.load(path.join(working_path_pets, "super_svetlo1.png")), pygame.image.load(path.join(working_path_pets, "super_svetlo2.png")), pygame.image.load(path.join(working_path_pets, "super_svetlo3.png")), pygame.image.load(path.join(working_path_pets, "super_svetlo4.png"))]
SuperUtok_ohen = [pygame.image.load(path.join(working_path_pets, "super_ohen0.png")), pygame.image.load(path.join(working_path_pets, "super_ohen1.png")), pygame.image.load(path.join(working_path_pets, "super_ohen2.png")), pygame.image.load(path.join(working_path_pets, "super_ohen3.png")), pygame.image.load(path.join(working_path_pets, "super_ohen4.png"))]
SuperUtok_zem = [pygame.image.load(path.join(working_path_pets, "super_zem0.png")), pygame.image.load(path.join(working_path_pets, "super_zem1.png")), pygame.image.load(path.join(working_path_pets, "super_zem2.png")), pygame.image.load(path.join(working_path_pets, "super_zem3.png")), pygame.image.load(path.join(working_path_pets, "super_zem4.png"))]





pet_trojocko = Pet("pet_trojocko.png", 71, 13, 18, 15, 21, "Nido", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_pav = Pet("pet_pav.png", 75, 15, 19, 14, 21, "Paon", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_pes_sgulou = Pet("pet_pes_sgulou.png", 77, 14, 20, 1, 5, "Hudy", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_gulko = Pet("pet_gulko.png", 79, 12, 14, 19, 5, "Melyn", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_slunce = Pet("pet_slunce.png", 82, 11, 17, 14, 18, "Solis", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_bojovnik = Pet("pet_bojovnik.png", 88, 9, 22, 13, 20, "Bellator", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_elektra = Pet("pet_elektra.png", 91, 10, 17, 13, 19, "Listrik", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_zvero_blesk = Pet("pet_zvero_blesk.png", 100, 9, 19, 13, 17, "Rayo", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_obluda = Pet("pet_obluda.png", 102, 9, 20, 13, 16, "Monis", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_svetlo_dog = Pet("pet_svetlo_dog.png", 103, 10, 20, 11, 18, "Hunden", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_helmet = Pet("pet_helmet.png", 107, 9, 21, 11, 17, "Helmet", "light", svetlo, coins_svetlo, SuperUtok_svetlo)
pet_jednorozec = Pet("pet_jednorožec.png", 114, 11, 21, 11, 16, "Jednorog", "light", svetlo, coins_svetlo, SuperUtok_svetlo)

pet_ohnivy_vtak = Pet("pet_ohnivy_vtak.png", 63, 20, 28, 18, 23, "Aderyn", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_vtak = Pet("pet_vtak.png", 66, 19, 26, 18, 22, "Lintu", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_guliocko = Pet("pet_guliocko.png", 69, 21, 28, 17, 23, "Hagi", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_rybka = Pet("pet_rybka.png", 72, 21, 24, 17, 22, "Fisk", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_ohniva_skala = Pet("pet_ohniva_skala.png", 73, 21, 26, 16, 22, "Sten", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_cvrecek = Pet("pet_cvrecek.png", 78, 22, 26, 16, 21, "Jang", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_kokohen = Pet("pet_kokohen.png", 81, 20, 25, 15, 23, "Gallus", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_zaba = Pet("pet_zaba.png", 85, 19, 25, 15, 22, "Roger", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_ohnivy_diviak = Pet("pet_ohnivy_diviak.png", 89, 19, 24, 14, 23, "Ferox", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_drako = Pet("pet_drak.png", 90, 18, 24, 14, 22, "Nago", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_rybohen = Pet("pet_rybohen.png", 109, 21, 27, 14, 21, "Kun", "fire", ohen, coins_ohen, SuperUtok_ohen)
pet_ohnivy_robot = Pet("pet_ohnivy_robot.png", 113, 22, 28, 14, 19, "Mecon", "fire", ohen, coins_ohen, SuperUtok_svetlo)

pet_fredka = Pet("pet_fredka.png", 82, 15, 19, 14, 18, "Dihor", "ground", zem, coins_zem, SuperUtok_zem)
pet_praopica = Pet("pet_praopica.png", 86, 13, 17, 14, 17, "Langaf", "ground", zem, coins_zem, SuperUtok_zem)
pet_vopicak = Pet("pet_vopicak.png", 87, 13, 18, 13, 18, "Maim", "ground", zem, coins_zem, SuperUtok_zem)
pet_liska = Pet("pet_liska.png", 92, 12, 18, 13, 17, "Vulpix", "ground", zem, coins_zem, SuperUtok_zem)
pet_diviak = Pet("pet_diviak.png", 104, 11, 16, 13, 16, "Neri", "ground", zem, coins_zem, SuperUtok_zem)
pet_stromcek = Pet("pet_stromcek.png", 105, 12, 19, 12, 17, "Abrak", "ground", zem, coins_zem, SuperUtok_zem)
pet_lisiak = Pet("pet_lisiak.png", 106, 12, 17, 12, 16, "Bax", "ground", zem, coins_zem, SuperUtok_zem)
pet_baran = Pet("pet_baran.png", 108, 11, 19, 12, 15, "Arcain", "ground", zem, coins_zem, SuperUtok_zem)
pet_konik = Pet("pet_konik.png", 111, 11, 18, 10, 16, "Zirg", "ground", zem, coins_zem, SuperUtok_zem)
pet_skala = Pet("pet_skala.png", 146, 11, 17, 10, 17, "Akmen", "ground", zem, coins_zem, SuperUtok_zem)
pet_velka_papula = Pet("pet_velka_papula.png", 150, 14, 19, 9, 14, "Gailis", "ground", zem, coins_zem, SuperUtok_zem)
pet_strom = Pet("pet_strom.png", 153, 11, 15, 8, 14, "Abra", "ground", zem, coins_zem, SuperUtok_zem)



monster_nindzaky = Monster("pet_nindžaky.png")
monster_tvrdy_bojovnik = Monster("pet_tvrdy-bojovnik.png")
monster_mozog = Monster("pet_megamozog.png")
monster_pauko = Monster("pet_pauko.png")
monster_dyna = Monster("pet_dyna.png")
monster_puma = Monster("pet_cica.png")
monster_dazdovka = Monster("pet_cica.png")

boss_mumia = Monster("boss_mumia.png")
boss_cert = Monster("boss_cert.png")
boss_smrtka = Monster("boss_smrtka.png")
boss_ultra_had = Monster("boss_ultra_had.png")