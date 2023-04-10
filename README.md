# Pets Brawl game

Simple game written in pygame.Purpose of the game is to fight with yours pets against monsters, improve them, take care of them and buy new ones.

Game can be divided into these parts:

-[Fights](#fights "Goto Fights")

-[Pets](#pets "Goto Pets")

-[Mines](#mines "Goto Mines")

-[Shop](#shop "Goto Shop")

-[Mission](#mission "Goto Mission")

-[Beds](#beds "Goto Beds")

## Fights
You can choose one out of three fight modes (1v1 - one pet vs one monster, Fight until die - one pet fight against multiple monsters until pet die, Boss fight - 4 pets vs Boss. By 'a', 's', 'r' buttons you can fight, use super attack or heal respectively.

1. 1v1 - You choose one pet which will fight against monster. Pet has pre-loaded stats (HP, atack range, heal range, super attack) but monster stats are calculated based
on your pet. Formulas are:
    - Monster_HP = randint(Pet_HP * 1.85, Pet_HP * 2.45)
    - Monster_attack = randint(Pet_HP / (Monster_HP / Pet_attack_MIN) * 1.2, Pet_HP / (Monster_HP / Pet_attack_MAX) * 1.2)
    
    Note that pet attack and heal depends on how much their are hungry and sleepy, formulas for that are here:
    - Pet_attack = randint(Pet_attack_MIN * sqrt(Pet_sleep *.01 * Pet_food *.01), Pet_attack_MAX * sqrt(Pet_sleep *.01 * Pet_food *.01)
    - Pet_heal = randint(Pet_heal_MIN * sqrt(Pet_sleep *.01 * Pet_food *.01), Pet_heal_MAX * sqrt(Pet_sleep *.01 * Pet_food *.01)
    
    After fight you can win between 40-90 coins or lose 5-10 and gain/lose score between 10-20 or 5-9 respectively.
    
2. Fight until die - One pet fight against multiple monsters until pet die. Similarly as before, monster stats are calculated based on this formulas:
    - Monster_HP = randint(Pet_HP / 4, Pet_HP * 2.1)
    - Monster_attack = randint(Pet_attack_MIN / 4, Pet_attack_MAX * 2.1)
    - Won_coins = randint(14, 20) * killed_monsters

3. Boss fight - You will choose 4 pets and you will fight against boss. Stats for boss are calculated here:
    
    sum = Pet1_HP + Pet2_HP + Pet3_HP + Pet4_HP
    - Boss_HP = randint(sum * 2.05, sum * 2.7)
    - Boss_attack = randint(Pet_HP * Pet_attack_MIN * 4 / Boss_HP, Pet_HP * Pet_attack_MAX * 4 / Boss_HP)
    - Won_coins = randint(100, 200)

## Pets

Pet is a python class and has this constructor parametres (img, health, damage1, damage2, reg1, reg2, name, druh, utok, druh_coin, super_pow)

-img - image of pet

-damage1 - damage_MIN

-damage2 - damage_MAX

-reg1 - heal_MIN

-reg2 - heal_MAX

-druh - type of Pet (light, fire, ground)

-utok - array of images for attack animation

-druh_coin - array of images for coin animation

-super_pow - array of images for super attack animation

Note that Pet class has more object variables which some of then i will explain later.

Firstly, let's say what you can do with pets:
1. You can feed then - Pets in order to be stronger in fights, they must have food indicator at the highest possible percentage
    - If you feed the pet with fruit of same type as pet (cherry - fire pet, banana - light pet, pear - ground pet)  
