# Requirements  
- python 3 with only standard libraries  
  
# How to start a game  
python /src/game.py < configfile path >  
  
# Design Information  
The configuration file is of yaml format. Each parameter follows this format  
category:  
&nbsp;&nbsp;&nbsp;&nbsp;component&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;value  
The game map is made from a matrix of rooms where some rooms be be blocked from play.  
There is no checking on if you created a valid game that can be finished.  
  
## Available Parameters  
<pre>  
gamemap:  
    width               : int< >   
    length              : int< >  
    dead_rooms          : [ int< comma separated list of rooms player cannot enter > ]   
    start               : int< room number the player will start in >  
    end                 : int< room number the player will exit if entering >  
    (optional)goal      : [ int< room number of item to pickup> , str<name of item >  (This item is required to exit) ]  
    (optional)monsters  : str< auto or empty >  (defaults to empty if not present)  
(optional)design:  
    intro               : str< file in /game-design directory >  
    escape              : str< file in /game-design directory >  
    monsters            : str< file in /game-design directory > (Note: will not be checked if monsters not set to auto)  
nav:  
    actions             : [ str< comma separated list from available [go, run, sneak] > ]  
player:  
    actions             : [ str< comma separated list from available [inspect room, pickup item, read map, attack] > ]  
</pre>  
