import argparse
import json
import os
import requests
import time

from dotenv import load_dotenv


def _read_file(path):

    with open(path, "rb") as f:
        data = f.read()

    return data


def upload_file(path, headers):

    data = _read_file(path)

    response = requests.post(
        url="https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=data,
    )

    return response.json()["upload_url"]


def request_transcript(payload, headers):

    response = requests.post(
        url="https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json=payload,
    )

    return response.json()["id"]


def _await_status(transcript_id, headers):

    while True:

        response = requests.get(
            url=f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=headers
        ).json()
        
        status = response["status"]

        if status == "completed":
            break
        elif status == "error":
            raise RuntimeError(f"Transcription failed: {response['error']}")
        else:
            time.sleep(3)
        
    return None


def get_transcript(transcript_id, headers):

    _await_status(transcript_id, headers)

    transcription = requests.get(
        url=f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
        headers=headers
    )
    
    return transcription.json()


def main():

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path to audio file")
    parser.add_argument("dest", help="location of where to write file")
    args = parser.parse_args()

    headers = {
        "authorization": os.getenv("ASSEMBLYAI_API_KEY"),
        "content-type": "application/json"
    }

    upload_url = upload_file(args.file, headers)
    
    transcript_id = request_transcript(
        payload={
            "audio_url": upload_url,
            "punctuate": True,
            "format_text": True,
        },
        headers=headers
    )

    transcription = get_transcript(transcript_id, headers)["text"]

    with open(args.dest, 'w') as f:
        f.write(transcription)


if __name__ == "__main__":
    main()