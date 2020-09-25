# get all supported supermarkets
supas =$(patsubst %.py,%,$(filter %.py,$(notdir $(wildcard src/stores/*))))

validCSVs = $(supas:=-items.csv)
validHTMLs = $(supas:=-items.html)
jsonFiles = asda-response.json

clean:
	-rm -f $(validCSVs) $(validHTMLs) $(jsonFiles)

${validHTMLs}:
	xclip -selection c -o > $@

%-items.csv: %-items.html
	python3 src/main.py -s $* -i $^ -o $@

# will override previous recipe
waitrose-items.html:
	@echo 'Please manually copy and paste two XHR responses into the following tags'
	@echo 'one contains quantity_price, the other contains names'
	echo '<script class="quantity_prices">' >> $@
	echo '</script>' >> $@
	echo '<script class="names">' >> $@
	echo '</script>' >> $@
	exit 1

asda-items.html: asda-response.json
	echo '<script class="json">' >> $@
	cat $< >> $@
	echo '</script>' >> $@

