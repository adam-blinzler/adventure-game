#Requirements  
- python 3 with only standard libraries
  
# How to start a game
python game.py < configfile >  
< configfile > must exist in the game-design folder  
  
#Design Information  
Each parameter follows this format  
category-component      : value  
There is no checking on if you created a valid game that can be finished.  
  
##Available Parameters  
gamemap-dims            : int< width,length >  
gamemap-dead_rooms      : int< comma separated list of rooms player cannot enter >  
gamemap-start           : int< room number the player will start in >  
gamemap-end             : int< room number the player will exit if entering >  
(optional)gamemap-goal  : int< room number of item to pickup> , str<name of item >  (This item is required to exit)  
(optional)gamemap-monsters        : str< auto or empty >  (defaults to empty if not present)  
(optional)design-intro  : str< file in /game-design directory >  
(optional)design-escape : str< file in /game-design directory >  
(optional)design-monsters         : str< file in /game-design directory > (Note: will not be checked if gamemap-monsters not set to auto)  
nav-actions             : str< comma separated list from available [go, run, sneak] >  
player-actions          : str< comma separated list from available [inspect room, pickup item, read map, attack] >  
  