# get all supported supermarkets
supas =$(patsubst %.py,%,$(filter %.py,$(notdir $(wildcard src/stores/*))))

validCSVs = $(supas:=-items.csv)
validHTMLs = $(supas:=-items.html)

clean:
	-rm -f $(validCSVs) $(validHTMLs)

${validHTMLs}:
	xclip -o > $@

%-items.csv: %-items.html
	python3 src/main.py -s $* -i $^ -o $@
