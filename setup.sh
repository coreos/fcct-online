set -eo pipefail

ver='v0.1.0'

print_help(){
    printf "options:\n\
            --local: setupt for local build\n\
            --container: setup for container build\n"
    exit 1
}

setup() {
    set -x
    rm -f ./fcct-* app-signing-pubkey.gpg

    # Download fcct binary and detached signature
    curl -O -L "https://github.com/coreos/fcct/releases/download/${ver}/fcct-x86_64-unknown-linux-gnu"
    curl -O -L "https://github.com/coreos/fcct/releases/download/${ver}/fcct-x86_64-unknown-linux-gnu.asc"

    # Download Coreos Application Signing Key and import it
    curl -O -L http://coreos.com/dist/pubkeys/app-signing-pubkey.gpg
    gpg --import app-signing-pubkey.gpg

    # Verify the downloaded binary
    gpg --verify fcct-x86_64-unknown-linux-gnu.asc fcct-x86_64-unknown-linux-gnu

    chmod +x fcct-x86_64-unknown-linux-gnu
    set +x
}

if [[ "$#" -eq 0 ]]; then
    print_help
fi

# Call getopt to validate the provided input.
rc=0
options=$(getopt --options=lc --longoptions=local,container -- "$@") || rc=$?
[ $rc -eq 0 ] || {
    print_help
    exit 1
}
eval set -- "$options"
while true; do
    case "$1" in
        -l | --local)
            cd ./server
            setup
            cd ..
            ;;
        -c | --container)
            setup
            ;;
        *)
            break
            ;;
    esac
    shift
done

echo "Finish setup"
