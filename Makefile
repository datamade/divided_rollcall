.PHONY : all
all : split_votes.csv oppose_together.csv

split_votes.csv :
	python split_votes.py | \
          csvcut -C 4 | \
          csvsort -c date --no-inference | \
          python resort_split.py > $@

oppose_together.csv : split_votes.csv
	cat $< | python vote_together.py > $@
