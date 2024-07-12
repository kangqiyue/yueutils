import json
import os
from os.path import abspath, dirname, join
import subprocess
from loguru import logger

def save_training_meta(args, **kwargs):
    def can_serialize(dictionary, key):
        try:
            json.dumps({key: dictionary[key]})
            return True
        except TypeError:
            return False
    def remove_unserializable(dictionary):
        return {key: value for key, value in dictionary.items() if can_serialize(dictionary, key)}

    # log dir
    if not os.path.exists(args.output_dir):
        os.makedirs(join(args.output_dir, 'log'))
    # save args
    with open(join(args.output_dir, 'log', 'hps.json'), 'w') as writer:
        json.dump(remove_unserializable(vars(args)), writer, indent=4)
    # kwargs
    if len(kwargs) > 0:
        logger.info(kwargs)
        for name, other_config in kwargs.items():
            with open(join(args.output_dir, 'log', f'{name}.json'), 'w') as writer:
                json.dump(remove_unserializable(vars(other_config))  , writer, indent=4)
    # git info
    try:
        logger.info("Waiting on git info....")
        c = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], timeout=10, stdout=subprocess.PIPE)
        git_branch_name = c.stdout.decode().strip()
        logger.info(f"Git branch: {git_branch_name}")
        c = subprocess.run(["git", "rev-parse", "HEAD"], timeout=10, stdout=subprocess.PIPE)
        git_sha = c.stdout.decode().strip()
        logger.info(f"Git SHA: {git_sha}", )
        git_dir = abspath(dirname(__file__))
        git_status = subprocess.check_output(
            ['git', 'status', '--short'],
            cwd=git_dir, universal_newlines=True).strip()
        with open(join(args.output_dir, 'log', 'git_info.json'), 'w') as writer:
            json.dump({'branch': git_branch_name,
                    'is_dirty': bool(git_status),
                    'status': git_status,
                    'sha': git_sha},
                    writer, indent=4)
    except subprocess.TimeoutExpired as e:
        logger.exception(e)
        logger.warn("Git info not found. Moving right along...")
