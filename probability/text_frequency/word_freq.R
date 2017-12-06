library(tm)
library(wordcloud)
library(RColorBrewer)

tf = function(fileAdd) {
  text = readLines(fileAdd)

  corpusText <- Corpus(VectorSource(text))
  corpusText_data <- tm_map(corpusText, stripWhitespace)
  corpusText_data <- tm_map(corpusText_data, tolower)
  corpusText_data <- tm_map(corpusText_data, removeNumbers)
  corpusText_data <- tm_map(corpusText_data, removePunctuation)
  corpusText_data <- tm_map(corpusText_data, removeWords, stopwords("english"))
  corpusText_data <- tm_map(corpusText_data, removeWords,
    c("thus","one","and","the","our","that","for","are","also","more","has","must","have","should","this","with", "will", "unto"))

  tdmText <- TermDocumentMatrix(corpusText_data)
  TDM1 <- as.matrix(tdmText)
  v = sort(rowSums(TDM1), decreasing = TRUE)

  wordcloud(corpusText_data, scale=c(5,0.5), max.words=20, random.order=FALSE, rot.per=0.35, use.r.layout=FALSE, colors=brewer.pal(8, "Dark2"))
}

tf("text")
tf("text2")
