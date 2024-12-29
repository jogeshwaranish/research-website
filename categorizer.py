from transformers import pipeline

classifier = pipeline("zero-shot-classification")

res = classifier(
    "Mass Media Science & Engineering Fellowship through AAASThis program strengthens connections between scientists and journalists by placing undergraduate scientists, engineers, and mathematicians at media organizations (National Public Radio, Los Angeles Times, WIRED, etc.). Students sharpen their abilities to communicate complex scientific issues and enhance coverage of science-related issues in media.",
    candidate_labels = ["STEM","Humanities","Arts","Health Sciences","Social Sciences"], 
)
print(res)

