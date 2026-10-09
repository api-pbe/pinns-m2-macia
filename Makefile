# =====================================================================
#  PINNs for PDEs — M2 MACIA
#  make            build every document, teacher version (with solutions)
#  make student    build every document without solutions
#  make notebooks  regenerate the lab notebooks from their source script
#  make release    student PDFs + student notebook, collected in dist/
#  make new-session N=03 SLUG=pinn-method   scaffold a new session
#  make clean      remove LaTeX auxiliaries
#  make distclean  also remove PDFs and dist/
# =====================================================================

TEX      := pdflatex -interaction=nonstopmode -halt-on-error
TEXINPUTS := $(CURDIR)/common:

SOURCES  := $(wildcard session-*/[a-z]*.tex)
PDFS     := $(SOURCES:.tex=.pdf)
STUDENT  := $(SOURCES:.tex=-student.pdf)

.PHONY: all student notebooks release new-session clean distclean

all: $(PDFS)

%.pdf: %.tex common/pinns-course.sty
	@echo "  [teacher] $<"
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) $(notdir $<) >/dev/null
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) $(notdir $<) >/dev/null

student: $(STUDENT)

%-student.pdf: %.tex common/pinns-course.sty
	@echo "  [student] $<"
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) -jobname=$(notdir $*)-student \
		"\def\StudentBuild{}\input{$(notdir $<)}" >/dev/null
	@cd $(dir $<) && TEXINPUTS=$(TEXINPUTS) $(TEX) -jobname=$(notdir $*)-student \
		"\def\StudentBuild{}\input{$(notdir $<)}" >/dev/null

notebooks:
	@for d in session-*/lab; do \
	  [ -f $$d/build_notebooks.py ] && (cd $$d && python3 build_notebooks.py); \
	done

# Names are prefixed by session: several sessions have a 'notes.tex', and a
# flat copy would silently overwrite one with another.
release: student notebooks
	@mkdir -p dist
	@for f in session-*/*-student.pdf; do \
	   d=$$(dirname $$f); s=$$(basename $$d | cut -d- -f1-2); \
	   b=$$(basename $$f -student.pdf); \
	   cp $$f dist/$$s-$$b.pdf; \
	 done
	@for f in session-*/lab/*-student.ipynb; do \
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
