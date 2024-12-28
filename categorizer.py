from transformers import pipeline

classifier = pipeline("zero-shot-classification")

res = classifier{
    "",
    candidate_labels = ["STEM","Humanities","Arts","Health Sciences","Social Sciences"],
}

