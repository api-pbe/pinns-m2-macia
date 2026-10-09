# =====================================================================
#  PINNs for PDEs — M2 MACIA
#  make            build every document, teacher version (with solutions)
#  make student    build every document without solutions
#  make notebooks  regenerate the lab notebooks from their source script
#  make release    student PDFs + student notebook, collected in dist/
#  make clean      remove LaTeX auxiliaries
#  make distclean  also remove PDFs and dist/
# =====================================================================

TEX      := pdflatex -interaction=nonstopmode -halt-on-error
TEXINPUTS := $(CURDIR)/common:

SOURCES  := $(wildcard session-*/[a-z]*.tex)
PDFS     := $(SOURCES:.tex=.pdf)
STUDENT  := $(SOURCES:.tex=-student.pdf)

.PHONY: all student notebooks release clean distclean

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

release: student notebooks
	@mkdir -p dist
	@cp session-*/*-student.pdf dist/ 2>/dev/null || true
	@cp session-*/lab/*-student.ipynb dist/ 2>/dev/null || true
	@echo "  -> dist/ contains:"; ls -1 dist/

clean:
	@find . \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.toc' \
	        -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' \) -delete
	@echo "  auxiliaries removed"

distclean: clean
	@find . -name '*.pdf' -delete; rm -rf dist
	@echo "  PDFs and dist/ removed"
