#!/bin/bash

RB_PLUGINS_DIR="/usr/lib/rhythmbox/plugins/"
RB_PLUGINS_DATA_DIR="/usr/share/rhythmbox/plugins/"
GLIB_DIR="/usr/share/glib-2.0/schemas/"
IGNORE_SEQUENCE='-not -name "*.pyc"' # the files to ignore as arguments for `find`

# find the plugin's name
MODULE_PREFIX="Module="
MODULE_LINE=`grep --text "${MODULE_PREFIX}" *.plugin`
PLUGIN_NAME="${MODULE_LINE#${MODULE_PREFIX}}"
SCHEMA_DIR="schema/"
UI_DIR="ui/"

function deployFiles() { # target_dir, source_dir, file masks ...
    target_dir="${1}";
    shift
    source_dir="${1}";
    shift
    if [ ! -d "${target_dir}" ]; then
        mkdir -pv "${target_dir}" || return 1
    fi
    until [ -z "${1}" ]; do
        mask="${1}"
        while read -d $'\0' -r source_file_path; do
            target_file_path="${source_file_path}"

            # strip '.' and './' at the beginning of paths
            if [[ "${target_file_path}" =~ ^\./(.*) ]]; then
                target_file_path="${BASH_REMATCH[1]}"
            fi

            # make the target file path realtive to the source directory
            target_file_path=${target_file_path#${source_dir}}
            target_subdir=`dirname ${target_file_path}`
            if [ "${target_subdir}" != "." -a ! -z "${target_subdir}" -a ! -d "${target_dir}${target_subdir}" ]; then
                mkdir -pv "${target_dir}${target_subdir}" || return 1
            fi
            cp -v "${source_file_path}" "${target_dir}${target_file_path}" || return 1
        done < <(find "${source_dir}" -name "${mask}" -type f $IGNORE_SEQUENCE -print0|sort -z)
        shift
    done
}

function fail() { # message
    if [ ! -z "${1}" ]; then
        echo "${1}"
    fi
    exit 1
}

# deploy and compile the settings schema
deployFiles "${GLIB_DIR}" "${SCHEMA_DIR}" "*.gschema.xml" || fail "Failed to deploy the application schemas."
glib-compile-schemas "${GLIB_DIR}" || fail "Failed to compile glib schemas"

# copy the resources to the target dir
deployFiles "${RB_PLUGINS_DATA_DIR}${PLUGIN_NAME}/" "${UI_DIR}" "*.ui" || fail "Failed to deploy the plugin resources"

# copy the files to the target dir
deployFiles "${RB_PLUGINS_DIR}${PLUGIN_NAME}/" "." "*.py" "*.plugin" || fail "Failed to deploy the plugin files"