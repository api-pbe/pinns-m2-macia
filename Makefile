# =====================================================================
#  PINNs for PDEs — M2 MACIA
#  make            build every document, teacher version (with solutions)
#  make handout    build every document without solutions (what you print)
#  make notebooks  regenerate the lab notebooks from their source script
#  make release    both variants + notebooks, collected in dist/
#  make new-session N=03 SLUG=pinn-method   scaffold a new session
#  make clean      remove LaTeX auxiliaries
#  make distclean  also remove PDFs and dist/
# =====================================================================

TEX      := pdflatex -interaction=nonstopmode -halt-on-error
TEXINPUTS := $(CURDIR)/common:

SOURCES  := $(wildcard session-[0-9]*/[a-z]*.tex)
PDFS     := $(SOURCES:.tex=.pdf)
HANDOUT  := $(SOURCES:.tex=-handout.pdf)

.PHONY: all handout notebooks release new-session clean distclean

all: $(PDFS)

%.pdf: %.tex common/pinns-course.sty
	@echo "  [teacher] $<"
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) $(notdir $<) >/dev/null
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) $(notdir $<) >/dev/null

handout: $(HANDOUT)

%-handout.pdf: %.tex common/pinns-course.sty
	@echo "  [handout] $<"
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) -jobname=$(notdir $*)-handout \
		"\def\HandoutBuild{}\input{$(notdir $<)}" >/dev/null
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) -jobname=$(notdir $*)-handout \
		"\def\HandoutBuild{}\input{$(notdir $<)}" >/dev/null

notebooks:
	@for d in session-[0-9]*/lab; do \
	  if [ -f $$d/build_notebooks.py ]; then (cd $$d && python3 build_notebooks.py); fi; \
	done

# Names are prefixed by session: several sessions have a 'notes.tex', and a
# flat copy would silently overwrite one with another.
release: all handout notebooks
	@mkdir -p dist
	@for f in session-[0-9]*/*.pdf; do \
	   d=$$(dirname $$f); s=$$(basename $$d | cut -d- -f1-2); \
	   cp $$f dist/$$s-$$(basename $$f); \
	 done
	@for f in session-[0-9]*/lab/*.ipynb; do \
	   [ -e $$f ] && cp $$f dist/ || true; \
	 done
	@echo "  -> dist/ contains:"; ls -1 dist/

new-session:
	@test -n "$(N)"    || { echo "usage: make new-session N=03 SLUG=pinn-method"; exit 1; }
	@test -n "$(SLUG)" || { echo "usage: make new-session N=03 SLUG=pinn-method"; exit 1; }
	@test ! -d session-$(N)-$(SLUG) || { echo "session-$(N)-$(SLUG) already exists"; exit 1; }
	@cp -r session-template session-$(N)-$(SLUG)
	@sed -i.bak 's/@N@/$(N)/g' session-$(N)-$(SLUG)/*.tex && rm -f session-$(N)-$(SLUG)/*.bak
	@echo "  created session-$(N)-$(SLUG)"
	@echo "  keep only the documents this session needs — see docs/authoring.md, section 1"

clean:
	@find . \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \
	        -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' \) -delete
	@echo "  auxiliaries removed"

distclean: clean
	@find . -name '*.pdf' -delete; rm -rf dist
	@echo "  PDFs and dist/ removed"
