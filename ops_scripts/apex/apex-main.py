import json
import base64
import re

###########################################################################

def get_word_context(text, target_string, context_length):
    # Create a case-insensitive regex for the exact word

    reg_pattern = rf"(.{{0,{context_length}}}){re.escape(target_string)}(.{{0,{context_length}}})"
    pattern = re.search(reg_pattern,text)

    if pattern:
        prefix = pattern.group(1)
        suffix = pattern.group(2)

        found_match = f'{prefix}{target_string}{suffix}'
        return found_match

    return None


###########################################################################

def search_keyword_in_json_file(json_file_name,target_string,context_length):

    with open(f'scripts/ops_scripts/apex/json-file/{json_file_name}', encoding= 'utf-8') as file:
        json_data = json.load(file)

    for entity in json_data:

        host_name = entity['host']
        request_method = entity['method']
        request_path = entity['path']
        request_length = entity['length']

        #('------------------[REQUEST]----------------------')
        decode_raw_request = base64.b64decode(entity['raw'])

        try:
            readable_raw_request = decode_raw_request.decode('utf-8')
        except:
            continue

        if not entity['response']:
            continue

        #('----------------[RESPONSE]------------------------')
        decode_raw_response = base64.b64decode(entity['response']['raw'])
        try:
            readable_raw_response = decode_raw_response.decode('utf-8') 
        except:
            continue

        found_data = get_word_context(
            text=readable_raw_response, 
            target_string=target_string, 
            context_length=context_length)

        if found_data:
            single_exerpt = {
                'Path': request_path,
                'Host':host_name,
                'Method': request_method,
                'Size': request_length,
                'Context': found_data
            }

            all_exerpts_found.append(single_exerpt)

###########################################################################

def search_results_returned(exerpt_list):

    if len(exerpt_list) == 0:
        print('no_match_found')

    for item in exerpt_list:
        print(item)
    
###########################################################################
###########################################################################

with open('scripts/ops_scripts/apex/search_config/search.json','r') as file:
    search_detail = json.load(file)


all_exerpts_found = []

search_keyword_in_json_file(
    json_file_name=search_detail['file_name'],
    target_string=search_detail['target_string'],
    context_length=search_detail['context_length']
    )

search_results_returned(all_exerpts_found)


###########################################################################
###########################################################################


