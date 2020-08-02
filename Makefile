# get all supported supermarkets
supas =$(patsubst %.py,%,$(notdir $(wildcard html2list/*)))

validCSVs = $(supas:=-items.csv)
validHTMLs = $(supas:=-items.html)

clean:
	-rm -f $(validCSVs) $(validHTMLs)

${validHTMLs}:
	xclip -o > $@

%-items.csv: %-items.html
	python3 src/main.py -s $* -i $^ -o $@
