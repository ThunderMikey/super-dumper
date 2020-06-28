CSVs = $(wildcard *-items.csv)
HTMLs = $(wildcard *-items.html)
clean:
	rm $(CSVs) $(HTMLs)

sainsburys-items.html tesco-items.html ss-items.html:
	xclip -o > $@

%-items.csv: %-items.html
	python3 $*-h2c.py -i $^ -o $@
