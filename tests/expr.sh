#!/bin/bash

cd "$(dirname $(readlink -f "$(which "$0")"))" &&
type ../transform.py &>/dev/null || exit 2

IFS=$'\n'

strs='
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
itufo.pc.ijkaq
mpcvywwaftskhx
mepl.oyghstay.sennzbur.uwjwmz
twrgcg.o.xisk
bhroqsvkb.yjxes
-m}>`U( .TC|9| |tv<`g;!YU
$@a21Q/F:x:31rY2y9-|+mfE3T/tnp]n
#|M_G@;KN"oUGtY^wpy5kvRcf=TXTA
DB1}bCX{(H9@##:`Q[A15|"!!"b!\E:&T
'
exprs='
y///
y///s
y///d
y///ds
y///c
y///cs
y///cd
y///cds
y/w-zw-zfa-ef/_sa-c/
y/fl-pf/a-c/s
y/w-zw-z/s_|/d
y/gg/_a-c/ds
y/gw-zw-zl-p//cs
y/iA-Hl-o/sf\n/cs
y//\n:-@A-C_/cd
y/ -,i>/e-l\ne-l/cd
y/l-o1-9[-]<OE/s_{-~+-0+-0e-l:-@A-CAAAA*AAAAAAAAAAAAAA_s/cds
'

echo "$0" "$@"

if [[ "$1" =~ ^[0-9]+$ ]]
then runs=$1 && shift
else runs=1000
fi
strs+=( $strs   $(./rand_strs.py $runs) ) || exit $?
exprs+=( $exprs $(./rand_yexp.py $runs) ) || exit $?

if [[ "$1" = time ]]; then
    TIMEFORMAT="%2Rs    %P%%"
    yexprs=()
    for (( i = 0; i < 5; ++i )); do
        yexprs+=("${exprs[$(( $RANDOM%(${#exprs[@]}-8)+8 ))]}")
    done
    run() {
        echo "$@"
        if [[ "$1" == perl ]]; then
            args="${yexprs[@]/%/;}"
            args=(-e "$args")
        else
            args=("${yexprs[@]}")
        fi
        time for str in "${strs[@]}"; do
            echo "$str"
        done | "$@" "${args[@]}" >/dev/null
    }
    (run perl -p &&
     run ../transform.py) 2>&1 && echo
    exit
fi

error() {
    echo "$1 error: $yex"
    exit 1
}

for (( i = 1; i <= runs; ++i )); do
    str="${strs[$i]}"
    yex="${exprs[$i]}"
    perl="$(echo "$str" | perl -pe        "$yex")" || error perl
    pyth="$(echo "$str" | ../transform.py "$yex")" || error python
    if [[ "$perl" != "$pyth" ]]; then
        echo -e "\e[31;1mrun $((i+1))\e[0m"
        echo "string is: $str"
        echo "transform: $yex"
        echo "result is: $pyth"
        echo "should be: $perl"
        exit 1
    elif ! (( i % 100 )); then
        echo "$i"
    fi
done

echo -e "\e[32;1mall tests passed\e[0m"
echo
