import openai # Version 0.28

def extract_properties(api_key, user_text, properties, cardinality, values_restriction):
    """
    Extracts specified properties from user text using GPT.

    :param api_key: OpenAI API key to use the GPT model.
    :param user_text: The text from which to extract properties.
    :param properties: A list of property names to extract.
    :param cardinality: A list specifying if each property should have 'single' or 'multiple' values.
    :return: A dictionary with properties and their extracted values.
    """
    if len(properties) != len(cardinality) != len(values_restriction):
        raise ValueError("Properties and cardinality lists must have the same length.")

    # Construct the prompt
    prompt = (
        "You are a text analysis assistant. Your job is to extract specified characteristics from the given user text. "
        "For each characteristic, provide only the requested information as either a single value or a list, based on the instructions. "
        "Return a Python dictionary containing each characteristic and the corresponding values, if found. "
        "There are some characteristics that may have limited values. If so, a list will be provided. If the value found doesn't match the restriction, leave the entry empty. "
        "Leave entries empty if no suitable information is found in the text.\n\n"
        f"User Text: \"{user_text}\"\n"
        "Characteristics to extract (with type):\n"
    )

    for prop, card, value_restriction in zip(properties, cardinality, values_restriction):
        addition = f"- {prop} ({'list' if card == 'multiple' else 'single'})"
        if value_restriction:
            addition += f" with values restricted to {value_restriction})\n"
        else:
            addition += "with no value restriction)\n"

        prompt += addition

    prompt += "\nReturn the result as a Python dictionary. Do not include any explanation or extra text and remember to respect the restrictions if there are any."

    # Call the OpenAI API
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    # Parse the API response
    try:
        result = response['choices'][0]['message']['content']
        return eval(result)
    except Exception as e:
        print("Error parsing the response:", e)
        return {prop: [] if card == 'multiple' else "" for prop, card in zip(properties, cardinality)}

def extract_similitude(api_key, first_text, second_text, objective, levels = ["low", "medium", "high"]):
    """
    Extracts the similitude between two texts using GPT.

    :param api_key: OpenAI API key to use the GPT model.
    :param first_text: The first text to compare.
    :param second_text: The second text to compare.
    :param objective: What you want to know about the similitude between the two texts.
    :param levels: A list with the values of similitude you can return.
    :return: One of the similitude levels that represents the similitude between the two texts.
    """
    # Construct the prompt
    prompt = (
        f"You are a text analysis assistant. Your job is to compare two texts and extract their similarity levels regarding the following characteristic: {objective}. "
        "Return a Python string containing how similars the texts are. "
        f"The similarity levels available are {levels}."
        "The texts are provided below.\n\n\n "
        f"First Text: \"{first_text}\"\n"
        f"Second Text: \"{second_text}\"\n"
    )

    prompt += "\nReturn the result as a Python string. Do not include any explanation or extra text."

    # Call the OpenAI API
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    # Parse the API response
    try:
        result = response['choices'][0]['message']['content']
        return eval(result)
    except Exception as e:
        print("Error parsing the response:", e)
        return "low"
    
def merge_property(api_key, first_description, second_description, additional_info=None):
    """
    Merges two descriptions into a single one using GPT.

    :param api_key: OpenAI API key to use the GPT model.
    :param first_description: The first description to merge.
    :param second_description: The second description to merge.
    :param additional_info: Additional information as to how the merge should be handled. 
    :return: The merged description.
    """
    # Construct the prompt
    prompt = (
        "You are a text analysis assistant. Your job is to merge two descriptions into a single one. "
        "You can also include additional information if needed. "
        "Return a Python string containing the merged description. "
        "The descriptions are provided below.\n\n\n "
        f"First Description: \"{first_description}\"\n"
        f"Second Description: \"{second_description}\"\n"
    )

    if additional_info:
        prompt += f"Additional information you should take into account: \"{additional_info}\"\n"

    prompt += "\nReturn the result as a Python string. Do not include any explanation or extra text."

    # Call the OpenAI API
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    # Parse the API response
    try:
        result = response['choices'][0]['message']['content']
        return eval(result)
    except Exception as e:
        print("Error parsing the response:", e)
        return first_description + second_description
    
def decision_explainer(api_key, matches_with_group, does_not_match_group):
    """
    Explains the decision made by a model using GPT.

    :param api_key: OpenAI API key to use the GPT model.
    :param matches_with_group: Caracteristics in which our rules have yielded a match for this group with another one. 
    :param does_not_match_group: Caracteristics in which our rules have yielded a match for this group with another one.
    :return: An explanation of the decision made by the model.
    """
    # Construct the prompt
    prompt = (
        "You are a text analysis assistant. Your job is to explain to a user which is searching for a group to work with why the model has made the decision to match them with a specific group. "
        "The model has made a decision based on expert-knowledge-derived rules. "
        "You need to provide an explanation for the decision made by the model given the aspects in which the groups match or do not match. "
        "The aspects that match between the user and group are provided below.\n\n\n "
        f"Matches with the decision: {matches_with_group}\n"
        f"Does not match with the decision: {does_not_match_group}\n"
    )

    prompt += "\nReturn the result as a Python string. Give some explanation but not unnecessary information. Keep it short."

    # Call the OpenAI API
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ], # limit tokens to 2048
        max_tokens=2048
    )

    # Parse the API response
    try:
        result = response['choices'][0]['message']['content']
        return eval(result)
    except Exception as e:
        print("Error parsing the response:", e)
        return "We are sorry, but we could not provide an explanation for the decision made by the model."
    
def modify_weights(api_key, weights, feedback): 
    """
    Given a list of weights for a ponderated sum of factors, which are used to determine if we should care more or less about them when we match a user with a group, this function returns the new ponderated sum of factors given the feedback about what the user liked or disliked about the group and our decision process. Keep the changes small, between -0.1 and 0.1.

    :param api_key: OpenAI API key to use the GPT model.
    :param weights: A dictionary with the weights for each factor.
    :param feedback: A dictionary with the feedback about the group.
    :return: A dictionary with the new weights for each factor.
    """
    # Construct the prompt
    prompt = (
        "You are a text analysis assistant. Your job is to modify the weights used in the decision process of matching a user with a group. "
        "The weights are used to determine the importance of each factor when matching a user with a group. "
        "You need to provide new weights based on the feedback received from the user about the group. "
        "Keep the changes small, between -0.1 and 0.1. "
        "The weights and feedback are provided below.\n\n\n "
        f"Weights: {weights}\n"
        f"Feedback: {feedback}\n"
    )

    prompt += "\nReturn the result as a Python dictionary. Do not include any explanation or extra text."

    # Call the OpenAI API
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    # Parse the API response
    try:
        result = response['choices'][0]['message']['content']
        return eval(result)
    except Exception as e:
        print("Error parsing the response:", e)
        return weights
    

# Example usage
if __name__ == "__main__":
    
    # Read api key from api_key.txt
    with open("./server/api_key.txt", "r") as file:
        api_key = file.read().strip()
    
    user_text = "I love hiking, painting, and playing guitar. I also speak three languages fluently and have a black belt in karate. My favourite color is purple"
    properties = ["hobbies", "abilities", "favourite_color"]
    cardinality = ["multiple", "multiple", "single"]
    restrictions = [None, None, ["blue", "red", "green"]]

    #result = extract_properties(api_key, user_text, properties, cardinality, restrictions)
    #print(result)

    first_text = "I love hiking, painting, and playing guitar. I also speak three languages fluently and have a black belt in karate. My favourite color is purple. I want to be an engineer. "
    second_text = "I enjoy videogames, literature, and playing the piano. My dream is to be an engineer someday. I am fluent in one language. My favourite color is blue"
    levels = ["low", "medium", "high"]
    objective = "future job"
    #result = extract_similitude(api_key, first_text, second_text, objective, levels)
    #print(result)

    first_description = "I love hiking, painting, and playing guitar. I also speak three languages fluently and have a black belt in karate. My favourite color is purple. I want to be an engineer. "
    second_description = "I enjoy videogames, literature, and playing the piano. My dream is to be an engineer someday. I am fluent in one language. My favourite color is blue"
    additional_info = "The final description should include only the hobbies and future jobs."
    #result = merge_property(api_key, first_description, second_description, additional_info)
    #print(result)

    matches_with_group = ["knowledge level", "abilities complementarity", "similar interests"]
    does_not_match_group = ["different job goals", "studying at different years"]
    #result = decision_explainer(api_key, matches_with_group, does_not_match_group)
    #print(result)

    weights = {"knowledge level": 0.5, "abilities complementarity": 0.3, "similar interests": 0.2, "different job goals": 0.3, "studying at different years": 0.4}
    feedback = {"i didn't really care about the knowledge level, i'm looking to work with different people, but i would have liked to have the same job goals"}
    #result = modify_weights(api_key, weights, feedback)
    #print(result)