#! /bin/bash
# -*- coding: utf-8 -*-
#
# pyxbgen
# Agenzia delle Entrate pyxb generator
#
# This free software is released under GNU Affero GPL3
# author: Antonio M. Vigliotti - antoniomaria.vigliotti@gmail.com
# (C) 2017-2022 by SHS-AV s.r.l. - http://www.shs-av.com - info@shs-av.com
#
READLINK=$(which greadlink 2>/dev/null) || READLINK=$(which readlink 2>/dev/null)
export READLINK
# Based on template 2.0.0
THIS=$(basename "$0")
TDIR=$(readlink -f $(dirname $0))
[ $BASH_VERSINFO -lt 4 ] && echo "This script $0 requires bash 4.0+!" && exit 4
if [[ -z $HOME_DEVEL || ! -d $HOME_DEVEL ]]; then
  [[ -d $HOME/odoo/devel ]] && HOME_DEVEL="$HOME/odoo/devel" || HOME_DEVEL="$HOME/devel"
fi
[[ -x $TDIR/../bin/python3 ]] && PYTHON=$(readlink -f $TDIR/../bin/python3) || [[ -x $TDIR/python3 ]] && PYTHON="$TDIR/python3" || PYTHON="python3"
[[ -z $PYPATH ]] && PYPATH=$(echo -e "import os,sys\no=os.path\na=o.abspath\nj=o.join\nd=o.dirname\nb=o.basename\nf=o.isfile\np=o.isdir\nC=a('"$TDIR"')\nD='"$HOME_DEVEL"'\nif not p(D) and '/devel/' in C:\n D=C\n while b(D)!='devel':  D=d(D)\nN='venv_tools'\nU='setup.py'\nO='tools'\nH=o.expanduser('~')\nT=j(d(D),O)\nR=j(d(D),'pypi') if b(D)==N else j(D,'pypi')\nW=D if b(D)==N else j(D,'venv')\nS='site-packages'\nX='scripts'\ndef pt(P):\n P=a(P)\n if b(P) in (X,'tests','travis','_travis'):\n  P=d(P)\n if b(P)==b(d(P)) and f(j(P,'..',U)):\n  P=d(d(P))\n elif b(d(C))==O and f(j(P,U)):\n  P=d(P)\n return P\ndef ik(P):\n return P.startswith((H,D,K,W)) and p(P) and p(j(P,X)) and f(j(P,'__init__.py')) and f(j(P,'__main__.py'))\ndef ak(L,P):\n if P not in L:\n  L.append(P)\nL=[C]\nK=pt(C)\nfor B in ('z0lib','zerobug','odoo_score','clodoo','travis_emulator'):\n for P in [C]+sys.path+os.environ['PATH'].split(':')+[W,R,T]:\n  P=pt(P)\n  if B==b(P) and ik(P):\n   ak(L,P)\n   break\n  elif ik(j(P,B,B)):\n   ak(L,j(P,B,B))\n   break\n  elif ik(j(P,B)):\n   ak(L,j(P,B))\n   break\n  elif ik(j(P,S,B)):\n   ak(L,j(P,S,B))\n   break\nak(L,os.getcwd())\nprint(' '.join(L))\n"|$PYTHON)
[[ $TRAVIS_DEBUG_MODE -ge 8 ]] && echo "PYPATH=$PYPATH"
for d in $PYPATH /etc; do
  if [[ -e $d/z0librc ]]; then
    . $d/z0librc
    Z0LIBDIR=$(readlink -e $d)
    break
  fi
done
[[ -z "$Z0LIBDIR" ]] && echo "Library file z0librc not found in <$PYPATH>!" && exit 72
[[ $TRAVIS_DEBUG_MODE -ge 8 ]] && echo "Z0LIBDIR=$Z0LIBDIR"

CFG_init "ALL"
link_cfg_def
link_cfg $DIST_CONF $TCONF
[[ $TRAVIS_DEBUG_MODE -ge 8 ]] && echo "DIST_CONF=$DIST_CONF" && echo "TCONF=$TCONF"
get_pypi_param ALL
RED="\e[1;31m"
GREEN="\e[1;32m"
CLR="\e[0m"

__version__=10.0.0.3.6

gen_init() {
  local mdl="${1//,/ }"
  local i=./__init__.py
  if [[ $opt_dry_run -eq 0 ]]; then
    echo "# flake8: noqa" >$i
    echo "# -*- coding: utf-8 -*-" >>$i
    echo "# Copyright 2017-2022 - SHS-AV s.r.l. <https://www.zeroincombenze.it>" >>$i
    echo "# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)." >>$i
    echo "#" >>$i
    echo "# Generated $(date '+%a %Y-%m-%d %H:%M:%S') by pyxbgen.sh $__version__" >>$i
    echo "# by Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>" >>$i
    echo "#" >>$i
    for m in $mdl; do
      if [[ -z $opt_mod ]]; then
        echo "from . import $m" >>$i
      else
        echo "import odoo.addons.${opt_mod}.bindings.$m" >>$i
      fi
    done
  fi
}

create_hook() {
  local fn=$1
  if [ $opt_dry_run -eq 0 ]; then
    echo "# flake8: noqa" >$fn
    echo "# -*- coding: utf-8 -*-" >>$fn
    echo "# Copyright 2017-2022 - SHS-AV s.r.l. <https://www.zeroincombenze.it>" >>$fn
    echo "# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)." >>$fn
    echo "#" >>$fn
    echo "import pyxb" >>$fn
    stmt="if"
    for v in 1.2.4 1.2.5 1.2.6; do
      echo "$stmt pyxb.__version__ == '$v':" >>$fn
      if [[ -z $opt_mod ]]; then
        echo "    from ${fn:0:-3}__${v//./_} import *" >>$fn
      else
        echo "    from odoo.addons.${opt_mod}.${fn:0:-3}__${v//./_} import *" >>$fn
      fi
      stmt="elif"
    done
    echo "else:" >>$fn
    echo "    raise pyxb.PyXBVersionError('1.2.4 to 1.2.6')" >>$fn
    # echo "">>$fn
  fi
}

excl="DatiFatturaMessaggi,Fattura_VFSM10.xsd,FatturaPA_versione_1.1,FatturaPA_versione_1.2,MessaggiTypes"


OPTOPTS=(h        b          K        k        l        I         M        m       n           o        p        q           S       u       V           v           w        x         3)
OPTDEST=(opt_help opt_branch opt_cont opt_keep opt_list opt_ginit opt_mult opt_mod opt_dry_run opt_odoo opt_pep8 opt_verbose opt_str opt_uri opt_version opt_verbose opt_venv opt_exclude opt_py3)
OPTACTI=("+"      "="        1        1        "1>"     "=>"      1        "="     1           "=>"     1        0           1       "1>"    "*"         1           "="      "=>"      1)
OPTDEFL=(1        ""         0        0        0        ""        0        ""      0           ""       0        -1          0       0       ""         -1          ""       "$excl"   0)
OPTMETA=("help"   "vers"     ""       ""       ""       "files"   ""       "name"  ""          "path"   ""       "silent"    ""      ""      "version"   "verbose"   "path"   "file"    "")
OPTHELP=("this help"
  "odoo branch; may be 6.1 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0 or 16.0"
  "keep binding directory, if found"
  "keep temporary files"
  "list xml schemas and module names"
  "generate __init__.py with modules list"
  "multi version (append pyxb version to file names)"
  "import module path (i.e. ~/10.0/l10n-italy/l10n_it_ade/"
  "do nothing (dry-run)"
  "odoo module name (def='.')"
  "do apply pep8"
  "silent mode"
  "do not convert Decimal to String"
  "execute uri Agenzia delle Entrate"
  "show version"
  "verbose mode"
  "virtual env (with pyxb) path"
  "modules exclusion list; i.e. fornituraIvp,FatturaPA,DatiFattura,DatiFatturaMessaggi"
  "generate for python3"
)
OPTARGS=()

parseoptargs "$@"
if [[ "$opt_version" ]]; then
  echo "$__version__"
  exit 0
fi
if [[ $opt_help -gt 0 ]]; then
  print_help "Agenzia delle Entrate pyxb generator\nPer generare file .py usare switch -u" \
    "(C) 2017-2022 by zeroincombenze®\nhttps://zeroincombenze-tools.readthedocs.io/\nAuthor: antoniomaria.vigliotti@gmail.com"
  exit 0
fi
XSD_FILES=("fornituraIvp_2017_v1.xsd" "FatturaPA_versione_1.2.1.xsd" "FatturaPA_versione_1.2.xsd" "FatturaPA_versione_1.1.xsd" "DatiFatturav2.1.xsd" "DatiFatturaMessaggiv2.0.xsd" "MessaggiTypes_v1.1.xsd" "Fattura_VFPR12.xsd" "Fattura_VFSM10.xsd")
MOD_NAMES=("vat_settlement_v_1_0" "fatturapa_v_1_2" "fatturapa_v_1_2" "fatturapa_v_1_1" "dati_fattura_v_2_1" "messaggi_fattura_v_2_0" "MessaggiTypes_v_1_1" "fatturapa_v_1_2" "fatturapa_v_1_0")
bin_path=${PATH//:/ }
PYXBGEN_BIN=
[[ -z $opt_odoo ]] && opt_odoo=$PWD
[[ -z $opt_venv && -d $(readlink -f $opt_odoo/../../venv_odoo) ]] && opt_venv="$(readlink -f $opt_odoo/../../venv_odoo)"
[[ -z $opt_venv && -n $opt_branch && -d $HOME/$opt_branch/venv_odoo ]] && opt_venv="$HOME/$opt_branch/venv_odoo"
if [[ -n $opt_venv ]]; then
    [[ -x $(readlink -e $opt_venv)/bin/pyxbgen ]] && PYXBGEN_BIN="$(readlink -e $opt_venv)/bin/pyxbgen"
fi
[[ -z "$PYXBGEN_BIN" ]] && echo "File pyxbgen not found! Please use -w path" && exit 1
[[ -x $(dirname $PYXBGEN_BIN)/python ]] && PYTHON="$(dirname $PYXBGEN_BIN)/python"
[[ -z $PYTHON ]] && echo "Python for $PYXBGEN_BIN not found!" && exit 1
PYXBGEN_PY=
for x in $TDIR $TDIR/.. $opt_odoo; do
  if [[ -f $x/pyxbgen.py ]]; then
    PYXBGEN_PY="$x/pyxbgen.py"
    break
  fi
done
[[ -z "$PYXBGEN_PY" ]] && echo "File pyxbgen.py not found!" && exit 1
BINDINGS=$TDIR/bindings
[[ ! -d $BINDINGS ]] && echo "Directory $BINDINGS not found!" && exit 1
SCHEMAS=$TDIR/data
[[ ! -d $SCHEMAS ]] && echo "Directory $SCHEMAS not found!" && exit 1
if [[ -z $opt_mod ]]; then
  x=$(find $(dirname $opt_venv) -name $(basename $0))
  opt_mod=$(basename $(dirname $x))
fi

TOPEP8=$(which topep8 2>/dev/null)
if [[ -z "$TOPEP8" ]]; then
  TOPEP8=$(which autopep8 2>/dev/null)
  [[ -n "$TOPEP8" ]] && TOPEP8="$TOPEP8 -eL"
else
  TOPEP8="$TOPEP8 -eL"
  [[ -n "$opt_branch" ]] && TOPEP8="$TOPEP8 -b$opt_branch"
fi
if [[ -z "$TOPEP8" && $opt_pep8 -ne 0 ]]; then
  echo "topep8/autopep8 not found!"
  echo "Operations will be executed ignoring switch -p"
fi
if [[ -n $opt_ginit ]]; then
  echo "$0 -I $opt_ginit"
  gen_init "$opt_ginit"
  exit 0
fi
pyxbgen_ver=$($PYXBGEN_BIN --version | grep --color=never -Eo "[0-9.]+")
pyxb_ver=$(vem $opt_venv show pyxb | grep "^Version" | grep -Eo "[0-9.]+")
if [[ $pyxbgen_ver != $pyxb_ver ]]; then
  echo "Version mismatch"
  echo "pyxb version is $pyxb_ver  "
  echo "$PYXBGEN_BIN version is $pyxbgen_ver"
  exit 1
fi
echo "PYXB generator $__version__ by pyxb $pyxb_ver"

FMLIST=
MDL=
grpl=
VALID_COLOR="\e[0;92;40m"
INVALID_COLOR="\e[0;31;40m"
NOP_COLOR="\e[0m"
[[ "$PWD" != "$TDIR" ]] && run_traced "cd $TDIR"

if [[ $opt_list -eq 0 ]]; then
  if [[ -d $BINDINGS.bak && ! -f $BINDINGS.bak/_ds.py && ! -f $BINDINGS.bak/_cm.py ]]; then
    run_traced "rm -fR $BINDINGS.bak"
  fi
  if [[ -d $BINDINGS && ! -f $BINDINGS/_ds.py && ! -f $BINDINGS/_cm.py ]]; then
    run_traced "rm -fR $BINDINGS"
  fi
  if [[ $opt_cont -eq 0 && -d $BINDINGS ]]; then
    [[ -d $BINDINGS.bak ]] && run_traced "rm -fR $BINDINGS.bak"
    run_traced "mv $BINDINGS $BINDINGS.bak"
  fi
  [[ -f $SCHEMAS//fattura_elettronica_B2B/Fattura_VFPR12.xsd && -f $SCHEMAS/fatturapa/FatturaPA_versione_1.2.1.xsd ]] && run_traced "cp $SCHEMAS/fatturapa/FatturaPA_versione_1.2.1.xsd $SCHEMAS//fattura_elettronica_B2B/Fattura_VFPR12.xsd"
fi
run_traced "mkdir -p $BINDINGS"
run_traced "pushd $BINDINGS >/dev/null"
exclude="(${opt_exclude//,/|})"
for d in $SCHEMAS/*; do
  if [[ -d $d ]]; then
    x=$(basename $d)
    if [[ $x != "common" ]]; then
      [[ $opt_verbose -ne 0 ]] && echo "# analyzing directory $d ..."
      [[ -L $d/xmldsig-core-schema.xsd ]] && run_traced "rm -f $d/xmldsig-core-schema.xsd"
      [[ ! -f $d/xmldsig-core-schema.xsd ]] && run_traced "cp $SCHEMAS/common/xmldsig-core-schema.xsd $SCHEMAS/$x/"
    fi
    p=$d
    for x in main liquidazione; do
      if [[ -d $d/$x ]]; then
        p=$d/$x
        break
      fi
    done
    [[ $opt_verbose -ne 0 ]] && echo "# searching for schemas into directory $p ..."
    for f in $p/*.xsd; do
      fn=$(basename $f)
      ff=$(readlink -f $f)
      if [[ ! $fn =~ $exclude || $opt_list -ne 0 ]]; then
        jy=0
        while ((jy < ${#XSD_FILES[*]})); do
          xsd="${XSD_FILES[jy]}"
          mdn="${MOD_NAMES[jy]}"
          if [[ $fn == $xsd ]]; then
            grp=${mdn:0:-6}
            if [[ $fn =~ $exclude ]]; then
              info="deprecated"
              TEXT_COLOR="$INVALID_COLOR"
            else
              info=""
              TEXT_COLOR="$VALID_COLOR"
            fi
            _xsd=$(printf "%-30.30s" "$xsd")
            _mdn=$(printf "%-20.20s" "$mdn")
            if [[ $opt_list -ne 0 ]]; then
              echo -e "Found schema $TEXT_COLOR$_xsd$NOP_COLOR module $_mdn (by $grp) $info"
            else
              [[ $grpl =~ $grp ]] && echo "Schema $_xsd may conflict with prior schema by $grp"
              grpl="$grpl $grp"
              MDL="$MDL $mdn"
              FMLIST="-u $f -m $mdn $FMLIST"
            fi
            break
          fi
          ((jy++))
        done
      fi
    done
  fi
done
cmd="$PYXBGEN_BIN $FMLIST --archive-to-file=./ade.wxs"
if [[ $opt_list -eq 0 ]]; then
  run_traced "$cmd"
  echo "$(readlink -f $0) -I ${MDL// /,}"
  gen_init "$MDL"
  for f in _cm _ds $MDL; do
    fn=$f.py
    if [[ ! -f $fn ]]; then
      echo "File $fn not found!"
      echo "Cannot execute $PYXBGEN_PY $fn $SCHEMAS"
    else
      [[ $opt_keep -ne 0 ]] && run_traced "cp $fn $fn.bak"
      run_traced "$PYTHON $PYXBGEN_PY $fn $SCHEMAS"
      if [[ $opt_pep8 -ne 0 ]]; then
        run_traced "$TOPEP8 $fn"
        run_traced "oca-autopep8 -i $fn"
      fi
      [[ $opt_py3 -ne 0 ]] && opts="3" || opts=""
      [[ $opt_str -ne 0 ]] && opts="${opts}S"
      [[ -n $opts ]] && opts="-$opts"
      run_traced "$PYTHON $PYXBGEN_PY $fn $opts"
      for x in TD16 TD17 TD18 TD19 TD24; do
        grep -q $x $BINDINGS/fatturapa*.py || echo "*** Error: TD16 not found! ***"
      done
      if [[ $opt_mult -gt 0 ]]; then
        if [[ ${fn: -3} == ".py" ]]; then
          tgt="${fn:0:-3}__${pyxb_ver//./_}${fn: -3}"
          run_traced "mv $fn $tgt"
          create_hook $fn
        fi
      fi
    fi
  done
fi
run_traced "popd >/dev/null"
if [[ $opt_list -eq 0 && $opt_keep -eq 0 ]]; then
  find $TDIR -type f -name "*.bak" -delete
  find $TDIR -type f -name "*.pyc" -delete
fi
echo ""
echo "You should copy ..."
if [[ $opt_mult -gt 0 ]]; then
  echo "cp $BINDINGS/*__${pyxb_ver}.py <PATH_TO_MODULE>"
else
  echo "cp $BINDINGS/*.py <PATH_TO_MODULE>"
fi
