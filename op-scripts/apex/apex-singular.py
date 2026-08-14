import json
import base64
import re

###########################################################################

def get_word_context(text, target_string, context_length):
    # Create a case-insensitive regex for the exact word

    reg_pattern = rf"(?:.{{0,{context_length}}}){re.escape(target_string)}(?:.{{0,{context_length}}})"
    pattern = re.findall(reg_pattern,text)

    all_matches_list = []

    for item in pattern:
        all_matches_list.append({
            'count': int(len(all_matches_list) + 1),
            'match_item': item
            })

    return all_matches_list


###########################################################################

def search_keyword_in_json_file(json_file_name,target_string,context_length):

    with open(f'ops-scripts/apex/json-file/{json_file_name}', encoding= 'utf-8') as file:
        json_data = json.load(file)

    all_exerpts_found = []

    for entity in json_data['items']:

        host_name = entity['request']['host']
        request_method = entity['request']['method']
        request_path = entity['request']['path']
        request_length = entity['request']['length']

        #('------------------[REQUEST]----------------------')
        decode_raw_request = base64.b64decode(entity['request']['raw'])

        try:
            readable_raw_request = decode_raw_request.decode('utf-8')
        except:
            continue

        if not entity['request']['response']['raw']:
            continue

        #('----------------[RESPONSE]------------------------')
        decode_raw_response = base64.b64decode(entity['request']['response']['raw'])
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
                'path': request_path,
                'host':host_name,
                'method': request_method,
                'size': request_length,
                'context_data_pool': found_data
            }

            all_exerpts_found.append(single_exerpt)
    
    return all_exerpts_found

###########################################################################

def search_results_returned(exerpt_list):

    if len(exerpt_list) == 0:
        print('no_match_found')


    item_count = 0
    for item in exerpt_list:
        item_count =+ 1
        print(f'///////////////////////[ITEM NO.{item_count}]//////////////////////////')
        print(f'[Path: {item['path']}], [Host: {item['host']}], [Method: {item['method']}], [Size: {item['size']}]')

        for singular_context in item['context_data_pool']:
            print('--------------------------------------------')
            print(f'context_number: {singular_context['count']}')
            print('--------------------------------------------')
            print(f'context_data: {singular_context['match_item']}')
    
###########################################################################
###########################################################################

with open('ops-scripts/apex/search_config/search.json','r') as file:
    search_detail = json.load(file)


search_result_list = search_keyword_in_json_file(
    json_file_name=search_detail['file_name'],
    target_string=search_detail['target_string'],
    context_length=search_detail['context_length']
    )


search_results_returned(search_result_list)


###########################################################################
###########################################################################


