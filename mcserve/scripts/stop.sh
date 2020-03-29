#!/usr/bin/bash
# @author Aakash Hemadri
# @email aakashhemadri123@gmail.com
#
# A menu driven shell script to run multiple minecraft servers.
## ----------------------------------------------------------------
# Variables
## ----------------------------------------------------------------

declare -r EDITOR=vim
source config.sh

## ----------------------------------------------------------------
# Functions
## ----------------------------------------------------------------

function git_post_menu() {
    cat <<-_EOF_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
|                      M I N E C R A F T                      |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| Would you like to push changes? Before shutting down server |
---------------------------------------------------------------
1] git status.
2] push all.
3] push only plugins/configs.
4] push server.
5] Nope just exit.
_EOF_
}

function pause() {
    read -p "Press [Enter] key to continue..." stubKey
}

function git_read_option() {
    local CHOICE
    read -p "Enter choice [1 - 5]: " CHOICE
    case ${CHOICE} in
    5) exit 0 ;;
    1) git status ;;
    2)
        echo -e "Are your environment variables set correctly? (see ./config.sh)"
        pause
        if [[ $(git ls-remote --heads ${ORIGIN_LOCAL} ${BRANCH} | wc -l) == 0 ]]; then
            git checkout ${BRANCH}
            git push
        else
            git branch --set-upstream-to=origin/${BRANCH} ${BRANCH}
            git push
        fi
        git checkout ${BRANCH}
        git add plugins mc
        git commit -m "${INSTANCE} | $(git config user.name) | $(git config user.email) | $(date +'%Y-%m-%d %H:%M:%S')"
        exit 0
        ;;
    3)
        read -p "Enter branch name: [ex: IGN-HOST-INSTANCE]" BRANCH
        git checkout ${BRANCH}
        git add plugins
        git commit -m "${INSTANCE} | $(git config user.name) | $(git config user.email) | $(date +'%Y-%m-%d %H:%M:%S')"
        exit 0
        ;;
    4)
        read -p "Enter branch name: [ex: IGN-HOST-INSTANCE]" BRANCH
        git checkout ${BRANCH}
        git add mc
        git commit -m "${INSTANCE} | $(git config user.name) | $(git config user.email) | $(date +'%Y-%m-%d %H:%M:%S')"
        exit 0
        ;;
    *)
        clear
        read -p "Bad option! Press [Enter] to try again..." stubKey
        ;;
    esac
}

## ----------------------------------------------------------------
#   Traps
## ----------------------------------------------------------------
trap exit_program SIGINT SIGTERM

## ----------------------------------------------------------------
# Main Loop
## ----------------------------------------------------------------

docker-compose down
while true; do
    git_post_menu
    git_read_option
done
