This ZIP file contains all the assets and scripts for MC to be used in the Mood Pose Tool.
To use, drop everything in the "MPT" folder into the folder with the same name in a mod which has the MPT installed.
The character's image name is "mc", so to show him you will use a line such as "show mc turned at t11"

To use the sprite with the MC character, find this line of code:
"define mc = DynamicCharacter('player', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")"
and replace it with:
"define mc = DynamicCharacter('player', image='mc', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")"

Credits:
Chronos, Yagamirai, Terra, DiabloGraves - Created the original MPT
Childish-N - Created the original MC sprite
SlightlySimple - Created the MC casual outfit and the individual expression pieces
Team Salvato - Made the game