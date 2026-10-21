from random import randint

class weapon():
    def __init__(self, dmg, splash_dmg, name):
        self.name = name
        
        self.dmg = dmg
        self.splash_dmg = splash_dmg

    def use(self, target_team, target):
        target_team[target].damage(self.dmg)

        for i in range(len(target_team)):
            target_team[i].damage(self.splash_dmg)



class person():
    def __init__(self, kind):
        self.alive = True
        self.kind = kind
        
        if self.kind == "light":
            self.max_hp = 12
            self.evade = 0.5
            self.aresnal = [weapon(6, 0, "sword")]

        elif self.kind == "heavy":
            self.max_hp = 20
            self.evade = 0.1
            self.aresnal = [weapon(5, 2, "maul")]

        elif self.kind == "glass cannon":
            self.max_hp = 5
            self.evade = 0.3
            self.aresnal = [weapon(8, 1, "cannon")]

        else:
            print(f"INVALID PERSON CREATED : {kind}\nDefaulted to light")
            self.kind = "light"
            self.max_hp = 12
            self.evade = 0.5
            self.aresnal = [weapon(6, 0, "sword")]
            
        self.hp = self.max_hp

    def damage(self, dmg_points):
        if self.evade < randint(0,10)/10: # if not dodged
            self.hp -= dmg_points

            if self.hp <= 0:
                self.hp = 0
                self.alive = False

    def attack(self, chosen_wep, target_team, target):
        self.aresnal[chosen_wep].use(target_team, target)



def display():
    print(f"\n\n          TURN {turn}\n")
    
    print("ENEMY TEAM")
    j = 0
    for i in enemy_team:
        print(f"{j} {i.kind} : HP = [{i.hp}/{i.max_hp}]")
        j+=1

    print("\n\n\nPLAYER TEAM")
    j = 0
    for i in player_team:
        print(f"{j} {i.kind} : HP = [{i.hp}/{i.max_hp}]")
        j+=1


def select_unit(team):
    selected = -1
    
    while selected == -1:
        flag = False
        try:
            temp_selc = int(input("Unit (type their ID): "))
        except:
            print("Try typing a number...")
            flag = True
        if not flag:
            if temp_selc < 0 or temp_selc > len(team) -1:
                print("Number out of range, try again.")
            elif not team[temp_selc].alive:
                print("Unit dead, try again.")
            else:
                selected = temp_selc
            
    print(f"Selected unit: {selected} {team[selected].kind}")
    return selected


def select_move():
    print("\nChoose a unit to use")
    unit_id = select_unit(player_team)

    print("Choose a weapon:")
    options = []
    for i in player_team[unit_id].aresnal:
        print(f" - {i.name}")
        options.append(i.name)

    chosen_wep = "none"
    while chosen_wep == "none":
        temp_cho = input("(Name string): ").lower()
        for i in range(len(options)):
            if temp_cho == options[i]:
                chosen_wep = i

    print("\nChoose a unit to target")
    target_id = select_unit(enemy_team)

    player_team[unit_id].attack(chosen_wep, enemy_team, target_id)


def enemy_turn():
    global playing
    print("Enemy Turn:")
    unit_id = randint(0, len(enemy_team)-1)
    start = unit_id
    while not enemy_team[unit_id].alive:
        unit_id = (unit_id + 1) % len(enemy_team) # wrap around until found valid unit
        if unit_id == start: # if got all the way around, must all be dead
            playing = False
            print("       YOU WON!      ")
            break

    # selects totally randomly
    chosen_wep = randint(0, len(enemy_team[unit_id].aresnal)-1)

    target_id = randint(0, len(player_team)-1)
    start = target_id
    while not player_team[target_id].alive:
        target_id = (target_id + 1) % len(player_team) # wrap around until found valid unit
        if target_id == start:
            playing = False # vise versa
            print("       YOU LOSE!      ")
            break

    if playing:
        print(f"Enemy used {unit_id}'s {enemy_team[unit_id].aresnal[chosen_wep].name} to attack {target_id}")
        enemy_team[unit_id].attack(chosen_wep, player_team, target_id)

# global variables, im sorry greg

player_team = [person("light"), person("heavy"),person("glass cannon")] 

enemy_team = [person("light"), person("heavy"), person("glass cannon")]

turn = 0

playing = True

def player_live():
    global playing
    one_alive = False
    for i in player_team:
        if i.alive:
            one_alive = True

    if not one_alive:
        playing = False
        print("       YOU LOSE!      ")


while playing:
    turn += 1
    display()
    player_live()
    if playing:
        select_move()
        enemy_turn()
