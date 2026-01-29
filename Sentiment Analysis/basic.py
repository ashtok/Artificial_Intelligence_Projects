from transformers import pipeline

classifier = pipeline("sentiment-analysis")

result = classifier("I am not sure i love this product")
print(result)