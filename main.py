import json
import argparse
from agent import run_agent

def main(args):

    response = run_agent(args.resume_path, args.job_url)

    try:
        with open(args.json_file, "a", encoding='utf-8') as f:
            json.dump(response.model_dump(), f, indent=4)
    except Exception as e:
        print(f"Error reading file: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file', default='./candidate.json', help="Path to the Json file")
    parser.add_argument('--resume_path', default='./sample.pdf', help="Path to the resume")
    parser.add_argument('--job_url', default="https://job-boards.greenhouse.io/reddit/jobs/7131934?gh_src=8a8a4d8a1us", help="URL of the tareted Job Description")
    args = parser.parse_args()
    main(args)