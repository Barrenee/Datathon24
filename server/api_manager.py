import openai

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
        return {level: "" for level in levels}
    



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
    result = extract_similitude(api_key, first_text, second_text, objective, levels)
    print(result)
