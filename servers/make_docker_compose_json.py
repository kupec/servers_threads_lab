import json

def make_services(template):
    result = {}

    for spec in template:
        dir = spec[0]
        variant = None
        options = {}

        if len(spec) == 2:
            if type(spec[1]) == str:
                variant = spec[1]
            else:
                options = spec[1]
        elif len(spec) == 3:
            variant = spec[1]
            options = spec[2]

        service_name = f'{dir}_{variant}' if variant else dir
        service_name = service_name.replace('/', '_')

        service_spec = {**options}

        build = {'context': dir}
        if variant:
            build['args'] = [f'variant={variant}']
        service_spec['build'] = build
        service_spec['ports'] = ['3001:80']

        result[service_name] = service_spec

    return result


def start():
    with open('docker-compose-template.json', 'r') as f:
        template = json.load(f)
        services = make_services(template)
        result = {
            'version': '3',
            'services': services,
        }

        print(json.dumps(result))

if __name__ == '__main__':
    start()
