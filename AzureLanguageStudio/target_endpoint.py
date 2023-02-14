from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
from pathlib import Path

def run_text_classification():
    # endpoint = os.environ["https://openai-classification-jh-ls.cognitiveservices.azure.com/"]
    # key = os.environ["ae7af333850f4b91b73aecbccb926d0b"]
    # project_name = os.environ["openai-textclass-test"]
    # deployment_name = os.environ["test-classifier"]

    endpoint = "https://openai-classification-jh-ls.cognitiveservices.azure.com/"
    key = "ae7af333850f4b91b73aecbccb926d0b"
    project_name = "openai-textclass-test"
    deployment_name = "test-classifier"

    sample_path = Path("AzureLanguageStudio", "sample_text.txt")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    with open(sample_path) as fd:
        document = [fd.read()]

    print(document)
    poller = text_analytics_client.begin_single_label_classify(
        document,
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = poller.result()
    # print(document_results, type(document_results))
    for doc, classification_result in zip(document, document_results):
        # print(doc, classification_result)
        # print(type(doc), type(classification_result))
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("The document text '{}' was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score)
            )
        elif classification_result.is_error is True:
            print("Document text '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message
            ))

if __name__ == "__main__":
    # print(os.getcwd())
    run_text_classification()
