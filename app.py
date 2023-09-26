from flask import Flask, render_template, request, jsonify
import json
import os
app = Flask(__name__)

# Load the JSON data from the file
# with open('data.json', 'r') as file:
#     json_data = json.load(file)


stream_name_to_modify = 'atNliveFeed1'
new_input_value = 'input https://test4.com;'

with open('flussonic.conf', 'r') as f:
    config_lines = f.readlines()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_url', methods=['POST'])
def update_url():
    new_input_value = request.form['new_url']
    new_input_value = 'input' + ' '+new_input_value + ';'
    start_line = None
    for i, line in enumerate(config_lines):
        if line.strip() == f'stream {stream_name_to_modify} {{':
            start_line = i
            break

    if start_line is not None:
        input_line_number = None
        for i in range(start_line, len(config_lines)):
            if config_lines[i].strip().startswith('input'):
                input_line_number = i
                break

        if input_line_number is not None:
            config_lines[input_line_number] = f'  {new_input_value}\n'

            with open('flussonic.conf', 'w') as f:
                f.writelines(config_lines)
            os.system('service flussonic reload')
            print(f"Updated input value for {stream_name_to_modify} stream.")
        else:
            print(f"Input value not found for {stream_name_to_modify} stream.")
        
    else:
        print(f"Stream {stream_name_to_modify} not found in the configuration file.")

   
    
    # with open('data.json', 'w') as file:
    #     json.dump(json_data, file, indent=4)
    
    return jsonify({'message': 'URL updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
