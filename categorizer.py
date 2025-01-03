from transformers import pipeline

def categorizer(title):
    classifier = pipeline("zero-shot-classification")

    res = classifier(
    title,
    candidate_labels = ["STEM","Humanities","Arts","Health Sciences","Social Sciences"], 
    )
    return res

