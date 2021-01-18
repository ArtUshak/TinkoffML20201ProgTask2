# Tinkoff ML course 2021, entry programming task #2

This is simple console-based sudoku game 9x9. Run `python ./task_prog2/sudoku.py` to play game.

## Interface

First, type `NEW` to start new game and generate random field, or `LOAD` to load saved game.

If you typed `NEW`, then type number of cells to be filled by generator, or type empty string to cancel.

If you typed `LOAD`, then type path to file with saved game, or type empty string to cancel.

Then you can play using commands. Type `HELP` to get list of commands.

## Example

```
Type NEW to start new game or LOAD to load game from pickle file
NEW
Type filled cell count or empty string to cancel: 32
 | | | |8|4|9| | 
-----------------
 | | | |7| |4| | 
-----------------
3|8| |5| | | | |1
-----------------
5|9| |6|3| | | | 
-----------------
 | | | |9|1| | |8
-----------------
7|6| | | |8|1|2| 
-----------------
8|2|6| | | | | |3
-----------------
 | | |9|6| |5|3| 
-----------------
 | |8| |2|9| | | 
> HELP
Commands:
SET i j v -- set cell at i, j to value v and print game
        i -- row id,    in range from 0 to 9
        j -- column id, in range from 0 to 9
        v -- new value, in range from 0 to 9
SAVE f    -- save game state to pickle file
        f -- file path, .pkl extension is recommended
PRINT     -- print game
HELP      -- print this help text
EXIT      -- give up and exit
> SET 8 8 9
You can not set cell at 8, 8 to 9
> SET 8 8 4
 | | | |8|4|9| | 
-----------------
 | | | |7| |4| | 
-----------------
3|8| |5| | | | |1
-----------------
5|9| |6|3| | | | 
-----------------
 | | | |9|1| | |8
-----------------
7|6| | | |8|1|2| 
-----------------
8|2|6| | | | | |3
-----------------
 | | |9|6| |5|3| 
-----------------
 | |8| |2|9| | |4
> PRINT
 | | | |8|4|9| | 
-----------------
 | | | |7| |4| | 
-----------------
3|8| |5| | | | |1
-----------------
5|9| |6|3| | | | 
-----------------
 | | | |9|1| | |8
-----------------
7|6| | | |8|1|2| 
-----------------
8|2|6| | | | | |3
-----------------
 | | |9|6| |5|3| 
-----------------
 | |8| |2|9| | |4
> EXIT
You lose!
```

## Limitations

* Only caring of columns and rows, ignoring blocks 3x3.
* Field generator does not guarantee that generated field would be solvable.
* Game is saved using `pickle` module, therefore it is **not safe** to load save files from other people you do not trust.
