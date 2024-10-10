
import jsonlines
import json



'''jsonlines utils'''
def read_jsonl_data(f_input):
    data = []
    with open(f_input, 'r', encoding="utf-8") as fd:
        for l in jsonlines.Reader(fd):
            data.append(l)
    print(f"Length of {f_input}:\n {len(data)}")
    return data

def write_jsonl_data(res, f_output):
    with jsonlines.open(f_output, 'w') as writer:
        print(f"Write {len(res)} samples to {f_output}")
        writer.write_all(res)

def read_json(f_input):
    with open(f_input, "r") as f:
        data = json.load(f)
    print(f"Length of {f_input}:\n {len(data)}")
    return data

def write_json(res, f_output):
    with open(f_output, "w") as f:
        print(f"Write {len(res)} samples to {f_output}")
        json.dump(res, f, ensure_ascii=False, indent=2)

# some alias
load_jsonl = read_jsonl_data
read_jsonl = read_jsonl_data
write_jsonl = write_jsonl_data
load_json = read_json


def load_json_or_jsonl(f_input):
    if f_input.endswith("jsonl"):
        return read_jsonl_data(f_input)
    elif f_input.endswith("json"):
        return read_json(f_input)
    else:
        raise NotImplementedError(f"ERROR, must be json or jsonl, but got {f_input}")

def write_json_or_jsonl(res, f_output):
    if f_output.endswith("jsonl"):
        write_jsonl(res, f_output)
    elif f_output.endwith("json"):
        write_json(res, f_output)
    else:
        raise NotImplementedError(f"ERROR, must be json or jsonl, but got {f_output}")


