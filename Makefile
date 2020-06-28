CSVs = $(wildcard *-items.csv)
HTMLs = $(wildcard *-items.html)
clean:
	rm $(CSVs) $(HTMLs)

%-items.html:
	xclip -o > $@

%-items.csv: %-items.html
	python3 html2list/$*.py -i $^ -o $@
