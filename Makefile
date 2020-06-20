clean:
	rm items.csv items.html

items.html:
	xclip -o > $@

items.csv: items.html
	python3 html_list_to_csv.py

