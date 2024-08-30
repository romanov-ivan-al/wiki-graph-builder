all: clean

part_1:
	python3 cache_wiki.py -p 'Erdős number'

part_1_d:
	python3 cache_wiki.py -p 'Erdős number' -d 10


part_2:
	python3 shortest_path.py -v --from 'Erdős number - Wikipedia' --to 'Alphabet - Wikipedia'


part_3:
	python3 render_graph.py


clean:
	rm -rf wiki_graph.png wiki_graph.html wiki.json lib __pycache__ log_file.log
 

