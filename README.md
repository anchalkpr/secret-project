# nlp-csci544-project
Final Project for CSCI 544 - NLP Applications 

Text summarization of comments in myGOV.in

In 2014, the Government of India launched a platform called myGOV for citizens to share their views on matters of national interest. Majority of the comments on the discussions are either in English or Hindi. Hundreds of comments are made on each discussion which makes it difficult to collate people's concerns. On most websites, comments are an afterthought, but on myGOV discussion forums, the comments are the highlight, where the government can listen to concerns of its citizens. Therefore its important to summarize most common themes of the discussion and identify dominant and recurrent views on the discussion topic.

Previous work on Hindi text summarization focuses on document summarization, and doesn't work well on comments. English has been the dominant language of inquiry in text summarization, and performance for Hindi is unknown.

We scraped the myGOV website for gathering a raw dataset, and the comment data has several noisy sentences. Curating the data was a significant task creating a bottleneck for good performance. Creating a meaningful summary is a hard task for this dataset because of sparse occurrences of relevant intelligible comments. Summarization is a complex task and we focus on using an extractive summarization technique. In this paradigm, its hard to ensure that summaries are coherent but they represent the content of the text. \newline

In comment summarization, LDA topic clustering is known to outperform other methods. Clustering is an important task because sentence extraction depends on good topic clusters. Our hypothesis is that using topic model with LDA will give us relevant summaries.
