# Pets Brawl game

Simple game written in pygame. Purpose of the game is to fight with yours pets against monsters, improve them, take care of them, buy new ones and complete achievements.

Game can be divided into these parts:

-[Fights](#fights "Goto Fights")

-[Pets](#pets "Goto Pets")

-[Coins](#coins "Goto Coins")

-[Mission](#mission "Goto Mission")


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

Firstly, let's say what you can do with pets:
1. You can feed then - Pets in order to be stronger in fights, they must have food indicator at the highest possible percentage. If you feed the pet with fruit of same type as pet (cherry - fire pet, banana - light pet, pear - ground pet), it will add them more food points than different types. Formulas: 
    - add_food = randint(28, 35) # Pet type = Fruit type
    - add_food = randint(17, 23) # Pet type != Fruit Type
    
2. Put them to bed - Pets in order to be stronger in fights, they must have sleep indicator at the highest possible percentage. If sleep percentage drops below 75 then you can put pet to bed. Roughly each second will add one percent. After they reach 90% you can pick them out of bed or wait to reach 100% and be stronger.

3. Level up your pets - Level up will increase pets HP, damage and heal by 7%, price for next level up

    -Price_for_upgrade - sqrt(Pet_HP) * 2 + (Pet_attack_MIN + Pet_attack_MAX) / 2.88

4. Use elixirs on pets - If pet drink elixir, then pet gain some additionall abillities, their effect is for two cycles. List of all elixirs and their effects:

    -Heal - increase healing 12-25%
    
    -HP - increase HP 12-17%
    
    -Damage - increase damage 12-22%
    
    -Sleep - Less sleepy after fight about 62-84%
    
    -Hunger - Less hungry after fight about 51-75%
    
    -Coins - 14-25% more coins if you win a fight
    
    -Resistance - 25-30% more durable in fights
    
    -Price - 20-50% lower price for uprading pet
    
    -Upgrade - 6-14% more pet upgrade for the same price

## Coins
There are four types of coins, one as a main currency and three secondary. Main currency can be obtained only in fights and can be used to upgrade mines storage, buy new pets or buy elixirs/food. Each pet type has it's own coin type (secondary currency), which can be mined and then used to upgrade pets or upgrade mines. There are three mines for three secondary currencies, they mine certain ammount of coins per hour after that this is stored in storage and then you can collect those coins from storage. Formulas:

    -coins_per_hour *= 1.13 # upgrade mines

    -storage *= 1.21        # upgrade storage
    
    -elixir_price = 5
    
    -pet_price = Pet_HP * 3

## Missions
After you complete a mission your 
