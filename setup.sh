PROJECT_NAME="Spatial-Multitasking"

CURRENT_PATH=$(pwd)
CURRENT_DIR_RUN_ERR="!Error: run script from project root"


# check if current path is the project root
pattern=".*\/${PROJECT_NAME}"
if ! [[ "$CURRENT_PATH" =~ $pattern ]]
then
 echo "$CURRENT_DIR_RUN_ERR"
 exit
fi


# check if the bash is running inside a python virtualenv or not
if [[ "$VIRTUAL_ENV" != "" ]]
then
  INENV=1
else
  INENV=0
fi

create_env() {
    pattern="Python (\d+)\.(\d+)"
    pyv="$(python3 -V 2>&1 | grep -Po "$pattern")"

    major_version=$(grep -Po "$pattern" <<< "$pyv" | cut -d' ' -f2 | cut -d'.' -f1)
    minor_version=$(grep -Po "$pattern" <<< "$pyv" | cut -d' ' -f2 | cut -d'.' -f2)

    if [ "$major_version" -eq 3 ] && [ "$minor_version" -gt 8 ];
    then
      # create venv
      python3 -m venv venv
      # install project dependencies
      ./venv/bin/pip install -r requirement.txt
    fi
}

if [[ "$INENV" -eq 1 ]]
then
  echo mio
else
  create_env
fi
