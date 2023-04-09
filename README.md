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
    - Monster HP = randint(Pet_HP * 1.85, Pet_HP * 2.45)
    - Monster Attack = randint(Pet_HP / (Monster_HP / Pet_attack_MIN) * 1.2, Pet_HP / (Monster_HP / Pet_attack_MAX) * 1.2)
    
    Note that pet attack and heal depends on how much their are hungry and sleepy, formulas for that are here:
    - Pet_attack = randint(Pet_attack_MIN * sqrt(Pet_sleep *.01 * Pet_food *.01), Pet_attack_MAX * sqrt(Pet_sleep *.01 * Pet_food *.01)
    - Pet_heal = randint(Pet_heal_MIN * sqrt(Pet_sleep *.01 * Pet_food *.01), Pet_heal_MAX * sqrt(Pet_sleep *.01 * Pet_food *.01)
    
    After fight you can win between 40-90 coins or lose 5-10 and gain score between 10-20 or 5-9 respectively.
