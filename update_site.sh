# Execute with either sh or bash

# Update every page
PYTHONPATH=${PYTHONPATH}:${PWD}/src python src/update_site.py
RV=$?
if [ ${RV} -ne 0 ]; then
    exit ${RV}
fi

# Recreate every web game page
PYTHONPATH=${PYTHONPATH}:${PWD}/src python src/update_site.py --webgame src/game/ldjam/ld22.json --webgame src/game/ldjam/ld23.json --webgame src/game/ldjam/ld24.json --webgame src/game/ldjam/ld25.json --webgame src/game/ldjam/ld26.json --webgame src/game/ldjam/ld27.json --webgame src/game/ldjam/ld28.json --webgame src/game/ldjam/ld29.json --webgame src/game/ldjam/ld30.json --webgame src/game/ggj/ggj14.json --webgame src/game/non-jam/laserdude.json
exit $?

