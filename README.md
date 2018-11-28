## DunGen
v1.00

#### Introduction
DunGen is a dungeon crawl generator for roguelike designers. 
It is meant to be a tool for designers to easily test different behaviours of monsters, vary the looks of different elements, work with player abilities/spells and attributes of the different entities, without having to write or modify a lot of real code.
DunGen takes a file containing just a list of specifications and definitions with some *code* to create a playable roguelike.

#### Requirements and Getting Ready

* DunGen requires Python 3. 
* Check whether it's the 32-bit version or the 64-bit version of Python. This will decide which DLLs are required. Copy the two DLL files from the appropriate folder inside `DLLs` to `dungen`.
* If these files are absent, an `SDL2.dll not found` exception will be thrown.
* If the incompatible DLLs are copied, an `Incompatible architecture` error will be generated.

#### Using DunGen

1. Write a specifications file containing all the details of the map, the monsters and the abilities to be included.
2. Copy it to the `dungen` folder.
3. Start the Prompt in the folder. Enter `python dungen.py <specs filename>`. Make sure to enter the full filename including the extension.
4. Test the game that opens up in a new window.

#### Writing the specifications file
A usual file for DunGen usually contains blocks of the following form. Details are given in later sections.

```
name                : <some name>
rooms               : <number>
small               : <another number>
.
.
monster             : <num>
<some monster name> : <num>
<another monster>   : <num>
..

define player
char   : <character>
colour : <one of the available colours>
hp     : <num>
attack : <num>
defence: <num>
mana   : <num>

define monster <name>
char   : <char>
colour : <colour>
.
<stats>: ..
.
behav  : <predefined or user-defined behaviour>

define monster <another name>
.
.

define behav <behav name>
...
<some 'code'>
...

define spell <key>
name : <name of spell>
dirn : <directional spell?>
cost : <num>
...
<some 'code'>
...

...
<more definitions of monsters/behavs/spells>
...
```

##### Writing a Really, Really, Really Basic Game for DunGen
DunGen has defaults for most things.  
There are defaults for most of the specifications.  
There is an inbuilt monster type simply called `monster`.  
There are 3 inbuilt monster behaviours, that will be covered later in this README. 

Having all these defaults makes it very easy to make (incredibly basic) games. A file with just two lines is enough to get DunGen going. (This file is present in the `samples` folder as `rrrbasic.txt`.)
```
rooms   : 10
monster : 40
```
Of course, this won't make an interesting game but it's enough to get things moving.

##### The Basics of Playing a DunGen Game

* Move using the arrow keys.
* When a monster is exactly one block away, attack the monster by pressing the arrow key in that direction.
* When a monster is killed, it turns to a corpse(%) and walking over it gives the player a health boost.
* Get to the door, which leads to a new map.

#### Customizing the Display and Basic Map Setup

Each file must start with a block containing at least the number of rooms and any of the specifications shown below. 
(Note that this list is not complete and only includes the more important ones. For a complete list, see the Appendix.) The specifications do not have to be in any specific order.

```
name   : <string>
player : <string>
wall_colour     : <colour>
wall_char       : <char>
floor_colour    : <colour>
floor_char      : <char>
obstacle_colour : <colour>
obstacle_char   : <char>
rooms  : <num>
small  : <num>
medium : <num>
large  : <num>
monster: <num>
<user-defined monster>  : <num>
```

* `<string>` can be any string of characters.
* `<colour>` must be one of the colours available. (See the Appendix at the end of this README for a list of valid colours.)
* `<char>` must be a single character. Space(' ') won't work.
* `<num>` must be a non-negative integer. (Certain fields only take positive integers. However no such fields are present in the above sample.)
* `<user-defined monster>` is the name of a monster type which is defined later in the file.


* `name` is the name that will be displayed in the title bar.
* `player` is the name of the player character.


* `wall_colour`, `floor_colour` and `obstacle_colour` are the colours which shall be used to represent the respective features on the map.
  `wall_char`, `floor_char` and `obstacle_char` are the characters which shall be used to represent the respective features on the map.

  
* `rooms` is the total number of rooms on the map. `small`, `medium` and `large` are the number of rooms of that particular size.
  Any combination of these four will work as long as they are not incompatible (like `rooms` being less than the sum of the other three fields).
  At least one of them must be present.
  
  
* The number of monsters of a particular kind is defined as shown above (`<monster type> : <num>`). `monster` is just a predefined monster type that can be used without defining.

#### Customizing Monsters and the Player Character

The definition of a player must start with `define player`.  
Similarly a monster definition must start with `define monster <name>`.  
The following fields are available for both monsters and the player (except where specifically noted).

```
char   : <char>
colour : <colour>
hp     : <num>
attack : <num>
defence: <num>
behav  : <behav name>
mana   : <num>
```

* `char` and `colour` denote how that character will be shown on the map (when alive).
* `hp`, `attack` and `defence` are statistics or attributes of the character. `hp` is the health or hitpoints. `attack` and `defence` are used for determining the results of an attack.
* `behav` is only for monsters. `behav` decides which behaviour will be followed by the monster when it takes its turn. <behav name> must be defined somewhere in the file (or must be a predefined behaviour).
* `mana` is only for the player. `mana` is the resource which will be used for casting spells (something which will be seen after a few sections in this README).

The `rrbasic.txt` file in `samples` makes use of whatever has been covered in these last two sections. The monsters only use the predefined behavs `basic`, `scaredycat` and `brave` for now. As always, all fields do not need to be specified in which case the default values will be taken.

#### Writing Code for DunGen

Behaviours and spells are defined through some 'code'. Basic programming constructs like conditionals and loops are available. If a language like C or Java is familiar, only a few major differences have to be taken care of.

* Only integers can be handled. (This means no actual booleans. 1 or 0 is the result of a logical/relational expression.)
* Variables are declared using `var <variable>` and must be initialized at declaration.
* Available operators are `+`, `-`, `*`, `/`, `~`, `>=`, `<=`, `>`, `<`, `==`, `!=`, `&`, `|` and `!`. Parentheses can also be used. Most of the operators behave the same way as in other languages. The different ones are shown below.
  * `~` is the unary negation operator. `-` cannot be used directly for storing negative integers.
  * `&` and `|` are the relational `AND` and `OR` operators, not bitwise operators.
* Writing an `if-else` is done by  
  ```
  if {<conditional expression>}{
    <statements if true>
  } {
    <statements if false>
  }
  ```  
  Important things to note include the use of braces{} (instead of parentheses()) for enclosing the condition and the absence of an actual `else` keyword. 
  The braces are always essential for the blocks of statements even if there is only one statement to be executed.  
  The second block may be skipped for a simple `if` statement.
  ```
  if {<conditional expression>}{
    <statements if true>
  }
  ```  
* Writing a loop is done through `while` as shown below  
  ```
  while {<condition>} {
    <statements to execute>
  }
  ```
  Like the `if` condition, the condition for `while` must be enclosed in braces and braces are necessary everywhere.
* Scoping is implemented for the blocks used in `if` and `while`. However separate blocks of code enclosed by braces (which are not used in `if` or `while`) cannot be created.

There are also some other predefined variables and functions which allow the code to interact with the actual game variables. The specifics will be covered in the respective sections on Creating Behaviours and Creating Spells.
* The predefined variables (called 'stats' from here onwards) already contain the appropriate values taken from the actual game variables. Modifying these may or may not change the actual game variables. These can be used just like other variables.
* Some 'functions' are used to detect the presence of certain features at a particular location on the map.
* 'actions' are like functions which make changes to the monsters or the player character.
For the 'functions' and 'actions' any integer arguments can also take expressions that result in an integer.

#### Creating Behaviours

The definition of a behaviour must start with `define behav <behav name>`.  
This must be followed by 'code' starting from a new line.

Available stats for behaviours:

* `health`     : The monster's current hp. Modifying this _changes_ the actual hp in the game.
* `maxhealth`  : The monster's maximum hp (the hp in the monster definition). Modifying this _does not change_ the actual max hp.
* `phealth`    : The player's current hp. Modifying this _changes_ player's actual hp in the game.
* `maxphealth` : The player's maximum hp (the hp in the player definition). Modifying this _does not change_ the actual max hp.
* `player_distance`: The player's distance from this monster. Modifying this _does not change_ the actual distance.

These stats can be used in expressions just like other variables. For example, `health > maxhealth/2 & phealth < maxphealth/2 & flag` is a valid expression (where `flag` is a variable that has already been declared).

Available actions for behaviours:

* `move(<dx>, <dy>)`  
  Moves the monster by (dx, dy). In other words, if the monster's current position on the map is (x, y), it changes it to (x + dx, y + dy) if possible.  
  An important thing to take care of is that the y-axis on the map points downward. So moving a monster by (0, 1) moves it one space below.
* `move_towards()`  
  Tries to move the monster one space closer to the player character.
* `flee()`
  Tries to move the monster one space away from the player character.
* `move_random()`
  Moves the monster one space in a random direction.
* `attack([num])`
  Executes the monster's attack on the player. The optional argument is the damage. If not given, the standard attack damage is considered.

These actions are executed by just calling them like functions. Some examples of valid action statements are given:

* `move(1, ~2);`
* `attack(maxphealth - health);`
* `attack(damage);` where damage is a variable that was defined earlier

See the `rbasic.txt` file in `samples` for some behaviours and how a behaviour can be used by multiple monsters. Also see the appendix for the code for the predefined behaviours (`brave`, `scaredycat` and `basic`).

#### Creating Spells

The definition of a behaviour must start with `define spell <key>`. Here <key> is the key which must be pressed to activate the spell.  
This may be followed by certain specifications: 
```
name  : <string>
cost  : <num>
dirn  : <bool>
```

* `name` is the name of the spell which will be displayed when using the spell.
* `cost` is the amount of mana that will be used up in casting the spell.
* `dirn` determines whether the spell is directional or non-directional. It must be one of `yes`, `y`, `true`, `no`, `n` or `false`.  
  If it is one of the first three, the spell will take a direction as input (through the arrow keys) once the spell is active before being put into effect. If it is one of the last three, the spell will not take any direction and always have the same effect.
  Directional spells require some more care than non-directional spells. These will be covered in the next section.
  
After the specifications (if any) have been specified, the code must be written for the spell.

Available stats for spells:

* `x` : The player's x coordinate on the map. Modifying this _does not change_ the actual x coordinate.
* `y` : The player's y coordinate on the map. Modifying this _does not change_ the actual y coordinate.
* `health`    : The player's current hp. Modifying this _changes_ the actual hp in the game.
* `maxhealth` : The player's max hp. Modifying this _changes_ the actual max hp in the game.
* `mana`      : The player's current mana. Modifying this _changes_ the actual mana in the game.

Available functions for spells:

* `is_monster(<x>, <y>)`
  Returns 1 if a monster is present at (x, y) on the map else 0.
* `is_wall(<x>, <y>)`
  Returns 1 if a wall is present at (x, y) on the map else 0.
* `in_fov(<x>, <y>)`
  Returns 1 if the player can 'see' (x, y) on the map else 0.
  
These functions can be used just like any functions that return integers. They can be used in an expression or on their own wherever an expression can be used.  
However the above functions are particularly useful in conditionals.

Available actions for spells:

* `hit(<x>, <y>, <damage>)`
  Tries to hit whatever may be present at (x, y) on the map and reduce its hp by the damage parameter.
  
The above functions and stats make it possible to go over an area and hit everything which satisfies certain conditions. 
For example, an area blast may go over a rectangular patch on the map centred at the player's position and hit everything which is visible. (See `rbasic.txt` for the code to implement area blast and some other spells.)

#### Creating Directional Spells

Directional spells are written exactly like non-directional spells. Only a couple of things need to be kept in mind.

* `dirn` must be specified and be one of `y`, `yes` or `true`. If it is not specified, the spell will be treated as a non-directional spell since that is the default.
* The code for the spell must be written exactly as you would like the spell to work if the chosen direction is right. DunGen will take care of what to do if the other directions are chosen.

Directional spells allow for simple ranged attacks in a single direction or a region based on the direction. See `basic.txt` for some directional spells.

#### Playing a DunGen Game: A More Complete Guide

* Move using the arrow keys.
* When a monster is exactly one block away, attack the monster by pressing the arrow key in that direction.
* When a monster is killed, it turns to a corpse(%) and walking over it gives the player a health boost.
* Press the 'H' key (if it has not been used for a spell) to see the health levels of the monsters nearby.
* Press the key for a spell to execute it. Note that a spell can be cast only if the cost can be afforded. If it is a directional spell, choose a direction using the arrow keys.
* Note that in one turn, the player can either move once, attack once or cast a spell. A spell is used up if it can be afforded even if it doesn't have any visible effect.
* Get to the door, which leads to a new map.
* When a new dungeon is created, the player's health is carried forward, max health and mana increase by 5. The monsters become a bit tougher.
* Press the Esc key to quit at any time.
* If you die and wish to play again, you'll have to quit and start DunGen again with the file.

### Appendix

#### Colours

DunGen supports 36 colours. Out of these, 30 are variations of 10 basic colours (3 shades for each) and 6 are other colours. 

The three shades of a basic <colour> are simply `<colour>`, `light_<colour>` and `dark_<colour>`.  
Basic colours:

* red
* orange
* yellow
* cyan
* green
* blue
* violet
* crimson
* grey
* sepia

Other colours:

* brass
* copper
* gold
* silver
* black
* white

#### Complete Specifications

* `name`
* `player`
* `wall_colour`
* `wall_char`
* `floor_char`
* `floor_colour`
* `obstacle_char`
* `obstacle_colour`
* `rooms`
* `small`
* `medium`
* `large` 


* `small_min`
* `small_max`
* `medium_min`
* `medium_max`
* `large_min`
* `large_max`  
  These are the minimum and maximum dimensions for those room types. Note that the side of a room includes the walls, so the minimum side must be at least 3.
  
* `map_type`  
  Either 1 or 2.  
  DunGen has two map generation methods.   
  The default (1) uses a random algorithm to fit all the rooms in a fixed map of size 80 by 40. It tries various possibilities before giving up. Due to this, it can be incredibly slow. If it is unable to generate the map, it gives the time taken and an error message.  
  The other (2) first decides the map size based on the number of rooms and then fits the rooms using a grid-based approach. Thus this always succeeds on the first try. However due to much less randomness involved, the rooms are placed in a more orderly fashion than usually expected from a dungeon.  
  Note that neither of these is particularly useful for maps with many rooms. The first because it won't be able to generate it all even after taking up much time. The other because the map will be so big, it won't fit completely on the screen.
  
* `health_boost`  
  The health boost the player receives after walking over corpses.
  
* `fov`  
  The player's field of vision or up to how many blocks away the player can see if nothing is blocking sight.

#### Predefined Behaviours

__basic__
```
if {health > maxhealth / 2} {
	if {player_distance < 2} {
		attack();
	} {
	move_towards();
	}
} {
	flee();
}
```

__scaredycat__
```
flee();
```

__brave__
```
if {player_distance < 2} {
	attack();
} {
	move_towards();
}
```
