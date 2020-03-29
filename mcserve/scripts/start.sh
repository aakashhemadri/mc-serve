#!/usr/bin/bash
# @author Aakash Hemadri
# @email aakashhemadri123@gmail.com
#
# A menu driven shell script to run multiple minecraft servers.
## ----------------------------------------------------------------
# Variables
## ----------------------------------------------------------------

declare -r EDITOR=vim
declare -r RED='\\033[0;41;30m'
declare -r STD='\\033[0;0;39m'
source config.sh

EXIT:=true

## ----------------------------------------------------------------
# Functions
## ----------------------------------------------------------------

function show_menu() {
    clear
    cat <<-_EOF_
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	|                    M I N E C R A F T                    |
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	| Welcome! You may run one of the pre-configured servers! |
	-----------------------------------------------------------
	1] mesa - [PaperMC][1.15.2][mc-paper]
	2] bukkit - [Bukkit][1.14.4][mc-bukkit]
	3] hardcore - [Vanilla][1.14.4][mc-hardcore]
	0] Exit.
	_EOF_
}

function read_option() {
    local CHOICE
    read -p "Enter choice [0 - 3]: " CHOICE
    case ${CHOICE} in
    0) exit_program ;;
    1) mc-paper ;;
    2) mc-bukkit ;;
    3) mc-hardcore ;;
    *)
        clear
        read -p "Bad option! Press [Enter] to try again..." stubKey
        ;;
    esac
}

function pause() {
    read -p "Press [Enter] key to continue..." stubKey
}

function exit_program() {
    clear
    local CHOICE
    read -p "Are you sure that you'd like to quit? [y/N]: " CHOICE
    if [ $CHOICE == 'y' ]; then
        clear
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "                  Have a great day!!                     "
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "Exiting..."
        exit 0
    else
        show_menu
    fi
}

function git_pre_menu() {
    cat <<-_EOF_
-----------------------------------------------------------
|             Would you like sync to origin?              |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
0] start server.
1] git status
2] sync
_EOF_
}
function git_read_option() {
    local CHOICE
    read -p "Enter choice [0 - 2]: " CHOICE
    case ${CHOICE} in
    0) EXIT=false ;;
    1) git status ;;
    2)
        echo -e "Are your environment variables set correctly? (see ./config.sh)"
        pause
        if [[ $(git ls-remote --heads ${ORIGIN_REMOTE} ${BRANCH} | wc -l) == 1 ]]; then
            git switch -c ${BRANCH}
        else
            git branch ${BRANCH}
            git checkout ${BRANCH}
            git push --set-upstream origin ${BRANCH}
        fi
        ;;
    *)
        clear
        read -p "Bad option! Press [Enter] to try again..." stubKey
        ;;
    esac
}

function mc-paper() {
    INSTANCE=mc-paper
    clear
    cat <<-_EOF_
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	|                       MC - PAPER                        |
	_EOF_
    while ${EXIT}; do
        git_pre_menu
        git_read_option
    done
    docker-compose up -d mc-paper
    echo -e "Done. Run ./stop.sh to kill the server"
    exit 0
}

function mc-bukkit() {
    INSTANCE=mc-bukkit
    clear
    cat <<-_EOF_
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	|                       MC - BUKKIT                       |
	_EOF_
    while ${EXIT}; do
        git_pre_menu
        git_read_option
    done
    docker-compose up -d mc-bukkit mc-rcon
    echo -e "Done. Run ./stop.sh to kill the server"
    exit 0
}

function mc-hardcore() {
    INSTANCE=mc-hardcore
    clear
    cat <<-_EOF_
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	|                       MC - HARDCORE                     |
	_EOF_
    while ${EXIT}; do
        git_pre_menu
        git_read_option
    done
    docker-compose up -d mc-hardcore mc-rcon
    echo -e "Done. Run ./stop.sh to kill the server"
    exit 0
}
## ----------------------------------------------------------------
#   Traps
## ----------------------------------------------------------------
trap exit_program SIGINT SIGTERM

## ----------------------------------------------------------------
# Main Loop
## ----------------------------------------------------------------

while true; do
    show_menu
    read_option
done
