import re
import ast

# Find all substrings that start and end with quotes, allowing for spaces before a comma or closing bracket
re_quote_capture = re.compile(
    r"""
        (['"])                    # Opening quote
        (                         # Start capturing the quoted content
            (?:\\.|[^\\])*?       # Non-greedy match for any escaped character or non-backslash character
        )                         # End capturing the quoted content
        \1                        # Matching closing quote
        (?=\s*,|\s*\])            # Lookahead for whitespace followed by a comma or closing bracket, without including it in the match
    """,
    re.VERBOSE)


def attempt_fix_list_string(s: str) -> str:
    """
    Attempt to fix unescaped quotes in a string that represents a list to make it parsable.

    Parameters
    ----------
    s : str
        A string representation of a list that potentially contains unescaped quotes.

    Returns
    -------
    str
        The corrected string where internal quotes are properly escaped, ensuring it can be parsed as a list.

    Notes
    -----
    This function is useful for preparing strings to be parsed by `ast.literal_eval` by ensuring that quotes inside
    the string elements of the list are properly escaped. It adds brackets at the beginning and end if they are missing.
    """
    # Check if the input starts with '[' and ends with ']'
    s = s.strip()
    if (not s.startswith('[')):
        s = "[" + s
    if (not s.endswith(']')):
        s = s + "]"

    def fix_quotes(match):
        # Extract the captured groups
        quote_char, content = match.group(1), match.group(2)
        # Escape quotes inside the string content
        fixed_content = re.sub(r"(?<!\\)(%s)" % re.escape(quote_char), r'\\\1', content)
        # Reconstruct the string with escaped quotes and the same quote type as the delimiters
        return f"{quote_char}{fixed_content}{quote_char}"

    # Fix the quotes inside the strings
    fixed_s = re_quote_capture.sub(fix_quotes, s)

    return fixed_s


my_list = [
    "['Check OpenShift Version: Verify the version of OpenShift installed in the containerized environment. The vulnerability affects OpenShift versions 4.0 and OpenShift Distributed Tracing version 2.0. Is the environment running a vulnerable version?']",
    "['Review Telemeter Configuration: Inspect the Telemeter configuration within the OpenShift environment to check if the 'iss' check during JSON web token (JWT) authentication is properly implemented. Are there any custom configurations or workarounds that might be vulnerable to forged tokens?']",
    "['Assess JWT Authentication Practices: Evaluate the JWT authentication practices within the application. Are tokens properly validated, and are there any weaknesses in the token verification process that could allow an attacker to bypass the 'iss' check?']",
    "['Inspect Token Handling: Review how tokens are handled and processed within the application. Are there any opportunities for an attacker to inject a forged token, and are there any input validation weaknesses that could be exploited?']"
]

llm3_8b_checklist = [
    'Here is the checklist for the given CVE details:\n\n[\n\t"Check OpenShift Version: Verify the version of OpenShift installed in the Docker container. The vulnerability affects OpenShift versions 4.0 and 2.0. Is the container running OpenShift 4.0 or 2.0? If so, it may be vulnerable.",\n\t"Review JWT Authentication: Does the application using Telemeter process JSON web tokens (JWTs) for authentication? Evaluate how the application handles JWTs, particularly the \'iss\' check during JWT authentication.",\n\t"Assess Token Forgery: Does the application using Telemeter allow the creation of forged tokens that could be used to bypass the \'iss\' check during JWT authentication? Evaluate how the application handles token creation and validation.",\n\t"Check for Spoofing Attacks: Assess the application\'s defenses against spoofing attacks, particularly in the context of JWT authentication. Are there any measures in place to prevent or detect forged tokens?",\n\t"Review OpenShift Configuration: Are there any configuration settings or options that could be exploited to bypass the \'iss\' check during JWT authentication? Evaluate the OpenShift configuration and settings for potential vulnerabilities.",\n\t"Check for Updates: Are the affected packages (openshift_container_platform and openshift_distributed_tracing) up-to-date? If not, recommend updating to the latest versions to mitigate the vulnerability."]']
llm3_8b_checklist_original = [
    'Here is the checklist for the given CVE details:\n\n[\n\t"Check OpenShift Version: Verify the version of OpenShift installed in the Docker container. The vulnerability affects OpenShift versions 4.0 and 2.0. Is the container running OpenShift 4.0 or 2.0? If so, it may be vulnerable.",\n\t"Review JWT Authentication: Does the application using Telemeter process JSON web tokens (JWTs) for authentication? Evaluate how the application handles JWTs, particularly the \'iss\' check during JWT authentication.",\n\t"Assess Token Forgery: Does the application using Telemeter allow the creation of forged tokens that could be used to bypass the \'iss\' check during JWT authentication? Evaluate how the application handles token creation and validation.",\n\t"Check for Spoofing Attacks: Assess the application\'s defenses against spoofing attacks, particularly in the context of JWT authentication. Are there any measures in place to prevent or detect forged tokens?",\n\t"Review OpenShift Configuration: Are there any configuration settings or options that could be exploited to bypass the \'iss\' check during JWT authentication? Evaluate the OpenShift configuration and settings for potential vulnerabilities.",\n\t"Check for Updates: Are the affected packages (openshift_container_platform and openshift_distributed_tracing) up-to-date? If not, recommend updating to the latest versions to mitigate the vulnerability."]']

def return_escaped_content_backslashes(match) -> str:
    return match.group(0).replace("\\", "\\\\")

def _parse_list(text: list[str]) -> list[list[str]]:
    """
    Asynchronously parse a list of strings, each representing a list, into a list of lists.

    Parameters
    ----------
    text : list of str
        A list of strings, each intended to be parsed into a list.

    Returns
    -------
    list of lists of str
        A list of lists, parsed from the input strings.

    Raises
    ------
    ValueError
        If the string cannot be parsed into a list or if the parsed object is not a list.

    Notes
    -----
    This function tries to fix strings that represent lists with unescaped quotes by calling
    `attempt_fix_list_string` and then uses `ast.literal_eval` for safe parsing of the string into a list.
    It ensures that each element of the parsed list is actually a list and will raise an error if not.
    """
    return_val = []

    for checklist_num, x in enumerate(text):
        try:
            # Try to cut out verbosity:
            x = x[x.find('['):x.rfind(']') + 1]

            # Remove newline characters that can cause incorrect string escaping in the next step
            x = x.replace("\n", "")

            # Ensure backslashes are escaped only when they are not already escaping other characters
            x = re.sub(r'\\[^"\'\\nrtbf]', return_escaped_content_backslashes, x)
            # Try to do some very basic string cleanup to fix unescaped quotes
            x = attempt_fix_list_string(x)

            # Only proceed if the input is a valid Python literal
            # This isn't really dangerous, literal_eval only evaluates a small subset of python
            current = ast.literal_eval(x)

            # Ensure that the parsed data is a list
            if not isinstance(current, list):
                raise ValueError(f"Input is not a list: {x}")

            # Process the list items
            for i in range(len(current)):
                if (isinstance(current[i], list) and len(current[i]) == 1):
                    current[i] = current[i][0]

            return_val.append(current)
        except (ValueError, SyntaxError) as e:
            # Handle the error, log it, or re-raise it with additional context
            raise ValueError(f"Failed to parse input for checklist number {checklist_num}: {x}. Error: {e}")

    return return_val


test1 = ['[	"Verify Windows Node Usage: Are there any Windows nodes present in the Kubernetes cluster? The vulnerability specifically affects clusters with Windows nodes, so the presence of such nodes is a prerequisite for exploitability.",	"Assess Container Log Permissions: Review the permissions set on container logs within the cluster. Are the permissions set to allow BUILTIN\\Users to read and NT AUTHORITY\\Authenticated Users to modify container logs? This is the specific vulnerability being exploited.",	"Evaluate User Group Membership: Identify which users are part of the BUILTIN\\Users and NT AUTHORITY\\Authenticated Users groups within the cluster. Are there any users who should not have these permissions but are inadvertently included in these groups, potentially increasing the attack surface?"]']

test2 = [
    '[\n\t"Verify Usage of `@octokit/request` Package: Check if the `@octokit/request` package is being used within the container image, specifically the `fetchWrapper` function that contains the vulnerable regular expression.",\n\t"Assess Input Data Handling: Evaluate how the application handles HTTP responses, particularly the `link` header, to determine if it could be exploited by a malicious input designed to trigger catastrophic backtracking.",\n\t"Review Regular Expression Complexity: Inspect the regular expression `/<([^>]+)>; rel=\\"deprecation\\"/` used in the `fetchWrapper` function to understand its complexity and potential for exponential backtracking. Consider alternative, more efficient regular expressions or input validation mechanisms to mitigate the vulnerability."\n]']

print(_parse_list(test2))
print(_parse_list(test1))

