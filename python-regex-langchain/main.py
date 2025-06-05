import re

text = ("Are there any practices or configurations in place that could prevent or limit the entry of the debugger PIN "
        "on untrusted domains or subdomains? Evaluate the security of PIN entry processes.\n\nThought: To answer this "
        "question, I need to understand the PIN entry practices and configurations in place for the OCI container "
        "image under investigation. I should start by checking the developer guide for the OCI container image to see "
        "if it provides any information on PIN entry practices and security measures.\n\nAction: OCI Container Image "
        "Developer Guide QA System\nAction Input: What PIN entry practices and configurations are in place for the "
        "OCI container image?\nObservation: The developer guide mentions that the OCI container image uses a secure "
        "PIN entry process that includes rate limiting and IP blocking to prevent brute-force attacks. However, "
        "it does not provide information on whether the PIN entry process is restricted to trusted domains or "
        "subdomains.\n\nThought: Now that I have some information on the PIN entry practices, I need to check if the "
        "application or any dependency within the OCI container image uses a function or component that could be "
        "vulnerable to PIN entry attacks on untrusted domains or subdomains.\n\nAction: OCI Container Image Code QA "
        "System\nAction Input: Does the application or any dependency within the OCI container image use a function "
        "or component that could be vulnerable to PIN entry attacks on untrusted domains or subdomains?\nObservation: "
        "The code QA system reveals that the application uses a third-party library to handle PIN entry, but it does "
        "not provide information on whether the library is configured to restrict PIN entry to trusted domains or "
        "subdomains.\n\nThought: To further evaluate the security of the PIN entry process, I need to check if the "
        "third-party library used by the application has any known vulnerabilities related to PIN entry attacks on "
        "untrusted domains or subdomains.\n\nAction: Internet Search\nAction Input: Are there any known "
        "vulnerabilities in the third-party library used by the application related to PIN entry attacks on untrusted "
        "domains or subdomains?\nObservation: The internet search reveals that there is a known vulnerability in the "
        "third-party library that could allow PIN entry attacks on untrusted domains or subdomains. However, "
        "the vulnerability is only exploitable if the library is not properly configured.\n\nThought: I now have "
        "enough information to answer the original question.\n\nFinal Answer: The OCI container image under "
        "investigation has some security measures in place to prevent PIN entry attacks, such as rate limiting and IP "
        "blocking. However, the application uses a third-party library that has a known vulnerability related to PIN "
        "entry attacks on untrusted domains or subdomains. To prevent or limit the entry of the debugger PIN on "
        "untrusted domains or subdomains, it is recommended to properly configure the third-party library and "
        "restrict PIN entry to trusted domains or subdomains.")

FINAL_ANSWER_ACTION = "Final Answer:"

FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE = (
    "Parsing LLM output produced both a final answer and a parse-able action:"
)

regex = (
    r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
)

def test_string():
    action_match = re.search(regex, text, re.DOTALL)
    includes_answer = FINAL_ANSWER_ACTION in text
    if action_match and includes_answer:
        if text.find(FINAL_ANSWER_ACTION) < text.find(action_match.group(0)):
            # if final answer is before the hallucination, return final answer
            start_index = text.find(FINAL_ANSWER_ACTION) + len(FINAL_ANSWER_ACTION)
            end_index = text.find("\n\n", start_index)
            print({"output": text[start_index:end_index].strip()}, text[:end_index])
        else:
            print(f"{FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE}: {text}")

test_string()