<h1>Project:-Movie recommendation system</h1>

Recommendation systems are becoming increasingly important in today’s extremely busy world. People are always short on time with the myriad tasks they need to accomplish in the limited 24 hours. Therefore, the recommendation systems are important as they help them make the right choices, without having to expend their cognitive resources.

The purpose of a recommendation system basically is to search for content that would be interesting to an individual. Moreover, it involves a number of factors to create personalised lists of useful and interesting content specific to each user/individual. Recommendation systems are Artificial Intelligence based algorithms that skim through all possible options and create a customized list of items that are interesting and relevant to an individual. These results are based on their profile, search/browsing history, what other people with similar traits/demographics are watching, and how likely are you to watch those movies. This is achieved through predictive modeling and heuristics with the data available.

<h1>About this project</h1>

This is a flask web application that can recommend various kinds of similar movies based on an user interest.

<h1>Concept used to build the model.pkl file : cosine_similarity</h1>

1 . Cosine Similarity is a metric that allows you to measure the similarity of the documents.

2 . In order to demonstrate cosine similarity function we need vectors. Here vectors are numpy array.

3 . Finally, Once we have vectors, We can call cosine_similarity() by passing both vectors. It will calculate the cosine similarity between these two.

4 . It will be a value between [0,1]. If it is 0 then both vectors are complete different. But in the place of that if it is 1, It will be completely similar.

5 . For more details , check URL : https://www.learndatasci.com/glossary/cosine-similarity/

<h1>How to run?</h1>

<h2>STEPS:</h2>

Clone the repository

https://github.com/Dhruti647/Movie_recommendation_system.git

<h2>STEP 01- Create a virutal environment after opening the repository</h2>

python -m venv movieenv

movieenv\scripts\activate

<h2>STEP 02- install the requirements</h2>

pip install -r requirements.txt

#run this file to generate the models

Movie recommendation system-checkpoint.ipynb

Now run,

python app.py
