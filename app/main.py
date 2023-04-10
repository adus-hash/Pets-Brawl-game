import pygame
from random import randint, uniform, choice
import pickle
from datetime import timedelta, datetime
from numpy import array
import os
from pets import *
from coins import *
from bag import *
pygame.font.init()
pygame.mixer.init()


max_lvl = 100
working_path_images = os.getcwd() + "\images"
working_path = os.getcwd()

tips = [pygame.image.load(os.path.join(working_path_images, "tips1.png")), pygame.image.load(os.path.join(working_path_images, "tips2.png")), pygame.image.load(os.path.join(working_path_images, "tips3.png")), pygame.image.load(os.path.join(working_path_images, "tips4.png")), pygame.image.load(os.path.join(working_path_images, "tips5.png"))]

class Game(Pet, Coin):
    def __init__(self):
        self.width_display = 950
        self.height_display = 630

        self.main_font = pygame.font.SysFont("comicsans", 38)

        # obrazky pre win_1
        self.win = pygame.display.set_mode((self.width_display,self.height_display))
        pygame.display.set_icon(pygame.image.load(os.path.join(working_path_images, "ikona.png")))
        pygame.display.set_caption("Pets brawl")

        self.start_btn = pygame.image.load(os.path.join(working_path_images, "start_btn.png"))
        self.save_btn = pygame.image.load(os.path.join(working_path_images, "save_btn.png"))
        self.exit_btn = pygame.image.load(os.path.join(working_path_images, "exit_btn.png"))
        self.settings_btn = pygame.image.load(os.path.join(working_path_images, "settings_button.png"))


        # obrazky pre win1_save
        self.yes_btn = pygame.image.load(os.path.join(working_path_images, "yes_btn.png"))
        self.no_btn = pygame.image.load(os.path.join(working_path_images, "no_btn.png"))

        # do win_exit
        self.y = 482

        # obrazky pre win_2
        self.tips_counter = randint(0, 4)
        self.x_pozicia_buttons_win_2 = 80

        self.fight_btn = pygame.image.load(os.path.join(working_path_images, "fight_button.png"))
        self.add_btn = pygame.image.load(os.path.join(working_path_images, "add_btn.png"))
        self.pets_btn = pygame.image.load(os.path.join(working_path_images, "pets_button.png"))
        self.mines_btn = pygame.image.load(os.path.join(working_path_images, "mines_button.png"))
        self.shop_btn = pygame.image.load(os.path.join(working_path_images, "shop_button.png"))
        self.mission_btn = pygame.image.load(os.path.join(working_path_images, "mission_btn.png"))
        self.bed_btn = pygame.image.load(os.path.join(working_path_images, "bed_button.png"))

        self.back_btn = pygame.image.load(os.path.join(working_path_images, "back_button.png"))

        self.edit_btn = pygame.image.load(os.path.join(working_path_images, "edit_btn.png"))

        self.name_player = "Adrian"
        self.enter_name = pygame.Rect(920, 0, 30, 30)          # toto je layer pre btn pre upravu mena vo win_2
        self.wins = 0
        self.skore = 0
        self.boss_fight_wins = 0
        self.total_killed_monsters = 0

        self.enter_kusov = pygame.Rect(739, 434, 125, 55)      # toto je layer pre btn pre pocet kusov vo win_shop_food

        # obrazky pre win_fight_menu
        self.pets = [pet_bojovnik, pet_svetlo_dog, pet_obluda, pet_ohnivy_vtak, pet_vtak, pet_diviak, pet_zaba, pet_liska, pet_pes_sgulou, pet_pav,
                     pet_slunce, pet_elektra, pet_trojocko, pet_zvero_blesk,pet_drako, pet_rybka, pet_cvrecek, pet_kokohen, pet_praopica,
                     pet_fredka, pet_vopicak, pet_gulko, pet_ohnivy_diviak, pet_lisiak, pet_ohniva_skala, pet_baran, pet_stromcek, pet_konik,
                     pet_skala, pet_guliocko, pet_jednorozec, pet_helmet, pet_ohnivy_robot, pet_rybohen, pet_strom, pet_velka_papula]


        self.pos_pets_buttons = []


        self.mission_pets = [pet_jednorozec, pet_helmet, pet_ohnivy_robot, pet_rybohen, pet_strom, pet_velka_papula]


        self.veci_bag = [ceresne, banan, hruska, heal, hp, dmg, sleep, food, coin, resistance, sale, upgrade]

        self.pets_v_posteli = [None, None, None]

        # veci pre win_mines
        self.bane_cas_ohen = 0
        self.bane_cas_svetlo = 0
        self.bane_cas_zem = 0

        self.pressed_prvy_ohen = True  # prvy klik na banu
        self.pressed_prvy_svetlo = True
        self.pressed_prvy_zem = True

        self.max_cap = 400  # maximalna kapacita pre storage
        self.btn3 = False
        self.x = 0
        self.upgrade_storage = 1  # lvl storage
        self.max_storage = 15  # max lvl pre storage
        self.cena_upgrade_storage = 400

        # casy do win_beds
        self.zlomok_pre_spanok = 0.4    # je to o kolko krat menej sa ti pripocita sleep napr. spis 90 sekund a nepripocita sa ti tych 90 sek. ale 90 * self.zlomok_pre_spaok

        self.kupene_pet = []
        if os.path.exists(working_path + "\data"):
            with open(os.path.join(working_path + "\data", "kupene_pet.txt")) as subor_names:
                line_name = subor_names.read()
                names = line_name.split(" ")        # mena pets

            for i in names:
                for j in self.pets:
                    if i == j.name:         # tu sa ti nacitaju vsetky ulozene pets
                        self.kupene_pet.append(j)


            path = working_path + "\data"
            data_lines = []
            for i in self.kupene_pet:
                pets_data_file = os.path.join(path + "\pets", "data_" + f"{i.name}" + ".txt")     # tu sa ti nacitaju vsetky udaje o pets
                with open(pets_data_file, "r") as data:
                    data_lines += data.readlines()

            counter = 0
            for index, pet in enumerate(self.kupene_pet, counter):      # tu sa priradia vsetky udaje o pets
                pet.health, pet.damage1, pet.damage2, pet.reg1, pet.reg2, pet.sleep, pet.less_sleep, pet.less_food, pet.more_coin, pet.resistance, pet.sale, pet.more_upgrade, pet.food, pet.lvl, pet.elixir, pet.elixir_duration, pet.elixir_ucinok = data_lines[index].split(" ")
                pet.health, pet.damage1, pet.damage2, pet.reg1, pet.reg2, pet.sleep, pet.less_sleep, pet.less_food, pet.more_coin, pet.resistance, pet.sale, pet.more_upgrade, pet.food, pet.lvl, pet.elixir, pet.elixir_duration, pet.elixir_ucinok = float(pet.health), float(pet.damage1), float(pet.damage2), float(pet.reg1), float(pet.reg2), int(float(pet.sleep)), float(pet.less_sleep), float(pet.less_food), float(pet.more_coin), float(pet.resistance), float(pet.sale), float(pet.more_upgrade), int(float(pet.food)), int(pet.lvl), str(pet.elixir), int(pet.elixir_duration), pet.elixir_ucinok
                try:
                    pet.elixir_ucinok = float(pet.elixir_ucinok)
                except:
                    pet.elixir_ucinok = None
                    pet.elixir = None

                for i in self.veci_bag:     # tu sa priradia elixiri k pets
                    if i.druh == pet.elixir:
                        pet.elixir = i

            docasne_veci = []
            with open(os.path.join(path, "bag.txt"), "r") as file:
                veci = file.readlines()
                veci = veci[0].split(" ")

                for i in self.veci_bag:     # tu sa ti pridaju vsetky elixiri a ovocia ktore sa ulozili
                    for j in veci:
                        if i.druh == j:
                            docasne_veci.append(i)
                self.veci_bag = docasne_veci


                                            # - 1 tu je pre to lebo ten array obsahuje na poslednom indexe prazdni string
                for i in range(0, len(veci) - 1, 2):        # tu sa ti priradi ku kazdemu elixiru ulozeny pocet
                    if "ceresne" in veci[i]:
                        ceresne.pocet = int(veci[i+1])

                    if "banan" in veci[i]:
                        banan.pocet = int(veci[i+1])

                    if "hruska" in veci[i]:
                        hruska.pocet = int(veci[i+1])

                    if "heal" in veci[i]:
                        heal.pocet = int(veci[i+1])

                    if "hp" in veci[i]:
                        hp.pocet = int(veci[i+1])

                    if "dmg" in veci[i]:
                        dmg.pocet = int(veci[i+1])

                    if "sleep" in veci[i]:
                        sleep.pocet = int(veci[i+1])

                    if "food" in veci[i]:
                        food.pocet = int(veci[i+1])

                    if "coin" in veci[i]:
                        coin.pocet = int(veci[i+1])

                    if "resistance" in veci[i]:
                        resistance.pocet = int(veci[i+1])

                    if "sale" in veci[i]:
                        sale.pocet = int(veci[i+1])

                    if "upgrade" in veci[i]:
                        upgrade.pocet = int(veci[i+1])

            with open(os.path.join(path, "pets_v_pelechu.txt"), "r") as file:
                pets = file.readline()
                pets = pets.split(" ")

                for j in range(0, 3):
                    for i in self.pets:     # totok pridava pets do postele z ulozeneho suboru
                        if i.name == pets[j]:
                            pet_to_append = i
                            break
                        else:
                            pet_to_append = None

                    self.pets_v_posteli.insert(j, pet_to_append)


            game_file = open(os.path.join(path, "data_game"), "rb")
            self.name_player = pickle.load(game_file)
            self.wins = pickle.load(game_file)
            self.skore = pickle.load(game_file)
            self.boss_fight_wins = pickle.load(game_file)
            self.total_killed_monsters = pickle.load(game_file)

            self.pressed_prvy_ohen = pickle.load(game_file)
            self.pressed_prvy_svetlo = pickle.load(game_file)
            self.pressed_prvy_zem = pickle.load(game_file)

            self.max_cap = pickle.load(game_file)
            self.upgrade_storage = pickle.load(game_file)

            coins.actual_money = pickle.load(game_file)
            coins.coins_per_sec = pickle.load(game_file)
            coins.upgrade_lvl = pickle.load(game_file)

            coins_ohen.actual_money = pickle.load(game_file)
            coins_ohen.coins_per_sec = pickle.load(game_file)
            coins_ohen.upgrade_lvl = pickle.load(game_file)

            coins_svetlo.actual_money = pickle.load(game_file)
            coins_svetlo.coins_per_sec = pickle.load(game_file)
            coins_svetlo.upgrade_lvl = pickle.load(game_file)

            coins_zem.actual_money = pickle.load(game_file)
            coins_zem.coins_per_sec = pickle.load(game_file)
            coins_zem.upgrade_lvl = pickle.load(game_file)

            try:
                self.pets_v_posteli[0].cas_od_kedy_spi = pickle.load(open(os.path.join(path + "\casi", "postel_cas1"), "rb"))
            except:
                pass

            try:
                self.pets_v_posteli[1].cas_od_kedy_spi = pickle.load(open(os.path.join(path + "\casi", "postel_cas2"), "rb"))
            except:
                pass
            try:
                self.pets_v_posteli[2].cas_od_kedy_spi = pickle.load(open(os.path.join(path + "\casi", "postel_cas3"), "rb"))
            except:
                pass
            try:
                self.bane_cas_ohen = pickle.load(open(os.path.join(path + "\casi", "bane_cas_ohen"), "rb"))
            except:
                pass
            try:
                self.bane_cas_svetlo = pickle.load(open(os.path.join(path + "\casi", "bane_cas_svetlo"), "rb"))
            except:
                pass
            try:
                self.bane_cas_zem = pickle.load(open(os.path.join(path + "\casi", "bane_cas_zem"), "rb"))
            except:
                pass

        else:
            self.kupene_pet = [pet_bojovnik, pet_obluda, pet_ohnivy_vtak, pet_diviak, pet_zaba, pet_liska]


        self.monsters = array([monster_puma, monster_nindzaky, monster_tvrdy_bojovnik, monster_mozog, monster_pauko, monster_dyna, monster_dazdovka])

        self.bosses = [boss_mumia, boss_cert, boss_smrtka, boss_ultra_had]

        self.boss_fight_pets = []
        self.pos_pets_to_fight = []


        self.next_pet = False
        self.animation_move_var_left = 20
        self.animation_move_var_right = 1
        self.monster_pointer = 0    # pointer ktory mi ukazuje na actualne_monster vo win_fight_until_die
        self.pet_pointer = 1        # pointer kt. ukazuje na actualne_pet vo win_fight_boss
        self.monsters_to_die = [monster_puma, monster_nindzaky, monster_tvrdy_bojovnik, monster_mozog, monster_pauko, monster_dyna]
        self.killed_monsters = 0


        self.pocet = 0          # ake pets sa zobrazia v riadku, ak tento pocet zvysim, pets sa posunu o nejaku hodnotu
        self.bool_fight_until_die = False
        self.bool_fight_boss = False

        self.click = False
        self.click_ovocie = False

        self.zvolene_pet = False
        self.zvolene_ovocie = False

        self.lack_sleep = False

        self.sipka_hore = pygame.image.load(os.path.join(working_path_images, "sipka.png"))
        self.sipka_dole = pygame.transform.flip(self.sipka_hore, 0, -180)

        # obrazky pre win_fight
        self.quit_btn = pygame.image.load(os.path.join(working_path_images, "quit_button.png"))

        self.health_count_hero = 0              # všetko čo uberé monster herovi tak sa po skoncení while_win_fight pripočítá naspäť
        self.health_reg_count_hero = 0          # všetko čo sa ti pripočitá pri rageneracii, ty to potrebuješ odpočítať od health_hero ked prebehne metoda set_default()
        self.reg_count = 0      # regeneration_count
        self.pow_count = 0      # SuperPower_count    # pocet_utokov a z toho sa vypocitava kolko ti ubere zo sleep
        self.won_hero = False

        self.won_monster = False

        self.clock = pygame.time.Clock()

        self.spustac = False
        self.pressed_a = False
        self.pressed_r = False
        self.pressed_s = False
        self.animation_suboj_count = 1
        self.anim_efekty_count = 1
        self.anim_coin = 0

        # obrayky pre win_shop
        self.buy_btn = pygame.image.load(os.path.join(working_path_images, "buy_button.png"))
        self.pressed_kupene = False

        self.pos_pet_shop = []
        self.chybajuce_pet = []
        self.ovocie = [ceresne, banan, hruska, heal, hp, dmg, sleep, food, coin, resistance, sale, upgrade]
        self.pocet_kusov = ""
        self.activated = False

        # veci pre win_pets
        self.upgrade_btn_small = pygame.image.load(os.path.join(working_path_images, "upgrade_storage.png"))
        self.moon = pygame.image.load(os.path.join(working_path_images, "moon.png"))
        self.burger = pygame.image.load(os.path.join(working_path_images, "burger.png"))

        # veci do win_mission
        self.get_btn = pygame.image.load(os.path.join(working_path_images, "get_btn.png"))

        #veci do win_beds
        self.ospalne_pets = []



    def run(self):
        run = True
        run_win_1 = True
        run_win1_save = False
        run_exit = False
        run_win_settings = False
        run_win_2 = False
        run_win_battle_menu = False
        run_win_fight_menu = False
        run_win_fight_1v1 = False
        run_win_fight_until_die = False
        run_win_fight_boss = False
        run_win_pets = False
        run_win_mines = False
        run_win_shop_menu = False
        run_win_shop_animals = False
        run_win_shop_food = False
        run_win_mission = False
        run_win_bed = False

        while run:
            self.clock.tick(60)

            while run_win_1:
                self.x_pozicia_buttons = self.width_display // 2 - self.start_btn.get_width() // 2


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_1 = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= self.x_pozicia_buttons and mouse[1] >= 220:
                                if mouse[0] <= self.x_pozicia_buttons +  self.start_btn.get_width() and mouse[1] <= 220 + self.start_btn.get_height():
                                    run_win_2 = True
                                    run_win_1 = False
                                    self.tips_counter = randint(0, 4)

                            if mouse[0] >= self.x_pozicia_buttons and mouse[1] >= 300:
                                if mouse[0] <= self.x_pozicia_buttons + self.save_btn.get_width() and mouse[1] <= 300 + self.save_btn.get_height():
                                    run_win1_save = True
                                    run_win_1 = False

                            if mouse[0] >= self.x_pozicia_buttons and mouse[1] >= 380:
                                if mouse[0] <= self.x_pozicia_buttons + self.exit_btn.get_width() and mouse[1] <= 380 + self.exit_btn.get_height():
                                    run_exit = True
                                    run_win_1 = False

                            if mouse[0] >= 855 and mouse[1] >= 537:
                                if mouse[0] <= 855 + self.settings_btn.get_width() and mouse[1] <= 537 + self.settings_btn.get_height():
                                    run_win_settings = True
                                    run_win_1 = False
                self.draw_win_1()

            while run_win1_save:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win1_save = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= 276 and mouse[1] >= 335:  # pre yes_button v win1_save
                                if mouse[0] <= 276 + self.yes_btn.get_width() and mouse[1] <= 335  + self.yes_btn.get_height():
                                    run_win1_save = False
                                    run_win_1 = True

                                    self.save_game()

                                    current_time = datetime.now()
                                    time_then = current_time + timedelta(seconds=2)

                                    while current_time < time_then:
                                        current_time = datetime.now()
                                        self.save_text_render()


                            if mouse[0] >= 547 and mouse[1] >= 335:
                                if mouse[0] <= 547 + self.no_btn.get_width() and mouse[1] <= 335  + self.no_btn.get_height():
                                    run_win_1 = True
                                    run_win1_save = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_1 = True
                            run_win1_save = False
                self.win_save()

            while run_exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_exit = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_1 = True
                            run_exit = False


                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= 276 and mouse[1] >= 335:  # pre yes_button v win1_save
                                if mouse[0] <= 276 + self.yes_btn.get_width() and mouse[1] <= 335 + self.yes_btn.get_height():
                                    run = False
                                    run_exit = False

                            if mouse[0] >= 547 and mouse[1] >= 335:  # pre yes_button v win1_save
                                if mouse[0] <= 547 + self.no_btn.get_width() and mouse[1] <= 335 + self.no_btn.get_height():
                                    run_win_1 = True
                                    run_exit = False
                                    self.y = 482
                self.draw_exit()

            while run_win_settings:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_settings = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:

                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                run_win_settings = False
                                run_win_1 = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_1 = True
                            run_win_settings = False
                self.draw_win_settings()

            while run_win_2:
                self.actual_time = datetime.now()       # cas tu je pre pocitanie stavu storage z tohto sa pocita ako velmi je plne storage a ptm sa to zobrazuje vedla pelechov vo win_2

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_win_2 = False
                        run = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = False
                            run_win_1 = True

                        if self.activated:
                            if event.key == pygame.K_BACKSPACE:
                                self.name_player = self.name_player[:-1]

                            elif event.key == pygame.K_DELETE:
                                self.name_player = ""

                            else:
                                if len(self.name_player) < 21:
                                    self.name_player += event.unicode


                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 75:
                                if mouse[0] <= self.x_pozicia_buttons_win_2 + self.fight_btn.get_width() and mouse[1] <= 75 + self.fight_btn.get_height():
                                    run_win_2 = False
                                    run_win_battle_menu = True
                                    self.bool_fight_until_die = False
                                    self.bool_fight_boss = False
                                    self.tips_counter = randint(0, 4)
                                    #self.pos_pets_buttons = []

                            if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 155:
                                if mouse[0] <= self.x_pozicia_buttons_win_2 + self.pets_btn.get_width() and mouse[1] <= 155 + self.pets_btn.get_height():
                                    run_win_2 = False
                                    run_win_pets = True
                                    self.pos_pets_buttons = []
                                    self.pos_pet_shop = []
                                    self.tips_counter = randint(0, 4)

                            if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 235:
                                if mouse[0] <= self.x_pozicia_buttons_win_2 + self.mines_btn.get_width() and mouse[1] <= 235 + self.mines_btn.get_height():
                                    run_win_2 = False
                                    run_win_mines = True
                                    self.tips_counter = randint(0, 4)

                            if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 315:
                                if mouse[0] <= self.x_pozicia_buttons_win_2 + self.shop_btn.get_width() and mouse[1] <= 315 + self.shop_btn.get_height():
                                    run_win_2 = False
                                    run_win_shop_menu = True
                                    self.tips_counter = randint(0, 4)

                            if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 395:
                                if mouse[0] <= self.x_pozicia_buttons_win_2 + self.shop_btn.get_width() and mouse[1] <= 395 + self.shop_btn.get_height():
                                    run_win_2 = False
                                    run_win_mission = True
                                    self.tips_counter = randint(0, 4)

                            if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 475:
                                if mouse[0] <= self.x_pozicia_buttons_win_2 + self.bed_btn.get_width() and mouse[1] <= 475 + self.bed_btn.get_height():
                                    run_win_2 = False
                                    run_win_bed = True
                                    self.ospalne_pets.clear()
                                    self.pos_pets_buttons.clear()
                                    self.tips_counter = randint(0, 4)
                                    time = datetime.now()
                            self.activated = False

                            if self.enter_name.collidepoint(event.pos):
                                self.activated = True


                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                run_win_1 = True
                                run_win_2 = False
                self.draw_win_2()


                while run_win_battle_menu:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run_win_battle_menu = False
                            run = False

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                run_win_2 = True
                                run_win_battle_menu = False

                        self.popis_battle = ""
                        self.pos_pets_buttons = []
                        mouse = pygame.mouse.get_pos()

                        if mouse[0] >= 80 and mouse[0] <= 298:
                            if mouse[1] >= 129 and mouse[1] <= 462:
                                self.popis_battle = "You will choose one pet and fight against one monster."
                                try:
                                    if event.button == 1:
                                        run_win_fight_menu = True
                                        run_win_battle_menu = False
                                except:
                                    pass

                        if mouse[0] >= 366 and mouse[0] <= 584:
                            if mouse[1] >= 129 and mouse[1] <= 462:
                                self.popis_battle = "You will choose one pet and fight until you die."
                                try:
                                    if event.button == 1:
                                        run_win_fight_menu = True
                                        run_win_battle_menu = False
                                        self.bool_fight_until_die = True
                                except:
                                    pass

                        if mouse[0] >= 652 and mouse[0] <= 870:
                            if mouse[1] >= 129 and mouse[1] <= 462:
                                self.popis_battle = "You will choose four pet and fight against boss. This boss is extremly strong."
                                try:
                                    if event.button == 1:
                                        run_win_fight_menu = True
                                        run_win_battle_menu = False
                                        self.bool_fight_boss = True
                                        self.boss_fight_pets = []
                                except:
                                    pass


                        if event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:

                                if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                    run_win_2 = True
                                    run_win_battle_menu = False
                    self.draw_win_battle_menu()



            while run_win_fight_menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_win_fight_menu = False
                        run = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[1] < 430:
                                self.pet_button(mouse, 900, 50, self.pos_pets_buttons, 9)
                            else:
                                self.delete_pet(mouse, self.pos_pets_to_fight)


                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                run_win_2 = True
                                run_win_fight_menu = False
                                self.zvolene_pet = False
                                self.pos_pets_buttons = []
                                self.pocet = 0
                                self.click = False
                                self.bool_fight_until_die = False

                            elif mouse[0] >= 640 and mouse[1] >= 550:
                                if mouse[0] <= 640 + self.fight_btn.get_width() and mouse[1] <= 550 + self.fight_btn.get_height():
                                    if self.bool_fight_boss and len(self.boss_fight_pets) == 4:
                                        self.actualne_monster = choice(self.bosses)
                                        self.Health_monster = self.actualne_monster.set_health_boos(self.boss_fight_pets)       # ak budes mat  4 pets v kolonke tak ta pusti bojovat
                                        self.Health_monster2 = self.Health_monster
                                        self.actualne_pet = self.boss_fight_pets[0]
                                        self.Health_hero2 = self.actualne_pet.health
                                        self.pet_pointer = 1
                                        run_win_fight_boss = True
                                        run_win_fight_menu = False


                                    if self.zvolene_pet:
                                        self.actualne_monster = choice(self.monsters)
                                        self.Health_hero2 = self.actualne_pet.health
                                        self.Health_monster = self.actualne_monster.set_health_1v1(self.actualne_pet) if not self.bool_fight_until_die else self.actualne_monster.set_health_until_die(self.Health_hero2)


                                        if self.actualne_pet.sleep - 5 > 0 and self.actualne_pet.food - 6 > 0:    # - 5 je maximalna hodnota ktora sa moze odcitat od sleep a - 6 je maximalna hodnota ktora sa moze odcitat od food

                                            self.Health_monster2 = self.Health_monster  # pre vypocet vyhernej aj prehratej ceny


                                            run_win_fight_1v1 = True if not self.bool_fight_until_die and not self.bool_fight_boss else False
                                            if self.bool_fight_until_die:
                                                for i in range(5):
                                                    self.monsters_to_die.append(choice(self.monsters))

                                                self.actualne_monster = self.monsters_to_die[0]

                                                self.next_pet = False
                                                self.monster_pointer = 0    # tieto 3 riadky tu su preto aby sa mi vsetko dalo do povodneho stavu
                                                self.killed_monsters = 0

                                                run_win_fight_until_die = True if self.bool_fight_until_die  else False

                                            run_win_fight_menu = False if not self.bool_fight_boss else True


                                            if self.zvolene_pet and self.bool_fight_boss and len(self.boss_fight_pets) < 4:
                                                self.boss_fight_pets.append(self.actualne_pet) if self.actualne_pet not in self.boss_fight_pets else None

                                            self.zvolene_pet = False
                                            self.anim_efekty_count = 0

                                        else:
                                            self.lack_sleep = True
                                            self.zvolene_pet = True
                                else:
                                    self.zvolene_pet = False

                            if mouse[0] >= 923 and mouse[1] >= 50:
                                if mouse[0] <= 923 + self.sipka_hore.get_width() and mouse[1] <= 50 + self.sipka_hore.get_height():
                                    if self.pocet >= 9:
                                        self.pocet -= 9

                            if mouse[0] >= 923 and mouse[1] >= 80:
                                if mouse[0] <= 923 + self.sipka_dole.get_width() and mouse[1] <= 80 + self.sipka_dole.get_height():
                                    if self.pocet < len(self.kupene_pet) - 27:
                                        self.pocet += 9


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = True
                            run_win_fight_menu = False
                            self.zvolene_pet = False
                            self.pos_pets_buttons.clear()
                            self.pocet = 0
                            self.click = False
                            self.bool_fight_until_die = False
                self.draw_win_fight_menu()


            while run_win_fight_1v1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_win_fight_1v1 = False
                        run = False


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.won_monster or self.won_hero:
                                run_win_2 = True
                                run_win_fight_1v1 = False
                                self.check_pet()
                                self.health_count_hero = 0
                                self.health_reg_count_hero = 0
                                self.won_hero = False
                                self.won_monster = False
                                self.reg_count = 0
                                self.pow_count = 0
                                coins.ount_for_money = 0


                        if not self.won_hero and not self.won_monster:
                            if event.key == pygame.K_a:
                                self.pressed_a = True
                                self.spustac = True


                                self.Damage_monster = int(self.actualne_monster.get_damage_1v1(self.Health_hero2, self.actualne_pet) * self.actualne_pet.resistance)
                                self.Damage_hero = self.actualne_pet.get_damage()


                                self.play_sound(str(self.actualne_pet.druh) + "_sound")


                                self.attack_hero()

                            if event.key == pygame.K_s:
                                if self.pow_count < 1:
                                    self.pressed_s = True
                                    self.spustac = True


                                    self.Damage_monster = int(self.actualne_monster.get_damage_1v1(self.Health_hero2, self.actualne_pet) * self.actualne_pet.resistance)
                                    self.Damage_hero = self.actualne_pet.get_super_damage()

                                    self.play_sound(str(self.actualne_pet.druh) + "_sound")

                                    self.attack_hero()
                                    self.pow_count += 1


                            if event.key == pygame.K_r:

                                if self.reg_count < 3:
                                    self.regeneration_random_number = self.actualne_pet.get_regeneration()
                                    self.regeneration()
                                    self.pressed_r = True
                                    self.spustac = True
                                    self.play_sound("heal_sound")

                                    self.reg_count += 1

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse_fight = pygame.mouse.get_pos()
                            if self.won_monster or self.won_hero:
                                if mouse_fight[0] >= 410 and mouse_fight[1] >= 285:
                                    if mouse_fight[0] <= 410 + self.quit_btn.get_width() and mouse_fight[1] <= 285 + self.quit_btn.get_height():
                                        run_win_2 = True
                                        run_win_fight_1v1 = False
                                        self.check_pet()
                                        self.health_count_hero = 0
                                        self.health_reg_count_hero = 0
                                        self.won_hero = False
                                        self.won_monster = False
                                        self.reg_count = 0
                                        self.pow_count = 0
                                        coins.count_for_money = 0
                self.draw_win_fight_1v1()



            while run_win_fight_until_die:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_win_fight_until_die = False
                        run = False


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.won_monster:
                                run_win_2 = True
                                run_win_fight_until_die = False
                                self.check_pet()
                                self.health_count_hero = 0
                                self.health_reg_count_hero = 0
                                self.won_hero = False
                                self.won_monster = False
                                self.reg_count = 0
                                self.pow_count = 0
                                coins.ount_for_money = 0

                        if not self.won_hero and not self.won_monster and not self.next_pet:
                            if event.key == pygame.K_a:
                                self.pressed_a = True
                                self.spustac = True

                                self.Damage_monster = int(self.actualne_monster.get_damage_until_die(self.actualne_pet) * self.actualne_pet.resistance)
                                self.Damage_hero = self.actualne_pet.get_damage()

                                self.play_sound(str(self.actualne_pet.druh) + "_sound")

                                self.attack_hero()

                            if event.key == pygame.K_s:
                                if self.pow_count < 1:
                                    self.pressed_s = True
                                    self.spustac = True


                                    self.Damage_monster = int(self.actualne_monster.get_damage_until_die(self.actualne_pet) * self.actualne_pet.resistance)
                                    self.Damage_hero = self.actualne_pet.get_super_damage()

                                    self.play_sound(str(self.actualne_pet.druh) + "_sound")

                                    self.attack_hero()
                                    self.pow_count += 1


                            if event.key == pygame.K_r:

                                if self.reg_count < 3:
                                    self.regeneration_random_number = self.actualne_pet.get_regeneration()
                                    self.regeneration()
                                    self.pressed_r = True
                                    self.spustac = True
                                    self.play_sound("heal_sound")

                                    self.reg_count += 1


                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse_fight = pygame.mouse.get_pos()

                            if self.won_monster:
                                if mouse_fight[0] >= 410 and mouse_fight[1] >= 285:
                                    if mouse_fight[0] <= 410 + self.quit_btn.get_width() and mouse_fight[1] <= 285 + self.quit_btn.get_height():
                                        run_win_2 = True
                                        run_win_fight_until_die = False
                                        self.check_pet()
                                        self.health_count_hero = 0
                                        self.health_reg_count_hero = 0
                                        self.won_hero = False
                                        self.won_monster = False
                                        self.reg_count = 0
                                        self.pow_count = 0
                                        coins.count_for_money = 0
                self.draw_win_fight_until_die()

            while run_win_fight_boss:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run_win_fight_boss = False
                        run = False


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            run_win_fight_boss = False
                            run_win_2 = True
                            self.check_pet()
                            self.health_count_hero = 0
                            self.health_reg_count_hero = 0
                            self.won_hero = False
                            self.won_monster = False
                            self.reg_count = 0
                            self.pow_count = 0

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.won_monster or self.won_hero:
                                run_win_2 = True
                                run_win_fight_boss = False
                                self.check_pet()
                                self.health_count_hero = 0
                                self.health_reg_count_hero = 0
                                self.won_hero = False
                                self.won_monster = False
                                self.reg_count = 0
                                self.pow_count = 0
                                coins.ount_for_money = 0

                        if not self.won_hero and not self.won_monster and not self.next_pet:
                            if event.key == pygame.K_a:
                                self.pressed_a = True
                                self.spustac = True

                                self.Damage_monster = int(self.actualne_monster.get_damage_boss(self.Health_monster2, self.Health_hero2, self.actualne_pet) * self.actualne_pet.resistance)
                                self.Damage_hero = self.actualne_pet.get_damage()

                                self.play_sound(str(self.actualne_pet.druh) + "_sound")

                                self.attack_hero()

                            if event.key == pygame.K_s:
                                if self.pow_count < 1:
                                    self.pressed_s = True
                                    self.spustac = True

                                    self.Damage_monster = int(self.actualne_monster.get_damage_boss(self.Health_monster2, self.Health_hero2, self.actualne_pet) * self.actualne_pet.resistance)
                                    self.Damage_hero = self.actualne_pet.get_super_damage()

                                    self.play_sound(str(self.actualne_pet.druh) + "_sound")


                                    self.attack_hero()
                                    self.pow_count += 1


                            if event.key == pygame.K_r:

                                if self.reg_count < 3:
                                    self.regeneration_random_number = self.actualne_pet.get_regeneration()
                                    self.regeneration()
                                    self.pressed_r = True
                                    self.spustac = True
                                    self.play_sound("heal_sound")

                                    self.reg_count += 1


                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse_fight = pygame.mouse.get_pos()

                            if self.won_monster or self.won_hero:
                                if mouse_fight[0] >= 410 and mouse_fight[1] >= 285:
                                    if mouse_fight[0] <= 410 + self.quit_btn.get_width() and mouse_fight[1] <= 285 + self.quit_btn.get_height():
                                        run_win_2 = True
                                        run_win_fight_boss = False
                                        self.check_pet()
                                        self.health_count_hero = 0
                                        self.health_reg_count_hero = 0
                                        self.won_hero = False
                                        self.won_monster = False
                                        self.reg_count = 0
                                        self.pow_count = 0
                                        coins.count_for_money = 0
                self.draw_win_fight_boss()

            while run_win_pets:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_pets = False

                    mouse = pygame.mouse.get_pos()

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            if mouse[0] < 700:
                                self.pet_button(mouse, 700, 50, self.pos_pets_buttons, 6)
                            else:
                                self.ovocie_button(mouse, 950, 75, self.pos_pet_shop, 3)

                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                    run_win_2 = True
                                    run_win_pets = False
                                    self.zvolene_pet = False
                                    self.zvolene_ovocie = False
                                    self.pocet = 0
                                    self.click = False
                                    self.click_ovocie = False


                            if self.zvolene_ovocie and self.zvolene_pet:

                                if 45 <= mouse[0] <= 45 + self.pets[0].get_width():
                                    if 490 <= mouse[1] <= 490 + self.pets[0].get_height():

                                        if self.actualne_ovocie.pocet > 0:
                                            if self.actualne_ovocie.druh == "ceresne" or self.actualne_ovocie.druh == "banan" or self.actualne_ovocie.druh == "hruska":
                                                eat_up = eat(self.actualne_pet, self.actualne_ovocie)
                                                if eat_up + self.actualne_pet.food < 100:
                                                    self.actualne_pet.food += eat_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.zvolene_ovocie = False
                                                    self.play_sound("jedenie")
                                                else:
                                                    if self.actualne_pet.food != 100:
                                                        self.actualne_pet.food += 100 - self.actualne_pet.food
                                                        self.actualne_ovocie.pocet -= 1
                                                        self.zvolene_ovocie = False
                                                        self.play_sound("jedenie")

                                            if self.actualne_pet.elixir == None:
                                                if self.actualne_ovocie.druh == "heal":
                                                    heal_up = rise_heal()
                                                    self.actualne_pet.reg1 *= heal_up
                                                    self.actualne_pet.reg2 *= heal_up
                                                    self.actualne_pet.elixir = heal
                                                    self.actualne_pet.elixir_ucinok = heal_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "hp":
                                                    hp_up = rise_hp()
                                                    self.actualne_pet.health *= hp_up
                                                    self.actualne_pet.elixir = hp
                                                    self.actualne_pet.elixir_ucinok = hp_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "dmg":
                                                    dmg_up = rise_dmg()
                                                    self.actualne_pet.damage1 *= dmg_up
                                                    self.actualne_pet.damage2 *= dmg_up
                                                    self.actualne_pet.elixir = dmg
                                                    self.actualne_pet.elixir_ucinok = dmg_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "sleep":
                                                    sleep_down = less_sleep()
                                                    self.actualne_pet.less_sleep *= sleep_down
                                                    self.actualne_pet.elixir = sleep
                                                    self.actualne_pet.elixir_ucinok = sleep_down
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "food":
                                                    food_down = less_food()
                                                    self.actualne_pet.less_food *= food_down
                                                    self.actualne_pet.elixir = food
                                                    self.actualne_pet.elixir_ucinok = food_down
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "coin":
                                                    coin_up = more_coin()
                                                    self.actualne_pet.more_coin *= coin_up
                                                    self.actualne_pet.elixir = coin
                                                    self.actualne_pet.elixir_ucinok = coin_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "resistance":
                                                    resistance_up = vacsia_vydrz()
                                                    self.actualne_pet.resistance *= resistance_up
                                                    self.actualne_pet.elixir = resistance
                                                    self.actualne_pet.elixir_ucinok = resistance_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "sale" and self.actualne_pet.lvl <= 98:
                                                    sale_up = lacnejsie_upgrady()
                                                    self.actualne_pet.sale = sale_up
                                                    self.actualne_pet.elixir = sale
                                                    self.actualne_pet.elixir_ucinok = sale_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                if self.actualne_ovocie.druh == "upgrade" and self.actualne_pet.lvl <= 98:
                                                    upgrade_up = vacsie_upgrade()
                                                    self.actualne_pet.more_upgrade = upgrade_up
                                                    self.actualne_pet.elixir = upgrade
                                                    self.actualne_pet.elixir_ucinok = upgrade_up
                                                    self.actualne_ovocie.pocet -= 1
                                                    self.play_sound("pitie")

                                                self.zvolene_ovocie = False


                            if self.zvolene_pet:
                                if 393 <= mouse[0] <= 393 + self.upgrade_btn_small.get_width():     # upgrade pets
                                    if 582 <= mouse[1] <= 582 + self.upgrade_btn_small.get_height():
                                        money_upgrade = self.actualne_pet.cena_upgrade()

                                        if self.actualne_pet.druh_coin.actual_money >= money_upgrade and self.actualne_pet.lvl < max_lvl:
                                            self.actualne_pet.upgrade()
                                            self.actualne_pet.druh_coin.actual_money -= money_upgrade
                                            self.actualne_pet.lvl += 1
                                            try:
                                                self.actualne_pet.elixir_duration -= 1 if self.actualne_pet.elixir.druh == "sale" or self.actualne_pet.elixir.druh == "upgrade" else 0


                                                if self.actualne_pet.elixir_duration == 0:
                                                    if self.actualne_pet.elixir.druh == "sale":
                                                        self.actualne_pet.sale = 1
                                                        self.actualne_pet.elixir_ucinok = None
                                                        self.actualne_pet.elixir = None
                                                        self.actualne_pet.elixir_duration = 2

                                                    if self.actualne_pet.elixir.druh == "upgrade":
                                                        self.actualne_pet.more_upgrade = 1
                                                        self.actualne_pet.elixir_ucinok = None
                                                        self.actualne_pet.elixir = None
                                                        self.actualne_pet.elixir_duration = 2
                                            except:
                                                pass
                                    else:
                                        if mouse[0] > 700 or 45 <= mouse[0] <= 45 + self.pets[0].get_width():   # aby si mal actualne pet aj ked kliknes v bag
                                            if mouse[1] < 433 or 490 <= mouse[1] <= 490 + self.pets[0].get_height():
                                                pass
                                            else:
                                                self.zvolene_pet = False
                                        else:
                                            self.zvolene_pet = False
                                else:
                                    if mouse[0] > 700 or 45 <= mouse[0] <= 45 + self.pets[0].get_width():
                                        if mouse[1] < 433 or 490 <= mouse[1] <= 490 + self.pets[0].get_height():
                                            pass
                                        else:
                                            self.zvolene_pet = False
                                    else:
                                        self.zvolene_pet = False


                            if mouse[0] > 700:
                                if mouse[1] < 433:
                                    self.zvolene_ovocie = False

                            if mouse[0] >= 664 and mouse[1] >= 50:
                                if mouse[0] <= 664 + self.sipka_hore.get_width() and mouse[1] <= 50 + self.sipka_hore.get_height():
                                    if self.pocet >= 6:
                                        self.pocet -= 6

                            if mouse[0] >= 664 and mouse[1] >= 79:
                                if mouse[0] <= 664 + self.sipka_dole.get_width() and mouse[1] <= 79 + self.sipka_dole.get_height():
                                    if self.pocet < len(self.kupene_pet) - 18:
                                        self.pocet += 6


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = True
                            run_win_pets = False
                            self.zvolene_pet = False
                            self.zvolene_ovocie = False
                            self.click_ovocie = False
                            self.pocet = 0
                            self.click = False
                self.draw_win_pets()

            while run_win_mines:
                self.actual_time = datetime.now()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_mines = False

                    self.coins_list = [coins_ohen, coins_svetlo, coins_zem]

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if self.pos_mines[0][0] <= mouse[0] <= self.pos_mines[0][2]:
                                if self.pos_mines[0][1] <= mouse[1] <= self.pos_mines[0][3]:
                                    if self.pressed_prvy_ohen:
                                        self.bane_cas_ohen = datetime.now()
                                        self.pressed_prvy_ohen = False


                            if self.pos_mines[1][0] <= mouse[0] <= self.pos_mines[1][2]:
                                if self.pos_mines[1][1] <= mouse[1] <= self.pos_mines[1][3]:
                                    if self.pressed_prvy_svetlo:
                                        self.bane_cas_svetlo = datetime.now()
                                        self.pressed_prvy_svetlo = False


                            if self.pos_mines[2][0] <= mouse[0] <= self.pos_mines[2][2]:
                                if self.pos_mines[2][1] <= mouse[1] <= self.pos_mines[2][3]:
                                    if self.pressed_prvy_zem:
                                        self.bane_cas_zem = datetime.now()
                                        self.pressed_prvy_zem = False


                            if 628 <= mouse[0] <= 727:        # collect_btn
                                if 159 <= mouse[1] <= 195:

                                    if not self.pressed_prvy_ohen:    # prv stlacis na bane tym si ich postavis a od vtedy ti tazia (hned po postaveni)
                                        self.play_sound("coin_sound")
                                        seconds_ohen = round((self.actual_time - self.bane_cas_ohen).total_seconds() * coins_ohen.coins_per_sec) # cas od kedy si postavil bane az kym si nestacil na storage
                                        if seconds_ohen < self.max_cap:
                                            self.bane_cas_ohen = datetime.now()
                                            coins_ohen.actual_money += seconds_ohen

                                        else:
                                            self.bane_cas_ohen = datetime.now()
                                            coins_ohen.actual_money += self.max_cap


                                    if not self.pressed_prvy_svetlo:
                                        self.play_sound("coin_sound")
                                        seconds_svetlo = round((self.actual_time - self.bane_cas_svetlo).total_seconds() * coins_svetlo.coins_per_sec)
                                        if seconds_svetlo < self.max_cap:
                                            self.bane_cas_svetlo = datetime.now()
                                            coins_svetlo.actual_money += seconds_svetlo

                                        else:
                                            self.bane_cas_svetlo = datetime.now()
                                            coins_svetlo.actual_money += self.max_cap

                                    if not self.pressed_prvy_zem:
                                        self.play_sound("coin_sound")
                                        seconds_zem = round((self.actual_time - self.bane_cas_zem).total_seconds() * coins_zem.coins_per_sec)
                                        if seconds_zem < self.max_cap:
                                            self.bane_cas_zem = datetime.now()
                                            coins_zem.actual_money += seconds_zem

                                        else:
                                            self.bane_cas_zem = datetime.now()
                                            coins_zem.actual_money += self.max_cap


                            if 628 <= mouse[0] <= 726:
                                if 114 <= mouse[1] <= 150:
                                    if self.upgrade_storage < self.max_storage and self.cena_upgrade_storage < coins.actual_money:
                                        coins.actual_money -= self.cena_upgrade_storage
                                        self.max_cap = int(self.max_cap * 1.21)
                                        self.upgrade_storage += 1
                                        self.pressed_kupene = True



                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                run_win_2 = True
                                run_win_mines = False

                            if self.btn3:
                                if 500 <= mouse[0] <= 624 and self.pos_mines[self.x][1] + 12 <= mouse[1] <= self.pos_mines[self.x][1] + 59:     # upgabde mines
                                    if self.coins_list[self.x].actual_money >= 250 and self.coins_list[self.x].upgrade_lvl < 8:
                                        self.coins_list[self.x].upgrade_mines()
                                        self.coins_list[self.x].upgrade_lvl += 1
                                else:
                                    self.btn3 = False

                        if event.button == 3:
                            self.btn3 = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = True
                            run_win_mines = False
                            self.btn3 = False
                self.draw_win_mines()

            while run_win_shop_menu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_shop_menu = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= 420 and mouse[1] >= 278:
                                if mouse[0] <= 509 and mouse[1] <= 437:
                                    run_win_shop_menu = False
                                    run_win_shop_animals = True
                                    self.pos_pet_shop = []
                                    self.chybajuce_pet = []

                            if mouse[0] >= 558 and mouse[1] >= 278:
                                if mouse[0] <= 647 and mouse[1] <= 437:
                                    run_win_shop_menu = False
                                    run_win_shop_food = True
                                    self.pos_pet_shop = []

                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                run_win_2 = True
                                run_win_shop_menu = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = True
                            run_win_shop_menu = False
                self.draw_win_shop_menu()

            while run_win_shop_animals:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_shop_animals = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            self.pet_button(mouse, 916, 234, self.pos_pet_shop, 3)

                            if self.zvolene_pet:
                                if mouse[0] >= 424 and mouse[1] >= 534:
                                    if mouse[0] <= 424 + self.back_btn.get_width() and mouse[1] <=  534 + self.back_btn.get_height():

                                        if coins.actual_money >= self.cislo_cena:
                                            self.play_sound("ka-ching")
                                            self.kupene_pet.append(self.actualne_pet)
                                            self.chybajuce_pet.remove(self.actualne_pet)
                                            coins.actual_money -= self.cislo_cena

                                            if len(self.chybajuce_pet) < 6:
                                                self.pos_pet_shop.pop(len(self.chybajuce_pet))
                                            self.pressed_kupene = True
                                            self.cislo_cena2 = self.cislo_cena

                            if mouse[0] >= 35 and mouse[1] >= 534:
                                if mouse[0] <= 35 + self.buy_btn.get_width() and mouse[1] <= 534 + self.buy_btn.get_height():
                                    run_win_shop_menu = True
                                    run_win_shop_animals = False
                                    self.zvolene_pet = False
                                    self.pressed_kupene = False
                                    self.click = False

                            self.zvolene_pet = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_shop_menu = True
                            run_win_shop_animals = False
                            self.zvolene_pet = False
                            self.click = False
                self.draw_win_shop_animals()

            while run_win_shop_food:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_shop_food = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_shop_menu = True
                            run_win_shop_food = False
                            self.zvolene_ovocie = False
                            self.pocet_kusov = ""

                        if self.activated:
                            if event.key == pygame.K_BACKSPACE:
                                self.pocet_kusov = self.pocet_kusov[:-1]
                            else:
                                if len(self.pocet_kusov) < 2:
                                    self.pocet_kusov += event.unicode


                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            self.ovocie_button(mouse, 950, 75, self.pos_pet_shop, 3)

                            if mouse[0] >= 484 and mouse[1] >= 534:
                                if mouse[0] <= 484 + self.back_btn.get_width() and mouse[1] <= 534 + self.back_btn.get_height():
                                    if self.zvolene_ovocie and self.actualne_ovocie.pocet < 99:
                                            if self.actualne_ovocie not in self.veci_bag:       # ak nemas v batohu zvolenu vec tak sa ti tam prida
                                                self.veci_bag.append(self.actualne_ovocie)
                                                self.actualne_ovocie.pocet = 0
                                            try:
                                                if int(self.pocet_kusov) * 5 < coins.actual_money:
                                                    coins.actual_money -= int(self.pocet_kusov) * 5 if int(self.pocet_kusov) + self.actualne_ovocie.pocet <= 99 else (99 - self.actualne_ovocie.pocet) * 5
                                                    self.actualne_ovocie.pocet += int(self.pocet_kusov) if int(self.pocet_kusov) + self.actualne_ovocie.pocet <= 99 else 99 - self.actualne_ovocie.pocet
                                                    self.zvolene_ovocie = False
                                                    self.play_sound("ka-ching")
                                                else:
                                                    kusov = int(coins.actual_money // 5)      # kolko ti moze nakupit kusov elixiru, jednoducho pocita kolko ti moze max. nakupit za peniaze ktore mas
                                                    if self.actualne_ovocie.pocet + kusov <= 99:
                                                        coins.actual_money -= kusov * 5
                                                        self.actualne_ovocie.pocet += kusov
                                                        self.zvolene_ovocie = False
                                                    else:
                                                        kusov = 99 - self.actualne_ovocie.pocet
                                                        coins.actual_money -= kusov * 5
                                                        self.actualne_ovocie.pocet += kusov
                                                        self.zvolene_ovocie = False
                                                    self.play_sound("ka-ching")
                                            except:
                                                pass

                            if mouse[0] >= 90 and mouse[1] >= 534:
                                if mouse[0] <= 90 + self.buy_btn.get_width() and mouse[1] <= 534 + self.buy_btn.get_height():
                                    run_win_shop_menu = True
                                    run_win_shop_food = False
                                    self.zvolene_ovocie = False

                            self.pocet_kusov = ""
                            self.activated = False

                        if self.enter_kusov.collidepoint(event.pos) and self.zvolene_ovocie:
                                self.activated = True
                self.draw_win_shop_food()

            while run_win_mission:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_mission = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            if mouse[0] >= 640 and mouse[1] >= 550 and mouse[0] <= 640 + self.get_btn.get_width() and mouse[1] <= 550 + self.get_btn.get_height():
                                if self.total_killed_monsters >= 25 and pet_jednorozec not in self.kupene_pet:
                                    self.kupene_pet.append(pet_jednorozec)
                                    self.mission_pets[0] = None

                                if self.total_killed_monsters >= 50 and pet_helmet not in self.kupene_pet:
                                    self.kupene_pet.append(pet_helmet)
                                    self.mission_pets[1] = None

                                if self.boss_fight_wins >= 10 and pet_ohnivy_robot not in self.kupene_pet:
                                    self.kupene_pet.append(pet_ohnivy_robot)
                                    self.mission_pets[2] = None

                                if self.boss_fight_wins >= 30 and pet_rybohen not in self.kupene_pet:
                                    self.kupene_pet.append(pet_rybohen)
                                    self.mission_pets[3] = None

                                if self.wins >= 60 and pet_strom not in self.kupene_pet:
                                    self.kupene_pet.append(pet_strom)
                                    self.mission_pets[4] = None

                                if self.skore >= 500 and pet_velka_papula not in self.kupene_pet:
                                    self.kupene_pet.append(pet_velka_papula)
                                    self.mission_pets[5] = None

                            if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
                                run_win_2 = True
                                run_win_mission = False


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = True
                            run_win_mission = False
                self.draw_win_mission()

            while run_win_bed:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        run_win_bed = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()

                            self.pet_button(mouse, 725, 532, self.pos_pets_buttons, 6)

                            if mouse[0] >= 765 and mouse[1] >= 560 and mouse[0] <= 765 + self.back_btn.get_width() and mouse[1] <= 560 + self.back_btn.get_height():
                                run_win_2 = True
                                run_win_bed = False
                                self.zvolene_pet = False
                                self.pocet = 0

                            if mouse[0] >= 55 and mouse[1] >= 562 and mouse[0] <= 55 + self.sipka_dole.get_width() and mouse[1] <= 562 + self.sipka_dole.get_height() and self.pocet > 0:
                                self.pocet -= 6

                            if mouse[0] >= 730 and mouse[1] >= 562 and mouse[0] <= 730 + self.sipka_dole.get_width() and mouse[1] <= 562 + self.sipka_dole.get_height() and self.pocet < len(self.ospalne_pets) - 6:
                                self.pocet += 6

                            if self.zvolene_pet:
                                if self.pets_v_posteli[0] == None and mouse[0] >= self.pos_pelech[0][0] and mouse[1] >= self.pos_pelech[0][1] and mouse[0] <= self.pos_pelech[0][2] and mouse[1] <= self.pos_pelech[0][3]:
                                    self.pets_v_posteli[0] = self.actualne_pet
                                    self.ospalne_pets.remove(self.actualne_pet)

                                    self.pets_v_posteli[0].cas_od_kedy_spi = datetime.now()


                                if self.pets_v_posteli[1] == None and mouse[0] >= self.pos_pelech[1][0] and mouse[1] >= self.pos_pelech[1][1] and mouse[0] <= self.pos_pelech[1][2] and mouse[1] <= self.pos_pelech[1][3]:
                                    self.pets_v_posteli[1] = self.actualne_pet
                                    self.ospalne_pets.remove(self.actualne_pet)

                                    self.pets_v_posteli[1].cas_od_kedy_spi = datetime.now()

                                if self.pets_v_posteli[2] == None and mouse[0] >= self.pos_pelech[2][0] and mouse[1] >= self.pos_pelech[2][1] and mouse[0] <= self.pos_pelech[2][2] and mouse[1] <= self.pos_pelech[2][3]:
                                    self.pets_v_posteli[2] = self.actualne_pet
                                    self.ospalne_pets.remove(self.actualne_pet)

                                    self.pets_v_posteli[2].cas_od_kedy_spi = datetime.now()


                            if self.btn3:
                                if self.pets_v_posteli[0] != None and int(self.pets_v_posteli[0].get_sleep()) + int((datetime.now() - self.pets_v_posteli[0].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) >= 90 and self.pos_pelech[0][0] + 9 <= mouse[0] <= self.pos_pelech[0][0] + 111 and self.pos_pelech[0][1] - 58 <= mouse[1] <= self.pos_pelech[0][1] - 35:
                                    self.pets_v_posteli[0].sleep = self.pets_v_posteli[0].sleep + int((datetime.now() - self.pets_v_posteli[0].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) if self.pets_v_posteli[0].sleep + int((datetime.now() - self.pets_v_posteli[0].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) <= 99 else 100
                                    self.pets_v_posteli[0] = None

                                if self.pets_v_posteli[1] != None and int(self.pets_v_posteli[1].get_sleep()) + int((datetime.now() - self.pets_v_posteli[1].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) >= 90 and self.pos_pelech[1][0] + 9 <= mouse[0] <= self.pos_pelech[1][0] + 111 and self.pos_pelech[1][1] - 58 <= mouse[1] <= self.pos_pelech[1][1] - 35:
                                    self.pets_v_posteli[1].sleep = self.pets_v_posteli[1].sleep + int((datetime.now() - self.pets_v_posteli[1].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) if self.pets_v_posteli[1].sleep + int((datetime.now() - self.pets_v_posteli[1].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) <= 99 else 100
                                    self.pets_v_posteli[1] = None

                                if self.pets_v_posteli[2] != None and int(self.pets_v_posteli[2].get_sleep()) + int((datetime.now() - self.pets_v_posteli[2].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) >= 90 and self.pos_pelech[2][0] + 9 <= mouse[0] <= self.pos_pelech[2][0] + 111 and self.pos_pelech[2][1] - 58 <= mouse[1] <= self.pos_pelech[2][1] - 35:
                                    self.pets_v_posteli[2].sleep = self.pets_v_posteli[2].sleep + int((datetime.now() - self.pets_v_posteli[2].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) if self.pets_v_posteli[2].sleep + int((datetime.now() - self.pets_v_posteli[2].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) <= 99 else 100
                                    self.pets_v_posteli[2] = None

                            self.zvolene_pet = False
                            self.btn3 = False

                        if event.button == 3:
                            self.btn3 = True

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run_win_2 = True
                            run_win_bed = False
                            self.zvolene_pet = False
                            self.pocet = 0
                self.draw_win_bed()

        pygame.quit()

    def draw_win_1(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_1.png")))

        mouse = pygame.mouse.get_pos()

        if mouse[0] >= self.x_pozicia_buttons and mouse[1] >= 220 and mouse[0] <= self.x_pozicia_buttons + self.start_btn.get_width() and mouse[1] <= 220 + self.start_btn.get_height():
            self.blit_zmensene_btn(self.start_btn, self.x_pozicia_buttons, 220)
        else:
            self.blit_normal_btn(self.start_btn, self.x_pozicia_buttons, 220)


        if mouse[0] >= self.x_pozicia_buttons and mouse[1] >= 300 and mouse[0] <= self.x_pozicia_buttons + self.save_btn.get_width() and mouse[1] <= 300 + self.save_btn.get_height():
            self.blit_zmensene_btn(self.save_btn, self.x_pozicia_buttons, 300)
        else:
            self.blit_normal_btn(self.save_btn, self.x_pozicia_buttons, 300)


        if mouse[0] >= self.x_pozicia_buttons and mouse[1] >= 380 and mouse[0] <= self.x_pozicia_buttons + self.exit_btn.get_width() and mouse[1] <= 380 + self.exit_btn.get_height():
            self.blit_zmensene_btn(self.exit_btn, self.x_pozicia_buttons, 380)
        else:
            self.blit_normal_btn(self.exit_btn, self.x_pozicia_buttons, 380)


        if mouse[0] >= 855 and mouse[1] >= 537 and mouse[0] <= 855 + self.settings_btn.get_width() and mouse[1] <= 537 + self.settings_btn.get_height():
            self.blit_zmensene_btn(self.settings_btn, 855, 537)
        else:
            self.blit_normal_btn(self.settings_btn, 855, 537)

        pygame.display.update()

    def win_save(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_save.png")))

        mouse = pygame.mouse.get_pos()

        if mouse[0] >= 276 and mouse[1] >= 335 and mouse[0] <= 276 + self.yes_btn.get_width() and mouse[1] <= 335 + self.yes_btn.get_height():
            self.blit_zmensene_btn(self.yes_btn, 276, 335)
        else:
            self.blit_normal_btn(self.yes_btn, 276, 335)


        if mouse[0] >= 547 and mouse[1] >= 335 and mouse[0] <= 547 + self.no_btn.get_width() and mouse[1] <= 335 + self.no_btn.get_height():
            self.blit_zmensene_btn(self.no_btn, 547, 335)
        else:
            self.blit_normal_btn(self.no_btn, 547, 335)

        pygame.display.update()

    def draw_exit(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_1.png")))
        self.win.blit(pygame.image.load(os.path.join(working_path_images, "win_exit.png")), (0, self.y))

        mouse_exit = pygame.mouse.get_pos()

        if self.y > 0:
            self.y -= 10

        else:
            if mouse_exit[0] >= 276 and mouse_exit[1] >= 335 and mouse_exit[0] <= 276 + self.yes_btn.get_width() and mouse_exit[1] <= 335 + self.yes_btn.get_height():
                self.blit_zmensene_btn(self.yes_btn, 276, 335)
            else:
                self.blit_normal_btn(self.yes_btn, 276, 335)


            if mouse_exit[0] >= 547 and mouse_exit[1] >= 335 and mouse_exit[0] <= 547 + self.no_btn.get_width() and mouse_exit[1] <= 335 + self.no_btn.get_height():
                self.blit_zmensene_btn(self.no_btn, 547, 335)
            else:
                self.blit_normal_btn(self.no_btn, 547, 335)

        pygame.display.update()

    def draw_win_settings(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_settings.png")))

        mouse = pygame.mouse.get_pos()

        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)


        pygame.display.update()

    def draw_win_2(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_2.png")))

        self.win.blit(tips[self.tips_counter], (313, 565))

        mouse = pygame.mouse.get_pos()

        if self.pets_v_posteli[0] != None:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "name tag " + self.pets_v_posteli[0].druh + ".png")), (582, 239))

        if self.pets_v_posteli[1] != None:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "name tag " + self.pets_v_posteli[1].druh + ".png")), (704, 238))

        if self.pets_v_posteli[2] != None:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "name tag " + self.pets_v_posteli[2].druh + ".png")), (827, 238))


        try:
            max_storage = max(round((self.actual_time - self.bane_cas_ohen).total_seconds() * coins_ohen.coins_per_sec), round((self.actual_time - self.bane_cas_svetlo).total_seconds() * coins_svetlo.coins_per_sec), round((self.actual_time - self.bane_cas_zem).total_seconds() * coins_zem.coins_per_sec)) # je pramenna ktora ukazuje ktora z minci ma najvacsi pocet
            if max_storage < self.max_cap:
                pygame.draw.rect(self.win, (229, 232, 225), (473, 292 - 110 * max_storage // self.max_cap, 98, 110 * max_storage // self.max_cap))
            else:
                pygame.draw.rect(self.win, (229, 232, 225), (473, 182, 98, 110))
        except:
            pass


        font = pygame.font.SysFont("comicsans", 28)
        storage_nadpis = font.render("Storage", 1, (43, 42, 42))
        self.win.blit(storage_nadpis, (487, 184))


        money = self.main_font.render(str(coins.actual_money), 1, (0, 0, 0))      # 255, 255, 190
        money_ohen = self.main_font.render(str(coins_ohen.actual_money), 1, (0, 0, 0))
        money_svetlo = self.main_font.render(str(coins_svetlo.actual_money), 1, (0, 0, 0))
        money_zem = self.main_font.render(str(coins_zem.actual_money), 1, (0, 0, 0))



        width_money = max(money.get_width(), money_ohen.get_width(), money_svetlo.get_width(), money_zem.get_width())
        self.layer_pod_mince = pygame.image.load(os.path.join(working_path_images, "layer_pod_mince_v_bani.png"))   # vo win_shops, win_2, mines
        self.win.blit(pygame.transform.scale(self.layer_pod_mince, (width_money + 48, 112)), (291, 182))


        dis = 301
        self.win.blit(money, (dis + 30, 184))
        self.win.blit(coins.animation_coin(self.anim_coin), (dis, 184))

        self.win.blit(money_ohen, (dis + 30, 212))
        self.win.blit(coins_ohen.animation_coin(self.anim_coin), (dis, 212))

        self.win.blit(money_svetlo, (dis + 30, 240))
        self.win.blit(coins_svetlo.animation_coin(self.anim_coin), (dis, 240))

        self.win.blit(money_zem, (dis + 30, 268))
        self.win.blit(coins_zem.animation_coin(self.anim_coin), (dis, 268))




        font = pygame.font.SysFont("comicsans", 35)
        name = font.render(f"Name: {self.name_player}", 1, (255, 255, 255) if not self.activated else (0, 0, 0))
        self.win.blit(name, (480, 10))

        total_pets = font.render(f"Total pets: {len(self.kupene_pet)}", 1, (255, 255, 255))
        self.win.blit(total_pets, (480, 40))

        skore = font.render(f"Skore: {self.skore}", 1, (255, 255, 255))
        self.win.blit(skore, (480, 70))

        wins = font.render(f"Wins: {self.wins}", 1, (255, 255, 255))
        self.win.blit(wins, (480, 100))

        boss_fight_wins = font.render(f"Boss fight wins: {self.boss_fight_wins}", 1, (255, 255, 255))
        self.win.blit(boss_fight_wins, (480, 130))

        total_killed_monsters = font.render(f"Killed monsters: {self.total_killed_monsters}", 1, (255, 255, 255))
        self.win.blit(total_killed_monsters, (480, 160))

        self.win.blit(self.edit_btn, (920, 0))

        if mouse[0] >= 316 and mouse[1] >= 25 and mouse[0] <= 446 and mouse[1] <= 155:
            self.blit_normal_btn(self.edit_btn, 416, 125)


        if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 75 and mouse[0] <= self.x_pozicia_buttons_win_2 + self.fight_btn.get_width() and mouse[1] <= 75 + self.fight_btn.get_height():
            self.blit_zmensene_btn(self.fight_btn, self.x_pozicia_buttons_win_2, 75)
        else:
            self.blit_normal_btn(self.fight_btn, self.x_pozicia_buttons_win_2, 75)


        if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 155 and mouse[0] <= self.x_pozicia_buttons_win_2 + self.pets_btn.get_width() and mouse[1] <= 155 + self.pets_btn.get_height():
            self.blit_zmensene_btn(self.pets_btn, self.x_pozicia_buttons_win_2, 155)
        else:
            self.blit_normal_btn(self.pets_btn, self.x_pozicia_buttons_win_2, 155)


        if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 235 and mouse[0] <= self.x_pozicia_buttons_win_2 + self.mines_btn.get_width() and mouse[1] <= 235 + self.mines_btn.get_height():
            self.blit_zmensene_btn(self.mines_btn, self.x_pozicia_buttons_win_2, 235)
        else:
            self.blit_normal_btn(self.mines_btn, self.x_pozicia_buttons_win_2, 235)


        if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 315 and mouse[0] <= self.x_pozicia_buttons_win_2 + self.shop_btn.get_width() and mouse[1] <= 315 + self.shop_btn.get_height():
            self.blit_zmensene_btn(self.shop_btn, self.x_pozicia_buttons_win_2, 315)
        else:
            self.blit_normal_btn(self.shop_btn, self.x_pozicia_buttons_win_2, 315)


        if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 395 and mouse[0] <= self.x_pozicia_buttons_win_2 + self.mission_btn.get_width() and mouse[1] <= 395 + self.mission_btn.get_height():
            self.blit_zmensene_btn(self.mission_btn, self.x_pozicia_buttons_win_2, 395)
        else:
            self.blit_normal_btn(self.mission_btn, self.x_pozicia_buttons_win_2, 395)


        if mouse[0] >= self.x_pozicia_buttons_win_2 and mouse[1] >= 475 and mouse[0] <= self.x_pozicia_buttons_win_2 + self.bed_btn.get_width() and mouse[1] <= 475 + self.bed_btn.get_height():
            self.blit_zmensene_btn(self.bed_btn, self.x_pozicia_buttons_win_2, 475)
        else:
            self.blit_normal_btn(self.bed_btn, self.x_pozicia_buttons_win_2, 475)

        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)


        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0

        pygame.display.update()

    def draw_win_battle_menu(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_battle_menu.png")))

        mouse = pygame.mouse.get_pos()

        pos = 80
        for i in range(1, 4):
            self.choose_pet(pos, 129, pygame.image.load(os.path.join(working_path_images, "fight" + str(i) + ".png")), mouse)
            pos += 286


        try:
            font = pygame.font.SysFont("comicsans", 26)
            popis_battle = font.render(self.popis_battle[:54], 1, (86, 86, 86))
            popis_battle_dodatok = font.render(self.popis_battle[54:], 1, (86, 86, 86))
            self.win.blit(popis_battle, (50, 545))
            self.win.blit(popis_battle_dodatok, (50, 565))
        except:
            pass

        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)

        pygame.display.update()

    def draw_win_fight_menu(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_fight_menu.png")))

        pos, pos1, pos2, pos3 = 578, 51, 51, 51

        mouse = pygame.mouse.get_pos()


        if self.bool_fight_boss:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "tabula pets_to_fight.png")), (572, 436))
            for i in self.boss_fight_pets:
                self.choose_pet_to_die(pos, 441, i.get_img(), mouse)

                if self.create_pos_pet_button(pos, 441, self.pets[0]) not in self.pos_pets_to_fight:
                    self.pos_pets_to_fight.append(self.create_pos_pet_button(pos, 441, self.pets[0]))

                pos += 93



        for i in self.kupene_pet[self.pocet:self.pocet + 9]:
            self.choose_pet(pos1, 50, i.get_img(), mouse)
            self.vybrate_pet(self.pos_pets_buttons, self.kupene_pet)

            if self.create_pos_pet_button(pos1, 50, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos1, 50, self.pets[0]))
            pos1 += 95

        for i in self.kupene_pet[self.pocet + 9:self.pocet + 18]:
            self.choose_pet(pos2, 180, i.get_img(), mouse)

            if self.create_pos_pet_button(pos2, 180, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos2, 180, self.pets[0]))
            pos2 += 95

        for i in self.kupene_pet[self.pocet + 18:self.pocet + 27]:
            self.choose_pet(pos3, 310, i.get_img(), mouse)

            if self.create_pos_pet_button(pos3, 310, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos3, 310, self.pets[0]))
            pos3 += 95


        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)



        if not self.bool_fight_boss:
            if mouse[0] >= 640 and mouse[1] >= 550 and mouse[0] <= 640 + self.fight_btn.get_width() and mouse[1] <= 550 + self.fight_btn.get_height():
                self.blit_zmensene_btn(self.fight_btn, 640, 550)
            else:
                self.blit_normal_btn(self.fight_btn, 640, 550)


        if self.bool_fight_boss and len(self.boss_fight_pets) < 4:
            if mouse[0] >= 640 and mouse[1] >= 540 and mouse[0] <= 650 + self.add_btn.get_width() and mouse[1] <= 550 + self.add_btn.get_height():
                self.blit_zmensene_btn(self.add_btn, 640, 550)
            else:
                self.blit_normal_btn(self.add_btn, 640, 550)


        if self.bool_fight_boss and len(self.boss_fight_pets) == 4:
            if mouse[0] >= 640 and mouse[1] >= 540 and mouse[0] <= 640 + self.fight_btn.get_width() and mouse[1] <= 540 + self.fight_btn.get_height():
                self.blit_zmensene_btn(self.fight_btn, 640, 550)
            else:
                self.blit_normal_btn(self.fight_btn, 640, 550)





        if len(self.kupene_pet) > 27:
            if mouse[0] >= 923 and mouse[1] >= 50 and mouse[0] <= 923 + self.sipka_hore.get_width() and mouse[1] <= 50 + self.sipka_hore.get_height():
                self.win.blit(pygame.transform.scale(self.sipka_hore, (23, 23)), (924, 51))
            else:
                self.blit_normal_btn(self.sipka_hore, 923, 50)


            if mouse[0] >= 923 and mouse[1] >= 80 and mouse[0] <= 923 + self.sipka_hore.get_width() and mouse[1] <= 80 + self.sipka_hore.get_height():
                self.win.blit(pygame.transform.scale(self.sipka_dole, (23, 23)), (924, 81))
            else:
                self.blit_normal_btn(self.sipka_dole, 923, 80)


        if self.lack_sleep:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "vykricknik.png")), self.animation_suboj(125, 425))


        if self.zvolene_pet:
            self.win.blit(self.actualne_pet.img, (45, 490))

            Hero_health_text = self.main_font.render(f"HP: {self.actualne_pet.get_health()}", 1, (210, 190, 255))
            self.win.blit(Hero_health_text, (185, 440))

            dmg_text = self.main_font.render(f"Damage: {self.actualne_pet.get_dmg()}", 1, (210, 190, 255))
            self.win.blit(dmg_text, (185, 467))

            reg_txt = self.main_font.render(f"Heal: {self.actualne_pet.get_reg()}", 1, (210, 190, 255))
            self.win.blit(reg_txt, (185, 493))

            trieda = self.main_font.render(f"Type: {self.actualne_pet.get_trieda()}", 1, (210, 190, 255))
            self.win.blit(trieda, (185, 520))

            meno = self.main_font.render(f"Name: {self.actualne_pet.get_name()}", 1, (210, 190, 255))
            self.win.blit(meno, (185, 547))

            self.win.blit(pygame.transform.scale(self.actualne_pet.elixir.img, (45, 46)), (105, 476)) if self.actualne_pet.elixir != None and self.actualne_pet.elixir_duration > 0 else 0

            lvl = self.main_font.render(f"Level: {self.actualne_pet.lvl}", 1, (210, 190, 255))
            self.win.blit(lvl, (185, 571 + (59 / 2 - lvl.get_height() / 2)))

            sleep = self.main_font.render(f"{self.actualne_pet.get_sleep()}%", 1, (210, 190, 255))
            self.win.blit(sleep, (45 + self.moon.get_width(), 458))
            self.win.blit(self.moon, (50, 458))

            meal = self.main_font.render(f"{self.actualne_pet.get_food()}%", 1, (210, 190, 255))
            self.win.blit(meal, (49 + self.burger.get_width(), 587))
            self.win.blit(self.burger, (47, 589))
        pygame.display.update()

    def draw_win_fight_1v1(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_fight.png")))

        mouse = pygame.mouse.get_pos()


        self.draw_hero()
        self.draw_monster()

        if self.pressed_a and self.spustac:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(tien) * 3:
                damage_hero_text = self.main_font.render("- " + f"{self.Damage_hero}", 1, (205, 63, 63))
                self.win.blit(damage_hero_text, self.animation_suboj(791, 201))

                damage_monster_text = self.main_font.render("- " + f"{self.Damage_monster}", 1, (205, 63, 63))
                self.win.blit(damage_monster_text, self.animation_suboj(259, 201))


            elif self.anim_efekty_count < len(tien) * 3:
                try:
                    self.win.blit(self.actualne_pet.utok[self.anim_efekty_count // 3], (680, 135))
                except:
                    pass
                self.win.blit(tien[self.anim_efekty_count // 3], (145, 135))



        if self.pressed_s and self.spustac and self.pow_count <= 1:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(tien) * 3:
                damage_hero_text = self.main_font.render("- " + f"{self.Damage_hero}", 1, (179, 9, 9))
                self.win.blit(damage_hero_text, self.animation_suboj(791, 201))

                damage_monster_text = self.main_font.render("- " + f"{self.Damage_monster}", 1, (179, 9, 9))
                self.win.blit(damage_monster_text, self.animation_suboj(259, 201))

            elif self.anim_efekty_count < len(tien) * 3:
                try:
                    self.win.blit(self.actualne_pet.super_pow[self.anim_efekty_count // 3], (680, 120))
                except:
                    pass
                self.win.blit(tien[self.anim_efekty_count // 3], (145, 135))



        if self.pressed_r and self.reg_count <= 3 and self.spustac:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(healing) * 3:
                reg_hero_text = self.main_font.render("+ " + f"{self.regeneration_random_number}", 1, (176, 171, 57))
                self.win.blit(reg_hero_text, self.animation_suboj(270, 190))

            elif self.anim_efekty_count <= len(healing) * 3:
                self.win.blit(healing[self.anim_efekty_count // 3], (147, 155))




        if self.won_monster or self.won_hero:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "vyherna_tabula.png")), (321, 204))
            if mouse[0] >= 410 and mouse[1] >= 285 and mouse[0] <= 410 + self.quit_btn.get_width() and mouse[1] <= 285 + self.quit_btn.get_height():
                self.blit_zmensene_btn(self.quit_btn, 410, 285)
            else:
                self.blit_normal_btn(self.quit_btn, 410, 285)


        if self.won_hero:
            won_hero_text = self.main_font.render("You won!", 1, (255, 255, 255))
            self.win.blit(won_hero_text, (415, 210))
            self.win.blit(pygame.transform.rotate(pygame.image.load(os.path.join(working_path_images, "korunka.png")), 35), (300, 180))

            if coins.count_for_money == 0:
                coins.v_h = int(coins.vyhrate_money(self.Health_hero2, self.Health_monster2) * self.actualne_pet.more_coin)
                coins.actual_money += coins.v_h
                coins.count_for_money += 1
                self.wins += 1
                self.total_killed_monsters += 1
                self.skore += randint(10, 20)

            vyhrate_money_text = self.main_font.render("You gain " + str(coins.v_h), 1, (255, 255, 255))
            self.win.blit(vyhrate_money_text, (321 + 309 // 2 - vyhrate_money_text.get_width() // 2, 245))
            self.win.blit(coins.animation_coin(self.anim_coin), (321 + 309 // 2 + vyhrate_money_text.get_width() // 2 + 10, 245))

        if self.won_monster:
            won_monster_text = self.main_font.render("You lose!", 1, (255, 255, 255))
            self.win.blit(won_monster_text, (415, 210))
            self.win.blit(pygame.transform.rotate(pygame.image.load(os.path.join(working_path_images, "korunka.png")), -35), (610, 180))

            if coins.actual_money - randint(self.Health_hero2 * 10 // 100, self.Health_hero2 * 20 // 100) > 0:
                if coins.count_for_money == 0:
                    coins.p_h = coins.prehrate_money(self.Health_hero2, self.Health_monster2)
                    coins.actual_money -= coins.p_h
                    coins.count_for_money += 1
                    self.skore -= randint(5, 9) if self.skore > 9 else self.skore

                prehrate_money_text = self.main_font.render("You lose " + str(coins.p_h), 1, (255, 255, 255))
                self.win.blit(prehrate_money_text, (321 + 309 // 2 - prehrate_money_text.get_width() // 2, 245))
                self.win.blit(coins.animation_coin(self.anim_coin), (321 + 309 // 2 + prehrate_money_text.get_width() // 2 + 10, 245))


        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0

        pygame.display.update()

    def draw_win_fight_until_die(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_fight.png")))

        mouse_fight = pygame.mouse.get_pos()

        self.draw_hero()
        self.draw_monster()

        pos = 700

        self.win.blit(pygame.image.load(os.path.join(working_path_images, "next_pet tabula.png")), (790, 189))
        for i in self.monsters_to_die[self.monster_pointer:]:
            self.win.blit(i.img, (self.animation_move_to_left(pos), 193))
            pos += 95


        if self.won_hero and not self.spustac:
            self.next_pet = True
            self.monster_pointer += 1
            self.monsters_to_die.append(choice(self.monsters))
            self.won_hero = False

        if self.pressed_a and self.spustac:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(tien) * 3:

                damage_hero_text = self.main_font.render("- " + f"{self.Damage_hero}", 1, (205, 63, 63))
                self.win.blit(damage_hero_text, self.animation_suboj(785, 170))

                damage_monster_text = self.main_font.render("- " + f"{self.Damage_monster}", 1, (205, 63, 63))
                self.win.blit(damage_monster_text, self.animation_suboj(259, 201))


            elif self.anim_efekty_count < len(tien) * 3:
                try:
                    self.win.blit(self.actualne_pet.utok[self.anim_efekty_count // 3], (680, 135))
                except:
                    pass
                self.win.blit(tien[self.anim_efekty_count // 3], (145, 135))


        if self.pressed_s and self.spustac and self.pow_count <= 1:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(tien) * 3:
                damage_hero_text = self.main_font.render("- " + f"{self.Damage_hero}", 1, (179, 9, 9))
                self.win.blit(damage_hero_text, self.animation_suboj(785, 170))

                damage_monster_text = self.main_font.render("- " + f"{self.Damage_monster}", 1, (179, 9, 9))
                self.win.blit(damage_monster_text, self.animation_suboj(259, 201))

            elif self.anim_efekty_count < len(tien) * 3:
                try:
                    self.win.blit(self.actualne_pet.super_pow[self.anim_efekty_count // 3], (680, 120))
                except:
                    pass
                self.win.blit(tien[self.anim_efekty_count // 3], (145, 135))

        if self.pressed_r and self.reg_count <= 3 and self.spustac:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(healing) * 3:
                reg_hero_text = self.main_font.render("+ " + f"{self.regeneration_random_number}", 1, (176, 171, 57))
                self.win.blit(reg_hero_text, self.animation_suboj(270, 190))

            elif self.anim_efekty_count <= len(healing) * 3:
                self.win.blit(healing[self.anim_efekty_count // 3], (147, 155))

        if self.won_monster:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "vyherna_tabula.png")), (321, 204))

            won_monster_text = self.main_font.render(f"You killed {self.killed_monsters} monsters", 1, (255, 255, 255))
            self.win.blit(won_monster_text, (321 + 309 // 2 - won_monster_text.get_width() // 2, 210))


            if coins.actual_money - randint(self.Health_hero2 * 10 // 100, self.Health_hero2 * 20 // 100) > 0:
                if coins.count_for_money == 0:
                    coins.p_h = int(randint(14, 20) * self.killed_monsters * self.actualne_pet.more_coin)
                    coins.actual_money += coins.p_h
                    coins.count_for_money += 1
                    self.total_killed_monsters += self.killed_monsters
                    self.skore += randint(self.killed_monsters, self.killed_monsters * 2)

                prehrate_money_text = self.main_font.render("You gain " + str(coins.p_h), 1, (255, 255, 255))
                self.win.blit(prehrate_money_text, (321 + 309 // 2 - prehrate_money_text.get_width() // 2, 245))
                self.win.blit(coins.animation_coin(self.anim_coin), (321 + 309 // 2 + prehrate_money_text.get_width() // 2 + 10, 245))



            if mouse_fight[0] >= 410 and mouse_fight[1] >= 285 and mouse_fight[0] <= 410 + self.quit_btn.get_width() and mouse_fight[1] <= 285 + self.quit_btn.get_height():
                self.blit_zmensene_btn(self.quit_btn, 410, 285)
            else:
                self.blit_normal_btn(self.quit_btn, 410, 285)


        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0


        pygame.display.update()

    def draw_win_fight_boss(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_fight.png")))

        mouse_fight = pygame.mouse.get_pos()

        self.draw_hero()
        self.draw_monster()

        pos = 72


        self.win.blit(pygame.transform.flip(pygame.image.load(os.path.join(working_path_images, "next_pet tabula.png")), True, False), (-86, 189))
        for i in self.boss_fight_pets[self.pet_pointer:]:
            self.win.blit(pygame.transform.flip(i.img, True, False), (self.animation_move_to_right(pos), 193))
            pos -= 95

        if self.won_monster and not self.spustac and self.pet_pointer != len(self.boss_fight_pets):
            self.next_pet = True
            self.won_monster = False

        if self.pressed_a and self.spustac:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(tien) * 3:

                damage_hero_text = self.main_font.render("- " + f"{self.Damage_hero}", 1, (205, 63, 63))
                self.win.blit(damage_hero_text, self.animation_suboj(815, 201))

                damage_monster_text = self.main_font.render("- " + f"{self.Damage_monster}", 1, (205, 63, 63))
                self.win.blit(damage_monster_text, self.animation_suboj(259, 201))

            elif self.anim_efekty_count < len(tien) * 3:
                try:
                    self.win.blit(self.actualne_pet.utok[self.anim_efekty_count // 3], (680, 135))
                except:
                    pass
                self.win.blit(tien[self.anim_efekty_count // 3], (145, 135))

        if self.pressed_s and self.spustac and self.pow_count <= 1:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(tien) * 3:
                damage_hero_text = self.main_font.render("- " + f"{self.Damage_hero}", 1, (179, 9, 9))
                self.win.blit(damage_hero_text, self.animation_suboj(815, 201))

                damage_monster_text = self.main_font.render("- " + f"{self.Damage_monster}", 1, (179, 9, 9))
                self.win.blit(damage_monster_text, self.animation_suboj(259, 201))

            elif self.anim_efekty_count < len(tien) * 3:
                try:
                    self.win.blit(self.actualne_pet.super_pow[self.anim_efekty_count // 3], (680, 120))
                except:
                    pass
                self.win.blit(tien[self.anim_efekty_count // 3], (145, 135))

        if self.pressed_r and self.reg_count <= 3 and self.spustac:
            self.anim_efekty_count += 1

            if self.anim_efekty_count >= len(healing) * 3:
                reg_hero_text = self.main_font.render("+ " + f"{self.regeneration_random_number}", 1, (176, 171, 57))
                self.win.blit(reg_hero_text, self.animation_suboj(270, 190))

            elif self.anim_efekty_count <= len(healing) * 3:
                self.win.blit(healing[self.anim_efekty_count // 3], (147, 155))


        if self.Health_monster <= 0 or (self.actualne_pet.health <= 0 and self.pet_pointer == len(self.boss_fight_pets)):
            if self.won_monster or self.won_hero:
                self.win.blit(pygame.image.load(os.path.join(working_path_images, "vyherna_tabula.png")), (321, 204))
                if mouse_fight[0] >= 410 and mouse_fight[1] >= 285 and mouse_fight[0] <= 410 + self.quit_btn.get_width() and mouse_fight[1] <= 285 + self.quit_btn.get_height():
                    self.blit_zmensene_btn(self.quit_btn, 410, 285)
                else:
                    self.blit_normal_btn(self.quit_btn, 410, 285)

            if self.won_hero:
                won_hero_text = self.main_font.render("You won!", 1, (255, 255, 255))
                self.win.blit(won_hero_text, (415, 210))
                self.win.blit(pygame.transform.rotate(pygame.image.load(os.path.join(working_path_images, "korunka.png")), 35), (300, 180))

                if coins.count_for_money == 0:
                    coins.v_h = int(randint(100, 200) * self.actualne_pet.more_coin)
                    coins.actual_money += coins.v_h
                    coins.count_for_money += 1
                    self.wins += 1
                    self.boss_fight_wins += 1
                    self.total_killed_monsters += 1
                    self.skore += randint(25, 40)

                vyhrate_money_text = self.main_font.render("You gain " + str(coins.v_h), 1, (255, 255, 255))
                self.win.blit(vyhrate_money_text, (321 + 309 // 2 - vyhrate_money_text.get_width() // 2, 245))
                self.win.blit(coins.animation_coin(self.anim_coin), (321 + 309 // 2 + vyhrate_money_text.get_width() // 2 + 10, 245))

            if self.won_monster:
                won_monster_text = self.main_font.render("You lose!", 1, (255, 255, 255))
                self.win.blit(won_monster_text, (415, 210))
                self.win.blit(pygame.transform.rotate(pygame.image.load(os.path.join(working_path_images, "korunka.png")), -35), (610, 180))

                if coins.actual_money - randint(self.Health_hero2 * 10 // 100, self.Health_hero2 * 20 // 100) > 0:
                    if coins.count_for_money == 0:
                        coins.p_h = coins.prehrate_money(self.Health_hero2, self.Health_monster2)
                        coins.actual_money -= coins.p_h
                        coins.count_for_money += 1

                    prehrate_money_text = self.main_font.render("You lose " + str(coins.p_h), 1, (255, 255, 255))
                    self.win.blit(prehrate_money_text, (321 + 309 // 2 - prehrate_money_text.get_width() // 2, 245))
                    self.win.blit(coins.animation_coin(self.anim_coin), (321 + 309 // 2 + prehrate_money_text.get_width() // 2 + 10, 245))

        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0

        pygame.display.update()

    def draw_win_pets(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_pets.png")))

        mouse = pygame.mouse.get_pos()
        cena_font = pygame.font.SysFont("comicsans", 32)

        pos1, pos2, pos3 = 50, 50, 50
        for i in self.kupene_pet[self.pocet:self.pocet + 6]:
            self.choose_pet(pos1, 50, i.get_img(), mouse)
            self.vybrate_pet(self.pos_pets_buttons, self.kupene_pet)


            if self.create_pos_pet_button(pos1, 50, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos1, 50, self.pets[0]))
            pos1 += 100

        for i in self.kupene_pet[self.pocet + 6:self.pocet + 12]:
            self.choose_pet(pos2, 180, i.get_img(), mouse)

            if self.create_pos_pet_button(pos2, 180, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos2, 180, self.pets[0]))
            pos2 += 100


        for i in self.kupene_pet[self.pocet + 12:self.pocet + 18]:
            self.choose_pet(pos3, 310, i.get_img(), mouse)

            if self.create_pos_pet_button(pos3, 310, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos3, 310, self.pets[0]))
            pos3 += 100


        for i in self.veci_bag:
            if i.pocet < 1:
                i.pocet = 0
                self.veci_bag.remove(i)


        pos = 720
        for i in self.veci_bag[:3]:
            self.choose_pet(pos, 75, i.get_img(), mouse)
            self.vybrate_ovocie(self.pos_pet_shop, self.veci_bag)

            pocet = cena_font.render(f"{i.pocet}x", 1, (255, 255, 255))
            self.win.blit(pocet, (pos + 40, 115))

            if self.create_pos_pet_button(pos, 75, i.get_img()) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos, 75, i.img))
            pos += 72

        pos1 = 720
        for i in self.veci_bag[3:6]:
            self.choose_pet(pos1, 150, i.get_img(), mouse)

            pocet = cena_font.render(f"{i.pocet}x", 1, (255, 255, 255))
            self.win.blit(pocet, (pos1 + 40, 190))

            if self.create_pos_pet_button(pos1, 150, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos1, 150, i.img))
            pos1 += 72

        pos2 = 720
        for i in self.veci_bag[6:9]:
            self.choose_pet(pos2, 225, i.get_img(), mouse)

            pocet = cena_font.render(f"{i.pocet}x", 1, (255, 255, 255))
            self.win.blit(pocet, (pos2 + 40, 265))

            if self.create_pos_pet_button(pos2, 225, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos2, 225, i.img))
            pos2 += 72

        pos3 = 720
        for i in self.veci_bag[9:12]:
            self.choose_pet(pos3, 300, i.get_img(), mouse)

            pocet = cena_font.render(f"{i.pocet}x", 1, (255, 255, 255))
            self.win.blit(pocet, (pos3 + 40, 340))

            if self.create_pos_pet_button(pos3, 300, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos3, 300, i.img))
            pos3 += 72


        bag = self.main_font.render("Bag", 1, (79, 35, 19))   # 86, 36, 15      | 94, 41, 22      | 96, 53, 37
        self.win.blit(bag, (709 + (110 - bag.get_width() / 2), 27))


        if self.zvolene_pet:
            self.win.blit(self.actualne_pet.img, (45, 490))

            Hero_health_text = self.main_font.render(f"HP: {self.actualne_pet.get_health()}", 1, (210, 190, 255))
            self.win.blit(Hero_health_text, (185, 440))

            dmg_text = self.main_font.render(f"Damage: {self.actualne_pet.get_dmg()}", 1, (210, 190, 255))
            self.win.blit(dmg_text, (185, 467))

            reg_txt = self.main_font.render(f"Heal: {self.actualne_pet.get_reg()}", 1, (210, 190, 255))
            self.win.blit(reg_txt, (185, 493))

            trieda = self.main_font.render(f"Type: {self.actualne_pet.get_trieda()}", 1, (210, 190, 255))
            self.win.blit(trieda, (185, 520))

            meno = self.main_font.render(f"Name: {self.actualne_pet.get_name()}", 1, (210, 190, 255))
            self.win.blit(meno, (185, 547))

            self.win.blit(pygame.transform.scale(self.actualne_pet.elixir.img, (45, 46)), (105, 476)) if self.actualne_pet.elixir != None and self.actualne_pet.elixir_duration > 0 else 0

            lvl = self.main_font.render(f"Level: {self.actualne_pet.lvl}", 1, (210, 190, 255))
            self.win.blit(lvl, (185, 571 + (59 / 2 - lvl.get_height() / 2)))


            sleep = self.main_font.render(f"{self.actualne_pet.get_sleep()}%", 1, (210, 190, 255))
            self.win.blit(sleep, (45 + self.moon.get_width(), 458))
            self.win.blit(self.moon, (50, 458))


            meal = self.main_font.render(f"{self.actualne_pet.get_food()}%", 1, (210, 190, 255))
            self.win.blit(meal, (49 + self.burger.get_width(), 587))
            self.win.blit(self.burger, (47, 589))

            self.win.blit(self.upgrade_btn_small, (393, 582))   #upgrade_btn pre pets

            if 393 <= mouse[0] <= 393 + self.upgrade_btn_small.get_width():
                if 582 <= mouse[1] <= 582 + self.upgrade_btn_small.get_height():
                    layer_cena = pygame.image.load(os.path.join(working_path_images, "layer_cena.png"))       # ak ukazes na upgrade_btn tak ten layer aj cena sa ti zobrazi
                    money_upgrade = cena_font.render(f"{self.actualne_pet.cena_upgrade()}", 1, (0, 0, 0))
                    self.win.blit(pygame.transform.scale(layer_cena, (money_upgrade.get_width() + 32, layer_cena.get_height())), (503, 582 + 18 - layer_cena.get_height() / 2))


                    self.win.blit(money_upgrade, (507, 582 + 20 - money_upgrade.get_height() / 2))
                    self.win.blit(pygame.transform.scale(self.actualne_pet.druh_coin.imgs[0], (18, 18)), (511 + money_upgrade.get_width(), 582 + 20 - money_upgrade.get_height() / 2))

        ohen_money = cena_font.render(f"{coins_ohen.actual_money}", 1, (0, 0, 0))
        svetlo_money = cena_font.render(f"{coins_svetlo.actual_money}", 1, (0, 0, 0))
        zem_money = cena_font.render(f"{coins_zem.actual_money}", 1, (0, 0, 0))

        self.win.blit(pygame.transform.scale(pygame.image.load(os.path.join(working_path_images, "layer_pod_mince_v_bani.png")), (max(ohen_money.get_width(), svetlo_money.get_width(), zem_money.get_width()) + coins_ohen.get_width() + 10, 87)), (503, 436))   #452, 520    tu je layer pod mince vo win_pets
        # peniaze s mincami
        self.win.blit(pygame.transform.scale(coins_ohen.animation_coin(self.anim_coin), (18, 18)), (485 + coins_ohen.imgs[0].get_width(), 441))
        self.win.blit(ohen_money, (507 + coins_ohen.imgs[0].get_width(), 441))

        self.win.blit(pygame.transform.scale(coins_svetlo.animation_coin(self.anim_coin), (18, 18)), (485 + coins_svetlo.imgs[0].get_width(), 469))
        self.win.blit(svetlo_money, (507 + coins_svetlo.imgs[0].get_width(), 469))

        self.win.blit(pygame.transform.scale(coins_zem.animation_coin(self.anim_coin), (18, 18)), (485 + coins_zem.imgs[0].get_width(), 497))
        self.win.blit(zem_money, (507 + coins_zem.imgs[0].get_width(), 497))

        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0

        if len(self.kupene_pet) > 18:
            if mouse[0] >= 664 and mouse[1] >= 50 and mouse[0] <= 664 + self.sipka_hore.get_width() and mouse[1] <= 50 + self.sipka_hore.get_height():
                self.win.blit(pygame.transform.scale(self.sipka_hore, (23, 23)), (664, 51))
            else:
                self.blit_normal_btn(self.sipka_hore, 663, 50)


            if mouse[0] >= 664 and mouse[1] >= 79 and mouse[0] <= 664 + self.sipka_dole.get_width() and mouse[1] <= 79 + self.sipka_dole.get_height():
                self.win.blit(pygame.transform.scale(self.sipka_dole, (23, 23)), (664, 80))
            else:
                self.blit_normal_btn(self.sipka_dole, 663, 79)


        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)


        if self.zvolene_ovocie:
            try:
                self.win.blit(self.actualne_ovocie.img, (mouse[0] - self.actualne_ovocie.img.get_width() // 2, mouse[1] - self.actualne_ovocie.img.get_height() // 2))
            except:
                pass


        pygame.display.update()

    def draw_win_mines(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_mines.png")))

        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0

        mouse = pygame.mouse.get_pos()

        self.pos_mines = [(217, 258, 480, 328), (217, 372, 480, 442), (217, 491, 480, 561)]


        cena_font = pygame.font.SysFont("comicsans", 31)

        ohen_money = cena_font.render(f"{coins_ohen.actual_money}", 1, (0, 0, 0))
        svetlo_money = cena_font.render(f"{coins_svetlo.actual_money}", 1, (0, 0, 0))
        zem_money = cena_font.render(f"{coins_zem.actual_money}", 1, (0, 0, 0))

        upgade_bane = pygame.image.load(os.path.join(working_path_images, "upgrade_bane.png"))
        max_upgrade_bane = pygame.image.load(os.path.join(working_path_images, "max_upgrade_bane.png"))

        znacka = pygame.image.load(os.path.join(working_path_images, "znacka.png"))

        if self.pressed_prvy_ohen:
            self.win.blit(znacka, (147, 263))

        if self.pressed_prvy_svetlo:
            self.win.blit(znacka, (147, 379))

        if self.pressed_prvy_zem:
            self.win.blit(znacka, (147, 494))

        if self.btn3:
            for i in range(3):
                if self.pos_mines[i][0] <= mouse[0] <= self.pos_mines[i][2] or 500 <= mouse[0] <= 624:
                    if self.pos_mines[i][1] <= mouse[1] <= self.pos_mines[i][3]:
                        self.x = i
                        self.win.blit(pygame.transform.scale(pygame.image.load(os.path.join(working_path_images, "layer_pre_upgrade_mines.png")), (140, 53)), (self.pos_mines[i][0] - 140, self.pos_mines[i][1] + 8))

                        if self.coins_list[i].upgrade_lvl < 8:
                            self.win.blit(upgade_bane, (500, self.pos_mines[i][1] + 12))

                            cena_upgrade_txt = cena_font.render("Cost:    250", 1, (255, 250, 250))
                            self.win.blit(cena_upgrade_txt, (self.pos_mines[i][0] - 137, self.pos_mines[i][1] + 14))
                            self.win.blit(pygame.transform.scale(self.coins_list[i].imgs[0], (18, 18)), (self.pos_mines[i][0] - 81, self.pos_mines[i][1] + 14))
                            #  int(self.coins_list[i].coins_per_sec * 3600) if int(self.coins_list[i].coins_per_sec * 3600) < 1000 else str(int(self.coins_list[i].coins_per_sec * 3600)) + chr(107)
                        else:
                            self.win.blit(max_upgrade_bane, (500, self.pos_mines[i][1] + 12))
                            max_lvl = cena_font.render("Max level", 1, (255, 250, 250))
                            self.win.blit(max_lvl, (self.pos_mines[i][0] - 135, self.pos_mines[i][1] + 14))


                        coin_hour_txt = cena_font.render(f"/hour: {int(self.coins_list[i].coins_per_sec * 3600) if int(self.coins_list[i].coins_per_sec * 3600) < 1000 else str(round(self.coins_list[i].coins_per_sec * 3.6, 1)) + 'k'}", 1, (255, 250, 250))
                        self.win.blit(coin_hour_txt, (self.pos_mines[i][0] + coins.imgs[0].get_width() - 137, self.pos_mines[i][1] + 38))

                        self.win.blit(pygame.transform.scale(self.coins_list[i].imgs[0], (18, 18)), (self.pos_mines[i][0] - 137, self.pos_mines[i][1] + 38))

        if 620 <= mouse[0] <= 950:
            if 0 <= mouse[1] <= 213:
                self.win.blit(pygame.image.load(os.path.join(working_path_images, "storage_layer.png")), (614, 10))

                if self.upgrade_storage == self.max_storage:
                    self.win.blit(pygame.transform.scale(max_upgrade_bane, (98, 36)), (628, 114))

                font = pygame.font.SysFont("comicsans", 26)

                if not self.pressed_prvy_ohen:                  # stlacis na banu a mas cas time_ohen dalsi cas mas ktory ti bezi stale a to je vo "while loop vo win_mines" no a ty od toho neustale sa meniaceho casu odcitavas cas kedy si stlacil na banu
                    self.win.blit(pygame.transform.scale(coins_ohen.imgs[0], (18, 18)), (627, 15))
                    try:
                        ohen_storage = font.render(f": {round((self.actual_time - self.bane_cas_ohen).total_seconds() * coins_ohen.coins_per_sec)}", 1, (5, 5, 5)) if round((self.actual_time - self.bane_cas_ohen).total_seconds() * coins_ohen.coins_per_sec) < self.max_cap else font.render(f": {self.max_cap}", 1, (5, 5, 5))
                        self.win.blit(ohen_storage, (647, 16))
                    except:
                        pass

                if not self.pressed_prvy_svetlo:
                    self.win.blit(pygame.transform.scale(coins_svetlo.imgs[0], (18, 18)), (627, 40))
                    try:
                        svetlo_storage = font.render(f": {round((self.actual_time - self.bane_cas_svetlo).total_seconds() * coins_svetlo.coins_per_sec)}", 1, (5, 5, 5)) if round((self.actual_time - self.bane_cas_svetlo).total_seconds() * coins_svetlo.coins_per_sec) < self.max_cap else font.render(f": {self.max_cap}", 1, (5, 5, 5))
                        self.win.blit(svetlo_storage, (647, 41))
                    except:
                        pass

                if not self.pressed_prvy_zem:
                    self.win.blit(pygame.transform.scale(coins_zem.imgs[0], (18, 18)), (627, 65))
                    try:
                        zem_storage = font.render(f": {round((self.actual_time - self.bane_cas_zem).total_seconds() * coins_zem.coins_per_sec)}", 1, (5, 5, 5)) if round((self.actual_time - self.bane_cas_zem).total_seconds() * coins_zem.coins_per_sec) < self.max_cap else font.render(f": {self.max_cap}", 1, (5, 5, 5))
                        self.win.blit(zem_storage, (647, 66))
                    except:
                        pass


                cap = font.render(f"Capacity: {self.max_cap if self.max_cap < 1000 else str(round(self.max_cap / 1000, 1)) + chr(107)}", 1, (5, 5, 5))
                self.win.blit(cap, (620, 90))   #capacity

        # layer pod mincami v lavo hore
        self.win.blit(pygame.transform.scale(self.layer_pod_mince, (max(ohen_money.get_width(), svetlo_money.get_width(), zem_money.get_width()) + coins_ohen.get_width() + 15, 84)), (0, 0))

        self.win.blit(pygame.transform.scale(coins_ohen.animation_coin(self.anim_coin), (18, 18)), (8, 7))
        self.win.blit(ohen_money, (10 + coins_ohen.imgs[0].get_width(), 7))

        self.win.blit(pygame.transform.scale(coins_svetlo.animation_coin(self.anim_coin), (18, 18)), (8, 33))
        self.win.blit(svetlo_money, (10 + coins_svetlo.imgs[0].get_width(), 33))

        self.win.blit(pygame.transform.scale(coins_zem.animation_coin(self.anim_coin), (18, 18)), (8, 59))
        self.win.blit(zem_money, (10 + coins_zem.imgs[0].get_width(), 59))


        if self.pressed_kupene:
            uprate_money_text = self.main_font.render(f"- {self.cena_upgrade_storage}", 1, (255, 255, 190))
            self.win.blit(uprate_money_text, (self.animation_suboj(739, 120)))
            self.win.blit(coins.imgs[0], (self.animation_suboj(745 + uprate_money_text.get_width(), 120)))


        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)

        pygame.display.update()

    def draw_win_shop_menu(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_shop_menu.png")))

        mouse = pygame.mouse.get_pos()
        dvere_animal = pygame.image.load(os.path.join(working_path_images, "dvere_animal.png"))
        dvere_food = pygame.image.load(os.path.join(working_path_images, "dvere_food.png"))

        if mouse[0] >= 420 and mouse[1] >= 278 and mouse[0] <= 420 + dvere_animal.get_width() and mouse[1] <= 278 + dvere_animal.get_height():
            self.blit_zmensene_btn(dvere_animal, 419, 276)

        if mouse[0] >= 558 and mouse[1] >= 278 and mouse[0] <= 558 + dvere_animal.get_width() and mouse[1] <= 278 + dvere_animal.get_height():
            self.blit_zmensene_btn(dvere_food, 556, 276)


        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)
        pygame.display.update()

    def draw_win_shop_animals(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_shop_animal.png")))

        money = self.main_font.render(f"{coins.actual_money}", 1, (255, 255, 190))
        self.win.blit(pygame.transform.scale(self.layer_pod_mince, (money.get_width() + coins.imgs[0].get_width() + 15, coins.imgs[0].get_height() + 12)), (590, 398))
        self.win.blit(money, (598 + coins.imgs[0].get_width(), 405))
        self.win.blit(coins.animation_coin(self.anim_coin), (595, 405))


        mouse = pygame.mouse.get_pos()
        pos = pos2 = 631


        for i in self.pets:
            if i not in self.kupene_pet and i not in self.chybajuce_pet and i not in self.mission_pets:
                self.chybajuce_pet.append(i)

        for i in self.chybajuce_pet[:3]:

            if i not in self.kupene_pet:
                self.choose_pet(pos, 75, i.get_img(), mouse)
                self.vybrate_pet(self.pos_pet_shop, self.chybajuce_pet)

                if self.create_pos_pet_button(pos, 75, self.pets[0]) not in self.pos_pet_shop:
                    self.pos_pet_shop.append(self.create_pos_pet_button(pos, 75, self.pets[0]))
                pos += 95

        for i in self.chybajuce_pet[3:6]:

            if i not in self.kupene_pet:
                self.choose_pet(pos2, 234, i.get_img(), mouse)

                if self.create_pos_pet_button(pos2, 234, self.pets[0]) not in self.pos_pet_shop:
                    self.pos_pet_shop.append(self.create_pos_pet_button(pos2, 234, self.pets[0]))
                pos2 += 95

        if self.zvolene_pet:
            hero_health_text = self.main_font.render(f"HP: {self.actualne_pet.health}", 1, (210, 190, 255))
            self.win.blit(hero_health_text, (597, 435))
                                            #625, 445

            dmg_text = self.main_font.render(f"Damage: {self.actualne_pet.get_dmg()}", 1, (210, 190, 255))
            self.win.blit(dmg_text, (597, 461))

            reg_text = self.main_font.render(f"Heal: {self.actualne_pet.get_reg()}", 1, (210, 190, 255))
            self.win.blit(reg_text, (597, 489))

            name = self.main_font.render(f"Name: {self.actualne_pet.name}", 1, (210, 190, 255))
            self.win.blit(name, (597, 516))

            trieda = self.main_font.render(f"Type: {self.actualne_pet.druh}", 1, (210, 190, 255))
            self.win.blit(trieda, (597, 543))

            self.cislo_cena = self.actualne_pet.get_cena()
            cena = self.main_font.render(f"Cost: {str(self.cislo_cena)}", 1, (207, 181, 59))
            self.win.blit(cena, (597, 570))


        if self.pressed_kupene:
            uprate_money_text = self.main_font.render("- " + str(self.cislo_cena2), 1, (255, 255, 190))
            self.win.blit(uprate_money_text, (self.animation_suboj(630 + money.get_width(), 405)))


        if mouse[0] >= 35 and mouse[1] >= 534 and mouse[0] <= 35 + self.back_btn.get_width() and mouse[1] <= 534  + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 35, 534)
        else:
            self.blit_normal_btn(self.back_btn, 35, 534)

        if mouse[0] >= 424 and mouse[1] >= 534 and mouse[0] <= 424 + self.buy_btn.get_width() and mouse[1] <= 534  + self.buy_btn.get_height():
            self.blit_zmensene_btn(self.buy_btn, 424, 534)
        else:
            self.blit_normal_btn(self.buy_btn, 424, 534)


        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0

        pygame.display.update()


    def draw_win_shop_food(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_shop_food.png")))

        mouse_food = pygame.mouse.get_pos()

        money = self.main_font.render(f"{coins.actual_money}", 1, (255, 255, 190))
        self.win.blit(pygame.transform.scale(self.layer_pod_mince, (money.get_width() + coins.imgs[0].get_width() + 15, coins.imgs[0].get_height() + 12)), (683, 398))
        self.win.blit(money, (692 + coins.imgs[0].get_width(), 405))
        self.win.blit(coins.animation_coin(self.anim_coin), (687, 405))


# pozor lebo tie pozicie btns sa mi ukladaju do self.pos_pet_shop
        pos = pos1 = pos2 = pos3 = 717
        for i in self.ovocie[:3]:
            self.draw_elixir_cena(pos, 45, i.img, mouse_food)
            self.vybrate_ovocie(self.pos_pet_shop, self.ovocie)

            if self.create_pos_pet_button(pos, 45, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos, 45, i.img))
            pos += 73

        for i in self.ovocie[3:6]:
            self.draw_elixir_cena(pos1, 130, i.img, mouse_food)

            if self.create_pos_pet_button(pos1, 130, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos1, 130, i.img))
            pos1 += 73

        for i in self.ovocie[6:9]:
            self.draw_elixir_cena(pos2, 213, i.img, mouse_food)

            if self.create_pos_pet_button(pos2, 213, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos2, 213, i.img))
            pos2 += 73

        for i in self.ovocie[9:12]:
            self.draw_elixir_cena(pos3, 296, i.img, mouse_food)

            if self.create_pos_pet_button(pos3, 296, i.img) not in self.pos_pet_shop:
                self.pos_pet_shop.append(self.create_pos_pet_button(pos3, 296, i.img))
            pos3 += 73

        if self.zvolene_ovocie:
            self.win.blit(self.actualne_ovocie.img, (683, 434))


        if mouse_food[0] >= 90 and mouse_food[1] >= 534 and mouse_food[0] <= 90 + self.back_btn.get_width() and mouse_food[1] <= 534  + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 89, 534)
        else:
            self.blit_normal_btn(self.back_btn, 90, 534)


        if mouse_food[0] >= 484 and mouse_food[1] >= 534 and mouse_food[0] <= 484 + self.buy_btn.get_width() and mouse_food[1] <= 534  + self.buy_btn.get_height():
            self.blit_zmensene_btn(self.buy_btn, 485, 534)
        else:
            self.blit_normal_btn(self.buy_btn, 484, 534)


        if self.zvolene_ovocie:
            popis = self.main_font.render(f"{self.actualne_ovocie.txt}", 1, (255, 255, 255))
            self.win.blit(popis, (105, 450))



        font = pygame.font.SysFont("stencil", 22)
        enter = font.render(f"Enter: {self.pocet_kusov}", 1, (100, 20, 20) if not self.activated else (10, 3, 3))
        self.win.blit(enter, (743, 435 + 55 // 2 - enter.get_height() // 2))

        self.anim_coin += 1
        if self.anim_coin >= len(coins.imgs) * 4:
            self.anim_coin = 0


        pygame.display.update()


    def draw_win_mission(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_mission.png")))

        mouse = pygame.mouse.get_pos()

        pos = 56
        height = 118
        posuv = 150


        if mouse[0] >= pos and mouse[1] >= height and mouse[0] <= pos + self.pets[0].get_width() and mouse[1] <= height + self.pets[0].get_height():
            podmienka = self.main_font.render("You need to kill 25 monsters", 1, (86, 86, 86))
            self.blit_zmensene_btn(podmienka, pos, 560)

        if mouse[0] >= pos + posuv and mouse[1] >= height and mouse[0] <= pos + posuv + self.pets[0].get_width() and mouse[1] <= height + self.pets[0].get_height():
            podmienka = self.main_font.render("You need to kill 50 monsters", 1, (86, 86, 86))
            self.blit_zmensene_btn(podmienka, pos, 560)

        if mouse[0] >= pos + 2*posuv and mouse[1] >= height and mouse[0] <= pos + 2*posuv + self.pets[0].get_width() and mouse[1] <= height + self.pets[0].get_height():
            podmienka = self.main_font.render("You need to kill 10 bosses", 1, (86, 86, 86))
            self.blit_zmensene_btn(podmienka, pos, 560)

        if mouse[0] >= pos + 3*posuv and mouse[1] >= height and mouse[0] <= pos + 3*posuv + self.pets[0].get_width() and mouse[1] <= height + self.pets[0].get_height():
            podmienka = self.main_font.render("You need to kill 30 bosses", 1, (86, 86, 86))
            self.blit_zmensene_btn(podmienka, pos, 560)

        if mouse[0] >= pos + 4*posuv and mouse[1] >= height and mouse[0] <= pos + 4*posuv + self.pets[0].get_width() and mouse[1] <= height + self.pets[0].get_height():
            podmienka = self.main_font.render("You need to need to win 60 times", 1, (86, 86, 86))
            self.blit_zmensene_btn(podmienka, pos, 560)

        if mouse[0] >= pos + 5*posuv and mouse[1] >= height and mouse[0] <= pos + 5*posuv + self.pets[0].get_width() and mouse[1] <= height + self.pets[0].get_height():
            podmienka = self.main_font.render("You need to have 500 skore", 1, (86, 86, 86))
            self.blit_zmensene_btn(podmienka, pos, 560)


        if self.total_killed_monsters >= 25 and pet_jednorozec not in self.kupene_pet:
            pygame.draw.rect(self.win, (255, 255, 255), (pos - 5, height - 5, 97, 93))

        if self.total_killed_monsters >= 50 and pet_helmet not in self.kupene_pet:
            pygame.draw.rect(self.win, (255, 255, 255), (pos + posuv - 5, height - 5, 97, 93))

        if self.boss_fight_wins >= 10 and pet_ohnivy_robot not in self.kupene_pet:
            pygame.draw.rect(self.win, (255, 255, 255), (pos + 2*posuv - 5, height - 5, 97, 93))

        if self.boss_fight_wins >= 30 and pet_rybohen not in self.kupene_pet:
            pygame.draw.rect(self.win, (255, 255, 255), (pos + 3*posuv - 5, height - 5, 97, 93))

        if self.wins >= 60 and pet_strom not in self.kupene_pet:
            pygame.draw.rect(self.win, (255, 255, 255), (pos + 4*posuv - 5, height - 5, 97, 93))

        if self.skore >= 500 and pet_velka_papula not in self.kupene_pet:
            pygame.draw.rect(self.win, (255, 255, 255), (pos + 5*posuv - 5, height - 5, 97, 93))

        if any([i != None for i in self.mission_pets]):
            for i in range(1, 7):
                self.win.blit(pygame.image.load(os.path.join(working_path_images, "pet_unknown" + str(i) + ".png")), (pos, height))
                pos += posuv

        self.win.blit(pet_jednorozec.img, (56, height)) if pet_jednorozec in self.kupene_pet else 0

        self.win.blit(pet_helmet.img, (56 + posuv, height)) if pet_helmet in self.kupene_pet else 0

        self.win.blit(pet_ohnivy_robot.img, (56 + 2*posuv, height)) if pet_ohnivy_robot in self.kupene_pet else 0

        self.win.blit(pet_rybohen.img, (56 + 3*posuv, height)) if pet_rybohen in self.kupene_pet else 0

        self.win.blit(pet_strom.img, (56 + 4*posuv, height)) if pet_strom in self.kupene_pet else 0

        self.win.blit(pet_velka_papula.img, (56 + 5*posuv, height)) if pet_velka_papula in self.kupene_pet else 0


        if mouse[0] >= 640 and mouse[1] >= 550 and mouse[0] <= 640 + self.get_btn.get_width() and mouse[1] <= 550 + self.get_btn.get_height():
            self.blit_zmensene_btn(self.get_btn, 640, 550)
        else:
            self.blit_normal_btn(self.get_btn, 640, 550)


        if mouse[0] >= 795 and mouse[1] >= 550 and mouse[0] <= 795 + self.back_btn.get_width() and mouse[1] <= 550 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 795, 550)
        else:
            self.blit_normal_btn(self.back_btn, 795, 550)
        pygame.display.update()

    def draw_win_bed(self):
        self.draw_bg(pygame.image.load(os.path.join(working_path_images, "win_beds.png")))

        mouse = pygame.mouse.get_pos()
        self.pos_pelech = [(190, 431, 315, 479), (441, 437, 565, 479), (568, 382, 688, 425)]


        if self.pets_v_posteli[0] != None:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "name tag " + self.pets_v_posteli[0].druh + ".png")), (183, 452))

        if self.pets_v_posteli[1] != None:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "name tag " + self.pets_v_posteli[1].druh + ".png")), (441, 457))

        if self.pets_v_posteli[2] != None:
            self.win.blit(pygame.image.load(os.path.join(working_path_images, "name tag " + self.pets_v_posteli[2].druh + ".png")), (553, 401))



        if self.btn3:
            for i in self.pos_pelech:
                if i[0] <= mouse[0] <= i[2]:
                    if i[1] - 150 <= mouse[1] <= i[3]: # i je pozicia pelechu
                        index = self.pos_pelech.index(i) # index je index v array pos_pelech a ten isty index bude aj v self.pets_v_posteli teda pozicia pelech_ohen je vzdy na indexe 0 a teda aj pet v self.pet_v_posteli na indexe 0 je vzdy to pet ktore je v pelech_ohen
                        try:
                            self.pets_v_posteli[index].get_name() # to tu je iba na to aby mi to hodilo error ak napr. ukazes na pelech kde nieje ziadne pet a ono ti neukaze tam tu tabulku

                            self.win.blit(pygame.image.load(os.path.join(working_path_images, "layer_v_beds.png")), (i[0], i[1] - 150))

                            sleep = self.main_font.render(f"{int(self.pets_v_posteli[index].get_sleep()) + int((datetime.now() - self.pets_v_posteli[index].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) if int(self.pets_v_posteli[index].get_sleep()) + int((datetime.now() - self.pets_v_posteli[index].cas_od_kedy_spi).total_seconds() * self.zlomok_pre_spanok) <= 99 else 100}%", 1, (210, 190, 255))
                            self.win.blit(pygame.transform.scale(sleep, (sleep.get_width() - 2, 25)), (i[0] + self.moon.get_width() + 21, i[1] - 145))
                            self.win.blit(pygame.transform.scale(self.moon, (22, 22)), (i[0] + 25, i[1] - 145))

                            self.win.blit(pygame.transform.scale(self.pets_v_posteli[index].img, (44, 44)), (i[0] + 38, i[1] - 115))
                        except:
                            pass


        for i in self.kupene_pet:
            if i.sleep <= 75 and i not in self.ospalne_pets and i not in self.pets_v_posteli:
                self.ospalne_pets.append(i)


        pos = 88
        for i in self.ospalne_pets[self.pocet:self.pocet + 6]:
            self.choose_pet(pos, 532, i.img, mouse)
            self.vybrate_pet(self.pos_pets_buttons, self.ospalne_pets)

            sleep = self.main_font.render(f"{(i.get_sleep())}%", 1, (210, 190, 255))
            self.win.blit(sleep, (pos + self.moon.get_width() - 4, 505))
            self.win.blit(self.moon, (pos, 505))

            if self.create_pos_pet_button(pos, 532, self.pets[0]) not in self.pos_pets_buttons:
                self.pos_pets_buttons.append(self.create_pos_pet_button(pos, 532, self.pets[0]))
            pos += 110


        if self.zvolene_pet:
            self.win.blit(self.actualne_pet.img, (mouse[0] - self.pets[0].img.get_width() // 2, mouse[1] - self.pets[0].img.get_height() // 2))


        if mouse[0] >= 765 and mouse[1] >= 560 and mouse[0] <= 765 + self.back_btn.get_width() and mouse[1] <= 560 + self.back_btn.get_height():
            self.blit_zmensene_btn(self.back_btn, 765, 560)
        else:
            self.blit_normal_btn(self.back_btn, 765, 560)


        if mouse[0] >= 55 and mouse[1] >= 562 and mouse[0] <= 55 + self.sipka_dole.get_width() and mouse[1] <= 562 + self.sipka_dole.get_height() and self.pocet > 0:
            self.blit_zmensene_btn(pygame.transform.rotate(self.sipka_dole, -90), 55, 562)
        else:
            self.win.blit(pygame.transform.scale(pygame.transform.rotate(self.sipka_dole, -90), (self.sipka_hore.get_width() -2, self.sipka_hore.get_height() -2)), (56, 563)) if self.pocet > 0 else 0


        if mouse[0] >= 730 and mouse[1] >= 562 and mouse[0] <= 730 + self.sipka_dole.get_width() and mouse[1] <= 562 + self.sipka_dole.get_height() and self.pocet < len(self.ospalne_pets) - 6:
            self.blit_zmensene_btn(pygame.transform.rotate(self.sipka_dole, 90), 730, 562)
        else:
            self.win.blit(pygame.transform.scale(pygame.transform.rotate(self.sipka_dole, 90), (self.sipka_hore.get_width() -2, self.sipka_hore.get_height() -2)), (731, 563)) if self.pocet < len(self.ospalne_pets) - 6 else 0

        pygame.display.update()



    def draw_bg(self, bg):
        self.win.blit(bg, (0, 0))

    def blit_zmensene_btn(self, img, x, y):
        self.win.blit(pygame.transform.scale(img, (img.get_width() - 4, img.get_height() - 4)), (x + 2, y + 2))

    def blit_normal_btn(self, img, x, y):
        self.win.blit(img, (x, y))

    def save_text_render(self):
        text = pygame.font.SysFont("comicsans", 48)
        save_text = text.render("Game was saved.", 1, (50, 20, 60))
        self.win.blit(save_text, (475 - save_text.get_width() // 2, 570))

        pygame.display.update()

    def choose_pet(self, x, y, actual_pet, mouse):
        if mouse[0] >= x and mouse[1] >= y and mouse[0] <= x + actual_pet.get_width() and mouse[1] <= y + actual_pet.get_height():
            self.blit_zmensene_btn(actual_pet, x, y)
        else:
            self.blit_normal_btn(actual_pet, x, y)

    def draw_elixir_cena(self, x, y, elixir, mouse):    # metoda zobrazuje elixir a ked ukazes na elixir mysou tak vedla ukaze cenu elixiru
        if mouse[0] >= x and mouse[1] >= y and mouse[0] <= x + elixir.get_width() and mouse[1] <= y + elixir.get_height():
            money = self.main_font.render("5", 1, (255, 255, 190))

            self.win.blit(money, (x + 45 + coins.imgs[0].get_width(), y + 15))
            self.win.blit(coins.animation_coin(self.anim_coin), (x + 45, y + 14))
            self.blit_zmensene_btn(elixir, x, y)

        else:
            self.blit_normal_btn(elixir, x, y)

    def choose_pet_to_die(self, x, y, actual_pet, mouse):
        if mouse[0] >= x and mouse[1] >= y and mouse[0] <= x + actual_pet.get_width() and mouse[1] <= y + actual_pet.get_height():
            self.blit_normal_btn(pygame.image.load(os.path.join(working_path_images, "pet_delete.png")), x, y)
        else:
            self.blit_normal_btn(actual_pet, x, y)


    def pet_button(self, mouse_pos, x, y, list_pos, index_list):
        if mouse_pos[0] <= x + self.pets[0].get_width() and mouse_pos[1] <= y + self.pets[0].get_height():
            for i in list_pos[:index_list]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_pet = tuple(i)
                        self.click = True

        if mouse_pos[0] <= x + self.pets[0].get_width() and mouse_pos[1] <= y + 130 + self.pets[0].get_height():
            for i in list_pos[index_list:index_list + index_list]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_pet = tuple(i)
                        self.click = True
        else:
            for i in list_pos[index_list + index_list:]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_pet = tuple(i)
                        self.click = True


    def ovocie_button(self, mouse_pos, x, y, list_pos, index_list):
        if mouse_pos[0] <= x and mouse_pos[1] <= y + self.ovocie[0].img.get_height():
            for i in list_pos[:index_list]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_ovocie = tuple(i)
                        self.click_ovocie = True

        if mouse_pos[0] <= x and mouse_pos[1] <= y + 75 + self.ovocie[0].img.get_height():
            for i in list_pos[index_list:6]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_ovocie = tuple(i)
                        self.click_ovocie = True

        if mouse_pos[0] <= x and mouse_pos[1] <= y + 150 + self.ovocie[0].img.get_height():
            for i in list_pos[6:9]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_ovocie = tuple(i)
                        self.click_ovocie = True
        else:
            for i in list_pos[9:]:
                if i[0] <= mouse_pos[0] <= i[2]:
                    if i[1] <= mouse_pos[1] <= i[3]:
                        self.actualne_ovocie = tuple(i)
                        self.click_ovocie = True

    def delete_pet(self, mouse_pos, pos_list):
        for i in pos_list[:len(self.pos_pets_to_fight)]:
            if i[0] <= mouse_pos[0] <= i[2]:
                if i[1] <= mouse_pos[1] <= i[3]:

                    for index, pet_to_delete in enumerate(pos_list):
                        if pos_list[index] == i:
                            try:
                                self.boss_fight_pets.pop(index)
                                self.pos_pets_to_fight.pop(len(self.boss_fight_pets))
                            except:
                                pass




    def vybrate_pet(self, pos_list, pet_list):
        if self.click:
            for index, pet in enumerate(pos_list):
                if pos_list[index] == self.actualne_pet:
                    try:
                        self.actualne_pet = pet_list[index + self.pocet]
                        self.zvolene_pet = True
                        self.click = False
                    except:
                        pass


    def vybrate_ovocie(self, pos_list, pet_list):
        if self.click_ovocie:
                for index, pet in enumerate(pos_list):
                    if pos_list[index] == self.actualne_ovocie:
                        try:
                            self.actualne_ovocie = pet_list[index]
                            self.zvolene_ovocie = True
                            self.click_ovocie = False
                        except:
                            pass


    def create_pos_pet_button(self, x, y, img):
        return x, y, x + img.get_width(), y + img.get_height()

    def attack_hero(self):
        if self.actualne_pet.health > 0 and self.Health_monster > 0:
            self.Health_monster -= self.Damage_hero
            self.actualne_pet.health -= self.Damage_monster
            self.health_count_hero += self.Damage_monster

        self.won_monster = True if self.actualne_pet.health <= 0 else False

        self.won_hero = True if self.Health_monster <= 0 else False


    def draw_hero(self):
        self.win.blit(pygame.transform.flip(self.actualne_pet.img, True, False), (167, 193))

        font = pygame.font.SysFont("comicsans", 32)
        Hero_health_text = font.render(f"HP: {int(self.actualne_pet.health)}", 1, (255, 255, 255))  # text pod postavou Hero
        self.win.blit(Hero_health_text, (163, 294))

        reg_count_text = font.render(f"Heal: {self.reg_count}" + "/3", 1, (255, 255, 255))  # text regeneration pod Health_hero
        self.win.blit(reg_count_text, (163, 317))

        ability = font.render(f"Ability: {self.pow_count}" + "/1", 1, (255, 255, 255))  # text regeneration pod Health_hero
        self.win.blit(ability, (163, 340))


    def draw_monster(self):
        self.win.blit(self.actualne_monster.get_img(), (700, 193)) if not self.bool_fight_boss else self.win.blit(self.actualne_monster.get_img(), (680, 151))

        font = pygame.font.SysFont("comicsans", 32)
        Monster_health_text = font.render(f"HP: {self.Health_monster}", 1, (255, 255, 255))  # text pod postavou Monster
        self.win.blit(Monster_health_text, (650 + 188 / 2 - Monster_health_text.get_width() / 2, 294))

    def regeneration(self):
        self.actualne_pet.health += self.regeneration_random_number
        self.health_reg_count_hero += self.regeneration_random_number

    def check_pet(self):
        self.actualne_pet.health += self.health_count_hero - self.health_reg_count_hero

        self.actualne_pet.sleep -= self.actualne_pet.get_tired() * self.actualne_pet.less_sleep
        self.actualne_pet.food -= self.actualne_pet.get_hunger() * self.actualne_pet.less_food


        self.actualne_pet.elixir_duration -= 1 if self.actualne_pet.elixir != None else 0

        if self.actualne_pet.elixir != None and self.actualne_pet.elixir_duration == 0:
            try:
                if self.actualne_pet.elixir.druh == "heal":
                    self.actualne_pet.reg1 /= self.actualne_pet.elixir_ucinok
                    self.actualne_pet.reg2 /= self.actualne_pet.elixir_ucinok
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2

                if self.actualne_pet.elixir.druh == "hp":
                    self.actualne_pet.health /= self.actualne_pet.elixir_ucinok
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2

                if self.actualne_pet.elixir.druh == "dmg":
                    self.actualne_pet.damage1 /= self.actualne_pet.elixir_ucinok
                    self.actualne_pet.damage2 /= self.actualne_pet.elixir_ucinok
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2

                if self.actualne_pet.elixir.druh == "sleep":
                    self.actualne_pet.less_sleep = 1
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2

                if self.actualne_pet.elixir.druh == "food":
                    self.actualne_pet.less_food = 1
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2

                if self.actualne_pet.elixir.druh == "coin":
                    self.actualne_pet.more_coin = 1
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2


                if self.actualne_pet.elixir.druh == "resistance":
                    self.actualne_pet.resistance = 1
                    self.actualne_pet.elixir_ucinok = None
                    self.actualne_pet.elixir = None
                    self.actualne_pet.elixir_duration = 2
            except:
                pass


    def animation_suboj(self, x, y):
        if 0 < self.animation_suboj_count < 8:
            x += (self.animation_suboj_count ** 1.5)
            y -= (self.animation_suboj_count ** 1.5)
            self.animation_suboj_count += 0.1

            if self.animation_suboj_count >= 7.7:
                self.animation_suboj_count = 1
                self.spustac = False
                self.pressed_a = False
                self.pressed_r = False
                self.pressed_s = False
                self.anim_efekty_count = 0
                self.pressed_kupene = False
                self.lack_sleep = False
        return x, y

    def animation_move_to_left(self, x):
        if self.next_pet:
            if 0 < self.animation_move_var_left <= 20:
                x += self.animation_move_var_left ** 1.5
                self.animation_move_var_left -= 0.1

                if self.animation_move_var_left <= 0.5:
                    self.animation_move_var_left = 20
                    self.next_pet = False
                    self.actualne_monster = self.monsters_to_die[self.monster_pointer]      # az sa skonci animacia tak budes mat nove aktulne_monster
                    self.Health_monster = self.monsters_to_die[self.monster_pointer].set_health_until_die(self.Health_hero2)
                    self.killed_monsters += 1
        return x

    def animation_move_to_right(self, x):
        if self.next_pet:
            if 0 < self.animation_move_var_right <= 21:
                x += self.animation_move_var_right ** 1.5
                self.animation_move_var_right += 0.1

                if self.animation_move_var_right >= 21:
                    self.animation_move_var_right = 1
                    self.next_pet = False
                    self.check_pet()
                    self.health_reg_count_hero = 0
                    self.health_count_hero = 0
                    self.actualne_pet = self.boss_fight_pets[self.pet_pointer]
                    self.Health_hero2 = self.actualne_pet.health

                    self.reg_count = 0
                    self.pow_count = 0
                    self.pet_pointer += 1
        return x

    def play_sound(self, nazov):
        pygame.mixer.music.load(os.path.join(working_path_images, nazov + ".mp3"))
        pygame.mixer.music.play(1)

    def save_game(self):
        path = working_path + "\data"  # totok vytvara subor kde sa budu ukaldat vsetky data
        if not os.path.exists(path):
            os.mkdir(path)

        if not os.path.exists(path + "\pets"):  # totok vytvara subor kde sa budu ukaldat iba data o pets
            os.mkdir(path + "\pets")

        if not os.path.exists(path + "\casi"):
            os.mkdir(path + "\casi")

        with open(os.path.join(path, "kupene_pet.txt"), "w") as subor_names:        # totok pise do .txt suboru vsetky mena pets
            for i in self.kupene_pet:
                subor_names.write(i.name + " ")


        for i in self.kupene_pet:
            pets_data_file = os.path.join(path + "\pets", "data_" + f"{i.name}" + ".txt")      # totok uklada data o pets v danom priecinku a v .txt a do caaaaaadata suboru
            with open(pets_data_file, "w") as f:
                f.write(str(i.health) + " " + str(i.damage1) + " " + str(i.damage2) + " " + str(i.reg1) + " " + str(i.reg2) + " " + str(i.sleep) + " " + str(i.less_sleep) + " " + str(i.less_food) + " " + str(i.more_coin) + " " + str(i.resistance) + " " + str(i.sale) + " " + str(i.more_upgrade) + " " + str(i.food) + " " + str(i.lvl) + " " + str(i.elixir.druh if i.elixir != None else None) + " " + str(i.elixir_duration) + " " + str(i.elixir_ucinok))


        with open(os.path.join(path, "bag.txt"), "w") as file:
            for i in self.veci_bag:
                file.write(str(i.druh) + " " + str(i.pocet) + " ")


        with open(os.path.join(path, "pets_v_pelechu.txt"), "w") as file:
            for i in self.pets_v_posteli[:3]:
                file.write(i.name + " " if i != None else str(None) + " ")


        game_file = open(os.path.join(path, "data_game"), "wb")
        pickle.dump(self.name_player, game_file)
        pickle.dump(self.wins, game_file)
        pickle.dump(self.skore, game_file)
        pickle.dump(self.boss_fight_wins, game_file)
        pickle.dump(self.total_killed_monsters, game_file)

        pickle.dump(self.pressed_prvy_ohen, game_file)
        pickle.dump(self.pressed_prvy_svetlo, game_file)
        pickle.dump(self.pressed_prvy_zem, game_file)

        pickle.dump(self.max_cap, game_file)
        pickle.dump(self.upgrade_storage, game_file)

        pickle.dump(coins.actual_money, game_file)
        pickle.dump(coins.coins_per_sec, game_file)
        pickle.dump(coins.upgrade_lvl, game_file)

        pickle.dump(coins_ohen.actual_money, game_file)
        pickle.dump(coins_ohen.coins_per_sec, game_file)
        pickle.dump(coins_ohen.upgrade_lvl, game_file)

        pickle.dump(coins_svetlo.actual_money, game_file)
        pickle.dump(coins_svetlo.coins_per_sec, game_file)
        pickle.dump(coins_svetlo.upgrade_lvl, game_file)

        pickle.dump(coins_zem.actual_money, game_file)
        pickle.dump(coins_zem.coins_per_sec, game_file)
        pickle.dump(coins_zem.upgrade_lvl, game_file)

        try:
            pickle.dump(self.pets_v_posteli[0].cas_od_kedy_spi, open(os.path.join(path + "\casi", "postel_cas1"), "wb"))
        except:
            pass
        try:
            pickle.dump(self.pets_v_posteli[1].cas_od_kedy_spi, open(os.path.join(path + "\casi", "postel_cas2"), "wb"))
        except:
            pass
        try:
            pickle.dump(self.pets_v_posteli[2].cas_od_kedy_spi, open(os.path.join(path + "\casi", "postel_cas3"), "wb"))
        except:
            pass
        try:
            pickle.dump(self.bane_cas_ohen, open(os.path.join(path + "\casi", "bane_cas_ohen"), "wb"))
        except:
            pass
        try:
            pickle.dump(self.bane_cas_svetlo, open(os.path.join(path + "\casi", "bane_cas_svetlo"), "wb"))
        except:
            pass
        try:
            pickle.dump(self.bane_cas_zem, open(os.path.join(path + "\casi", "bane_cas_zem"), "wb"))
        except:
            pass
        game_file.close()

if __name__ == "__main__":
    g = Game()
    g.run()
