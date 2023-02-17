import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, RecognizeCustomEntitiesAction
from azure.ai.language.questionanswering import QuestionAnsweringClient

load_dotenv()

def check_env_vars(project_vars) -> None:
    var_names = project_vars + ["AZURE_LANGUAGE_ENDPOINT", "AZURE_LANGUAGE_KEY"]
    for var in var_names:
        if var not in os.environ:
            raise OSError(f"Environment variable {var} not found. Please set it and try again.")


def ls_prediction(input_text) -> tuple:

    prediction_vars = ["CUSTOM_CLASSIFICATION_PROJECT_NAME", "CUSTOM_CLASSIFICATION_DEPLOYMENT_NAME"]
    check_env_vars(prediction_vars)

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    project_name = os.environ["CUSTOM_CLASSIFICATION_PROJECT_NAME"]
    deployment_name = os.environ["CUSTOM_CLASSIFICATION_DEPLOYMENT_NAME"]

    classification_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = classification_client.begin_single_label_classify(
        [input_text], # why does this need to be a list?
        project_name=project_name,
        deployment_name=deployment_name
    )

    document_results = poller.result()

    for doc, classification_result in zip([input_text], document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classification = classification_result.classifications[0]
            print("The document text '{}' was classified as '{}' with confidence score {}.".format(
                doc, classification.category, classification.confidence_score))
            return classification.category, classification.confidence_score

        elif classification_result.is_error is True:
            # print("Document text '{}' has an error with code '{}' and message '{}'".format(
            #     doc, classification_result.error.code, classification_result.error.message
            # ))
            return 'classification error', classification_result.error.code

def ls_entity_recognition(input_text: str) -> dict:

    recognition_vars = ["CUSTOM_ENTITIES_PROJECT_NAME", "CUSTOM_ENTITIES_DEPLOYMENT_NAME"]
    check_env_vars(recognition_vars)

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    project_name = os.environ["CUSTOM_ENTITIES_PROJECT_NAME"]
    deployment_name = os.environ["CUSTOM_ENTITIES_DEPLOYMENT_NAME"]

    entity_recognition_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = entity_recognition_client.begin_analyze_actions(
        [input_text], # why does this need to be a list?
        actions=[
            RecognizeCustomEntitiesAction(
                project_name=project_name, deployment_name=deployment_name
            )
        ],
    )

    document_results = poller.result()
    # works only for one document (i.e. one result)
    for result in document_results:
        custom_entities_result = result[0] 
        if not custom_entities_result.is_error:
            for entity in custom_entities_result.entities:
                print("Text: {}, Category: {}, Confidence Score: {}".format(
                        entity.text, entity.category, entity.confidence_score))

            entities = {f'entity{idx}': {'text': ent.text, 'category': ent.category, 'confidence': ent.confidence_score} for idx, ent in enumerate(custom_entities_result.entities)}
            return entities
        else:
            print("There was an error with the request.")
            return 'entity recognition error', custom_entities_result.error.code
            

def ls_question_answering(input_text: str) -> tuple:

    answering_vars = ["CUSTOM_QUESTIONS_PROJECT_NAME", "CUSTOM_QUESTIONS_DEPLOYMENT_NAME"]
    check_env_vars(answering_vars)

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    project_name = os.environ["CUSTOM_QUESTIONS_PROJECT_NAME"]
    deployment_name = os.environ["CUSTOM_QUESTIONS_DEPLOYMENT_NAME"]
    
    client = QuestionAnsweringClient(
        endpoint=endpoint,  
        credential=AzureKeyCredential(key)
        )

    with client:
        output = client.get_answers(
            question=input_text,
            top=1,
            confidence_threshold=0.2,
            project_name=project_name,
            deployment_name=deployment_name
        )

        if output.answers:
            best_candidate = [a for a in output.answers if a.confidence and a.confidence >= 0.2][0]
            print("Q: {}".format(input_text))
            print("A: {}".format(best_candidate.answer))
            return best_candidate.answer
        else:
            print(f"No answers found for '{input_text}'.")
            return 'no answer found', 424

if __name__ == '__main__':
    # print(ls_question_answering('Winter Berlin'))
    if 'AZURE' in os.environ:
        print('WORKS')
    else:
        print('ERROR')