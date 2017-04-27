python2 ./scripts/detect_relations.py embeddings/wiki-$1/vocab-cbow-0-64-2-800.txt embeddings/wiki-$1/embedding-cbow-0-64-2-800.txt relational_data/$1_morph.train relational_data/$1_morph.train.labels relational_data/$1_morph.test > result_$1.txt
echo ok
python2 ./scripts/evaluate.py relational_data/$1_morph.test.labels ./result_$1.txt
