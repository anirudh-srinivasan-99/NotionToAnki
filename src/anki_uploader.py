import requests


class AnkiUploader:
    """
    This class is used to upload/ create deck into Anki.
    """
    def __init__(self, host_name: str = 'localhost', port: int = 8765) -> None:
        self._anki_url = ''
        self._set_url(host_name, port)

    def _set_url(self, host_name: str, port: int) -> None:
        self._anki_url = f'http://{host_name}:{port}'
    
    def create_deck(self, deck_name: str) -> bool:
        request = {
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deck_name
            }
        }
        response = requests.post(self._anki_url, json=request).json()
        return response.get("error") is None
    
    def add_card(self, deck_name: str, model_name: str, front: str, back: str) -> bool:
        request = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Front": front,
                        "Back": back
                    },
                    "tags": ["auto-generated"]
                }
            }
        }
        response = requests.post(self._anki_url, json=request).json()
        return response.get("error") is None

if __name__ == '__main__':
    DECK_NAME = 'test1'
    MODEL_NAME = 'basic'
    front="Why do we need to use Anki?"
    back="We use Anki as it is the easiest way to learn !!"

    anki_uploader_obj = AnkiUploader()
    anki_uploader_obj.add_card(DECK_NAME, MODEL_NAME, front, back)

