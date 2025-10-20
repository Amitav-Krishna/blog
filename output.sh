#!/bin/bash
set -euo pipefail

HTMLIZE_DIR="$HOME/.emacs.d/elpa/htmlize-1.59"
OB_TMP_DIR="./.ob-tmp"
OUT_DIR="./output"

mkdir -p "$OB_TMP_DIR" "$OUT_DIR"

command -v g++ >/dev/null 2>&1 || { echo "g++ not found. Install it (e.g.,: sudo dnf install gcc-c++)"; exit 1; }
rm -f "$OUT_DIR"/*.html
for f in *.org; do
  base="$(basename "$f" .org)"
  out="$OUT_DIR/$base.html"
  echo "==> Exporting $f → $out"

  emacs --batch "$f" \
    --eval "(require 'org)" \
    --eval "(add-to-list 'load-path (expand-file-name \"$HTMLIZE_DIR\"))" \
    --eval "(require 'htmlize)" \
    \
    --eval "(setq org-babel-temporary-directory (expand-file-name \"$OB_TMP_DIR\"))" \
    --eval "(make-directory org-babel-temporary-directory t)" \
    \
    --eval "(setq org-babel-C-compiler \"g++\")" \
    --eval "(setq org-babel-default-header-args:C
                 '((:results . \"output\")
                   (:flags   . \"-std=c++17\")))" \
    --eval "(setq org-babel-default-header-args:cpp
                 '((:results . \"output\")
                   (:flags   . \"-x c++ -std=c++17\")))" \
    --eval "(setq org-babel-default-header-args:C++
                 '((:results . \"output\")
                   (:flags   . \"-x c++ -std=c++17\")))" \
    \
    --eval "(org-babel-do-load-languages
              'org-babel-load-languages
              '((C . t) (python . t) (shell . t)))" \
    \
    --eval "(add-to-list 'org-src-lang-modes '(\"cpp\" . c++))" \
    --eval "(add-to-list 'org-src-lang-modes '(\"C++\" . c++))" \
    \
    --eval "(defalias 'org-babel-execute:C++  #'org-babel-execute:C)" \
    --eval "(defalias 'org-babel-expand-body:C++ #'org-babel-expand-body:C)" \
    --eval "(defalias 'org-babel-execute:cpp  #'org-babel-execute:C)" \
    --eval "(defalias 'org-babel-expand-body:cpp #'org-babel-expand-body:C)" \
    \
    --eval "(setq org-confirm-babel-evaluate nil)" \
    \
    --eval "(with-current-buffer (find-file-noselect \"$f\")
               (org-export-to-file 'html \"$out\"))" \
  || { echo "Export failed for $f"; exit 1; }
done

echo "✅ Done. HTML files generated in $OUT_DIR"
