from ua_parser import user_agent_parser

def parse_user_agent(user_agent_string):
    parsed_string = user_agent_parser.Parse(user_agent_string)
    brand = parsed_string['device']['brand'] or ""
    model = parsed_string['device']['model'] or ""
    device = (brand+" "+model).strip() or "UnKnown" 
    os = parsed_string['os']['family']
    browser = parsed_string['user_agent']['family']
    
    return {
        'device': device,
        'os': os,
        'browser': browser,
    }
